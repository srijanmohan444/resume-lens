from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.concurrency import run_in_threadpool
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from . import db, jobs as job_sources, llm, matcher
from .config import (ADZUNA_APP_ID, ADZUNA_APP_KEY, CITIES, FRONTEND_DIR, GEMINI_API_KEY,
                     MAX_UPLOAD_BYTES, RAPIDAPI_KEY)
from .parser import extract_text


@asynccontextmanager
async def lifespan(_):
    db.init()
    yield


app = FastAPI(title="Resume Lens India", lifespan=lifespan)


class JobQuery(BaseModel):
    analysis_id: str = Field(min_length=4, max_length=40)
    role: str = Field(min_length=2, max_length=80)
    city: str = "All India"


class TailorQuery(BaseModel):
    analysis_id: str = Field(min_length=4, max_length=40)
    job_title: str = Field(default="", max_length=150)
    company: str = Field(default="", max_length=150)
    job_description: str = Field(min_length=10, max_length=15000)


class InterviewEvalQuery(BaseModel):
    analysis_id: str = Field(default="", max_length=40)
    role: str = Field(default="Candidate", max_length=120)
    question: str = Field(min_length=5, max_length=500)
    user_answer: str = Field(min_length=5, max_length=5000)


@app.get("/api/health")
def health():
    return {
        "gemini": bool(GEMINI_API_KEY),
        "adzuna": bool(ADZUNA_APP_ID and ADZUNA_APP_KEY),
        "jsearch": bool(RAPIDAPI_KEY),
        "cities": CITIES,
    }


@app.post("/api/analyze")
async def analyze(file: UploadFile = File(...), target_role: str = Form("")):
    data = await file.read(MAX_UPLOAD_BYTES + 1)
    if len(data) > MAX_UPLOAD_BYTES:
        raise HTTPException(413, "File is larger than 5 MB.")
    try:
        text = await run_in_threadpool(extract_text, file.filename or "", data)
        result = await llm.analyze_resume(text, target_role.strip()[:80])
    except ValueError as e:
        raise HTTPException(422, str(e))
    except llm.ApiError as e:
        raise HTTPException(502, str(e))

    # Persist resume text along with analysis for JD tailoring & bullet point rewriter
    result["resume_text"] = text
    aid = uuid4().hex[:12]
    db.save_analysis(aid, result)
    return {"analysis_id": aid, "analysis": result}


@app.post("/api/jobs")
async def jobs(q: JobQuery):
    analysis = db.get_analysis(q.analysis_id)
    if not analysis:
        raise HTTPException(404, "Analysis not found. Upload your resume again.")
    city = q.city if q.city in CITIES else "All India"
    try:
        found, warnings = await job_sources.find_jobs(q.role.strip(), city)
    except job_sources.SourceError as e:
        raise HTTPException(503, str(e))
    return {"jobs": matcher.rank(found, analysis, q.role)[:40], "warnings": warnings}


@app.post("/api/tailor")
async def tailor(q: TailorQuery):
    analysis = db.get_analysis(q.analysis_id)
    if not analysis:
        raise HTTPException(404, "Analysis not found. Upload your resume again.")
    resume_text = analysis.get("resume_text", "")
    try:
        tailored = await llm.tailor_for_job(
            resume_text=resume_text,
            analysis=analysis,
            job_title=q.job_title,
            company=q.company,
            job_description=q.job_description,
        )
    except llm.ApiError as e:
        raise HTTPException(502, str(e))
    return {"tailored": tailored}


@app.post("/api/interview/evaluate")
async def evaluate_interview(q: InterviewEvalQuery):
    try:
        result = await llm.evaluate_interview_answer(
            role=q.role,
            question=q.question,
            user_answer=q.user_answer,
        )
    except llm.ApiError as e:
        raise HTTPException(502, str(e))
    return {"evaluation": result}


app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="ui")
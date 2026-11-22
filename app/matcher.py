import re
from functools import lru_cache

TAXONOMY = """python,java,javascript,typescript,react,angular,vue,node.js,express,django,flask,fastapi,spring boot,
c++,c#,.net,php,laravel,ruby,golang,kotlin,swift,android,ios,flutter,react native,html,css,sql,mysql,postgresql,
mongodb,redis,oracle,aws,azure,gcp,docker,kubernetes,terraform,jenkins,ci/cd,git,linux,rest api,graphql,microservices,
kafka,spark,hadoop,airflow,etl,data warehouse,snowflake,tableau,power bi,excel,machine learning,deep learning,nlp,
computer vision,tensorflow,pytorch,scikit-learn,pandas,numpy,statistics,data analysis,data visualization,llm,
generative ai,selenium,manual testing,automation testing,qa,devops,agile,scrum,jira,product management,
project management,business analysis,ui/ux,figma,seo,sem,digital marketing,content writing,social media,
google analytics,sales,lead generation,crm,salesforce,customer support,accounting,tally,gst,taxation,
financial analysis,financial modelling,auditing,recruitment,hr operations,payroll,supply chain,logistics,
procurement,operations,communication,leadership""".replace("\n", "").split(",")

ALIAS = {"js": "javascript", "reactjs": "react", "react.js": "react", "nodejs": "node.js", "node": "node.js",
         "ml": "machine learning", "postgres": "postgresql", "k8s": "kubernetes", "powerbi": "power bi",
         "ms excel": "excel", "advanced excel": "excel", "go": "golang", "sklearn": "scikit-learn",
         "ai": "generative ai", "gen ai": "generative ai", "ui ux": "ui/ux", "cicd": "ci/cd"}
STOP = {"and", "the", "of", "for", "in", "at", "to", "a", "an", "-", "&"}


def _norm(s):
    s = s.strip().lower()
    return ALIAS.get(s, s)


@lru_cache(maxsize=None)
def _pattern(skill):
    n = _norm(skill)
    names = {n} | {k for k, v in ALIAS.items() if v == n}
    alt = "|".join(re.escape(x) for x in sorted(names, key=len, reverse=True))
    return re.compile(rf"(?<![a-z0-9+#]){alt}(?![a-z0-9+#])")


def _has(text, skill):
    return bool(_pattern(skill).search(text))


def _tokens(s):
    return {t for t in re.findall(r"[a-z0-9+#.]+", s.lower()) if t not in STOP}


def _seniority(title, years):
    t = title.lower()
    if re.search(r"\b(senior|sr|lead|principal|head|manager|architect|director)\b", t) and years < 4:
        return 0.3
    if re.search(r"\b(intern|trainee|fresher|junior|jr|associate)\b", t) and years > 4:
        return 0.4
    return 1.0


def rank(jobs, analysis, role):
    skills, years = analysis.get("skills", []), analysis.get("experience_years") or 0
    have = {_norm(s) for s in skills}
    role_tokens = _tokens(role)
    out = []
    for j in jobs:
        text = f"{j['title']} {j['description']}".lower()
        matched = [s for s in skills if _has(text, s)]
        wanted = [s for s in TAXONOMY if _has(text, s)]
        missing = [s for s in wanted if _norm(s) not in have][:6]
        skill_score = min(len(matched) / max(len(wanted), len(matched), 3), 1.0)
        title_score = len(role_tokens & _tokens(j["title"])) / len(role_tokens) if role_tokens else 0.5
        final = 0.6 * skill_score + 0.3 * title_score + 0.1 * _seniority(j["title"], years)
        j = dict(j)
        j["match"] = min(98, round(final * 100))
        j["matched_skills"] = matched[:8]
        j["missing_skills"] = missing
        j["snippet"] = j.pop("description")[:360]
        out.append(j)
    return sorted(out, key=lambda x: x["match"], reverse=True)

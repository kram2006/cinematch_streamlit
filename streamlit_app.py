import json
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(
    page_title="CineMatch | Research Portfolio & Recommendation Engine",
    page_icon=str((Path(__file__).resolve().parent / "cm_favicon.svg")),
    layout="wide",
    initial_sidebar_state="collapsed",
)


st.markdown(
    """
<style>
 header { visibility: hidden; height: 0; }
 .stApp { background: transparent; }
 .block-container { padding: 0 !important; max-width: 100% !important; }
 [data-testid="stSidebar"] { display: none; }
 iframe { border: 0 !important; }
 html, body { overflow-x: hidden; }
</style>
    """,
    unsafe_allow_html=True,
)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


root = Path(__file__).resolve().parent
index_html = _read_text(root / "index.html")
css = _read_text(root / "style.css")
js = _read_text(root / "app.js")

movies = _read_json(root / "data" / "movies.json")
recommendations = _read_json(root / "data" / "recommendations.json")
manifold = _read_json(root / "data" / "manifold.json")

evaluation_path = root / "data" / "evaluation.json"
evaluation = _read_json(evaluation_path) if evaluation_path.exists() else []


injected = {
    "movies": movies,
    "recommendations": recommendations,
    "manifold": manifold,
    "evaluation": evaluation,
}


override_js = f"""
<script>
window.__CINEMATCH_DATA__ = {json.dumps(injected, ensure_ascii=False)};

function loadAllData() {{
    try {{
        moviesData = window.__CINEMATCH_DATA__.movies || [];
        recommendationsData = window.__CINEMATCH_DATA__.recommendations || {{}};
        manifoldData = window.__CINEMATCH_DATA__.manifold || [];
        dataLoaded = true;
        loadEvaluationData();
    }} catch (e) {{
        console.error('Injected data load failed:', e);
    }}
}}

function loadEvaluationData() {{
    try {{
        const data = window.__CINEMATCH_DATA__.evaluation || [];
        data.forEach(item => {{
            const method = (item.method || '').toLowerCase();
            const precEl = document.getElementById(`${{method}}-precision`);
            const latEl = document.getElementById(`${{method}}-latency`);
            if (precEl) precEl.textContent = Number(item.precision).toFixed(4);
            if (latEl) latEl.textContent = Number(item.latency).toFixed(2) + 'ms';
        }});
    }} catch (e) {{
        console.warn('Evaluation inject failed:', e);
    }}
}}
</script>
"""


def _inline_static(index_html_text: str, css_text: str, js_text: str) -> str:
    html = index_html_text
    html = html.replace('<link rel="stylesheet" href="style.css">', f"<style>\n{css_text}\n</style>")
    html = html.replace('<script src="app.js"></script>', f"<script>\n{js_text}\n</script>\n{override_js}")
    return html


final_html = _inline_static(index_html, css, js)
components.html(final_html, height=2600, scrolling=False)


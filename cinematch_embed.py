import json
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def apply_streamlit_chrome_hiding_css(*, hide_sidebar: bool = True) -> None:
    sidebar_css = "[data-testid=\"stSidebar\"] { display: none; }" if hide_sidebar else ""

    st.markdown(
        f"""
<style>
 header {{ visibility: hidden; height: 0; }}
 .stApp {{ background: transparent; }}
 .block-container {{ padding: 0 !important; max-width: 100% !important; }}
 {sidebar_css}
 iframe {{ border: 0 !important; }}
 html, body {{ overflow-x: hidden; }}
</style>
        """,
        unsafe_allow_html=True,
    )


def render(selected_tab: str | None = None, *, height: int = 2600) -> None:
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

    tab_js = ""
    if selected_tab:
        safe_tab = json.dumps(selected_tab)
        tab_js = f"""
(function() {{
    try {{
        const desired = {safe_tab};
        const clickTab = () => {{
            const btn = Array.from(document.querySelectorAll('.tab-btn'))
                .find(b => (b.dataset && b.dataset.tab) === desired);
            if (btn) btn.click();
        }};

        if (document.readyState === 'loading') {{
            document.addEventListener('DOMContentLoaded', clickTab);
        }} else {{
            clickTab();
        }}
    }} catch (e) {{
        console.warn('Failed to auto-select tab:', e);
    }}
}})();
"""

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

{tab_js}
</script>
"""

    html = index_html
    html = html.replace('<link rel="stylesheet" href="style.css">', f"<style>\n{css}\n</style>")
    html = html.replace('<script src="app.js"></script>', f"<script>\n{js}\n</script>\n{override_js}")

    components.html(html, height=height, scrolling=False)

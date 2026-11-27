"""Presentation helpers for the MOLE-AI Streamlit interface.

All visual styling lives here so the app module only describes layout.
"""

from __future__ import annotations

import base64
from html import escape

import streamlit as st

ACCENT = "#1F4E3D"

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&family=Source+Serif+4:opsz,wght@8..60,400;8..60,500;8..60,600&display=swap');

:root {
  --paper: #F7F5F0;
  --surface: #FFFFFF;
  --ink: #1B1D1F;
  --ink-2: #4A4F55;
  --ink-3: #80868C;
  --rule: #E3DED4;
  --rule-strong: #CFC8BB;
  --accent: #1F4E3D;
  --accent-soft: #E6EEE9;
  --amber: #8A5A12;
  --amber-soft: #F5ECDC;
  --red: #8B2E2E;
  --red-soft: #F4E4E1;
  --serif: 'Source Serif 4', Georgia, 'Times New Roman', serif;
  --sans: 'IBM Plex Sans', -apple-system, 'Segoe UI', sans-serif;
  --mono: 'IBM Plex Mono', ui-monospace, Consolas, monospace;
}

/* ---- page frame ---------------------------------------------------- */
.stApp { background: var(--paper); }
header[data-testid="stHeader"] { background: transparent; }
[data-testid="stDecoration"] { display: none; }
.block-container, [data-testid="stMainBlockContainer"] {
  max-width: 1120px;
  padding-top: 2.5rem;
  padding-bottom: 4rem;
}
html, body, .stApp, .stMarkdown, button, input, textarea {
  font-family: var(--sans);
}
h1, h2, h3, h4 {
  font-family: var(--serif) !important;
  font-weight: 500 !important;
  letter-spacing: -0.01em;
  color: var(--ink);
}
code, pre, .mono { font-family: var(--mono) !important; }
.stMarkdown p, .stCaption, [data-testid="stCaptionContainer"] { color: var(--ink-2); }

/* ---- masthead ------------------------------------------------------ */
.mh {
  display: flex; align-items: flex-end; justify-content: space-between;
  gap: 24px; padding-bottom: 18px; border-bottom: 1px solid var(--ink);
  margin-bottom: 4px;
}
.mh-brand { display: flex; align-items: center; gap: 14px; }
.mh-mark { width: 38px; height: 38px; color: var(--accent); flex: none; }
.mh-name {
  font-family: var(--serif); font-size: 30px; font-weight: 600;
  letter-spacing: 0.01em; color: var(--ink); line-height: 1;
}
.mh-tag {
  font-size: 13px; color: var(--ink-3); margin-top: 6px; letter-spacing: 0.01em;
}
.mh-meta {
  font-family: var(--mono); font-size: 11.5px; color: var(--ink-3);
  text-transform: uppercase; letter-spacing: 0.08em; text-align: right;
}
@media (max-width: 640px) { .mh-meta { display: none; } .mh-name { font-size: 26px; } }

/* ---- tabs as a quiet text nav -------------------------------------- */
[data-testid="stTabs"] [role="tablist"] {
  gap: 28px; border-bottom: 1px solid var(--rule); background: transparent;
}
[data-testid="stTab"] {
  min-height: 46px; padding: 0; background: transparent; color: var(--ink-3);
}
[data-testid="stTab"] p { font-size: 14.5px !important; font-weight: 500; color: var(--ink-3); }
[data-testid="stTab"]:hover p, [data-testid="stTab"][aria-selected="true"] p { color: var(--ink); }
[data-testid="stTab"] .react-aria-SelectionIndicator { background: var(--accent); height: 2px; }
[data-testid="stTabs"] [role="tabpanel"] { padding-top: 28px; }

/* nested result tabs: smaller */
[data-testid="stTabs"] [data-testid="stTabs"] [role="tablist"] { gap: 22px; }
[data-testid="stTabs"] [data-testid="stTabs"] [data-testid="stTab"] { min-height: 38px; }
[data-testid="stTabs"] [data-testid="stTabs"] [data-testid="stTab"] p { font-size: 13.5px !important; }
[data-testid="stTabs"] [data-testid="stTabs"] [role="tabpanel"] { padding-top: 22px; }

/* ---- buttons ------------------------------------------------------- */
.stButton button, .stDownloadButton button, .stFormSubmitButton button {
  border-radius: 4px; font-weight: 500; font-size: 14px;
  padding: 0.45rem 1.1rem; box-shadow: none;
  border: 1px solid var(--rule-strong); background: var(--surface); color: var(--ink);
}
.stButton button:hover, .stDownloadButton button:hover {
  border-color: var(--ink); color: var(--ink);
}
.stButton button[kind="primary"], .stDownloadButton button[kind="primary"],
.stFormSubmitButton button[kind="primaryFormSubmit"] {
  background: var(--accent); border-color: var(--accent); color: #fff;
}
.stButton button[kind="primary"]:hover, .stDownloadButton button[kind="primary"]:hover {
  background: #173D30; border-color: #173D30; color: #fff;
}
.stButton button[kind="tertiary"] {
  border: none; background: transparent; padding: 0.2rem 0; color: var(--accent);
  font-family: var(--mono); font-size: 12.5px; text-decoration: underline;
  text-underline-offset: 3px; text-decoration-color: var(--rule-strong);
}
.stButton button[kind="tertiary"]:hover { text-decoration-color: var(--accent); }

/* ---- inputs -------------------------------------------------------- */
.stTextInput input, .stNumberInput input {
  font-family: var(--mono); font-size: 14px; background: var(--surface);
}
.stTextInput label p, .stNumberInput label p, .stFileUploader label p {
  font-size: 12px; font-weight: 500; color: var(--ink-2);
  text-transform: uppercase; letter-spacing: 0.06em;
}
[data-testid="stFileUploaderDropzone"] {
  background: var(--surface); border: 1px dashed var(--rule-strong); border-radius: 4px;
}

/* ---- tables, expanders, alerts ------------------------------------ */
[data-testid="stDataFrame"] { border: 1px solid var(--rule); border-radius: 4px; }
[data-testid="stExpander"] details {
  border: 1px solid var(--rule); border-radius: 4px; background: var(--surface);
}
[data-testid="stExpander"] summary p { font-size: 14px; font-weight: 500; }
[data-testid="stAlert"] { border-radius: 4px; }
hr { border-color: var(--rule) !important; }

/* ---- section heading ---------------------------------------------- */
.sec { margin: 0 0 22px; }
.sec-k {
  font-family: var(--mono); font-size: 11.5px; color: var(--accent);
  text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 6px;
}
.sec-t { font-family: var(--serif); font-size: 28px; font-weight: 500; color: var(--ink); line-height: 1.2; }
.sec-n { font-size: 15px; color: var(--ink-2); margin-top: 6px; max-width: 62ch; }
.sub-t {
  font-family: var(--serif); font-size: 19px; font-weight: 500; color: var(--ink);
  margin: 6px 0 12px;
}

/* ---- stat cards ---------------------------------------------------- */
.stats {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
  border: 1px solid var(--rule); background: var(--surface); border-radius: 4px;
  margin: 4px 0 22px;
}
.stat { padding: 18px 20px; border-left: 1px solid var(--rule); }
.stat:first-child { border-left: none; }
.stat-l {
  font-size: 11.5px; color: var(--ink-3); text-transform: uppercase;
  letter-spacing: 0.08em; font-weight: 500;
}
.stat-v {
  font-family: var(--serif); font-size: 30px; color: var(--ink);
  margin-top: 6px; line-height: 1.1; font-variant-numeric: tabular-nums;
}
.stat-v small { font-family: var(--sans); font-size: 13px; color: var(--ink-3); margin-left: 3px; }
@media (max-width: 640px) {
  .stat { border-left: none; border-top: 1px solid var(--rule); }
  .stat:first-child { border-top: none; }
}

/* ---- badges -------------------------------------------------------- */
.badge {
  display: inline-block; font-size: 12px; font-weight: 500; padding: 3px 9px;
  border-radius: 3px; letter-spacing: 0.02em; vertical-align: middle;
}
.b-good { background: var(--accent-soft); color: var(--accent); }
.b-warn { background: var(--amber-soft); color: var(--amber); }
.b-bad  { background: var(--red-soft); color: var(--red); }
.b-neutral { background: #ECE8E0; color: var(--ink-2); }

/* ---- note / callout ----------------------------------------------- */
.note {
  border-left: 2px solid var(--accent); background: var(--surface);
  padding: 14px 18px; margin: 0 0 22px; font-size: 15px; color: var(--ink);
  border-radius: 0 4px 4px 0;
}
.note-t {
  font-size: 11.5px; font-weight: 500; color: var(--accent);
  text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 4px;
}
.note.warn { border-left-color: var(--amber); }
.note.warn .note-t { color: var(--amber); }

/* ---- score bars ---------------------------------------------------- */
.bars { display: flex; flex-direction: column; gap: 16px; }
.bar-h { display: flex; justify-content: space-between; font-size: 13.5px; color: var(--ink-2); }
.bar-h b { font-family: var(--mono); font-weight: 500; color: var(--ink); }
.bar-t { height: 6px; background: #ECE8E0; border-radius: 3px; margin-top: 7px; overflow: hidden; }
.bar-f { height: 100%; background: var(--accent); border-radius: 3px; }

/* ---- definition list (interpretations) ---------------------------- */
.dl { border-top: 1px solid var(--rule); }
.dl-r { display: grid; grid-template-columns: 120px 1fr; gap: 18px; padding: 14px 0; border-bottom: 1px solid var(--rule); }
.dl-k { font-size: 12px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.08em; color: var(--ink-3); padding-top: 2px; }
.dl-v { font-size: 14.5px; color: var(--ink); line-height: 1.55; }
@media (max-width: 640px) { .dl-r { grid-template-columns: 1fr; gap: 4px; } }

/* ---- feature cards (overview) ------------------------------------- */
.cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px; margin: 8px 0 36px; }
.card {
  background: var(--surface); border: 1px solid var(--rule); border-radius: 4px;
  padding: 22px 22px 20px; display: flex; flex-direction: column; gap: 10px;
  transition: border-color .15s ease;
}
.card:hover { border-color: var(--rule-strong); }
.card-n { font-family: var(--mono); font-size: 12px; color: var(--accent); }
.card-t { font-family: var(--serif); font-size: 21px; font-weight: 500; color: var(--ink); }
.card-d { font-size: 14.5px; color: var(--ink-2); line-height: 1.5; flex: 1; }
.card-m {
  font-family: var(--mono); font-size: 11.5px; color: var(--ink-3);
  border-top: 1px solid var(--rule); padding-top: 12px; margin-top: 4px;
}

/* ---- hero ----------------------------------------------------------- */
.hero { padding: 18px 0 30px; }
.hero-t {
  font-family: var(--serif); font-size: 44px; font-weight: 400; line-height: 1.12;
  color: var(--ink); letter-spacing: -0.015em; max-width: 20ch;
}
.hero-t em { font-style: italic; color: var(--accent); }
.hero-s { font-size: 17px; color: var(--ink-2); margin-top: 16px; max-width: 54ch; line-height: 1.55; }
@media (max-width: 640px) { .hero-t { font-size: 32px; } }

/* ---- workflow steps ------------------------------------------------ */
.steps { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); border-top: 1px solid var(--ink); }
.step { padding: 16px 18px 6px 0; }
.step-n { font-family: var(--mono); font-size: 12px; color: var(--ink-3); }
.step-t { font-weight: 600; font-size: 15px; color: var(--ink); margin-top: 6px; }
.step-d { font-size: 14px; color: var(--ink-2); margin-top: 4px; line-height: 1.5; }

/* ---- plan cards ---------------------------------------------------- */
.plans { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 14px; }
.plan { border: 1px solid var(--rule); border-radius: 4px; padding: 14px 16px; background: var(--surface); }
.plan.on { border-color: var(--accent); box-shadow: inset 0 0 0 1px var(--accent); }
.plan-t { font-size: 12px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.08em; color: var(--ink-3); }
.plan-p { font-family: var(--serif); font-size: 24px; color: var(--ink); margin-top: 4px; }
.plan-d { font-size: 13px; color: var(--ink-2); margin-top: 2px; }

/* ---- smiles line --------------------------------------------------- */
.mol { display: flex; flex-wrap: wrap; align-items: center; gap: 12px; margin: 4px 0 16px; }
.mol-s {
  font-family: var(--mono); font-size: 15px; color: var(--ink);
  background: var(--surface); border: 1px solid var(--rule); padding: 6px 12px; border-radius: 4px;
  word-break: break-all;
}

/* ---- footer -------------------------------------------------------- */
.foot {
  margin-top: 56px; padding-top: 16px; border-top: 1px solid var(--rule);
  display: flex; justify-content: space-between; flex-wrap: wrap; gap: 8px;
  font-size: 12.5px; color: var(--ink-3);
}
.small { font-size: 13px; color: var(--ink-3); }
</style>
"""

_MARK_SVG = (
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 40 40' fill='none' "
    "stroke='#1F4E3D' stroke-width='1.6' stroke-linejoin='round'>"
    "<path d='M20 4 L34 12 L34 28 L20 36 L6 28 L6 12 Z'/>"
    "<path d='M20 10 L29 15 L29 25 L20 30 L11 25 L11 15 Z' stroke-width='1.1'/>"
    "<circle cx='20' cy='4' r='1.8' fill='#1F4E3D' stroke='none'/>"
    "<circle cx='34' cy='28' r='1.8' fill='#1F4E3D' stroke='none'/>"
    "<circle cx='6' cy='28' r='1.8' fill='#1F4E3D' stroke='none'/></svg>"
)
_MARK = (
    '<img class="mh-mark" alt="" src="data:image/svg+xml;base64,'
    + base64.b64encode(_MARK_SVG.encode()).decode()
    + '">'
)


def _html(markup: str) -> None:
    st.html(markup)


def apply_theme() -> None:
    """Inject the global stylesheet."""
    st.html(_CSS)


def masthead() -> None:
    _html(
        f"""
        <div class="mh">
          <div class="mh-brand">
            {_MARK}
            <div>
              <div class="mh-name">MOLE-AI</div>
              <div class="mh-tag">Computational drug discovery</div>
            </div>
          </div>
          <div class="mh-meta">Version 2<br>Research use</div>
        </div>
        """
    )


def section(title: str, kicker: str | None = None, note: str | None = None) -> None:
    k = f'<div class="sec-k">{escape(kicker)}</div>' if kicker else ""
    n = f'<div class="sec-n">{escape(note)}</div>' if note else ""
    _html(f'<div class="sec">{k}<div class="sec-t">{escape(title)}</div>{n}</div>')


def subheading(title: str) -> None:
    _html(f'<div class="sub-t">{escape(title)}</div>')


def stats(items) -> None:
    """items: iterable of (label, value, unit_or_None)."""
    cells = []
    for label, value, unit in items:
        u = f"<small>{escape(str(unit))}</small>" if unit else ""
        cells.append(
            f'<div class="stat"><div class="stat-l">{escape(str(label))}</div>'
            f'<div class="stat-v">{escape(str(value))}{u}</div></div>'
        )
    _html(f'<div class="stats">{"".join(cells)}</div>')


def tone_for(text: str | None) -> str:
    t = (text or "").lower()
    if "high" in t or "drug-like" in t and "not" not in t or "active" == t.strip():
        return "good"
    if "medium" in t or "moderate" in t:
        return "warn"
    if "low" in t or "not" in t or "inactive" in t or "error" in t:
        return "bad"
    return "neutral"


def badge_html(text: str, tone: str | None = None) -> str:
    tone = tone or tone_for(text)
    return f'<span class="badge b-{tone}">{escape(str(text))}</span>'


def note(text: str, title: str | None = None, warn: bool = False) -> None:
    t = f'<div class="note-t">{escape(title)}</div>' if title else ""
    cls = "note warn" if warn else "note"
    _html(f'<div class="{cls}">{t}{escape(str(text))}</div>')


def score_bars(items) -> None:
    """items: iterable of (label, value 0-100)."""
    rows = []
    for label, value in items:
        v = max(0.0, min(100.0, float(value)))
        rows.append(
            f'<div><div class="bar-h"><span>{escape(label)}</span><b>{v:.1f}</b></div>'
            f'<div class="bar-t"><div class="bar-f" style="width:{v:.1f}%"></div></div></div>'
        )
    _html(f'<div class="bars">{"".join(rows)}</div>')


def definition_list(items) -> None:
    """items: iterable of (key, value_text)."""
    rows = "".join(
        f'<div class="dl-r"><div class="dl-k">{escape(k)}</div>'
        f'<div class="dl-v">{escape(str(v))}</div></div>'
        for k, v in items
        if v
    )
    _html(f'<div class="dl">{rows}</div>')


def molecule_line(smiles: str, badge: str | None = None) -> None:
    b = badge_html(badge) if badge else ""
    _html(f'<div class="mol"><span class="mol-s">{escape(smiles)}</span>{b}</div>')


def hero(title_html: str, subtitle: str) -> None:
    _html(
        f'<div class="hero"><div class="hero-t">{title_html}</div>'
        f'<div class="hero-s">{escape(subtitle)}</div></div>'
    )


def feature_cards(items) -> None:
    """items: iterable of (number, title, description, meta)."""
    cards = "".join(
        f'<div class="card"><div class="card-n">{escape(n)}</div>'
        f'<div class="card-t">{escape(t)}</div>'
        f'<div class="card-d">{escape(d)}</div>'
        f'<div class="card-m">{escape(m)}</div></div>'
        for n, t, d, m in items
    )
    _html(f'<div class="cards">{cards}</div>')


def steps(items) -> None:
    """items: iterable of (title, description)."""
    cells = "".join(
        f'<div class="step"><div class="step-n">{i:02d}</div>'
        f'<div class="step-t">{escape(t)}</div><div class="step-d">{escape(d)}</div></div>'
        for i, (t, d) in enumerate(items, start=1)
    )
    _html(f'<div class="steps">{cells}</div>')


def plans(free_limit: int, paid_limit: int, active: str | None = None) -> None:
    free_on = " on" if active == "free" else ""
    paid_on = " on" if active == "paid" else ""
    _html(
        f"""
        <div class="plans">
          <div class="plan{free_on}"><div class="plan-t">Free</div>
            <div class="plan-p">€0</div><div class="plan-d">Up to {free_limit} molecules</div></div>
          <div class="plan{paid_on}"><div class="plan-t">Batch</div>
            <div class="plan-p">€49</div><div class="plan-d">Up to {paid_limit} molecules, PDF report</div></div>
        </div>
        """
    )


def small(text: str) -> None:
    _html(f'<div class="small">{escape(text)}</div>')


def footer() -> None:
    _html(
        '<div class="foot"><span>MOLE-AI v2</span>'
        "<span>Computational predictions. Validate experimentally before any "
        "biological or clinical decision.</span></div>"
    )

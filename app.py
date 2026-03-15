import streamlit as st
import json
from pathlib import Path
from datetime import datetime

# ══════════════════════════════════════════════════════════════════════════════
# CONFIG
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(page_title="Daily Task Manager", page_icon="✅", layout="centered")

# ── Store data in user's home directory so it always persists on their system ──
DATABASE = Path.home() / ".task_manager" / "data.json"
DATABASE.parent.mkdir(parents=True, exist_ok=True)

CATEGORIES = {
    "🏢 Work":      {"color": "#60a5fa", "bg": "rgba(96,165,250,0.15)"},
    "👤 Personal":  {"color": "#c084fc", "bg": "rgba(192,132,252,0.15)"},
    "💪 Health":    {"color": "#34d399", "bg": "rgba(52,211,153,0.15)"},
    "🛒 Shopping":  {"color": "#fb923c", "bg": "rgba(251,146,60,0.15)"},
    "💡 Other":     {"color": "#94a3b8", "bg": "rgba(148,163,184,0.15)"},
}
CAT_LIST = list(CATEGORIES.keys())

# ══════════════════════════════════════════════════════════════════════════════
# DATA LAYER
# ══════════════════════════════════════════════════════════════════════════════
def load_tasks():
    if DATABASE.exists():
        with DATABASE.open("r") as f:
            data = json.load(f)
        for t in data:          # back-compat migration
            t.setdefault("category",   "💡 Other")
            t.setdefault("created_at", datetime.now().strftime("%b %d, %Y"))
        return data
    return []

def save_tasks(data):
    with DATABASE.open("w") as f:
        json.dump(data, f, indent=4)

# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
DEFAULTS = {
    "tasks": None, "theme": "dark",
    "input_key": 0, "editing": None,
    "toast": None, "just_completed": [],
    "confirm_delete": None,
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

if st.session_state.tasks is None:
    st.session_state.tasks = load_tasks()

tasks   = st.session_state.tasks
is_dark = st.session_state.theme == "dark"

# Consume just_completed for this render cycle only
_anim_ids = list(st.session_state.just_completed)
st.session_state.just_completed = []

# ══════════════════════════════════════════════════════════════════════════════
# THEME VARIABLES
# ══════════════════════════════════════════════════════════════════════════════
if is_dark:
    T = dict(
        app_bg="linear-gradient(135deg,#0f0c29 0%,#302b63 55%,#24243e 100%)",
        card_bg="rgba(255,255,255,0.055)", card_hover="rgba(255,255,255,0.095)",
        card_border="rgba(255,255,255,0.09)",
        done_bg="rgba(52,211,153,0.07)", done_border="rgba(52,211,153,0.22)",
        edit_bg="rgba(167,139,250,0.10)", edit_border="rgba(167,139,250,0.40)",
        text1="#e2e8f0", text2="#94a3b8", text_muted="#64748b",
        text_done="#4b5563", hero_sub="#94a3b8",
        stat_bg="rgba(255,255,255,0.06)", stat_border="rgba(255,255,255,0.10)",
        inp_bg="rgba(255,255,255,0.07)", inp_border="rgba(167,139,250,0.40)",
        inp_color="#f1f5f9", inp_ph="#475569",
        prog_track="rgba(255,255,255,0.08)",
        tab_bg="rgba(255,255,255,0.05)", tab_act_bg="rgba(124,58,237,0.55)",
        tab_color="#94a3b8", tab_act_col="#ffffff",
        divider="rgba(255,255,255,0.07)", sec_label="#64748b",
        empty_col="#475569",
        sel_bg="rgba(255,255,255,0.07)", sel_color="#f1f5f9",
        sec_btn_bg="rgba(255,255,255,0.08)", sec_btn_col="#e2e8f0",
        sec_btn_bdr="rgba(255,255,255,0.12)",
        conf_bg="rgba(239,68,68,0.10)", conf_border="rgba(239,68,68,0.30)",
        bar_track="rgba(255,255,255,0.07)",
    )
else:
    T = dict(
        app_bg="linear-gradient(135deg,#f0f4ff 0%,#e8eeff 55%,#f5f0ff 100%)",
        card_bg="rgba(255,255,255,0.92)", card_hover="rgba(255,255,255,1.0)",
        card_border="rgba(0,0,0,0.08)",
        done_bg="rgba(16,185,129,0.06)", done_border="rgba(16,185,129,0.22)",
        edit_bg="rgba(167,139,250,0.07)", edit_border="rgba(124,58,237,0.35)",
        text1="#1e293b", text2="#475569", text_muted="#94a3b8",
        text_done="#9ca3af", hero_sub="#64748b",
        stat_bg="rgba(255,255,255,0.95)", stat_border="rgba(0,0,0,0.07)",
        inp_bg="rgba(255,255,255,0.95)", inp_border="rgba(124,58,237,0.30)",
        inp_color="#1e293b", inp_ph="#94a3b8",
        prog_track="rgba(0,0,0,0.06)",
        tab_bg="rgba(0,0,0,0.04)", tab_act_bg="rgba(124,58,237,0.12)",
        tab_color="#64748b", tab_act_col="#6d28d9",
        divider="rgba(0,0,0,0.07)", sec_label="#94a3b8",
        empty_col="#94a3b8",
        sel_bg="rgba(255,255,255,0.95)", sel_color="#1e293b",
        sec_btn_bg="rgba(0,0,0,0.05)", sec_btn_col="#374151",
        sec_btn_bdr="rgba(0,0,0,0.10)",
        conf_bg="rgba(239,68,68,0.06)", conf_border="rgba(239,68,68,0.20)",
        bar_track="rgba(0,0,0,0.06)",
    )

# ══════════════════════════════════════════════════════════════════════════════
# CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {{ font-family: 'Sora', sans-serif !important; }}
.stApp {{ background: {T['app_bg']} !important; min-height: 100vh; }}
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding-top:1.2rem !important; padding-bottom:3rem !important; max-width:760px !important; }}

/* Hero */
.hero {{ text-align:center; padding:1.2rem 1rem 0.8rem; }}
.hero h1 {{
    font-size:2.5rem; font-weight:800; letter-spacing:-0.03em; margin:0;
    background:linear-gradient(90deg,#a78bfa,#60a5fa,#34d399);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
}}
.hero p {{ color:{T['hero_sub']}; font-size:0.9rem; font-weight:300; margin-top:0.25rem; }}

/* Stats row */
.stats-row {{ display:flex; gap:0.7rem; margin:1rem 0; }}
.stat-card {{
    flex:1; background:{T['stat_bg']}; border:1px solid {T['stat_border']};
    border-radius:16px; padding:0.9rem 0.8rem; text-align:center;
    backdrop-filter:blur(12px); box-shadow:0 2px 14px rgba(0,0,0,0.08);
}}
.stat-num {{ font-size:1.85rem; font-weight:800; line-height:1; }}
.stat-lbl {{ font-size:0.67rem; text-transform:uppercase; letter-spacing:0.12em; color:{T['text_muted']}; margin-top:0.2rem; }}
.stat-total   .stat-num {{ color:#a78bfa; }}
.stat-done    .stat-num {{ color:#34d399; }}
.stat-pending .stat-num {{ color:#fb923c; }}

/* Progress — gold → coral → rose */
.stProgress > div > div > div {{ background:linear-gradient(90deg,#f59e0b,#f97316,#f43f5e) !important; border-radius:99px !important; box-shadow:0 0 10px rgba(249,115,22,0.40) !important; }}
.stProgress > div > div       {{ background:{T['prog_track']} !important; border-radius:99px !important; height:10px !important; }}
.prog-label {{ text-align:center; color:{T['text_muted']}; font-size:0.75rem; margin-top:-0.3rem; margin-bottom:0.5rem; }}

/* Inputs */
.stTextInput > div > div > input,
.stTextArea  > div > div > textarea {{
    background:{T['inp_bg']} !important; border:1.5px solid {T['inp_border']} !important;
    border-radius:12px !important; color:{T['inp_color']} !important;
    font-family:'Sora',sans-serif !important; font-size:0.92rem !important;
}}
.stTextInput > div > div > input:focus,
.stTextArea  > div > div > textarea:focus {{
    border-color:#7c3aed !important; box-shadow:0 0 0 3px rgba(124,58,237,0.18) !important;
}}
.stTextInput > div > div > input::placeholder,
.stTextArea  > div > div > textarea::placeholder {{ color:{T['inp_ph']} !important; }}
.stTextInput label, .stTextArea label, .stSelectbox label {{
    color:{T['text2']} !important; font-size:0.82rem !important; font-weight:600 !important;
}}

/* Selectbox */
.stSelectbox > div > div {{
    background:{T['sel_bg']} !important; border:1.5px solid {T['inp_border']} !important;
    border-radius:12px !important; color:{T['sel_color']} !important;
}}

/* Buttons */
.stButton > button {{
    font-family:'Sora',sans-serif !important; font-weight:600 !important;
    border-radius:10px !important; transition:all 0.16s ease !important;
}}
.stButton > button:hover {{ transform:translateY(-1px) !important; filter:brightness(1.1) !important; }}
.stButton > button[kind="primary"] {{
    background:linear-gradient(135deg,#7c3aed,#6d28d9) !important;
    color:#fff !important; border:none !important;
    box-shadow:0 4px 14px rgba(124,58,237,0.35) !important;
}}
.stButton > button[kind="secondary"] {{
    background:{T['sec_btn_bg']} !important; color:{T['sec_btn_col']} !important;
    border:1px solid {T['sec_btn_bdr']} !important;
}}

/* Task card animations */
@keyframes completePop {{
    0%   {{ box-shadow:0 0 0 0   rgba(52,211,153,0.0); background:{T['card_bg']}; }}
    30%  {{ box-shadow:0 0 28px 4px rgba(52,211,153,.45); background:rgba(52,211,153,.12); }}
    100% {{ box-shadow:0 0 0 0   rgba(52,211,153,0.0); background:{T['done_bg']}; }}
}}
@keyframes slideIn {{
    from {{ opacity:0; transform:translateY(-5px); }}
    to   {{ opacity:1; transform:translateY(0); }}
}}

/* Task cards */
.task-card {{
    background:{T['card_bg']}; border:1px solid {T['card_border']};
    border-radius:14px; padding:0.85rem 1.1rem; margin-bottom:0.15rem;
    transition:background .2s,border-color .2s,box-shadow .2s;
    backdrop-filter:blur(10px); animation:slideIn .22s ease;
}}
.task-card:hover  {{ background:{T['card_hover']}; border-color:rgba(167,139,250,.28); }}
.task-card.done   {{ background:{T['done_bg']};    border-color:{T['done_border']}; }}
.task-card.anim   {{ animation:completePop .75s ease-out forwards; }}
.task-card.editing {{ background:{T['edit_bg']}; border-color:{T['edit_border']}; box-shadow:0 0 22px rgba(124,58,237,.18); }}

.task-top {{ display:flex; align-items:center; gap:0.65rem; flex-wrap:wrap; }}
.task-num {{ font-family:'DM Mono',monospace; font-size:0.7rem; color:{T['text_muted']}; min-width:24px; }}
.task-txt {{ flex:1; font-size:0.92rem; font-weight:500; color:{T['text1']}; line-height:1.4; }}
.task-txt.done {{ text-decoration:line-through; color:{T['text_done']}; }}
.cat-badge  {{ font-size:0.67rem; font-weight:700; padding:.18rem .6rem; border-radius:99px; white-space:nowrap; }}
.st-badge   {{ font-size:0.62rem; font-weight:700; text-transform:uppercase; letter-spacing:.08em; padding:.15rem .55rem; border-radius:99px; }}
.st-done    {{ background:rgba(52,211,153,.15);  color:#34d399; }}
.st-pending {{ background:rgba(251,146,60,.15);  color:#fb923c; }}
.task-meta  {{ font-family:'DM Mono',monospace; font-size:0.68rem; color:{T['text_muted']}; margin-top:.32rem; padding-left:32px; }}

/* Confirm box */
.confirm-box {{
    background:{T['conf_bg']}; border:1px solid {T['conf_border']};
    border-radius:12px; padding:0.75rem 1rem; margin-bottom:0.3rem;
}}
.confirm-txt {{ color:#ef4444; font-size:0.83rem; font-weight:500; margin-bottom:0.45rem; }}

/* Empty state */
.empty {{ text-align:center; padding:2.5rem 1rem; color:{T['empty_col']}; }}
.empty .ico {{ font-size:2.8rem; margin-bottom:.5rem; }}
.empty p {{ font-size:0.9rem; line-height:1.6; }}

/* Section label */
.sec-lbl {{ font-size:.71rem; font-weight:600; text-transform:uppercase; letter-spacing:.14em; color:{T['sec_label']}; margin:1.1rem 0 .45rem; }}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {{
    background:{T['tab_bg']} !important; border-radius:12px !important;
    padding:4px !important; gap:3px !important; border-bottom:none !important;
}}
.stTabs [data-baseweb="tab"] {{
    border-radius:9px !important; color:{T['tab_color']} !important;
    font-weight:600 !important; font-size:0.84rem !important; padding:0.36rem 1rem !important;
}}
.stTabs [aria-selected="true"] {{ background:{T['tab_act_bg']} !important; color:{T['tab_act_col']} !important; }}
.stTabs [data-baseweb="tab-panel"] {{ padding-top:1rem !important; }}

/* Divider */
hr {{ border-color:{T['divider']} !important; margin:.9rem 0 !important; }}

/* Expander */
.streamlit-expanderHeader {{
    background:{T['sec_btn_bg']} !important; border-radius:10px !important;
    color:{T['text2']} !important; font-weight:600 !important; font-size:0.87rem !important;
}}

/* Stats bars */
.cat-bar-row {{ display:flex; align-items:center; gap:.65rem; margin-bottom:.55rem; }}
.cat-bar-lbl {{ font-size:.78rem; font-weight:500; color:{T['text2']}; min-width:110px; }}
.cat-bar-track {{ flex:1; height:8px; background:{T['bar_track']}; border-radius:99px; overflow:hidden; }}
.cat-bar-fill  {{ height:100%; border-radius:99px; transition:width .5s ease; }}
.cat-bar-cnt   {{ font-size:.72rem; font-family:'DM Mono',monospace; color:{T['text_muted']}; min-width:35px; text-align:right; }}

/* Alerts */
.stSuccess>div, .stInfo>div, .stWarning>div {{ border-radius:12px !important; font-size:.87rem !important; }}

/* ── Theme toggle pill ── */
.theme-pill {{
    display:inline-flex; align-items:center; gap:.45rem;
    padding:.35rem .9rem; border-radius:99px; cursor:pointer;
    font-size:.82rem; font-weight:700; letter-spacing:.04em;
    border:1.5px solid; transition:all .2s ease;
    user-select:none;
}}
.theme-pill.dark {{
    background:rgba(255,255,255,0.07); border-color:rgba(255,255,255,0.18);
    color:#e2e8f0;
}}
.theme-pill.light {{
    background:rgba(124,58,237,0.08); border-color:rgba(124,58,237,0.28);
    color:#4c1d95;
}}
.theme-pill:hover {{ filter:brightness(1.12); transform:translateY(-1px); }}
.pill-dot {{
    width:18px; height:18px; border-radius:50%; display:grid; place-items:center;
    font-size:12px;
}}

/* ── Reorder + delete icon buttons ── */
button[data-testid="baseButton-secondary"][title="Move up"],
button[data-testid="baseButton-secondary"][title="Move down"] {{
    background:rgba(96,165,250,0.12) !important;
    border:1.5px solid rgba(96,165,250,0.30) !important;
    color:#60a5fa !important; border-radius:8px !important;
    font-size:1rem !important;
    padding:0 !important;
    width:100% !important;
    min-height:34px !important;
    height:34px !important;
    line-height:1 !important;
    display:flex !important;
    align-items:center !important;
    justify-content:center !important;
}}
button[data-testid="baseButton-secondary"][title="Move up"]:hover,
button[data-testid="baseButton-secondary"][title="Move down"]:hover {{
    background:rgba(96,165,250,0.25) !important;
    border-color:#60a5fa !important;
    box-shadow:0 0 10px rgba(96,165,250,.30) !important;
}}
button[data-testid="baseButton-secondary"][title="Delete"] {{
    background:rgba(239,68,68,0.10) !important;
    border:1.5px solid rgba(239,68,68,0.30) !important;
    color:#f87171 !important; border-radius:8px !important;
    font-size:.85rem !important;
}}
button[data-testid="baseButton-secondary"][title="Delete"]:hover {{
    background:rgba(239,68,68,0.22) !important;
    border-color:#ef4444 !important;
    box-shadow:0 0 10px rgba(239,68,68,.30) !important;
    transform:scale(1.06) translateY(-1px) !important;
}}

/* ── Footer ── */
.footer {{
    text-align:center; padding:1.8rem .5rem .5rem;
    font-size:.72rem; color:{T['text_muted']};
    letter-spacing:.04em; font-family:'DM Mono',monospace;
}}
.footer span {{ color:#a78bfa; font-weight:600; }}

</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# HEADER  (theme toggle + hero)
# ══════════════════════════════════════════════════════════════════════════════
_, col_toggle = st.columns([5, 1])
with col_toggle:
    if st.button("💡", key="theme_btn", help="Toggle theme", use_container_width=True):
        st.session_state.theme = "light" if is_dark else "dark"
        st.rerun()

st.markdown("""
<div class="hero">
  <h1>✅ Daily Task Manager</h1>
  <p>Stay focused · Ship your day</p>
</div>
""", unsafe_allow_html=True)

# Toast
if st.session_state.toast:
    msg, kind = st.session_state.toast
    {"success": st.success, "info": st.info, "warn": st.warning}[kind](msg)
    st.session_state.toast = None

# Stats bar
total  = len(tasks)
done_n = sum(1 for t in tasks if t["completed"])
pend_n = total - done_n
pct    = done_n / total if total else 0

st.markdown(f"""
<div class="stats-row">
  <div class="stat-card stat-total">
    <div class="stat-num">{total}</div><div class="stat-lbl">Total</div>
  </div>
  <div class="stat-card stat-done">
    <div class="stat-num">{done_n}</div><div class="stat-lbl">Completed</div>
  </div>
  <div class="stat-card stat-pending">
    <div class="stat-num">{pend_n}</div><div class="stat-lbl">Pending</div>
  </div>
</div>
""", unsafe_allow_html=True)

if total:
    st.progress(pct)
    st.markdown(f'<p class="prog-label">{int(pct*100)}% complete</p>', unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def cat_badge_html(cat: str) -> str:
    info = CATEGORIES.get(cat, CATEGORIES["💡 Other"])
    return (f'<span class="cat-badge" style="color:{info["color"]};'
            f'background:{info["bg"]}">{cat}</span>')

def status_badge_html(done: bool) -> str:
    return ('<span class="st-badge st-done">✓ done</span>' if done
            else '<span class="st-badge st-pending">● pending</span>')

def render_task(i: int, task: dict, show_reorder: bool = True):
    is_done    = task["completed"]
    is_editing = st.session_state.editing == i
    is_anim    = i in _anim_ids

    classes    = "task-card"
    if is_done:    classes += " done"
    if is_anim:    classes += " anim"
    if is_editing: classes += " editing"

    txt_cls = "task-txt done" if is_done else "task-txt"

    st.markdown(f"""
    <div class="{classes}">
      <div class="task-top">
        <span class="task-num">#{i+1:02d}</span>
        <span class="{txt_cls}">{task['task']}</span>
        {cat_badge_html(task.get('category','💡 Other'))}
        {status_badge_html(is_done)}
      </div>
      <div class="task-meta">📅 {task.get('created_at','—')}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Edit form ──────────────────────────────────────────────────────────────
    if is_editing:
        st.markdown('<div class="sec-lbl">✏️ Editing task</div>', unsafe_allow_html=True)
        edit_txt = st.text_input(
            "Task description", value=task["task"],
            key=f"et_{i}", label_visibility="visible"
        )
        edit_cat = st.selectbox(
            "Category", CAT_LIST,
            index=CAT_LIST.index(task.get("category", "💡 Other")),
            key=f"ec_{i}"
        )
        s1, s2, _ = st.columns([1, 1, 4])
        with s1:
            if st.button("💾 Save", key=f"save_{i}", type="primary", use_container_width=True):
                stripped = edit_txt.strip()
                if stripped:
                    st.session_state.tasks[i]["task"]     = stripped
                    st.session_state.tasks[i]["category"] = edit_cat
                    save_tasks(st.session_state.tasks)
                    st.session_state.editing = None
                    st.session_state.toast   = ("Task updated ✨", "success")
                    st.rerun()
                else:
                    st.warning("Task text can't be empty.")
        with s2:
            if st.button("✕ Cancel", key=f"cancel_{i}", use_container_width=True):
                st.session_state.editing = None
                st.rerun()

    # ── Action row ─────────────────────────────────────────────────────────────
    else:
        n = len(tasks)
        up_c, dn_c, edit_c, comp_c, del_c, _ = st.columns([0.4, 0.4, 1.0, 1.0, 0.55, 3.55])
        with up_c:
            if show_reorder and i > 0:
                if st.button("↑", key=f"up_{i}", help="Move up"):
                    st.session_state.tasks[i], st.session_state.tasks[i-1] = \
                        st.session_state.tasks[i-1], st.session_state.tasks[i]
                    save_tasks(st.session_state.tasks)
                    st.rerun()
        with dn_c:
            if show_reorder and i < n - 1:
                if st.button("↓", key=f"dn_{i}", help="Move down"):
                    st.session_state.tasks[i], st.session_state.tasks[i+1] = \
                        st.session_state.tasks[i+1], st.session_state.tasks[i]
                    save_tasks(st.session_state.tasks)
                    st.rerun()
        with edit_c:
            if st.button("✏️ Edit", key=f"edit_{i}", use_container_width=True):
                st.session_state.editing        = i
                st.session_state.confirm_delete = None
                st.rerun()
        with comp_c:
            lbl  = "↩ Undo" if is_done else "✅ Done"
            kind = "secondary" if is_done else "primary"
            if st.button(lbl, key=f"comp_{i}", type=kind, use_container_width=True):
                st.session_state.tasks[i]["completed"] = not is_done
                if not is_done:
                    st.session_state.just_completed = [i]
                    st.session_state.toast = ("🎉 Task completed! Great work!", "success")
                else:
                    st.session_state.toast = ("Task moved back to pending.", "info")
                save_tasks(st.session_state.tasks)
                st.rerun()
        with del_c:
            if st.button("✕", key=f"del_{i}", help="Delete", use_container_width=True):
                st.session_state.confirm_delete = i
                st.session_state.editing        = None
                st.rerun()

    # ── Confirm delete ─────────────────────────────────────────────────────────
    if st.session_state.confirm_delete == i:
        preview = task["task"][:48] + ("…" if len(task["task"]) > 48 else "")
        st.markdown(f"""
        <div class="confirm-box">
          <div class="confirm-txt">⚠️ Delete "<strong>{preview}</strong>"? This cannot be undone.</div>
        </div>
        """, unsafe_allow_html=True)
        c1, c2, _ = st.columns([1.2, 1, 4])
        with c1:
            if st.button("🗑️ Delete", key=f"yes_{i}", use_container_width=True):
                removed = st.session_state.tasks.pop(i)
                save_tasks(st.session_state.tasks)
                st.session_state.confirm_delete = None
                name = removed["task"][:30] + ("…" if len(removed["task"]) > 30 else "")
                st.session_state.toast = (f'Deleted "{name}"', "info")
                st.rerun()
        with c2:
            if st.button("Keep it", key=f"no_{i}", use_container_width=True):
                st.session_state.confirm_delete = None
                st.rerun()

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════════════
tab_tasks, tab_add, tab_stats = st.tabs(["📋  Tasks", "➕  Add Task", "📊  Stats"])

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 · TASKS
# ─────────────────────────────────────────────────────────────────────────────
with tab_tasks:
    if not tasks:
        st.markdown("""
        <div class="empty">
          <div class="ico">🌱</div>
          <p>No tasks yet.<br>Head to <strong>Add Task</strong> to plant your first one!</p>
        </div>""", unsafe_allow_html=True)
    else:
        f_col, s_col = st.columns([1, 2])
        with f_col:
            filt = st.selectbox(
                "Filter", ["All Tasks", "⏳ Pending", "✅ Completed"],
                label_visibility="collapsed", key="filt"
            )
        with s_col:
            search = st.text_input(
                "Search", placeholder="🔍  Search tasks…",
                label_visibility="collapsed", key="search"
            )

        show_reorder = (filt == "All Tasks" and not search.strip())
        found = 0
        for i, task in enumerate(tasks):
            if filt == "⏳ Pending"  and task["completed"]:     continue
            if filt == "✅ Completed" and not task["completed"]: continue
            if search.strip() and search.strip().lower() not in task["task"].lower(): continue
            found += 1
            render_task(i, task, show_reorder=show_reorder)

        if found == 0:
            st.markdown("""
            <div class="empty">
              <div class="ico">🔎</div>
              <p>No tasks match your filter or search.</p>
            </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 · ADD TASK
# ─────────────────────────────────────────────────────────────────────────────
with tab_add:
    st.markdown('<div class="sec-lbl">What do you need to do?</div>', unsafe_allow_html=True)

    inp_col, btn_col = st.columns([4, 1])
    with inp_col:
        # Changing key on each add automatically clears the input
        new_task = st.text_input(
            "Task", placeholder="e.g. Review project proposal…",
            label_visibility="collapsed",
            key=f"newtask_{st.session_state.input_key}"
        )
    with btn_col:
        add_clicked = st.button("Add ✦", type="primary", use_container_width=True, key="add_btn")

    cat_col, _ = st.columns([2, 3])
    with cat_col:
        new_cat = st.selectbox("Category", CAT_LIST, key="new_cat")

    if add_clicked:
        text = new_task.strip()
        if text:
            st.session_state.tasks.append({
                "task":       text,
                "completed":  False,
                "category":   new_cat,
                "created_at": datetime.now().strftime("%b %d, %Y"),
            })
            save_tasks(st.session_state.tasks)
            st.session_state.input_key += 1   # <-- clears text input on rerun
            st.session_state.toast = (f'✦ Added **"{text}"** to {new_cat}!', "success")
            st.rerun()
        else:
            st.warning("Please type something before adding.")

    st.markdown("<hr>", unsafe_allow_html=True)

    with st.expander("📝  Bulk add — paste a list"):
        bulk_txt = st.text_area(
            "Bulk", placeholder="One task per line…",
            height=140, label_visibility="collapsed", key="bulk_txt"
        )
        bulk_cat = st.selectbox("Category for all", CAT_LIST, key="bulk_cat")
        if st.button("Add all tasks", key="bulk_btn", type="primary"):
            lines = [ln.strip() for ln in bulk_txt.splitlines() if ln.strip()]
            if lines:
                today = datetime.now().strftime("%b %d, %Y")
                for ln in lines:
                    st.session_state.tasks.append({
                        "task": ln, "completed": False,
                        "category": bulk_cat, "created_at": today,
                    })
                save_tasks(st.session_state.tasks)
                st.session_state.toast = (f"✦ Added **{len(lines)}** tasks!", "success")
                st.rerun()
            else:
                st.warning("Nothing to add — enter at least one line.")

# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 · STATS
# ─────────────────────────────────────────────────────────────────────────────
with tab_stats:
    if not tasks:
        st.markdown("""
        <div class="empty">
          <div class="ico">📊</div>
          <p>Add some tasks to see your stats!</p>
        </div>""", unsafe_allow_html=True)
    else:
        m1, m2, m3 = st.columns(3)
        m1.metric("Completion Rate", f"{int(pct*100)}%")
        m2.metric("Tasks Remaining", pend_n)
        m3.metric("Total Created",   total)

        # Motivational message
        if pct == 1.0:
            msg_color, msg_text = "#34d399", "🏆 All done! You absolutely crushed it today!"
        elif pct >= 0.7:
            msg_color, msg_text = "#60a5fa", "🔥 Almost there — great momentum!"
        elif pct >= 0.3:
            msg_color, msg_text = "#a78bfa", "✨ Good progress — keep going!"
        else:
            msg_color, msg_text = "#fb923c", "🚀 Let's get rolling!"

        st.markdown(
            f'<p style="text-align:center;font-size:.92rem;color:{msg_color};'
            f'font-weight:600;margin:.6rem 0 1rem">{msg_text}</p>',
            unsafe_allow_html=True
        )

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div class="sec-lbl">Tasks by category</div>', unsafe_allow_html=True)

        for cat, info in CATEGORIES.items():
            cat_tasks = [t for t in tasks if t.get("category", "💡 Other") == cat]
            if not cat_tasks:
                continue
            cat_done  = sum(1 for t in cat_tasks if t["completed"])
            cat_total = len(cat_tasks)
            bar_pct   = int((cat_done / cat_total) * 100)
            st.markdown(f"""
            <div class="cat-bar-row">
              <span class="cat-bar-lbl">{cat}</span>
              <div class="cat-bar-track">
                <div class="cat-bar-fill" style="width:{bar_pct}%;background:{info['color']}"></div>
              </div>
              <span class="cat-bar-cnt">{cat_done}/{cat_total}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div class="sec-lbl">Danger zone</div>', unsafe_allow_html=True)
        with st.expander("🚨  Clear all tasks"):
            st.warning("This will **permanently delete every task**. Are you sure?")
            if st.button("Yes, clear everything", key="clear_all", type="secondary"):
                st.session_state.tasks = []
                save_tasks([])
                st.session_state.toast = ("All tasks cleared.", "warn")
                st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="footer">
  ✦ Designed &amp; built by <span>Mohammad Saad Raza</span><br>
  &copy; 2026 All Rights Reserved
</div>
""", unsafe_allow_html=True)
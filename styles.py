"""
CampusRide Streamlit - Design System & Custom CSS
Light theme: warm neutral canvas, navy text, teal accents.
Keeps Streamlit widgets readable even when browser/app theme is dark.
"""

import streamlit as st


def inject_custom_styles():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        /* ---------- Base theme ---------- */
        :root {
            color-scheme: light;
            --cr-bg: #F8FAFC;
            --cr-surface: #FFFFFF;
            --cr-text: #172033;
            --cr-muted: #475569;
            --cr-border: #E2E8F0;
            --cr-teal: #0D9488;
            --cr-teal-dark: #0F766E;
        }

        html, body, [class*="css"], [data-testid="stAppViewContainer"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
            color: var(--cr-text) !important;
        }

        html, body {
            background: var(--cr-bg) !important;
        }

        .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"],
        [data-testid="stMainBlockContainer"] {
            background: var(--cr-bg) !important;
            color: var(--cr-text) !important;
        }

        /* Streamlit header / toolbar */
        header[data-testid="stHeader"],
        [data-testid="stToolbar"] {
            background: #FFFFFF !important;
            color: var(--cr-text) !important;
        }

        /* ---------- Sidebar ---------- */
        section[data-testid="stSidebar"],
        section[data-testid="stSidebar"] > div {
            background: #FFFFFF !important;
            color: var(--cr-text) !important;
            border-right: 1px solid var(--cr-border);
        }

        section[data-testid="stSidebar"] * {
            color: var(--cr-text);
        }

        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
        section[data-testid="stSidebar"] [data-testid="stCaptionContainer"],
        section[data-testid="stSidebar"] small {
            color: var(--cr-muted) !important;
        }

        /* ---------- Typography ---------- */
        .stApp h1, .stApp h2, .stApp h3, .stApp h4,
        .stApp p, .stApp label, .stApp li,
        .stApp [data-testid="stMarkdownContainer"] {
            color: var(--cr-text);
        }

        .stApp h1, .stApp h2, .stApp h3, .stApp h4 {
            font-weight: 700;
        }

        .stCaption, [data-testid="stCaptionContainer"] {
            color: var(--cr-muted) !important;
        }

        /* ---------- Cards ---------- */
        .cr-brand-card {
            background: #FFFFFF;
            color: var(--cr-text);
            border: 1px solid var(--cr-border);
            border-radius: 12px;
            padding: 16px 20px;
            margin-bottom: 20px;
            box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
        }

        .cr-brand-title {
            font-size: 18px;
            font-weight: 700;
            color: #0F172A;
            letter-spacing: -0.02em;
            margin: 0;
        }

        .cr-brand-tagline {
            font-size: 12px;
            color: #475569;
            margin-top: 2px;
            font-weight: 400;
        }

        .cr-card {
            background: #FFFFFF;
            color: #172033;
            border: 1px solid #E2E8F0;
            border-radius: 10px;
            padding: 16px;
            margin-bottom: 16px;
            box-shadow: 0 1px 2px rgba(15, 23, 42, 0.03);
        }

        .cr-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 4px 10px;
            border-radius: 9999px;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .cr-badge-live {
            background: #F0FDF4;
            color: #166534 !important;
            border: 1px solid #BBF7D0;
        }

        .cr-badge-stale {
            background: #FFFBEB;
            color: #92400E !important;
            border: 1px solid #FDE68A;
        }

        .cr-badge-admin {
            background: #EFF6FF;
            color: #1E40AF !important;
            border: 1px solid #BFDBFE;
        }

        .cr-badge-student {
            background: #F0FDFA;
            color: #0F766E !important;
            border: 1px solid #99F6E4;
        }

        /* ---------- ETA ---------- */
        .cr-eta-card {
            background: #F0FDFA;
            color: #134E4A;
            border: 1px solid #99F6E4;
            border-radius: 10px;
            padding: 16px;
            text-align: center;
            margin-bottom: 16px;
        }

        .cr-eta-value {
            font-size: 28px;
            font-weight: 800;
            color: #0D9488 !important;
            line-height: 1.1;
            margin: 4px 0;
        }

        /* ---------- GPS warning ---------- */
        .cr-stale-banner {
            background: #FFFBEB;
            color: #78350F;
            border: 1px solid #FCD34D;
            border-radius: 8px;
            padding: 12px 16px;
            margin-bottom: 16px;
            display: flex;
            align-items: flex-start;
            gap: 12px;
        }

        .cr-stale-title {
            font-weight: 700;
            color: #92400E !important;
            font-size: 13px;
            margin: 0;
        }

        .cr-stale-desc {
            font-size: 12px;
            color: #92400E !important;
            margin: 2px 0 0 0;
        }

        /* ---------- Metrics ---------- */
        .cr-metric {
            background: #FFFFFF;
            color: #172033;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            padding: 14px;
            text-align: left;
        }

        .cr-metric-label {
            font-size: 11px;
            font-weight: 600;
            color: #475569 !important;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }

        .cr-metric-value {
            font-size: 22px;
            font-weight: 700;
            color: #0F172A !important;
            margin-top: 4px;
        }

        .cr-metric-subtitle {
            font-size: 11px;
            color: #0F766E !important;
            font-weight: 500;
            margin-top: 2px;
        }

        /* ---------- Inputs / selects / radio ---------- */
        .stApp input,
        .stApp textarea {
            background: #FFFFFF !important;
            color: #172033 !important;
            border: 1px solid #CBD5E1 !important;
            caret-color: #0D9488 !important;
        }

        .stApp input::placeholder,
        .stApp textarea::placeholder {
            color: #64748B !important;
            opacity: 1 !important;
        }

        [data-baseweb="select"] > div {
            background: #FFFFFF !important;
            color: #172033 !important;
            border-color: #CBD5E1 !important;
        }

        [data-baseweb="select"] * {
            color: #172033 !important;
        }

        [role="radiogroup"] label,
        [data-testid="stCheckbox"] label {
            color: #172033 !important;
        }

        /* Dropdown menu */
        [data-baseweb="popover"],
        [data-baseweb="menu"],
        [role="listbox"] {
            background: #FFFFFF !important;
            color: #172033 !important;
        }

        [role="option"] {
            color: #172033 !important;
        }

        /* ---------- Buttons ---------- */
        div.stButton > button,
        div[data-testid="stFormSubmitButton"] > button {
            background: #0D9488 !important;
            color: #FFFFFF !important;
            border: 1px solid #0F766E !important;
            border-radius: 7px !important;
            font-weight: 600 !important;
            font-size: 13px !important;
            padding: 6px 16px !important;
            opacity: 1 !important;
        }

        div.stButton > button *,
        div[data-testid="stFormSubmitButton"] > button * {
            color: #FFFFFF !important;
        }

        div.stButton > button:hover,
        div[data-testid="stFormSubmitButton"] > button:hover {
            background: #0F766E !important;
            border-color: #115E59 !important;
        }

        div.stButton > button:disabled {
            background: #CBD5E1 !important;
            color: #475569 !important;
            border-color: #CBD5E1 !important;
        }

        /* Secondary buttons */
        div.stButton > button[kind="secondary"] {
            background: #FFFFFF !important;
            color: #172033 !important;
            border: 1px solid #CBD5E1 !important;
        }

        div.stButton > button[kind="secondary"] * {
            color: #172033 !important;
        }

        div.stButton > button[kind="secondary"]:hover {
            background: #F1F5F9 !important;
            border-color: #94A3B8 !important;
        }

        /* ---------- Alerts ---------- */
        [data-testid="stAlert"] {
            color: #172033 !important;
            opacity: 1 !important;
        }

        [data-testid="stAlert"] p,
        [data-testid="stAlert"] [data-testid="stMarkdownContainer"] {
            color: #172033 !important;
        }

        /* ---------- Tables / dataframe ---------- */
        [data-testid="stDataFrame"],
        [data-testid="stTable"] {
            background: #FFFFFF !important;
            color: #172033 !important;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            overflow: hidden;
        }

        /* ---------- Tabs / expanders ---------- */
        [data-testid="stTabs"] button,
        [data-testid="stExpander"] summary {
            color: #172033 !important;
        }

        [data-testid="stExpander"] {
            background: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 8px !important;
        }

        /* Avoid faded/disabled-looking general text */
        .stApp,
        .stApp * {
            text-shadow: none;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )

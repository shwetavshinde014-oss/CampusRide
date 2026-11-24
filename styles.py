"""
CampusRide — Light Design System
Readable light theme with navy text, teal accents, and consistent Streamlit widgets.
Replace the existing styles.py with this file.
"""

import streamlit as st


def inject_custom_styles():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        :root {
            color-scheme: light;
            --cr-bg: #F8FAFC;
            --cr-surface: #FFFFFF;
            --cr-text: #172033;
            --cr-muted: #52627A;
            --cr-border: #D9E2EC;
            --cr-teal: #0D9488;
            --cr-teal-dark: #0F766E;
            --cr-teal-pale: #F0FDFA;
        }

        html, body, [class*="css"], [data-testid="stAppViewContainer"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
        }

        html, body, .stApp, [data-testid="stAppViewContainer"] {
            background: var(--cr-bg) !important;
            color: var(--cr-text) !important;
        }

        /* Main page and content */
        [data-testid="stMain"],
        [data-testid="stMainBlockContainer"],
        .block-container {
            background: var(--cr-bg) !important;
            color: var(--cr-text) !important;
        }

        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 2rem !important;
            max-width: 1600px;
        }

        /* Streamlit header and toolbar */
        header[data-testid="stHeader"],
        [data-testid="stToolbar"] {
            background: #FFFFFF !important;
        }

        header[data-testid="stHeader"] {
            border-bottom: 1px solid var(--cr-border) !important;
        }

        /* All regular text */
        [data-testid="stMarkdownContainer"],
        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] li,
        [data-testid="stMarkdownContainer"] span,
        [data-testid="stText"],
        [data-testid="stCaptionContainer"],
        .stMarkdown, .stText, .stCaption {
            color: var(--cr-text) !important;
        }

        h1, h2, h3, h4, h5, h6 {
            color: var(--cr-text) !important;
            font-family: 'Inter', sans-serif !important;
            font-weight: 700 !important;
        }

        p, label, span, small {
            color: inherit;
        }

        [data-testid="stCaptionContainer"],
        .stCaption {
            color: var(--cr-muted) !important;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background: #FFFFFF !important;
            border-right: 1px solid var(--cr-border) !important;
        }

        section[data-testid="stSidebar"] > div {
            background: #FFFFFF !important;
        }

        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] h4 {
            color: var(--cr-text) !important;
        }

        /* Cards used by CampusRide */
        .cr-brand-card, .cr-card, .cr-metric {
            background: var(--cr-surface) !important;
            color: var(--cr-text) !important;
            border: 1px solid var(--cr-border) !important;
            border-radius: 12px !important;
            box-shadow: 0 2px 8px rgba(15, 23, 42, 0.045) !important;
        }

        .cr-brand-card {
            padding: 16px 20px;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
        }

        .cr-brand-title {
            font-size: 18px;
            font-weight: 700;
            color: var(--cr-text) !important;
            margin: 0;
        }

        .cr-brand-tagline {
            font-size: 12px;
            color: var(--cr-muted) !important;
            margin-top: 2px;
        }

        .cr-card {
            padding: 16px;
            margin-bottom: 16px;
        }

        .cr-metric {
            padding: 14px;
            text-align: left;
        }

        .cr-metric-label {
            color: var(--cr-muted) !important;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: .04em;
        }

        .cr-metric-value {
            color: var(--cr-text) !important;
            font-size: 22px;
            font-weight: 800;
            margin-top: 4px;
        }

        .cr-metric-subtitle {
            color: var(--cr-teal-dark) !important;
            font-size: 11px;
            font-weight: 600;
            margin-top: 2px;
        }

        /* Badges */
        .cr-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 4px 10px;
            border-radius: 999px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: .04em;
        }

        .cr-badge-live {
            background: #ECFDF5 !important;
            color: #166534 !important;
            border: 1px solid #BBF7D0 !important;
        }

        .cr-badge-stale {
            background: #FFFBEB !important;
            color: #92400E !important;
            border: 1px solid #FDE68A !important;
        }

        .cr-badge-admin {
            background: #EFF6FF !important;
            color: #1D4ED8 !important;
            border: 1px solid #BFDBFE !important;
        }

        .cr-badge-student {
            background: #F0FDFA !important;
            color: #0F766E !important;
            border: 1px solid #99F6E4 !important;
        }

        /* GPS stale banner */
        .cr-stale-banner {
            background: #FFFBEB !important;
            color: #78350F !important;
            border: 1px solid #FCD34D !important;
            border-radius: 10px;
            padding: 12px 16px;
            margin-bottom: 16px;
            display: flex;
            align-items: flex-start;
            gap: 12px;
        }

        .cr-stale-title {
            color: #92400E !important;
            font-size: 14px;
            font-weight: 700;
            margin: 0;
        }

        .cr-stale-desc {
            color: #92400E !important;
            font-size: 12px;
            margin: 3px 0 0;
        }

        /* ETA */
        .cr-eta-card {
            background: var(--cr-teal-pale) !important;
            color: var(--cr-text) !important;
            border: 1px solid #99F6E4 !important;
            border-radius: 12px;
            padding: 16px;
            text-align: center;
            margin-bottom: 16px;
        }

        .cr-eta-value {
            color: var(--cr-teal) !important;
            font-size: 28px;
            font-weight: 800;
            line-height: 1.15;
            margin: 4px 0;
        }

        /* Inputs: text, password, number, date, time */
        div[data-testid="stTextInput"] input,
        div[data-testid="stNumberInput"] input,
        div[data-testid="stDateInput"] input,
        div[data-testid="stTimeInput"] input,
        div[data-testid="stTextArea"] textarea {
            background: #FFFFFF !important;
            color: #172033 !important;
            -webkit-text-fill-color: #172033 !important;
            border: 1px solid #CBD5E1 !important;
            border-radius: 8px !important;
        }

        div[data-testid="stTextInput"] input::placeholder,
        div[data-testid="stTextArea"] textarea::placeholder {
            color: #64748B !important;
            -webkit-text-fill-color: #64748B !important;
            opacity: 1 !important;
        }

        div[data-testid="stTextInput"] label,
        div[data-testid="stNumberInput"] label,
        div[data-testid="stDateInput"] label,
        div[data-testid="stTimeInput"] label,
        div[data-testid="stTextArea"] label,
        div[data-testid="stSelectbox"] label,
        div[data-testid="stRadio"] label,
        div[data-testid="stCheckbox"] label {
            color: #172033 !important;
        }

        /* Selectbox and dropdown */
        div[data-testid="stSelectbox"] [data-baseweb="select"] > div,
        div[data-testid="stMultiSelect"] [data-baseweb="select"] > div {
            background: #FFFFFF !important;
            color: #172033 !important;
            border-color: #CBD5E1 !important;
        }

        div[data-testid="stSelectbox"] [data-baseweb="select"] *,
        div[data-testid="stMultiSelect"] [data-baseweb="select"] * {
            color: #172033 !important;
        }

        [data-baseweb="popover"],
        [data-baseweb="menu"],
        [role="listbox"],
        [role="option"] {
            background: #FFFFFF !important;
            color: #172033 !important;
        }

        [role="option"]:hover {
            background: #F1F5F9 !important;
        }

        /* Buttons and form submit buttons */
        div[data-testid="stButton"] > button,
        div[data-testid="stFormSubmitButton"] > button,
        div.stButton > button,
        button[kind="primary"] {
            background: #0D9488 !important;
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
            border: 1px solid #0D9488 !important;
            border-radius: 8px !important;
            font-weight: 700 !important;
            box-shadow: none !important;
        }

        div[data-testid="stButton"] > button *,
        div[data-testid="stFormSubmitButton"] > button *,
        div.stButton > button *,
        button[kind="primary"] * {
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
        }

        div[data-testid="stButton"] > button:hover,
        div[data-testid="stFormSubmitButton"] > button:hover,
        div.stButton > button:hover,
        button[kind="primary"]:hover {
            background: #0F766E !important;
            border-color: #0F766E !important;
            color: #FFFFFF !important;
        }

        /* Secondary buttons */
        button[kind="secondary"] {
            background: #FFFFFF !important;
            color: #172033 !important;
            -webkit-text-fill-color: #172033 !important;
            border: 1px solid #CBD5E1 !important;
        }

        button[kind="secondary"] * {
            color: #172033 !important;
            -webkit-text-fill-color: #172033 !important;
        }

        button[kind="secondary"]:hover {
            background: #F1F5F9 !important;
            border-color: #94A3B8 !important;
        }

        button:disabled {
            background: #E2E8F0 !important;
            color: #64748B !important;
            -webkit-text-fill-color: #64748B !important;
            border-color: #CBD5E1 !important;
        }

        /* Tabs */
        [data-testid="stTabs"] button,
        [data-testid="stTabs"] button p {
            color: #334155 !important;
        }

        [data-testid="stTabs"] button[aria-selected="true"],
        [data-testid="stTabs"] button[aria-selected="true"] p {
            color: #0F766E !important;
        }

        /* Radio, checkbox, slider */
        div[data-testid="stRadio"] *,
        div[data-testid="stCheckbox"] *,
        div[data-testid="stSlider"] * {
            color: #172033 !important;
        }

        /* Alerts and status messages */
        div[data-testid="stAlert"] {
            color: #172033 !important;
            border-radius: 10px !important;
        }

        div[data-testid="stAlert"] p,
        div[data-testid="stAlert"] span {
            color: inherit !important;
        }

        /* Tables */
        [data-testid="stDataFrame"],
        [data-testid="stTable"] {
            background: #FFFFFF !important;
            border: 1px solid #D9E2EC !important;
            border-radius: 8px !important;
        }

        /* Horizontal rules */
        hr {
            border-color: #D9E2EC !important;
        }

        /* Links */
        a, a:visited {
            color: #0F766E !important;
        }

        /* Keep the dashboard comfortable on narrower screens */
        @media (max-width: 900px) {
            .block-container {
                padding-left: 1rem !important;
                padding-right: 1rem !important;
            }

            .cr-brand-card {
                align-items: flex-start;
                flex-direction: column;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

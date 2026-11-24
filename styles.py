"""
CampusRide Streamlit - Design System & Custom CSS
Enforces warm neutral canvas, deep navy typography, restrained teal accents, and clean SaaS aesthetics.
"""

import streamlit as st

def inject_custom_styles():
    st.markdown("""
    <style>
    /* Google Fonts Inter */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        color: #0F172A;
    }

    /* Main Container background */
    .stApp {
        background-color: #F8F9FA;
    }

    /* Streamlit header adjustments */
    header[data-testid="stHeader"] {
        background-color: #FFFFFF;
        border-bottom: 1px solid #E2E8F0;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E2E8F0;
        box-shadow: 1px 0 2px 0 rgba(15, 23, 42, 0.02);
    }

    /* Custom Header Card */
    .cr-brand-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px 0 rgba(15, 23, 42, 0.04);
        display: flex;
        align-items: center;
        justify-content: space-between;
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
        color: #64748B;
        margin-top: 2px;
        font-weight: 400;
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
        background-color: #F0FDF4;
        color: #166534;
        border: 1px solid #BBF7D0;
    }

    .cr-badge-stale {
        background-color: #FFFBEB;
        color: #92400E;
        border: 1px solid #FDE68A;
    }

    .cr-badge-admin {
        background-color: #EFF6FF;
        color: #1E40AF;
        border: 1px solid #BFDBFE;
    }

    .cr-badge-student {
        background-color: #F0FDFA;
        color: #0F766E;
        border: 1px solid #99F6E4;
    }

    /* Clean Card */
    .cr-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 16px;
        box-shadow: 0 1px 2px 0 rgba(15, 23, 42, 0.03);
    }

    /* ETA Display Card */
    .cr-eta-card {
        background: #F0FDFA;
        border: 1px solid #CCFBF1;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
        margin-bottom: 16px;
    }

    .cr-eta-value {
        font-size: 28px;
        font-weight: 800;
        color: #0D9488;
        line-height: 1.1;
        margin: 4px 0;
    }

    /* Stale Warning Banner */
    .cr-stale-banner {
        background-color: #FFFBEB;
        border: 1px solid #FCD34D;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 16px;
        display: flex;
        align-items: flex-start;
        gap: 12px;
    }

    .cr-stale-title {
        font-weight: 600;
        color: #92400E;
        font-size: 13px;
        margin: 0;
    }

    .cr-stale-desc {
        font-size: 12px;
        color: #B45309;
        margin: 2px 0 0 0;
    }

    /* Metric Box */
    .cr-metric {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 14px;
        text-align: left;
    }

    .cr-metric-label {
        font-size: 11px;
        font-weight: 600;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    .cr-metric-value {
        font-size: 22px;
        font-weight: 700;
        color: #0F172A;
        margin-top: 4px;
    }

    .cr-metric-subtitle {
        font-size: 11px;
        color: #0D9488;
        font-weight: 500;
        margin-top: 2px;
    }

    /* Streamlit Button Overrides */
    div.stButton > button {
        background-color: #0D9488;
        color: #FFFFFF;
        border: 1px solid #0F766E;
        border-radius: 6px;
        font-weight: 600;
        font-size: 13px;
        padding: 6px 16px;
        transition: all 0.15s ease-in-out;
    }

    div.stButton > button:hover {
        background-color: #0F766E;
        border-color: #115E59;
        color: #FFFFFF;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.1);
    }

    /* Primary button variant */
    div.stButton > button[kind="secondary"] {
        background-color: #FFFFFF;
        color: #0F172A;
        border: 1px solid #CBD5E1;
    }

    div.stButton > button[kind="secondary"]:hover {
        background-color: #F8FAFC;
        border-color: #94A3B8;
        color: #0F172A;
    }

    /* Table styling */
    .stDataFrame {
        border-radius: 8px;
        border: 1px solid #E2E8F0;
        overflow: hidden;
    }
    </style>
    """, unsafe_allow_html=True)

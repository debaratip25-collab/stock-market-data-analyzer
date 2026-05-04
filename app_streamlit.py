import streamlit as st
import pandas as pd
from datetime import date

from src.yahoo_fetcher import fetch_from_yahoo
from src.cleaning import clean_stock_data
from src.analytics import add_indicators, summarize
from src.reporting import generate_basic_insights


def apply_accessible_theme(base_font_px: int = 22, high_contrast: bool = True):
    if high_contrast:
        bg = "#0B0F14"
        card = "#111827"
        text = "#F9FAFB"
        muted = "#D1D5DB"
        accent = "#22C55E"
        accent2 = "#60A5FA"
        border = "#374151"
        code_bg = "#0F172A"
    else:
        bg = "white"
        card = "white"
        text = "#111827"
        muted = "#374151"
        accent = "#16A34A"
        accent2 = "#2563EB"
        border = "#E5E7EB"
        code_bg = "#F3F4F6"

    st.markdown(
        f"""
        <style>
        html, body, [class*="css"] {{
            font-size: {base_font_px}px !important;
        }}

        .stApp {{
            background: {bg};
            color: {text};
        }}

        h1 {{
            font-size: {base_font_px + 18}px !important;
            line-height: 1.15 !important;
            color: {text} !important;
        }}
        h2 {{
            font-size: {base_font_px + 10}px !important;
            color: {text} !important;
        }}
        h3 {{
            font-size: {base_font_px + 6}px !important;
            color: {text} !important;
        }}

        p, li, label, div {{
            color: {text};
        }}

        section[data-testid="stSidebar"] {{
            background: {card} !important;
            border-right: 2px solid {border} !important;
        }}
        section[data-testid="stSidebar"] * {{
            font-size: {base_font_px}px !important;
            color: {text} !important;
        }}

        div[data-baseweb="input"] input,
        div[data-baseweb="select"] div,
        div[data-baseweb="textarea"] textarea {{
            background-color: {bg} !important;
            color: {text} !important;
            border: 2px solid {border} !important;
            border-radius: 10px !important;
        }}

        div.stButton > button {{
            font-size: {base_font_px}px !important;
            padding: 0.65rem 1rem !important;
            border-radius: 12px !important;
            border: 2px solid {border} !important;
            background: {accent2} !important;
            color: white !important;
            font-weight: 800 !important;
        }}

        [data-testid="stMetricValue"] {{
            font-size: {base_font_px + 14}px !important;
            color: {accent} !important;
            font-weight: 900 !important;
        }}
        [data-testid="stMetricLabel"] {{
            font-size: {base_font_px}px !important;
            color: {muted} !important;
            font-weight: 800 !important;
        }}

        [data-testid="stDataFrame"] {{
            border: 2px solid {border} !important;
            border-radius: 12px !important;
            overflow: hidden !important;
        }}

        hr {{
            border: none !important;
            border-top: 2px solid {border} !important;
        }}

        a {{
            color: {accent2} !important;
            font-weight: 800 !important;
        }}

        code, pre {{
            background: {code_bg} !important;
            color: {text} !important;
            border: 2px solid {border} !important;
            border-radius: 12px !important;
            font-size: {max(base_font_px - 2, 14)}px !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


st.set_page_config(page_title="Stock Market Data Analyzer", page_icon="📈", layout="wide")

st.sidebar.header("Accessibility")
base_font_px = st.sidebar.slider("Font size (px)", 18, 28, 22, 1)
high_contrast = st.sidebar.toggle("High contrast mode", value=True)
apply_accessible_theme(base_font_px=base_font_px, high_contrast=high_contrast)

st.title("Stock Market Data Analyzer Dashboard")
st.caption("Disclaimer: This dashboard is for educational purposes only and not financial advice.")

st.sidebar.header("Analysis Controls")
ticker = st.sidebar.text_input("Ticker", value="INFY.NS").upper().strip()
start = st.sidebar.date_input("Start date", value=pd.to_datetime("2023-01-01"))
end = st.sidebar.date_input("End date", value=date.today())
show_raw = st.sidebar.checkbox("Show raw data", value=False)
preview_rows = st.sidebar.slider("Rows to preview", 5, 50, 15)
run = st.sidebar.button("Run Analysis")

if run:
    try:
        with st.spinner("Fetching data from Yahoo Finance..."):
            raw = fetch_from_yahoo(ticker=ticker, start=str(start), end=str(end)).df

        df = clean_stock_data(raw)
        df = add_indicators(df)
        summary = summarize(df, ticker=ticker)
        insights = generate_basic_insights(df, summary)

        st.subheader("Key Metrics")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Highest Close", f"{summary['highest_close']:.2f}", summary["highest_close_date"])
        c2.metric("Lowest Close", f"{summary['lowest_close']:.2f}", summary["lowest_close_date"])
        c3.metric("Latest 20D Volatility", f"{summary['volatility_20_latest']:.4f}")
        c4.metric("Max Drawdown", f"{summary['max_drawdown']:.2%}")

        st.divider()

        st.subheader("Charts")

        chart_df = df.reset_index()
        chart_df.columns = [c.lower() for c in chart_df.columns]

        st.markdown("### Closing Price")
        st.line_chart(chart_df.set_index("date")[["close"]], height=420)

        st.markdown("### Moving Averages (SMA 20 / 50 / 200)")
        ma_cols = [c for c in ["close", "sma_20", "sma_50", "sma_200"] if c in chart_df.columns]
        st.line_chart(chart_df.set_index("date")[ma_cols], height=480)

        st.markdown("### Rolling Volatility (20D)")
        if "volatility_20" in chart_df.columns:
            st.line_chart(chart_df.set_index("date")[["volatility_20"]], height=380)

        st.divider()

        st.subheader("Auto-generated Insights")
        for i, text in enumerate(insights, start=1):
            st.write(f"{i}. {text}")

        st.divider()

        st.subheader("Data Preview")
        if show_raw:
            st.write("Raw preview:")
            st.dataframe(raw.head(preview_rows), use_container_width=True)

        st.write("Cleaned + indicators preview:")
        st.dataframe(df.reset_index().head(preview_rows), use_container_width=True)

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("Choose inputs in the sidebar and click **Run Analysis**.")
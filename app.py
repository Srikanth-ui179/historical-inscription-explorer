"""
Historical Inscription Explorer — Streamlit app for browsing South Indian epigraphic records.
"""

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

DATA_FILE = Path(__file__).parent / "inscriptions.json"


@st.cache_data
def load_inscriptions() -> pd.DataFrame:
    """Load inscription records from the local JSON file."""
    if not DATA_FILE.exists():
        st.error(f"Data file not found: `{DATA_FILE.name}`. Place it next to `app.py`.")
        return pd.DataFrame()
    return pd.read_json(DATA_FILE)


def apply_filters(df: pd.DataFrame, search: str, dynasties: list, centuries: list) -> pd.DataFrame:
    """Search across text fields and apply dynasty / century filters."""
    if df.empty:
        return df

    result = df.copy()

    if dynasties:
        result = result[result["dynasty"].isin(dynasties)]

    if centuries:
        result = result[result["century"].isin(centuries)]

    if search.strip():
        query = search.strip().lower()
        mask = (
            result["title"].str.lower().str.contains(query, na=False)
            | result["dynasty"].str.lower().str.contains(query, na=False)
            | result["location"].str.lower().str.contains(query, na=False)
            | result["language"].str.lower().str.contains(query, na=False)
        )
        result = result[mask]

    return result.sort_values("year").reset_index(drop=True)


def render_timeline(df: pd.DataFrame) -> None:
    """Interactive timeline of inscriptions by year."""
    if df.empty:
        st.info("No inscriptions match your filters for the timeline.")
        return

    timeline_df = df.copy()

    fig = px.scatter(
        timeline_df,
        x="year",
        y="dynasty",
        color="dynasty",
        hover_name="title",
        hover_data={
            "date": True,
            "location": True,
            "language": True,
            "year": False,
            "dynasty": False,
        },
        labels={"year": "Year (CE)", "dynasty": "Dynasty"},
        title="Inscription Timeline",
    )
    fig.update_traces(marker=dict(size=14, opacity=0.85, line=dict(width=1, color="white")))
    fig.update_layout(
        height=420,
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Segoe UI, system-ui, sans-serif"),
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="rgba(128,128,128,0.2)")
    fig.update_yaxes(showgrid=False)

    st.plotly_chart(fig, use_container_width=True)


def render_inscription_card(row: pd.Series) -> None:
    """Display a single inscription in a styled card."""
    st.markdown(
        f"""
        <div class="inscription-card">
            <h3 class="card-title">{row['title']}</h3>
            <div class="card-meta">
                <span class="badge dynasty">{row['dynasty']}</span>
                <span class="badge date">{row['date']}</span>
                <span class="badge location">{row['location']}</span>
            </div>
            <div class="card-details">
                <p><strong>Language:</strong> {row['language']}</p>
                <p><strong>Script:</strong> {row['script']}</p>
            </div>
            <p class="card-description">{row['description']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    st.set_page_config(
        page_title="Historical Inscription Explorer",
        page_icon="📜",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Crimson+Pro:wght@400;600&family=DM+Sans:wght@400;500;600&display=swap');

        .stApp {
            background: linear-gradient(165deg, #0f1419 0%, #1a2332 45%, #15202b 100%);
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1e2a3a 0%, #16202d 100%);
            border-right: 1px solid rgba(212, 175, 55, 0.15);
        }

        [data-testid="stSidebar"] .stMarkdown h1,
        [data-testid="stSidebar"] .stMarkdown h2,
        [data-testid="stSidebar"] .stMarkdown h3 {
            color: #e8dcc4 !important;
            font-family: 'Crimson Pro', Georgia, serif !important;
        }

        .hero-title {
            font-family: 'Crimson Pro', Georgia, serif;
            font-size: 2.6rem;
            font-weight: 600;
            color: #f4ecd8;
            margin-bottom: 0.25rem;
            letter-spacing: 0.02em;
        }

        .hero-subtitle {
            font-family: 'DM Sans', sans-serif;
            color: #9ca8b8;
            font-size: 1.05rem;
            margin-bottom: 1.5rem;
        }

        .stat-box {
            background: rgba(30, 42, 58, 0.8);
            border: 1px solid rgba(212, 175, 55, 0.2);
            border-radius: 12px;
            padding: 1rem 1.25rem;
            text-align: center;
        }

        .stat-value {
            font-family: 'Crimson Pro', serif;
            font-size: 2rem;
            color: #d4af37;
            font-weight: 600;
        }

        .stat-label {
            font-family: 'DM Sans', sans-serif;
            font-size: 0.85rem;
            color: #8b98a8;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }

        .inscription-card {
            background: linear-gradient(145deg, rgba(28, 38, 52, 0.95) 0%, rgba(22, 32, 45, 0.98) 100%);
            border: 1px solid rgba(212, 175, 55, 0.18);
            border-radius: 14px;
            padding: 1.35rem 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 4px 24px rgba(0, 0, 0, 0.25);
        }

        .card-title {
            font-family: 'Crimson Pro', Georgia, serif;
            color: #f0e6d2 !important;
            font-size: 1.35rem !important;
            margin: 0 0 0.75rem 0 !important;
            border: none !important;
        }

        .card-meta {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-bottom: 0.85rem;
        }

        .badge {
            font-family: 'DM Sans', sans-serif;
            font-size: 0.78rem;
            padding: 0.25rem 0.65rem;
            border-radius: 6px;
            font-weight: 500;
        }

        .badge.dynasty {
            background: rgba(212, 175, 55, 0.2);
            color: #e8c547;
            border: 1px solid rgba(212, 175, 55, 0.35);
        }

        .badge.date {
            background: rgba(100, 149, 237, 0.15);
            color: #8eb4e8;
            border: 1px solid rgba(100, 149, 237, 0.3);
        }

        .badge.location {
            background: rgba(72, 187, 120, 0.12);
            color: #7dcea0;
            border: 1px solid rgba(72, 187, 120, 0.28);
        }

        .card-details p {
            font-family: 'DM Sans', sans-serif;
            color: #b8c4d0;
            font-size: 0.92rem;
            margin: 0.2rem 0;
        }

        .card-description {
            font-family: 'DM Sans', sans-serif;
            color: #a8b4c0;
            font-size: 0.95rem;
            line-height: 1.55;
            margin: 0.75rem 0 0 0;
            padding-top: 0.75rem;
            border-top: 1px solid rgba(255, 255, 255, 0.06);
        }

        div[data-testid="stMetricValue"] {
            color: #d4af37 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    df = load_inscriptions()
    if df.empty:
        st.stop()

    # —— Sidebar: search & filters ——
    with st.sidebar:
        st.markdown("## Explore")
        st.caption("Search and filter South Indian epigraphic records")

        search = st.text_input(
            "Search",
            placeholder="Title, dynasty, location, language…",
            help="Matches any of: title, dynasty, location, or language.",
            key="search_input",
        )

        st.markdown("### Filters")
        all_dynasties = sorted(df["dynasty"].unique())
        selected_dynasties = st.multiselect(
            "Dynasty",
            options=all_dynasties,
            placeholder="All dynasties",
            key="dynasty_filter",
        )

        all_centuries = sorted(df["century"].unique())
        century_labels = {c: f"{c}th century" for c in all_centuries}
        selected_century_labels = st.multiselect(
            "Century",
            options=[century_labels[c] for c in all_centuries],
            placeholder="All centuries",
            key="century_filter",
        )
        selected_centuries = [
            c for c in all_centuries if century_labels[c] in selected_century_labels
        ]

        st.divider()
        if st.button("Clear all filters", use_container_width=True):
            st.session_state["search_input"] = ""
            st.session_state["dynasty_filter"] = []
            st.session_state["century_filter"] = []
            st.rerun()

    filtered = apply_filters(df, search, selected_dynasties, selected_centuries)

    # —— Header ——
    st.markdown('<p class="hero-title">Historical Inscription Explorer</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="hero-subtitle">Discover temple grants, copper plates, and rock inscriptions from South India</p>',
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(
            f'<div class="stat-box"><div class="stat-value">{len(df)}</div><div class="stat-label">Total records</div></div>',
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f'<div class="stat-box"><div class="stat-value">{len(filtered)}</div><div class="stat-label">Showing</div></div>',
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            f'<div class="stat-box"><div class="stat-value">{df["dynasty"].nunique()}</div><div class="stat-label">Dynasties</div></div>',
            unsafe_allow_html=True,
        )
    with col4:
        year_span = f"{int(df['year'].min())}–{int(df['year'].max())}"
        st.markdown(
            f'<div class="stat-box"><div class="stat-value" style="font-size:1.4rem;">{year_span}</div><div class="stat-label">Year range (CE)</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("")

    tab_timeline, tab_browse = st.tabs(["Timeline", "Browse inscriptions"])

    with tab_timeline:
        st.markdown("#### Chronological overview")
        st.caption("Each point is one inscription. Hover for details; color indicates dynasty.")
        render_timeline(filtered)

    with tab_browse:
        st.markdown("#### Inscription details")
        if filtered.empty:
            st.warning("No inscriptions match your search or filters. Try clearing filters in the sidebar.")
        else:
            for _, row in filtered.iterrows():
                render_inscription_card(row)

    st.divider()
    st.caption("Data source: `inscriptions.json` · Built with Streamlit")


if __name__ == "__main__":
    main()

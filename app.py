"""
Historical Inscription Explorer — Streamlit app for browsing South Indian epigraphic records.
"""

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

DATA_FILE = Path(__file__).parent / "inscriptions.json"

# Short labels for the timeline Y-axis only; full names remain everywhere else.
DYNASTY_AXIS_LABELS = {
    "Early Tamil community (Dameda)": "Dameda",
    "Local chieftaincy (Velir)": "Velir",
    "Athiyaman (Satyaputra)": "Athiyaman",
}

TIMELINE_HOVER_TEMPLATE = (
    "<b>Title:</b> %{hovertext}<br>"
    "<b>Dynasty:</b> %{customdata[0]}<br>"
    "<b>Date:</b> %{customdata[1]}<br>"
    "<b>Location:</b> %{customdata[2]}<br>"
    "<b>Historical Significance:</b> %{customdata[3]}"
    "<extra></extra>"
)


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


def get_significance(row: pd.Series) -> str:
    """Return historical significance text, falling back to description if needed."""
    if "historical_significance" in row.index and pd.notna(row.get("historical_significance")):
        return str(row["historical_significance"])
    return str(row["description"])


def select_inscription(inscription_id: int) -> None:
    st.session_state["selected_inscription_id"] = inscription_id


def clear_selection() -> None:
    st.session_state["selected_inscription_id"] = None


def init_filter_state() -> None:
    """Ensure filter widget keys exist before widgets are drawn."""
    if "search_input" not in st.session_state:
        st.session_state["search_input"] = ""
    if "dynasty_filter" not in st.session_state:
        st.session_state["dynasty_filter"] = []
    if "century_filter" not in st.session_state:
        st.session_state["century_filter"] = []


def clear_filters() -> None:
    """Reset sidebar filters. Invoked via on_click before widgets are instantiated."""
    st.session_state["search_input"] = ""
    st.session_state["dynasty_filter"] = []
    st.session_state["century_filter"] = []


def shorten_dynasty_for_axis(dynasty: str) -> str:
    """Return a compact dynasty label for the timeline Y-axis."""
    return DYNASTY_AXIS_LABELS.get(dynasty, dynasty)


def render_timeline(df: pd.DataFrame) -> None:
    """Interactive timeline of inscriptions by year."""
    if df.empty:
        st.info("No inscriptions match your filters for the timeline.")
        return

    timeline_df = df.copy()
    timeline_df["dynasty_axis"] = timeline_df["dynasty"].map(shorten_dynasty_for_axis)
    timeline_df["significance_hover"] = timeline_df.apply(get_significance, axis=1)

    dynasty_count = timeline_df["dynasty_axis"].nunique()
    chart_height = max(540, min(820, dynasty_count * 24 + 100))

    fig = px.scatter(
        timeline_df,
        x="year",
        y="dynasty_axis",
        color="dynasty",
        hover_name="title",
        custom_data=["dynasty", "date", "location", "significance_hover", "id"],
        labels={"year": "Year (CE)", "dynasty_axis": "Dynasty"},
    )
    fig.update_traces(
        hovertemplate=TIMELINE_HOVER_TEMPLATE,
        marker=dict(size=10, opacity=0.92, line=dict(width=0.6, color="rgba(240, 230, 210, 0.85)")),
        selector=dict(mode="markers"),
    )
    fig.update_layout(
        height=chart_height,
        margin=dict(l=44, r=4, t=0, b=32),
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.01,
            font=dict(size=9, color="#c5d0db"),
            title_font=dict(color="#8b98a8"),
            itemsizing="constant",
            tracegroupgap=2,
            bgcolor="rgba(0,0,0,0)",
        ),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Segoe UI, system-ui, sans-serif", size=11, color="#9ca8b8"),
        xaxis_title="Year (CE)",
        yaxis_title="",
        hoverlabel=dict(
            bgcolor="rgba(22, 32, 45, 0.97)",
            bordercolor="rgba(212, 175, 55, 0.35)",
            font=dict(family="Segoe UI, system-ui, sans-serif", size=12, color="#e8dcc4"),
            align="left",
        ),
        hovermode="closest",
    )
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor="rgba(128, 128, 128, 0.15)",
        zeroline=False,
        title_standoff=2,
        tickfont=dict(size=10, color="#9ca8b8"),
        title_font=dict(color="#8b98a8", size=11),
    )
    fig.update_yaxes(
        showgrid=False,
        automargin=True,
        tickfont=dict(size=10, color="#9ca8b8"),
        categoryorder="category ascending",
    )

    event = st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False, "scrollZoom": False},
        on_select="rerun",
        selection_mode="points",
        key="timeline_chart",
    )

    if event and event.selection and event.selection.points:
        point = event.selection.points[0]
        custom = point.get("customdata")
        if custom and len(custom) >= 5:
            select_inscription(int(custom[4]))
            st.rerun()


def render_inscription_card(row: pd.Series) -> None:
    """Display an inscription card; opens the detail view when clicked."""
    preview = str(row["description"])
    if len(preview) > 140:
        preview = preview[:137] + "…"

    with st.container(border=True):
        st.markdown(
            f"""
            <div class="inscription-card-inner">
                <h3 class="card-title">{row['title']}</h3>
                <div class="card-meta">
                    <span class="badge dynasty">{row['dynasty']}</span>
                    <span class="badge date">{row['date']}</span>
                    <span class="badge location">{row['location']}</span>
                </div>
                <p class="card-preview">{preview}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.button(
            "Open inscription →",
            key=f"card_{row['id']}",
            use_container_width=True,
            type="secondary",
            on_click=select_inscription,
            args=(int(row["id"]),),
        )


def render_detail_page(row: pd.Series) -> None:
    """Full inscription detail view."""
    if st.button("← Back", key="detail_back", type="primary", on_click=clear_selection):
        pass

    st.markdown(
        f"""
        <div class="detail-header">
            <h2 class="detail-title">{row['title']}</h2>
            <div class="card-meta">
                <span class="badge dynasty">{row['dynasty']}</span>
                <span class="badge date">{row['date']}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<p class="detail-section-label">Historical significance</p>', unsafe_allow_html=True)
    st.markdown(
        f'<p class="detail-significance">{get_significance(row)}</p>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="detail-grid">', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    detail_fields = [
        ("Location", row["location"]),
        ("Dynasty", row["dynasty"]),
        ("Date", row["date"]),
        ("Language", row["language"]),
        ("Script", row["script"]),
    ]
    with col_a:
        for label, value in detail_fields[:3]:
            st.markdown(f'<p class="field-label">{label}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="detail-value">{value}</p>', unsafe_allow_html=True)
    with col_b:
        for label, value in detail_fields[3:]:
            st.markdown(f'<p class="field-label">{label}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="detail-value">{value}</p>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<p class="detail-section-label">Description</p>', unsafe_allow_html=True)
    st.markdown(
        f'<p class="detail-description">{row["description"]}</p>',
        unsafe_allow_html=True,
    )


def inject_styles() -> None:
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
            margin-bottom: 0.75rem;
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

        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: linear-gradient(145deg, rgba(28, 38, 52, 0.95) 0%, rgba(22, 32, 45, 0.98) 100%);
            border-color: rgba(212, 175, 55, 0.22) !important;
            border-radius: 14px !important;
            margin-bottom: 0.65rem;
            padding: 0.15rem 0.35rem 0.35rem;
        }

        .inscription-card-inner {
            padding: 0.5rem 0.65rem 0.25rem;
        }

        .card-title {
            font-family: 'Crimson Pro', Georgia, serif;
            color: #f0e6d2 !important;
            font-size: 1.2rem !important;
            margin: 0 0 0.55rem 0 !important;
            border: none !important;
        }

        .card-meta {
            display: flex;
            flex-wrap: wrap;
            gap: 0.45rem;
            margin-bottom: 0.55rem;
        }

        .badge {
            font-family: 'DM Sans', sans-serif;
            font-size: 0.76rem;
            padding: 0.22rem 0.6rem;
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

        .card-preview {
            font-family: 'DM Sans', sans-serif;
            color: #a8b4c0;
            font-size: 0.88rem;
            line-height: 1.45;
            margin: 0;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stButton"] > button {
            background: rgba(212, 175, 55, 0.1);
            border-color: rgba(212, 175, 55, 0.28);
            color: #d4af37;
            font-family: 'DM Sans', sans-serif;
            font-size: 0.85rem;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stButton"] > button:hover {
            background: rgba(212, 175, 55, 0.2);
            border-color: rgba(212, 175, 55, 0.4);
            color: #f0e6d2;
        }

        .detail-title {
            font-family: 'Crimson Pro', Georgia, serif;
            color: #f4ecd8 !important;
            font-size: 2rem !important;
            margin: 0.75rem 0 0.65rem 0 !important;
        }

        .detail-section-label {
            font-family: 'DM Sans', sans-serif;
            color: #8b98a8;
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin: 1rem 0 0.4rem 0;
        }

        .detail-significance {
            font-family: 'DM Sans', sans-serif;
            color: #e8dcc4;
            font-size: 1.05rem;
            line-height: 1.6;
            background: rgba(212, 175, 55, 0.08);
            border-left: 3px solid #d4af37;
            padding: 0.85rem 1rem;
            border-radius: 0 8px 8px 0;
            margin: 0;
        }

        .field-label {
            font-family: 'DM Sans', sans-serif;
            color: #8b98a8;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin: 0 0 0.2rem 0;
        }

        .detail-value {
            font-family: 'DM Sans', sans-serif;
            color: #c5d0db;
            font-size: 0.95rem;
            margin: 0 0 0.85rem 0;
        }

        .detail-description {
            font-family: 'DM Sans', sans-serif;
            color: #a8b4c0;
            font-size: 1rem;
            line-height: 1.65;
            margin: 0 0 1rem 0;
        }

        .timeline-tab [data-testid="stCaptionContainer"] {
            margin-bottom: 0.1rem;
            padding-bottom: 0;
        }

        .timeline-tab [data-testid="stVerticalBlock"] {
            gap: 0.2rem;
        }

        .timeline-tab div[data-testid="stPlotlyChart"] {
            margin-top: -0.5rem;
            margin-bottom: -1rem;
        }

        .timeline-tab .js-plotly-plot .plotly {
            margin-bottom: 0 !important;
        }

        [data-testid="stTabs"] [data-testid="stVerticalBlock"] {
            padding-top: 0.35rem;
        }

        div[data-testid="stMetricValue"] {
            color: #d4af37 !important;
        }
        </style>
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

    if "selected_inscription_id" not in st.session_state:
        st.session_state["selected_inscription_id"] = None

    inject_styles()

    df = load_inscriptions()
    if df.empty:
        st.stop()

    init_filter_state()

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
        st.button(
            "Clear all filters",
            use_container_width=True,
            on_click=clear_filters,
            key="clear_filters_button",
        )

    filtered = apply_filters(df, search, selected_dynasties, selected_centuries)
    selected_id = st.session_state.get("selected_inscription_id")

    if selected_id is not None:
        match = df[df["id"] == selected_id]
        if match.empty:
            clear_selection()
            st.rerun()
        st.markdown('<p class="hero-title">Inscription details</p>', unsafe_allow_html=True)
        render_detail_page(match.iloc[0])
        st.caption("Data source: `inscriptions.json` · Built with Streamlit")
        return

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

    tab_timeline, tab_browse = st.tabs(["Timeline", "Browse inscriptions"])

    with tab_timeline:
        st.markdown('<div class="timeline-tab">', unsafe_allow_html=True)
        st.caption("Hover for details · click a point to open its record")
        render_timeline(filtered)
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_browse:
        st.caption("Open any inscription below to view full historical details.")
        if filtered.empty:
            st.warning("No inscriptions match your search or filters. Try clearing filters in the sidebar.")
        else:
            for _, row in filtered.iterrows():
                render_inscription_card(row)

    st.divider()
    st.caption("Data source: `inscriptions.json` · Built with Streamlit")


if __name__ == "__main__":
    main()

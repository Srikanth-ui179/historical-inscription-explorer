# Historical Inscription Explorer

A full-stack-style data exploration web application built with Python and Streamlit. The app surfaces historically significant South Indian epigraphic records—from Tamil-Brahmi cave inscriptions to Chola copper-plate grants—through search, filtering, and interactive visualisation.

> **Portfolio project** demonstrating data-driven UI development, clean Python architecture, and domain-aware content design for cultural heritage.

---

## Project Overview

**Historical Inscription Explorer** is an interactive dashboard for browsing a curated corpus of South Indian inscriptions stored in a local JSON dataset. Users can search records by title, dynasty, location, and language; narrow results by dynasty and century; inspect full epigraphic metadata in a card-based layout; and explore chronological patterns on an interactive timeline.

The project bridges software engineering and digital humanities: the frontend is a single-page Streamlit application, the data layer is a structured JSON file (no external database required), and the presentation layer uses custom CSS plus Plotly for professional, portfolio-ready visuals.

**Problem addressed:** Historical inscription data is often scattered across academic corpora and difficult for non-specialists to explore. This app provides a lightweight, self-contained interface to discover, filter, and contextualise key epigraphic sources in one place.

---

## Features

| Feature | Description |
|---------|-------------|
| **Full-text search** | Query across title, dynasty, location, and language fields |
| **Multi-select filters** | Filter by dynasty and century independently or in combination |
| **Inscription detail cards** | Display title, date, dynasty, location, language, script, and description |
| **Interactive timeline** | Plotly scatter chart of inscriptions by year (CE) and dynasty with hover details |
| **Dashboard metrics** | Summary stats for total records, filtered count, dynasty coverage, and year span |
| **Responsive sidebar** | Persistent search and filter controls with one-click reset |
| **Cached data loading** | `@st.cache_data` for fast reloads on filter changes |
| **Custom UI theme** | Dark, heritage-inspired design with typography and colour hierarchy |

---

## Technologies Used

| Technology | Role |
|------------|------|
| **Python 3.9+** | Core application language |
| **Streamlit** | Web UI framework, layout, widgets, and session state |
| **Pandas** | JSON ingestion, filtering, sorting, and tabular data handling |
| **Plotly Express** | Interactive timeline visualisation |
| **JSON** | Local, version-controlled data store (`inscriptions.json`) |

**Architecture highlights**

- Modular functions: `load_inscriptions()`, `apply_filters()`, `render_timeline()`, `render_inscription_card()`
- Path-relative data loading via `pathlib` (portable across environments)
- Separation of data (JSON), logic (`app.py`), and dependencies (`requirements.txt`)

---

## Installation

### Prerequisites

- Python 3.9 or later — [python.org/downloads](https://www.python.org/downloads/)
- Git (optional, for cloning)
- A modern web browser

### Steps

**1. Clone or download the repository**

```bash
git clone https://github.com/<your-username>/Historical-Inscription-Explorer.git
cd Historical-Inscription-Explorer
```

**2. Create and activate a virtual environment**

*Windows (PowerShell)*

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

*macOS / Linux*

```bash
python3 -m venv venv
source venv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Run the application**

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501` by default.

**Alternative (Windows launcher)**

```powershell
py -m streamlit run app.py
```

### Troubleshooting

| Issue | Fix |
|-------|-----|
| `streamlit` command not found | Activate the virtual environment and reinstall: `pip install -r requirements.txt` |
| PowerShell blocks venv activation | Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` once |
| Port 8501 in use | `streamlit run app.py --server.port 8502` |
| Missing data file | Ensure `inscriptions.json` sits in the same directory as `app.py` |

---

## Usage

1. Open the **sidebar** and enter a search term (e.g. `Chola`, `Tamil`, `Nagapattinam`).
2. Apply **Dynasty** and/or **Century** filters to narrow the corpus.
3. Review summary metrics at the top of the main view.
4. Switch to the **Timeline** tab for a chronological overview.
5. Switch to the **Browse inscriptions** tab for full record cards.
6. Click **Clear all filters** to reset the sidebar.

---

## Screenshots

Portfolio screenshots live in [`docs/screenshots/`](docs/screenshots/). The folder is tracked in Git via `.gitkeep`; add PNG files there after running the app locally and they will render in this README on GitHub.

| View | File | Preview |
|------|------|---------|
| Home dashboard | `docs/screenshots/dashboard.png` | ![Home dashboard](docs/screenshots/dashboard.png) |
| Timeline | `docs/screenshots/timeline.png` | ![Timeline view](docs/screenshots/timeline.png) |
| Browse inscriptions | `docs/screenshots/browse.png` | ![Inscription cards](docs/screenshots/browse.png) |
| Filtered results | `docs/screenshots/filters.png` | ![Filtered search](docs/screenshots/filters.png) |

### How to add screenshots

1. Start the app: `streamlit run app.py` (or `py -m streamlit run app.py` on Windows).
2. Capture each view at a consistent window size (1280×720 or 1440×900 works well for READMEs).
3. Save the files with these exact names into `docs/screenshots/`:

   | Filename | What to capture |
   |----------|-----------------|
   | `dashboard.png` | Main page with hero title, stat boxes, and sidebar visible |
   | `timeline.png` | **Timeline** tab with the Plotly chart and a few dynasties shown |
   | `browse.png` | **Browse inscriptions** tab with one or more detail cards |
   | `filters.png` | Sidebar filters applied (e.g. dynasty **Chola**) with reduced result count |

4. Commit and push — GitHub will display the images in this section automatically.

> **Note:** Until you add the PNG files, the preview cells above may show broken image links. That is expected; replace them by following the steps above.

---

## Historical Significance

The dataset focuses on landmark South Indian epigraphic sources that shaped our understanding of early Tamil polities, religion, and administration:

| Inscription | Period | Significance |
|-------------|--------|--------------|
| **Mangulam inscriptions** | c. 3rd–2nd c. BCE | Earliest Tamil-Brahmi records; name the Pandya king Nedunjeliyan I |
| **Jambai inscription** | c. 1st c. CE | Links Ashoka's *Satyaputras* to the Athiyaman chieftains |
| **Pugalur inscription** | c. 1st–2nd c. CE | Three-generation Chera genealogy in Tamil-Brahmi |
| **Tamil-Brahmi cave inscriptions** | c. 2nd c. BCE–1st c. CE | Jain monastic patronage in rock-cut caves |
| **Velvikudi grant** | c. 770 CE | Pandya restoration after the Kalabhra interregnum |
| **Leiden plates** | 1006 & 1090 CE | Chola grants to the Nagapattinam Buddhist vihara; Indo–Southeast Asian trade |
| **Thiruvalangadu copper plates** | c. 1018 CE | Authoritative Chola genealogy from Rajendra Chola I |
| **Uttiramerur inscriptions** | 919 & 921 CE | Medieval village self-governance and *kudavolai* elections |
| **Anuradhapura Tamil inscription** | c. 2nd–1st c. BCE | Early Tamil merchant and mariner community in Sri Lanka |
| **Koneswaram inscription** | c. 11th c. CE | Chola patronage of the Tirukonamalai (Trincomalee) shrine |

These records span roughly **three millennia** of written history—from Brahmi cave beds to imperial copper-plate *sasanas*—and illustrate how epigraphy complements literary sources such as Sangam poetry.

**Data sources for further reading**

- [South Indian Inscriptions (ASI)](https://www.whatisindia.com/inscriptions/)
- [Tamil Nadu Department of Archaeology](https://tnarch.gov.in/)
- Iravatham Mahadevan, *Early Tamil Epigraphy* (2003)

---

## Project Structure

```
Historical-Inscription-Explorer/
├── app.py                      # Streamlit application (UI, filters, timeline)
├── inscriptions.json           # Curated epigraphic dataset (16 records)
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
└── docs/
    └── screenshots/
        ├── .gitkeep            # Keeps folder in Git before PNGs are added
        ├── dashboard.png       # (add) Home dashboard screenshot
        ├── timeline.png        # (add) Timeline tab screenshot
        ├── browse.png          # (add) Browse inscriptions screenshot
        └── filters.png         # (add) Filtered results screenshot
```

### Data schema

Each record in `inscriptions.json` follows a consistent schema:

```json
{
  "id": 1,
  "title": "Example Inscription",
  "date": "919 CE",
  "year": 919,
  "century": 10,
  "dynasty": "Chola",
  "location": "Uttaramerur, Tamil Nadu",
  "language": "Tamil",
  "script": "Tamil",
  "description": "Brief scholarly summary of the inscription."
}
```

| Field | Purpose |
|-------|---------|
| `year` | Numeric year for sorting and timeline (BCE values are negative) |
| `century` | Powers century filter and chronological grouping |
| `date` | Human-readable date string shown in the UI |

---

## Future Enhancements

Planned improvements that would extend this from a portfolio demo to a production-grade heritage tool:

- [ ] **Expanded corpus** — Integrate additional records from [South Indian Inscriptions](https://www.whatisindia.com/inscriptions/) or institutional APIs
- [ ] **Detail page routing** — Dedicated view per inscription with transliteration and references
- [ ] **Map visualisation** — Plot inscription locations with Folium or PyDeck
- [ ] **Export** — Download filtered results as CSV or PDF
- [ ] **Database backend** — Migrate from JSON to SQLite or PostgreSQL for larger datasets
- [ ] **Multilingual UI** — Tamil and English interface labels
- [ ] **Image gallery** — Attach photographs of inscriptions and temple sites
- [ ] **Deployment** — Host on Streamlit Community Cloud, Render, or Azure App Service
- [ ] **Automated tests** — Unit tests for filter logic and data validation with `pytest`

---

## Author

Built as a portfolio project demonstrating Python web development, data visualisation, and culturally informed product design.

**Skills demonstrated:** Python · Streamlit · Pandas · Plotly · JSON data modelling · UI/UX · Git · Technical writing

---

## License

This project is provided for educational and portfolio purposes. Epigraphic summaries are based on published scholarly sources; extend the dataset responsibly when adding new records.

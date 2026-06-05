# Historical Inscription Explorer

A beginner-friendly **Streamlit** web app to explore South Indian historical inscriptions stored in a local JSON file. Search, filter by dynasty and century, browse detailed records, and view an interactive timeline.

## What’s in this project?

| File | Purpose |
|------|---------|
| `app.py` | Main application: loads data, search, filters, cards, and timeline |
| `inscriptions.json` | Local database of 28 sample South Indian inscriptions |
| `requirements.txt` | Python packages to install (`streamlit`, `pandas`, `plotly`) |
| `README.md` | This guide |

## Prerequisites

- **Python 3.9+** installed ([python.org](https://www.python.org/downloads/))
- A terminal (PowerShell, Command Prompt, or VS Code terminal)

## Quick start

### 1. Open the project folder

```powershell
cd C:\Users\KIIT\OneDrive\Desktop\Historical-Inscription-Explorer
```

### 2. Create a virtual environment (recommended)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run once:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Run the app

```powershell
streamlit run app.py
```

Your browser should open at `http://localhost:8501`. If it does not, copy that URL from the terminal.

## How to use the app

1. **Search** (sidebar): Type any word matching title, dynasty, location, or language.
2. **Filter by dynasty**: Choose one or more dynasties (e.g. Chola, Pallava).
3. **Filter by century**: Choose centuries (e.g. 11th century).
4. **Timeline tab**: Scatter plot of inscriptions by year and dynasty.
5. **Browse tab**: Cards showing title, date, dynasty, location, language, script, and description.

Click **Clear all filters** in the sidebar to reset.

## JSON data format

Each record in `inscriptions.json` looks like this:

```json
{
  "id": 1,
  "title": "Example Inscription",
  "date": "1010 CE",
  "year": 1010,
  "century": 11,
  "dynasty": "Chola",
  "location": "Thanjavur, Tamil Nadu",
  "language": "Tamil",
  "script": "Tamil",
  "description": "Short summary of the inscription."
}
```

- `year` and `century` power sorting, the timeline, and century filters.
- You can add more objects to the JSON array; restart or refresh the app to see them.

## Project structure

```
Historical-Inscription-Explorer/
├── app.py
├── inscriptions.json
├── requirements.txt
└── README.md
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `streamlit` not found | Activate your venv and run `pip install -r requirements.txt` again |
| Empty app / error about JSON | Ensure `inscriptions.json` is in the same folder as `app.py` |
| Port already in use | Run `streamlit run app.py --server.port 8502` |

## Learn more

- [Streamlit docs](https://docs.streamlit.io/)
- [Pandas JSON I/O](https://pandas.pydata.org/docs/reference/api/pandas.read_json.html)
- [Plotly Express](https://plotly.com/python/plotly-express/)

## License

Sample educational project — feel free to extend with real epigraphic data from corpora such as [South Indian Inscriptions](https://www.whatisindia.com/inscriptions/) or institutional archives.

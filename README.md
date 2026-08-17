# DatasetGuard AI

DatasetGuard AI is an original dataset-quality and annotation-audit platform built with Python and Streamlit.

## Features
- CSV dataset profiling
- Exact duplicate detection
- Text similarity duplicate detection
- Label consistency and distribution analysis
- Numeric outlier detection
- Potential PII pattern scanning
- Explainable 0-100 quality score
- Clean CSV export
- PDF audit report
- Automated tests
- GitHub Actions CI

## Run locally

```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

Install:
```bash
pip install -r requirements.txt
```

Test:
```bash
pytest -q
```

Run:
```bash
streamlit run app/main.py
```

Keep Git history truthful, do not copy another repository, and never commit secrets or private data.

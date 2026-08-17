# 🛡️ DatasetGuard AI

> AI-assisted dataset quality and annotation audit platform built with Python and Streamlit.

DatasetGuard AI is a data-quality auditing application designed for machine-learning and annotation datasets. It helps users identify common dataset problems, inspect annotation quality, detect duplicate and similar records, identify potential outliers and privacy-sensitive patterns, and generate an audit report.

## ✨ Features

- 📊 Dataset profiling
- 🔍 Exact duplicate detection
- 🧠 Text similarity duplicate detection
- 🏷️ Label distribution and imbalance analysis
- 📈 Numeric outlier detection using Isolation Forest
- 🔐 Potential PII pattern scanning
- ⭐ Explainable 0–100 dataset quality score
- 🧹 Cleaned CSV export
- 📄 PDF audit report generation
- 🧪 Automated tests with Pytest
- ⚙️ GitHub Actions CI

## 🏗️ Project Structure

```text
datasetguard-ai/
│
├── app/
│   ├── analysis/
│   │   ├── duplicates.py
│   │   ├── labels.py
│   │   ├── outliers.py
│   │   ├── pii.py
│   │   ├── profiling.py
│   │   └── quality.py
│   │
│   ├── reports/
│   │   └── pdf_report.py
│   │
│   └── main.py
│
├── tests/
│   ├── test_duplicates.py
│   ├── test_labels.py
│   ├── test_outliers.py
│   ├── test_pii.py
│   ├── test_profiling.py
│   └── test_quality.py
│
├── sample_data/
│   └── sample_annotations.csv
│
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── README.md
├── requirements.txt
├── pyproject.toml
├── LICENSE
└── .gitignore
from __future__ import annotations

import pandas as pd
import streamlit as st

from app.analysis.duplicates import find_exact_duplicates, find_text_duplicates
from app.analysis.labels import analyze_labels
from app.analysis.outliers import detect_outliers
from app.analysis.pii import scan_pii
from app.analysis.profiling import profile_dataset
from app.analysis.quality import calculate_quality_score
from app.reports.pdf_report import build_pdf_report

st.set_page_config(page_title="DatasetGuard AI", page_icon="🛡️", layout="wide")

st.title("🛡️ DatasetGuard AI")
st.caption("Dataset quality, annotation consistency, privacy, and audit reporting")

uploaded = st.file_uploader("Upload a CSV dataset", type=["csv"])

if not uploaded:
    st.info("Upload a CSV to begin an audit.")
    st.stop()

try:
    df = pd.read_csv(uploaded)
except Exception as exc:
    st.error(f"Could not read the CSV: {exc}")
    st.stop()

if df.empty:
    st.warning("The uploaded dataset is empty.")
    st.stop()

profile = profile_dataset(df)
duplicates = find_exact_duplicates(df)
outliers = detect_outliers(df)
pii = scan_pii(df)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Rows", profile["rows"])
col2.metric("Columns", profile["columns"])
col3.metric("Missing", f"{profile['missing_rate']:.1%}")
col4.metric("Duplicates", duplicates["duplicate_rows"])

st.subheader("Dataset preview")
st.dataframe(df.head(20), use_container_width=True)

st.subheader("Analysis configuration")
label_column = st.selectbox("Label column (optional)", ["None"] + df.columns.tolist())
text_columns = profile["text_columns"]
text_column = st.selectbox(
    "Text column for similarity analysis (optional)", ["None"] + text_columns
)

label_result = analyze_labels(df, label_column) if label_column != "None" else None

similar_matches = []
if text_column != "None":
    threshold = st.slider("Similarity threshold", 0.70, 0.99, 0.90, 0.01)
    similar_matches = find_text_duplicates(df, text_column, threshold)

quality = calculate_quality_score(
    missing_rate=profile["missing_rate"],
    duplicate_rate=duplicates["duplicate_rate"],
    outlier_rate=outliers["outlier_rate"],
    pii_findings=pii["finding_count"],
    rows=profile["rows"],
)

results = {
    "profile": profile,
    "duplicates": duplicates,
    "outliers": outliers,
    "pii": pii,
    "quality": quality,
    "label": label_result,
    "semantic_duplicates": similar_matches,
}

st.subheader("Quality result")
st.metric("Overall quality score", f"{quality['score']}/100")
st.write(f"**Grade: {quality['grade']}**")

for reason in quality["reasons"]:
    st.warning(reason)

c1, c2 = st.columns(2)
with c1:
    st.subheader("Label analysis")
    if label_result:
        st.json(label_result)
    else:
        st.write("No label column selected.")

with c2:
    st.subheader("Privacy scan")
    st.write(f"Potential findings: **{pii['finding_count']}**")
    if pii["types"]:
        st.write("Types:", ", ".join(pii["types"]))

st.subheader("Similarity duplicates")
if similar_matches:
    st.dataframe(pd.DataFrame(similar_matches), use_container_width=True)
else:
    st.write("No high-similarity row pairs found with the selected threshold.")

st.subheader("Outlier detection")
st.write(
    f"Detected **{outliers['outlier_count']}** potential outlier rows "
    f"({outliers['outlier_rate']:.1%})."
)

clean_df = df.drop_duplicates().copy()
st.download_button(
    "Download cleaned CSV",
    data=clean_df.to_csv(index=False).encode("utf-8"),
    file_name="datasetguard_cleaned.csv",
    mime="text/csv",
)

st.download_button(
    "Download PDF audit report",
    data=build_pdf_report(uploaded.name, results),
    file_name="datasetguard_audit_report.pdf",
    mime="application/pdf",
)

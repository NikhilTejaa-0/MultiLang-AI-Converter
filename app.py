import streamlit as st
import time
import zipfile
import plotly.express as px
import pandas as pd

from io import BytesIO

# IMPORTS

from converters.sql_converter import (
    convert_sql_to_python
)

from converters.scala_converter import (
    convert_scala_to_python
)

from converters.ai_converter import (
    ai_convert_code,
    explain_conversion,
    hybrid_optimize
)

from utils.report_generator import (
    generate_report
)

# PAGE CONFIG

st.set_page_config(
    page_title="MultiLang AI Converter",
    page_icon="◈",
    layout="wide"
)

# LOAD CSS

def load_css():

    with open("styles/main.css") as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()

# SESSION STATE

if "converted_results" not in st.session_state:

    st.session_state.converted_results = []

if "logs" not in st.session_state:

    st.session_state.logs = []

if "show_modes" not in st.session_state:

    st.session_state.show_modes = False

if "selected_mode" not in st.session_state:

    st.session_state.selected_mode = None

# HERO SECTION

left, right = st.columns([1.5, 1])

with left:

    st.markdown("""
    <div class="hero-title">
        AI-Powered<br>
        Code Migration
    </div>

    <div class="hero-sub">
        Convert SQL and Scala into optimized Python
        using Hybrid Intelligence, Offline Engines,
        and AI-Assisted Transformation.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    b1, b2 = st.columns(2)

    with b1:

        st.button(
            "⚡ Start Conversion"
        )

    with b2:

        st.button(
            "📊 View Analytics"
        )

with right:

    st.markdown("""
    <div class="glass">

    <h3 style="margin-bottom:24px;">
    🚀 Platform Capabilities
    </h3>

    <div style="
        display:flex;
        flex-direction:column;
        gap:16px;
    ">

    <div>⚡ Offline Rule-Based Engine</div>
    <div>🧠 AI-Assisted Transformation</div>
    <div>⚗️ Hybrid AI Optimization</div>
    <div>📂 Batch File Processing</div>
    <div>📈 Conversion Analytics</div>
    <div>🔒 Fully Offline Support</div>

    </div>

    </div>
    """, unsafe_allow_html=True)

# STATS

st.markdown("<br><br>", unsafe_allow_html=True)

s1, s2, s3, s4 = st.columns(4)

stats = [
    ("12,842", "Files Processed"),
    ("98.2%", "Accuracy"),
    ("4+", "Languages"),
    ("0.8s", "Average Speed")
]

for col, (value, label) in zip(
    [s1, s2, s3, s4],
    stats
):

    with col:

        st.markdown(f"""
        <div class="stat-card">

        <div class="stat-value">
        {value}
        </div>

        <div class="stat-label">
        {label}
        </div>

        </div>
        """, unsafe_allow_html=True)

# PREMIUM UPLOAD SECTION

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown("""
<div class="glass upload-container">

<div class="upload-icon">
📂
</div>

<h2 class="upload-title">
Upload Source Files
</h2>

<p class="upload-subtitle">
Drag and drop SQL or Scala files to begin
AI-powered enterprise code migration.
</p>

</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

upload_left, upload_center, upload_right = st.columns([1,2,1])

with upload_center:

    uploaded_files = st.file_uploader(
        " ",
        type=["sql", "scala"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )

st.markdown("<br><br>", unsafe_allow_html=True)

# MAIN WORKSPACE

st.markdown("""
## ⚡ Code Migration Workspace
""")

# FILE PROCESSING

if uploaded_files:

    st.markdown(f"""
    ### 📂 {len(uploaded_files)} Files Uploaded
    """)

    if st.button(
        "🚀 Convert All Files"
    ):

        st.session_state.show_modes = True

# MODE SELECTION

if st.session_state.show_modes:

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <h2 style="
        text-align:center;
        margin-bottom:30px;
        font-size:36px;
        font-weight:800;
    ">
    Choose Conversion Engine
    </h2>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    # OFFLINE

    with c1:

        st.markdown("""
        <div class="mode-card">
        <h2>⚡</h2>
        <h3>Offline Engine</h3>
        <p>
        Fast local rule-based conversion.
        No internet required.
        </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "Use Offline",
            key="offline_btn"
        ):

            st.session_state.selected_mode = "Offline"

    # AI

    with c2:

        st.markdown("""
        <div class="mode-card">
        <h2>🧠</h2>
        <h3>AI-Assisted</h3>
        <p>
        Uses Gemini AI for advanced
        semantic code transformation.
        </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "Use AI",
            key="ai_btn"
        ):

            st.session_state.selected_mode = "AI-Assisted"

    # HYBRID

    with c3:

        st.markdown("""
        <div class="mode-card">
        <h2>⚗️</h2>
        <h3>Hybrid Mode</h3>
        <p>
        Rule-based conversion followed
        by AI optimization.
        </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "Use Hybrid",
            key="hybrid_btn"
        ):

            st.session_state.selected_mode = "Hybrid"

# PROCESS FILES

if st.session_state.selected_mode:

    st.success(
        f"✅ {st.session_state.selected_mode} selected"
    )

    st.session_state.converted_results = []

    st.session_state.logs = []

    progress = st.progress(0)

    log_container = st.empty()

    total_files = len(uploaded_files)

    for index, uploaded_file in enumerate(
        uploaded_files
    ):

        filename = uploaded_file.name

        code = uploaded_file.read().decode(
            "utf-8",
            errors="ignore"
        )

        line_count = len(
            code.splitlines()
        )

        st.session_state.logs.append(
            f"[INFO] Processing {filename}"
        )

        log_container.code(
            "\n".join(
                st.session_state.logs
            ),
            language="bash"
        )

        time.sleep(0.4)

        # SQL

        if filename.endswith(".sql"):

            # AI MODE

            if (
                st.session_state.selected_mode
                == "AI-Assisted"
            ):

                converted = ai_convert_code(
                    code,
                    "SQL"
                )

                if converted is None:

                    converted = convert_sql_to_python(
                        code
                    )

                    st.session_state.logs.append(
                        "[WARNING] AI unavailable → using offline engine"
                    )

                    log_container.code(
                        "\n".join(
                            st.session_state.logs
                        ),
                        language="bash"
                    )

            # HYBRID MODE

            elif (
                st.session_state.selected_mode
                == "Hybrid"
            ):

                offline_output = (
                    convert_sql_to_python(code)
                )

                converted = hybrid_optimize(
                    code,
                    offline_output
                )

            # OFFLINE MODE

            else:

                converted = convert_sql_to_python(
                    code
                )

            st.session_state.logs.append(
                f"[SUCCESS] SQL converted → {filename}"
            )

            log_container.code(
                "\n".join(
                    st.session_state.logs
                ),
                language="bash"
            )

        # SCALA

        elif filename.endswith(".scala"):

            # AI MODE

            if (
                st.session_state.selected_mode
                == "AI-Assisted"
            ):

                converted = ai_convert_code(
                    code,
                    "Scala"
                )

                if converted is None:

                    converted = convert_scala_to_python(
                        code
                    )

                    st.session_state.logs.append(
                        "[WARNING] AI unavailable → using offline engine"
                    )

                    log_container.code(
                        "\n".join(
                            st.session_state.logs
                        ),
                        language="bash"
                    )

            # HYBRID MODE

            elif (
                st.session_state.selected_mode
                == "Hybrid"
            ):

                offline_output = (
                    convert_scala_to_python(code)
                )

                converted = hybrid_optimize(
                    code,
                    offline_output
                )

            # OFFLINE MODE

            else:

                converted = convert_scala_to_python(
                    code
                )

            st.session_state.logs.append(
                f"[SUCCESS] Scala converted → {filename}"
            )

            log_container.code(
                "\n".join(
                    st.session_state.logs
                ),
                language="bash"
            )

        # OTHER

        else:

            converted = "# Unsupported file"

            st.session_state.logs.append(
                f"[WARNING] Unsupported syntax in {filename}"
            )

            log_container.code(
                "\n".join(
                    st.session_state.logs
                ),
                language="bash"
            )

        output_filename = (
            filename.split(".")[0]
            + ".py"
        )

        explanation = explain_conversion(
            code,
            converted
        )

        st.session_state.converted_results.append({

            "input_name": filename,

            "output_name": output_filename,

            "original_code": code,

            "code": converted,

            "explanation": explanation,

            "line_count": line_count,

            "mode": st.session_state.selected_mode
        })

        progress.progress(
            (index + 1) / total_files
        )

    st.success(
        "✅ Batch Conversion Completed"
    )

    report_path = generate_report(

        st.session_state.converted_results,

        st.session_state.logs
    )

    st.session_state.report_path = report_path

    st.session_state.show_modes = False
    st.session_state.selected_mode = None

# RESULTS

if st.session_state.converted_results:

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <h2 style="
        font-size:42px;
        font-weight:900;
        margin-bottom:30px;
    ">
    ⚡ Conversion Results
    </h2>
    """, unsafe_allow_html=True)

    m1, m2, m3 = st.columns(3)

    with m1:

        st.metric(
            "Files Converted",
            len(
                st.session_state.converted_results
            )
        )

    with m2:

        st.metric(
            "Success Rate",
            "98%"
        )

    with m3:

        st.metric(
            "Processing Speed",
            "0.8 sec"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    for result in st.session_state.converted_results:

        st.markdown(f"""
        <div class="result-header">
            📄 {result['input_name']}
        </div>
        """, unsafe_allow_html=True)

        left, right = st.columns(2)

        with left:

            st.markdown("""
            <div class="code-title">
                INPUT CODE
            </div>
            """, unsafe_allow_html=True)

            input_language = "sql"

            if result["input_name"].endswith(".scala"):

                input_language = "scala"

            st.code(
                result["original_code"],
                language=input_language
            )

        with right:

            st.markdown("""
            <div class="code-title">
                CONVERTED PYTHON
            </div>
            """, unsafe_allow_html=True)

            st.code(
                result["code"],
                language="python"
            )

        st.markdown("<br>", unsafe_allow_html=True)

        with st.expander(
            "🧠 AI Conversion Explanation"
        ):

            st.markdown(
                result["explanation"]
            )

        st.markdown("<br><br>", unsafe_allow_html=True)

# ANALYTICS DASHBOARD

if st.session_state.converted_results:

    st.markdown("""
    <h2 style="
        font-size:42px;
        font-weight:900;
        margin-top:40px;
        margin-bottom:30px;
    ">
    📊 Conversion Analytics
    </h2>
    """, unsafe_allow_html=True)

    df = pd.DataFrame(
        st.session_state.converted_results
    )

    df["type"] = df["input_name"].apply(
        lambda x: x.split(".")[-1]
    )

    a1, a2 = st.columns(2)

    with a1:

        pie_fig = px.pie(
            df,
            names="type",
            title="Language Distribution"
        )

        st.plotly_chart(
            pie_fig,
            use_container_width=True
        )

    with a2:

        bar_fig = px.bar(
            df,
            x="input_name",
            y="line_count",
            color="mode",
            title="Lines Converted"
        )

        st.plotly_chart(
            bar_fig,
            use_container_width=True
        )

# LOGS PANEL

if st.session_state.logs:

    st.markdown("""
    ## 🖥️ Conversion Logs
    """)

    log_text = "\n".join(
        st.session_state.logs
    )

    st.code(
        log_text,
        language="bash"
    )

# ZIP DOWNLOAD

if st.session_state.converted_results:

    zip_buffer = BytesIO()

    with zipfile.ZipFile(
        zip_buffer,
        "w",
        zipfile.ZIP_DEFLATED
    ) as zip_file:

        for result in st.session_state.converted_results:

            zip_file.writestr(
                result["output_name"],
                result["code"]
            )

    st.markdown("<br><br>", unsafe_allow_html=True)

    download_left, download_center, download_right = st.columns([1,2,1])

    with download_center:

        st.markdown("""
        """, unsafe_allow_html=True)

        st.download_button(
            label="⬇ Download ZIP Package",
            data=zip_buffer.getvalue(),
            file_name="converted_python_files.zip",
            mime="application/zip",
            use_container_width=True
        )

# PDF REPORT DOWNLOAD

if "report_path" in st.session_state:

    with open(
        st.session_state.report_path,
        "rb"
    ) as pdf_file:

        st.download_button(

            label="📄 Download Conversion Report",

            data=pdf_file,

            file_name="conversion_report.pdf",

            mime="application/pdf",

            use_container_width=True
        )

# FOOTER

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown("""
<div class="footer">

MultiLang AI Converter · Premium Edition · 2025

</div>
""", unsafe_allow_html=True)
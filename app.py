"""
Main Streamlit Application
Automated Exam Result Processing & Performance Analytics System
"""

import streamlit as st
import pandas as pd
import os
import sys
from pathlib import Path
from contextlib import contextmanager

# Add src directory to path for module imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.data_processor import DataProcessor
from src.analyzer import Analyzer
from src.report_generator import PDFReportGenerator

# Configure page
st.set_page_config(
        page_title="Exam Result Processing System",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="collapsed"
)

# Centralized DARK glassmorphism CSS + animations
st.markdown(r"""
<style>
:root{
    --bg-0: #0b1020;
    --bg-1: rgba(255,255,255,0.02);
    --glass: rgba(255,255,255,0.04);
    --accent: #6ee7b7;
    --muted: rgba(255,255,255,0.6);
    --glass-border: rgba(255,255,255,0.06);
    --card-radius: 14px;
    --gap: 16px;
}
html, body, [data-testid='stAppViewContainer'] {
    background: linear-gradient(180deg, #071026 0%, #081226 60%);
    color: #e6eef8;
    font-family: Inter, system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial;
}
.main-header {
    font-size: 2.1rem;
    color: var(--accent);
    font-weight: 700;
    text-align: center;
    margin: 8px 0 20px 0;
    letter-spacing: 0.4px;
}
.subheader-style{
    font-size: 1.05rem;
    color: #cfe9df;
    font-weight: 600;
    margin: 8px 0 12px 0;
}
.glass-card{
    background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.02));
    border-radius: var(--card-radius);
    padding: 18px;
    margin: 10px 0;
    backdrop-filter: blur(8px) saturate(120%);
    -webkit-backdrop-filter: blur(8px) saturate(120%);
    border: 1px solid var(--glass-border);
    box-shadow: 0 6px 18px rgba(2,6,23,0.6), inset 0 1px 0 rgba(255,255,255,0.02);
    transition: transform 0.28s ease, box-shadow 0.28s ease;
}
.glass-card:hover{ transform: translateY(-6px) scale(1.005); box-shadow: 0 16px 36px rgba(2,6,23,0.7); }
.metric-card{ display:flex; flex-direction:column; gap:6px; padding:14px; border-radius:10px; background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01)); border:1px solid rgba(255,255,255,0.03);}
.stButton>button, .stDownloadButton>button{ background: linear-gradient(90deg,#2dd4bf,#60a5fa) !important; color:#071026 !important; font-weight:600; border-radius:10px; padding:8px 12px; box-shadow: 0 6px 18px rgba(32, 139, 255, 0.12); border: none; }
.stButton>button:hover, .stDownloadButton>button:hover{ transform: translateY(-2px); }
div[data-testid='stFileUploader']{ border-radius:12px; padding:12px; background: rgba(255,255,255,0.01); border:1px dashed rgba(255,255,255,0.04); }
.dataframe-container{ border-radius:12px; overflow:hidden; }
.tab-header{ display:flex; align-items:center; gap:10px; }
.fade-in{ animation: fadeIn 420ms ease both; }
.slide-up{ animation: slideUp 420ms cubic-bezier(.2,.9,.3,1) both; }
@keyframes fadeIn{ from{opacity:0} to{opacity:1} }
@keyframes slideUp{ from{opacity:0; transform: translateY(8px);} to{opacity:1; transform: translateY(0);} }

/* Improve table look */
div[data-testid='stDataFrame'] > div { border-radius:10px; }

/* Tabs */
div[data-testid='stTabs'] button{ background:transparent; color:var(--muted); border-radius:10px; padding:10px 14px; margin:0 6px; }
div[data-testid='stTabs'] button[data-selected='true']{ color: #e6fff3; background: linear-gradient(90deg, rgba(255,255,255,0.03), rgba(255,255,255,0.02)); border:1px solid rgba(255,255,255,0.04); box-shadow: 0 8px 24px rgba(2,6,23,0.6); }

/* Responsive tweaks */
@media (max-width: 800px){ .main-header{ font-size:1.6rem } .glass-card{ padding:12px } }
</style>
""", unsafe_allow_html=True)

# small helper to render glass card headers and return a container for inner content
@contextmanager
def glass_card(title: str = None, subtitle: str = None, icon: str = ""):
    st.markdown(f"<div class='glass-card slide-up'>", unsafe_allow_html=True)
    if title:
        st.markdown(f"<div class='tab-header'><h3 style='margin:0'>{icon} {title}</h3></div>", unsafe_allow_html=True)
    if subtitle:
        st.markdown(f"<div style='color:var(--muted);margin-top:6px;margin-bottom:10px'>{subtitle}</div>", unsafe_allow_html=True)
    container = st.container()
    try:
        yield container
    finally:
        st.markdown("</div>", unsafe_allow_html=True)

# Initialize session state
if 'processor' not in st.session_state:
    st.session_state.processor = None
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = None
if 'charts' not in st.session_state:
    st.session_state.charts = {}
if 'file_uploaded' not in st.session_state:
    st.session_state.file_uploaded = False


def main():
    """Main application function"""
    st.markdown('<div class="main-header">📊 Automated Exam Result Processing & Performance Analytics System</div>', unsafe_allow_html=True)

    # Top tabs navigation (professional)
    tabs = st.tabs(["📤 Upload & Validate", "📈 Analysis & Statistics", "📄 Generate Report"])

    with tabs[0]:
        with glass_card("Upload & Validate", "Upload an Excel file and validate student marks", icon="📥"):
            upload_and_validate_page()

    with tabs[1]:
        with glass_card("Analysis & Statistics", "Overview of class performance and visualizations", icon="📈"):
            analysis_page()

    with tabs[2]:
        with glass_card("Generate Report", "Create and download a professional PDF report", icon="📄"):
            report_page()


def upload_and_validate_page():
    """File upload and data validation page"""
    with glass_card("Step 1: Upload and Validate Data", "Upload an Excel file and validate student marks", icon="📥"):
        col1, col2 = st.columns([2, 1])

        with col1:
            st.write("""
            Upload an Excel file (.xlsx) with the following format:
            - **Column 1**: `Student_Name` - Name of the student
            - **Column 2**: `Roll_No` - Roll number
            - **Columns 3+**: Subject marks (0-100 range)
            
            Example columns: `Student_Name`, `Roll_No`, `Math`, `English`, `Science`, `History`
            """)

        with col2:
            if st.button("📥 Download Sample Format", key="download_sample"):
                create_sample_excel()
                st.success("Sample file created in /data/sample_marks.xlsx")

        # File uploader
        uploaded_file = st.file_uploader(
            "Choose an Excel file",
            type=['xlsx'],
            help="Upload an Excel file with student marks"
        )
    
        if uploaded_file is not None:
            # Save uploaded file temporarily
            temp_file_path = os.path.join("data", uploaded_file.name)
            os.makedirs("data", exist_ok=True)

            with open(temp_file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            st.success(f"✅ File uploaded: {uploaded_file.name}")

            # Initialize processor and load file
            processor = DataProcessor()
            success, message = processor.load_excel(temp_file_path)

            if success:
                st.session_state.processor = processor
                st.session_state.file_uploaded = True

                # Display loaded data
                st.markdown('<div class="subheader-style">Loaded Data Preview</div>', unsafe_allow_html=True)
                st.dataframe(processor.df, use_container_width=True)

                # Validate data
                st.markdown('<div class="subheader-style">Data Validation</div>', unsafe_allow_html=True)

                is_valid, errors = processor.validate_data()

                if is_valid:
                    st.success("✅ Data validation passed! All records are valid.")

                    # Calculate grades
                    st.info("🔄 Processing data and calculating grades...")
                    df_processed = processor.calculate_grades()
                    st.success("✅ Grades calculated successfully!")

                    # Display processed data
                    st.markdown('<div class="subheader-style">Processed Results</div>', unsafe_allow_html=True)

                    # Create columns for display
                    display_cols = ['Student_Name', 'Roll_No', 'Average', 'Grade', 'GPA', 'Status']
                    st.dataframe(df_processed[display_cols], use_container_width=True)

                    # Summary statistics
                    st.markdown('<div class="subheader-style">Quick Summary</div>', unsafe_allow_html=True)

                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Students", len(df_processed))
                    with col2:
                        pass_count = len(df_processed[df_processed['Status'] == 'PASS'])
                        st.metric("Pass Count", pass_count)
                    with col3:
                        fail_count = len(df_processed[df_processed['Status'] == 'FAIL'])
                        st.metric("Fail Count", fail_count)
                    with col4:
                        class_avg = df_processed['Average'].mean()
                        st.metric("Class Average", f"{class_avg:.2f}")

                else:
                    st.error("❌ Data validation failed! Please fix the following errors:")
                    for error in errors:
                        st.error(f"  • {error}")
            else:
                st.error(f"❌ Error loading file: {message}")


def analysis_page():
    """Analysis and statistics page"""
    st.markdown('<div class="subheader-style">Step 2: Analysis & Statistics</div>', unsafe_allow_html=True)

    if not st.session_state.file_uploaded:
        st.warning("⚠️ Please upload and validate a file first on the 'Upload & Validate' page.")
        return

    processor = st.session_state.processor
    df = processor.get_processed_data()

    # Initialize analyzer
    analyzer = Analyzer(df)
    st.session_state.analyzer = analyzer

    # Overall Statistics - styled metric cards
    stats = analyzer.get_statistics()

    with glass_card("Overall Statistics", "High level class metrics", icon="✨"):
        cols = st.columns(4, gap='large')
        metrics = [
            ("Class Average", f"{stats['Class Average']:.2f}"),
            ("Class GPA", f"{stats['Class GPA']:.2f}"),
            ("Highest Score", f"{stats['Highest Score']:.2f}"),
            ("Lowest Score", f"{stats['Lowest Score']:.2f}")
        ]
        for col, (label, value) in zip(cols, metrics):
            with col:
                st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                st.metric(label, value)
                st.markdown("</div>", unsafe_allow_html=True)

    with glass_card("More Metrics", "Pass rates and counts", icon="📌"):
        cols = st.columns(3, gap='large')
        more = [
            ("Pass Rate", f"{stats['Pass %']:.1f}%"),
            ("Total Students", int(stats['Total Students'])),
            ("Pass Count", int(stats['Pass Count']))
        ]
        for col, (label, value) in zip(cols, more):
            with col:
                st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                st.metric(label, value)
                st.markdown("</div>", unsafe_allow_html=True)

    # Tabs for different analyses
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Top Performers",
        "📉 Subject Analysis",
        "📈 Charts & Visualizations",
        "📋 Full Student Data"
    ])

    # Top Performers Tab
    with tab1:
        with glass_card("Top 10 Performers", "Top students by average score", icon="🏅"):
            toppers = analyzer.get_toppers(top_n=10)
            st.dataframe(toppers, use_container_width=True)

    # Subject Analysis Tab
    with tab2:
        with glass_card("Subject Analysis", "Strong and weak subjects at a glance", icon="📚"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('<div class="subheader-style">Strong Subjects</div>', unsafe_allow_html=True)
                strong = analyzer.get_strong_subjects()
                strong_df = pd.DataFrame([
                    {'Subject': k, 'Average Marks': f"{v:.2f}"}
                    for k, v in list(strong.items())[:5]
                ])
                st.dataframe(strong_df, use_container_width=True)

            with col2:
                st.markdown('<div class="subheader-style">Weak Subjects</div>', unsafe_allow_html=True)
                weak = analyzer.get_weak_subjects()
                weak_df = pd.DataFrame([
                    {'Subject': k, 'Average Marks': f"{v:.2f}"}
                    for k, v in list(weak.items())[:5]
                ])
                st.dataframe(weak_df, use_container_width=True)

    # Charts & Visualizations Tab
    with tab3:
        with glass_card("Charts & Visualizations", "Interactive charts and distributions", icon="📈"):
            if not st.session_state.charts:
                with st.spinner("🔄 Generating visualization charts..."):
                    charts = analyzer.generate_all_charts()
                    st.session_state.charts = charts

            charts = st.session_state.charts
            # Display charts in responsive grid
            rcol1, rcol2 = st.columns(2)
            with rcol1:
                if 'grade_distribution' in charts:
                    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                    st.image(charts['grade_distribution'], caption="Grade Distribution", use_column_width=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                if 'average_distribution' in charts:
                    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                    st.image(charts['average_distribution'], caption="Average Marks Distribution", use_column_width=True)
                    st.markdown("</div>", unsafe_allow_html=True)

            with rcol2:
                if 'pass_fail_distribution' in charts:
                    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                    st.image(charts['pass_fail_distribution'], caption="Pass/Fail Distribution", use_column_width=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                if 'gpa_distribution' in charts:
                    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                    st.image(charts['gpa_distribution'], caption="GPA Distribution", use_column_width=True)
                    st.markdown("</div>", unsafe_allow_html=True)

            if 'subject_performance' in charts:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.image(charts['subject_performance'], caption="Subject-wise Performance", use_column_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

    # Full Student Data Tab
    with tab4:
        with glass_card("Complete Student Records", "Filter and export full student data", icon="📋"):
            filter_status = st.selectbox(
                "Filter by Status:",
                ["All", "PASS", "FAIL"]
            )

            if filter_status == "All":
                display_df = df
            else:
                display_df = df[df['Status'] == filter_status]

            st.dataframe(display_df, use_container_width=True)

            # Download CSV option
            csv = display_df.to_csv(index=False)
            st.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name="exam_results.csv",
                mime="text/csv"
            )


def report_page():
    """PDF Report generation page"""
    
    st.markdown('<p class="subheader-style">Step 3: Generate Professional Report</p>', 
               unsafe_allow_html=True)
    
    if not st.session_state.file_uploaded:
        st.warning("⚠️ Please upload and validate a file first on the 'Upload & Validate' page.")
        return
    
    if st.session_state.analyzer is None:
        st.warning("⚠️ Please go to the 'Analysis & Statistics' page first to generate charts.")
        return
    
    st.info("""
    📄 This will generate a professional PDF report containing:
    - Overall statistics and summary
    - Top 5 performers
    - Strong and weak subjects
    - Performance analysis charts
    """)
    
    if st.button("🎯 Generate PDF Report", key="generate_report"):
        with st.spinner("⏳ Generating comprehensive PDF report..."):
            try:
                processor = st.session_state.processor
                analyzer = st.session_state.analyzer
                
                # Get data for report
                df = processor.get_processed_data()
                stats = analyzer.get_statistics()
                toppers = analyzer.get_toppers(top_n=5)
                weak_subjects = analyzer.get_weak_subjects()
                strong_subjects = analyzer.get_strong_subjects()
                
                # Generate charts if not already done
                if not st.session_state.charts:
                    charts = analyzer.generate_all_charts()
                else:
                    charts = st.session_state.charts
                
                # Generate PDF
                pdf_gen = PDFReportGenerator()
                pdf_path = pdf_gen.generate_report(
                    df, stats, toppers, weak_subjects, 
                    strong_subjects, charts
                )
                
                st.success("✅ PDF Report generated successfully!")
                
                # Read and provide download button
                with open(pdf_path, "rb") as pdf_file:
                    pdf_data = pdf_file.read()
                
                st.download_button(
                    label="📥 Download PDF Report",
                    data=pdf_data,
                    file_name=os.path.basename(pdf_path),
                    mime="application/pdf"
                )
                
                # Display file info
                st.info(f"📍 Report saved at: {pdf_path}")
                
            except Exception as e:
                st.error(f"❌ Error generating report: {str(e)}")


def create_sample_excel():
    """Create a sample Excel file for users"""
    try:
        sample_data = {
            'Student_Name': [
                'Aarav Patel', 'Bhavna Singh', 'Chirag Verma', 'Deepika Nair',
                'Esha Sharma', 'Fahad Khan', 'Gita Desai', 'Harsh Gupta',
                'Isha Reddy', 'Jatin Malhotra'
            ],
            'Roll_No': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
            'Math': [92, 78, 85, 88, 95, 72, 81, 89, 76, 84],
            'English': [88, 92, 79, 85, 90, 76, 88, 82, 94, 87],
            'Science': [95, 85, 92, 80, 88, 75, 90, 86, 85, 91],
            'History': [85, 88, 78, 92, 87, 70, 84, 80, 88, 86],
            'Computer': [89, 80, 95, 87, 91, 82, 86, 93, 79, 89]
        }
        
        df_sample = pd.DataFrame(sample_data)
        os.makedirs("data", exist_ok=True)
        df_sample.to_excel("data/sample_marks.xlsx", index=False)
        return True
    except Exception as e:
        st.error(f"Error creating sample file: {e}")
        return False


if __name__ == "__main__":
    main()

import streamlit as st
import pandas as pd


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title=" ( MPLADS AI  )",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)



# ==========================================
# TITLE
# ==========================================

st.title("🏛️  CivicLens-MPLADS AI")

st.subheader(
    "Smart Anomaly & Efficiency Detection System"
)

st.write(
    "AI-assisted system for detecting potential anomalies, "
    "high-risk patterns and inefficiencies in MPLADS works."
) 





# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv(
    "data/mplads_ml_results.csv"
)




# ==========================================
# SIDEBAR FILTERS
# ==========================================

st.sidebar.header("🔎 Filters")

states = sorted(
    df["State"].dropna().unique()
)

selected_state = st.sidebar.selectbox(
    "Select State",
    ["All States"] + states
)

risk_options = [
    "All Risk Levels",
    "Low",
    "Medium",
    "High"
]

selected_risk = st.sidebar.selectbox(
    "Select Risk Level",
    risk_options
)

ml_options = [
    "All",
    "Potential Anomaly",
    "Normal"
]

selected_ml = st.sidebar.selectbox(
    "ML Anomaly",
    ml_options
)


# ==========================================
# APPLY FILTERS
# ==========================================

filtered_df = df.copy()

if selected_state != "All States":
    filtered_df = filtered_df[
        filtered_df["State"] == selected_state
    ]

if selected_risk != "All Risk Levels":
    filtered_df = filtered_df[
        filtered_df["Risk Level"] == selected_risk
    ]

if selected_ml != "All":
    filtered_df = filtered_df[
        filtered_df["ML Anomaly"] == selected_ml
    ]


st.sidebar.write(
    f"Showing {len(filtered_df):,} projects"
)
# ==========================================
# EXECUTIVE SUMMARY
# ==========================================

st.header("📌 Executive Summary")

st.write(
    "Quick overview of MPLADS project implementation "
    "and detected risk patterns."
)

summary_col1, summary_col2 = st.columns(2)

with summary_col1:

    st.info(
        f"📁 **{len(filtered_df):,} projects** "
        f"are currently being analyzed."
    )

    st.info(
        f"💰 Total completed works value is "
        f"**₹{filtered_df['Final Amount (₹)'].sum():,.0f}**."
    )


with summary_col2:

    st.warning(
        f"🔴 **{(filtered_df['Risk Level'] == 'High').sum():,}** "
        f"projects are classified as high risk."
    )

    st.warning(
        f"🤖 **{(filtered_df['ML Anomaly'] == 'Potential Anomaly').sum():,}** "
        f"projects are identified as potential anomalies by ML."
    )

# ==========================================
# KEY METRICS
# ==========================================

total_projects = len(filtered_df)

total_amount = filtered_df[
    "Final Amount (₹)"
].sum()

high_risk = (
    filtered_df["Risk Level"] == "High"
).sum()

medium_risk = (
    filtered_df["Risk Level"] == "Medium"
).sum()

ml_anomalies = (
    filtered_df["ML Anomaly"] == "Potential Anomaly"
).sum()


col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "📁 Total Projects",
    f"{total_projects:,}"
)

col2.metric(
    "💰 Total Amount",
    f"₹{total_amount:,.0f}"
)

col3.metric(
    "🔴 High Risk",
    f"{high_risk:,}"
)

col4.metric(
    "🟡 Medium Risk",
    f"{medium_risk:,}"
)

col5.metric(
    "🤖 ML Anomalies", 
     
    f"{ml_anomalies:,}"
)
col5.caption("Overlaps with risk levels above")
 



st.divider()


# ==========================================
# STATE-WISE ANALYSIS
# ==========================================

st.header("🗺️ State-wise Analysis")

state_analysis = (
    filtered_df
    .groupby("State")
    .agg(
        Projects=("Work ID", "count"),

        Total_Amount=(
            "Final Amount (₹)",
            "sum"
        ),

        High_Risk=(
            "Risk Level",
            lambda x: (x == "High").sum()
        ),

        Potential_Anomalies=(
            "ML Anomaly",
            lambda x: (
                x == "Potential Anomaly"
            ).sum()
        )
    )
    .reset_index()
)

state_analysis = state_analysis.sort_values(
    "Projects",
    ascending=False
)

st.dataframe(
    state_analysis,
    width="stretch"
)


# ==========================================
# STATE-WISE PROJECT CHART
# ==========================================

st.subheader("📊 Projects by State")

state_chart = state_analysis.head(15)

st.bar_chart(
    state_chart,
    x="State",
    y="Projects"
)


# ==========================================
# PROJECT FLAG EXPLANATION
# ==========================================

st.header("🔍 Why is this project flagged?")

st.write(
    "Select a project to understand why the system "
    "has marked it as a potential anomaly or high-risk project."
)


project_ids = filtered_df[
    "Work ID"
].astype(str).tolist()


if len(project_ids) > 0:
    default_id = "138858"
    default_index = project_ids.index(default_id)if default_id in project_ids else 0

    selected_project = st.selectbox(
        "Select Work ID",
        project_ids,
        index = default_index
    )

    project = filtered_df[
        filtered_df["Work ID"].astype(str)
        == selected_project
    ].iloc[0]


    col1, col2, col3 = st.columns(3)


    col1.metric(
        "Risk Score",
        project["Risk Score"]
    )


    col2.metric(
        "Risk Level",
        project["Risk Level"]
    )


    col3.metric(
        "ML Status",
        project["ML Anomaly"]
    )


    st.write("### 📌 Detection Reason")


    st.info(
        project["Risk Reason"]
    )


    st.write("### 📋 Project Details")


    st.write(
        f"**MP Name:** {project['MP Name']}"
    )


    st.write(
        f"**State:** {project['State']}"
    )


    st.write(
        f"**Final Amount:** "
        f"₹{project['Final Amount (₹)']:,.0f}"
    )


else:

    st.info(
        "No projects available for the selected filters."
    )


# ==========================================
# RISK DISTRIBUTION
# ==========================================

st.header("📊 Risk Distribution")

risk_counts = (
    filtered_df["Risk Level"]
    .value_counts()
)

st.bar_chart(
    risk_counts
)


# ==========================================
# ML ANOMALY DISTRIBUTION
# ==========================================

st.header("🤖 ML Anomaly Detection")

ml_counts = (
    filtered_df["ML Anomaly"]
    .value_counts()
)

st.bar_chart(
    ml_counts
)


# ==========================================
# POTENTIAL ANOMALIES
# ==========================================

st.header("🚨 Potential Anomalies")

anomaly_df = filtered_df[
    filtered_df["ML Anomaly"]
    == "Potential Anomaly"
]


if len(anomaly_df) > 0:

    st.dataframe(
        anomaly_df[
            [
                "Work ID",
                "MP Name",
                "State",
                "Final Amount (₹)",
                "Risk Score",
                "Risk Level",
                "Risk Reason",
                "ML Anomaly"
            ]
        ],
        width="stretch"
    )

else:

    st.info(
        "No potential anomalies found "
        "for the selected filters."
    )


# ==========================================
# HIGH RISK PROJECTS
# ==========================================

st.header("🔴 High Risk Projects")

high_risk_df = filtered_df[
    filtered_df["Risk Level"] == "High"
]


if len(high_risk_df) > 0:

    st.dataframe(
        high_risk_df[
            [
                "Work ID",
                "MP Name",
                "State",
                "Final Amount (₹)",
                "Risk Score",
                "Risk Level",
                "Risk Reason"
            ]
        ],
        width="stretch"
    )

else:

    st.info(
        "No high-risk projects found "
        "for the selected filters."
    )


# ==========================================
# ALL PROJECTS
# ==========================================

st.header("🔎 All Projects")

st.dataframe(
    filtered_df[
        [
            "Work ID",
            "MP Name",
            "State",
            "Final Amount (₹)",
            "Risk Score",
            "Risk Level",
            "Risk Reason",
            "ML Anomaly"
        ]
    ],
    width="stretch"
)


# ==========================================
# DOWNLOAD REPORT
# ==========================================

st.header("📥 Download Report")

download_data = filtered_df.to_csv(
    index=False
).encode("utf-8")


st.download_button(
    label="📥 Download Filtered Report",
    data=download_data,
    file_name="MPLADS_AI_Filtered_Report.csv",
    mime="text/csv",
    width="stretch"
)
# ==========================================
# DATA & MODEL LIMITATIONS
# ==========================================

st.header("⚠️ Data & Model Limitations")

st.write(
    "The following points should be considered while interpreting "
    "the detected risk patterns:"
)

st.markdown("""
- ⚠️ **Potential anomaly does not mean confirmed fraud.**
  Every flagged case requires human verification.

- 🔗 **Payment data limitation:** Payment information is available
  at MP/Constituency/State level in the available expenditure data,
  so it is not directly linked to every individual Work ID.

- 🤖 **ML model:** The Isolation Forest model is a prototype
  anomaly-detection approach and is not an official government
  fraud-detection model.

- 📊 **Risk score:** The current risk score is a prototype
  prioritization mechanism, not an official MPLADS risk rating.

- 🧑‍💼 **Human-in-the-loop:** Final decisions should be made by
  authorized officials after checking supporting records.
""")

# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "⚠️ This system identifies potential anomalies "
    "and risk patterns for human verification. "
    "An anomaly does not automatically indicate fraud."
)

            # =========================================================
# REAL-TIME RISK EVALUATOR & SOLUTION RECOMMENDATION ENGINE
# =========================================================
import streamlit as st
import datetime

st.markdown("---")
st.markdown("---")
st.markdown("## 🔮 Predictive Risk Tools")
st.caption("AI-assisted checks that predict and prevent risk before sanction")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Real-Time Evaluator",
    "Split-Tender Detector",
    "Duplicate Work Checker",
    "Geo Verification",
    "CAG Audit Report",
    "Vendor Collusion Detector",
])
import streamlit as st
import pandas as pd

# --- ye poora block sabse pehle, kisi bhi tab/section se upar ---
st.markdown("""
<style>
.cl-card-info { background-color:#2f6fed; color:#fff; padding:14px 18px; border-radius:10px; font-weight:600; margin-bottom:10px; }
.cl-card-warn { background-color:#b8ab3f; color:#fff; padding:14px 18px; border-radius:10px; font-weight:600; margin-bottom:10px; }
.cl-card-danger { background-color:#b23a5c; color:#fff; padding:14px 18px; border-radius:10px; font-weight:600; margin-bottom:10px; }
.cl-card-success { background-color:#2f8a5c; color:#fff; padding:14px 18px; border-radius:10px; font-weight:600; margin-bottom:10px; }
</style>
""", unsafe_allow_html=True)

def cl_box(text, kind="info"):
    css_class = {"info": "cl-card-info", "warn": "cl-card-warn",
                 "danger": "cl-card-danger", "success": "cl-card-success"}.get(kind, "cl-card-info")
    st.markdown(f'<div class="{css_class}">{text}</div>', unsafe_allow_html=True)

# --- yahan se aapka baaki purana + naya code shuru hoga (tabs, charts, etc.) ---
# ---------------- TAB 1: Real-Time Risk Evaluator ----------------
with tab1:
    st.subheader("⚡ CivicLens: Real-Time Risk Evaluator & Action Engine")
    st.caption("Enter project parameters to compute real-time risk scores and get AI-recommended corrective actions.")

    col1, col2 = st.columns(2)
    with col1:
        project_name = st.text_input("Project Name / Work Description", "Construction of Community Hall")
        sanctioned_amount = st.number_input("Sanctioned Amount (in ₹)", min_value=0, value=5000000, step=50000)
        district = st.selectbox("District / Region", ["Bhopal", "Indore", "Gwalior", "Jabalpur"])
    with col2:
        sanction_date = st.date_input("Sanction Date")
        target_timeline = st.slider("Target Timeline (Months)", 1, 72, 6)
        vendor_past_anomalies = st.number_input("Vendor Past Anomalies Flagged", min_value=0, value=2, step=1)

    if st.button("🔍 Analyze Risk & Generate Recommended Action"):
        # Simple heuristic scoring — replace with your actual model if you have one
        score = 0
        if sanctioned_amount > 3000000:
            score += 30
        if vendor_past_anomalies >= 2:
            score += 40
        if target_timeline < 3:
            score += 20

        if score >= 60:
            risk_level = "High"
            action = "Recommend site inspection before fund release."
        elif score >= 30:
            risk_level = "Medium"
            action = "Recommend documentation review before approval."
        else:
            risk_level = "Low"
            action = "No additional action required."

        st.metric("Risk Score", score)
        st.metric("Risk Level", risk_level)
        st.info(f"💡 Recommended Action: {action}")

# ---------------- TAB 2: Split-Tender Detector ----------------
with tab2:
    st.subheader("🔗 Split-Tender Detector")
    st.markdown("**Detect Intentional Work Splitting (Bypassing Approval Caps)**")
    st.caption("Flags multiple tenders issued to the same vendor in the same location within a short window.")

    col1, col2 = st.columns(2)
    with col1:
        contractor_name = st.text_input("Contractor / Agency Name", "Shree Ram Infra Ltd.")
        location = st.text_input("Location / Panchayat", "Ward 12, District Hospital Area")
    with col2:
        num_tenders = st.number_input("Number of Sanctioned Tenders (Within 30 Days)", min_value=1, value=4, step=1)
        avg_amount = st.number_input("Average Amount per Tender (in ₹)", min_value=0, value=950000, step=10000)

    if st.button("🔍 Check Split Work Anomaly"):
        if num_tenders >= 3:
            st.error(
                f"⚠️ SPLIT-TENDER RISK IDENTIFIED: '{contractor_name}' received {num_tenders} "
                f"tenders in {location} within 30 days, avg ₹{avg_amount:,.0f} each — "
                f"possible splitting to bypass approval caps."
            )
            st.info("💡 Recommended Action: Consolidate tenders and route through standard approval workflow.")
        else:
            st.success("No split-tender pattern detected for this contractor/location.")
            # ---------------- TAB 3: Duplicate Work Checker ----------------
with tab3:
    st.subheader("👥 Duplicate Work Checker")
    st.markdown("**Detect Duplicate or Re-billed Works**")
    st.caption("Flags works with the same description, location and MP that may have been billed more than once.")

    col1, col2 = st.columns(2)
    with col1:
        work_description = st.text_input("Work Description", "Construction of Overhead Water Tank")
        mp_name = st.text_input("MP Name", "Daggumalla Prasada Rao")
    with col2:
        location = st.text_input("Location / Village", "Ward 5, Rajahmundry")
        amount = st.number_input("Final Amount (₹)", min_value=0, value=450000, step=10000)

    if st.button("🔍 Check for Duplicate Work"):
        # Matches against the loaded dataset on description + location + MP
        matches = df[
            (df["Work Description"].str.strip().str.lower() == work_description.strip().lower()) &
            (df["Location"].str.strip().str.lower() == location.strip().lower()) &
            (df["MP Name"].str.strip().str.lower() == mp_name.strip().lower())
        ] if all(c in df.columns for c in ["Work Description", "Location", "MP Name"]) else pd.DataFrame()

        if len(matches) > 1:
            st.error(
                f"⚠️ DUPLICATE WORK DETECTED: {len(matches)} entries found for the same "
                f"work, location and MP — possible re-billing."
            )
            st.dataframe(matches, use_container_width=True)
            st.info("💡 Recommended Action: Cross-check physical completion before releasing further payment.")
        else:
            st.success("No duplicate entries found for this work.")

# ---------------- TAB 4: Geo-Tagged Citizen Verification ----------------
with tab4:
    st.subheader("📷 Geo-Tagged Citizen Verification")
    st.markdown("**Crowd-Sourced Ground-Truth Check**")
    st.caption("Citizens upload a geo-tagged photo of a completed work; the system compares it against the sanctioned location.")

    col1, col2 = st.columns(2)
    with col1:
        verify_work_id = st.text_input("Work ID", "138858")
        uploaded_photo = st.file_uploader("Upload Geo-Tagged Photo", type=["jpg", "jpeg", "png"])
    with col2:
        reported_lat = st.number_input("Reported Latitude", value=17.3850, format="%.4f")
        reported_lon = st.number_input("Reported Longitude", value=78.4867, format="%.4f")

    if st.button("📍 Verify Location Match"):
        record = df[df["Work ID"].astype(str) == str(verify_work_id)] if "Work ID" in df.columns else pd.DataFrame()

        if record.empty:
            st.warning("Work ID not found in records.")
        elif "Latitude" in record.columns and "Longitude" in record.columns:
            sanctioned_lat = record.iloc[0]["Latitude"]
            sanctioned_lon = record.iloc[0]["Longitude"]
            distance_deg = ((reported_lat - sanctioned_lat) ** 2 + (reported_lon - sanctioned_lon) ** 2) ** 0.5

            if distance_deg > 0.01:  # roughly >1 km mismatch
                st.error("⚠️ LOCATION MISMATCH: Uploaded photo's coordinates do not match the sanctioned site.")
                st.info("💡 Recommended Action: Flag for field-level physical verification.")
            else:
                st.success("✅ Location verified — matches sanctioned project site.")
            if uploaded_photo:
                st.image(uploaded_photo, caption="Citizen-submitted photo", use_container_width=True)
        else:
            st.warning("No coordinate data available for this Work ID to compare against.")

# ---------------- TAB 5: Automated CAG Audit Report ----------------
with tab5:
    st.subheader("📄 Automated CAG Audit Report")
    st.markdown("**Auto-Generated Summary for Statutory Audit**")
    st.caption("Compiles all flagged high-risk and anomalous works into a CAG-style audit-ready summary.")

    col1, col2 = st.columns(2)
    with col1:
        report_state = st.selectbox("Select State", ["All States"] + sorted(df["State"].unique().tolist()) if "State" in df.columns else ["All States"])
    with col2:
        report_period = st.text_input("Reporting Period", "FY 2025–26")

    if st.button("📝 Generate Audit Report"):
        filtered = df if report_state == "All States" else df[df["State"] == report_state]
        high_risk = filtered[filtered["Risk Level"] == "High"] if "Risk Level" in filtered.columns else pd.DataFrame()
        anomalies = filtered[filtered["ML Anomaly"] == "Potential Anomaly"] if "ML Anomaly" in filtered.columns else pd.DataFrame()

        st.markdown(f"### Audit Summary — {report_state} ({report_period})")
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Works Reviewed", len(filtered))
        c2.metric("High-Risk Works", len(high_risk))
        c3.metric("ML-Flagged Anomalies", len(anomalies))

        summary_text = (
            f"CAG-Style Audit Summary\n"
            f"Period: {report_period}\n"
            f"Scope: {report_state}\n"
            f"Total works reviewed: {len(filtered)}\n"
            f"High-risk works: {len(high_risk)}\n"
            f"ML-flagged anomalies: {len(anomalies)}\n"
            f"Note: Findings are AI-generated for prioritisation and require officer verification.\n"
        )
        st.download_button(
            "📥 Download Audit Report (TXT)",
            data=summary_text,
            file_name=f"CAG_Audit_Report_{report_state.replace(' ', '_')}.txt",
        )
 


# ---------------- TAB 6: Vendor Collusion & Cartel Detector ----------------
with tab6:
    st.subheader("🌐 Vendor Collusion & Cartel Detector")
    st.markdown("**Contractor Cartel & Monopolization Risk**")
    st.caption("Identifies if a specific vendor is monopolizing MPLADS funds across multiple MPs in the district.")

    cartel_df = pd.DataFrame({
        "Contractor Name": ["Apex Constructions", "Bharat Infra", "Metro Tech", "Apex Constructions", "Apex Constructions"],
        "MP Constituency": ["Ward 1", "Ward 1", "Ward 2", "Ward 2", "Ward 3"],
        "Sanction Amount (₹)": [1500000, 800000, 1200000, 2200000, 1800000],
        "Bidding Type": ["Single Bidder", "Open", "Open", "Single Bidder", "Single Bidder"],
    })
    st.dataframe(cartel_df, use_container_width=True)

    if st.button("🕸️ Run Cartel / Collusion Graph Analysis"):
        total_works = len(cartel_df)
        top_contractor = cartel_df["Contractor Name"].value_counts().idxmax()
        top_share = cartel_df["Contractor Name"].value_counts().max() / total_works * 100
        single_bidder_share = (
            cartel_df[cartel_df["Contractor Name"] == top_contractor]["Bidding Type"]
            .eq("Single Bidder").mean() * 100
        )

        st.error(
            f"🚨 HIGH COLLUSION RISK IDENTIFIED: Contractor '{top_contractor}' won "
            f"{top_share:.0f}% of works, {single_bidder_share:.0f}% via Single-Bidder process."
        )
        st.info("💡 Recommended Action: Mandatory re-tendering under Central Public Procurement Portal (CPPP) norms.")
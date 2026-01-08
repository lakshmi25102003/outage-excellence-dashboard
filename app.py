import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# --- PAGE CONFIGURATION ---
st.set_page_config(layout="wide", page_title="Outage Excellence Suite", page_icon="⚡")

# --- CUSTOM CSS FOR UX ---
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        border-left: 5px solid #ff4b4b;
        padding: 20px;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    .status-green { color: green; font-weight: bold; }
    .status-amber { color: orange; font-weight: bold; }
    .status-red { color: red; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- MOCK DATA GENERATION ---
@st.cache_data
def generate_data():
    # 85 Projects Generation
    projects = []
    categories = ['Turbine', 'Generator', 'HRSG', 'BOP', 'Electrical', 'I&C']
    for i in range(1, 86):
        cat = random.choice(categories)
        budget_labor = random.randint(50000, 500000)
        budget_mat = random.randint(20000, 300000)
        start_date = datetime.now() - timedelta(days=random.randint(0, 10))
        duration = random.randint(5, 45)
        
        projects.append({
            "Project ID": f"PRJ-{1000+i}",
            "Name": f"{cat} Work Package #{i}",
            "Category": cat,
            "Status": random.choice(['Not Started', 'In Progress', 'Completed', 'Delayed']),
            "Owner": f"Manager {random.randint(1, 5)}",
            "Budget Labor": budget_labor,
            "Actual Labor": budget_labor * random.uniform(0.8, 1.2),
            "Budget Material": budget_mat,
            "Actual Material": budget_mat * random.uniform(0.9, 1.1),
            "Start Date": start_date,
            "End Date": start_date + timedelta(days=duration),
            "Critical Path": random.choice([True, False, False, False]) # 25% chance
        })
    return pd.DataFrame(projects)

df_projects = generate_data()

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("⚡ Outage Excellence")
st.sidebar.caption("Role: CXO / Plant Director")

nav_options = [
    "1. CXO Command Center",
    "2. Outage Dashboard (Unit View)",
    "3. The 85 Projects Matrix",
    "4. Financial & Budget Master",
    "5. Execution & Critical Path",
    "6. Closeout & Reconciliation"
]
selection = st.sidebar.radio("Go to Screen:", nav_options)

st.sidebar.markdown("---")
st.sidebar.info("**Outage Context:**\n\nUnit 4 Combined Cycle\nType: GE 7F.05\nStatus: Execution (Day 12/45)")

# --- SCREEN 1: CXO COMMAND CENTER ---
if selection == "1. CXO Command Center":
    st.title("🌎 CXO Fleet Command Center")
    st.markdown("High-level view of all assets and outage readiness across the fleet.")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Active Outages", "3", "1 Delayed")
    col2.metric("Fleet TRIR (Safety)", "0.0", "Target: 0.0")
    col3.metric("Total CapEx Committed", "$45.2M", "-$1.2M (Under)")
    col4.metric("Supply Chain Risk", "Medium", "2 Rotors in Transit")

    st.markdown("### Fleet Outage Timeline (Next 24 Months)")
    
    # Mock Fleet Data
    fleet_data = pd.DataFrame([
        dict(Task="Plant Alpha (Major)", Start='2025-01-01', Finish='2025-02-28', Resource="Region A"),
        dict(Task="Plant Beta (HGPI)", Start='2025-03-15', Finish='2025-04-15', Resource="Region A"),
        dict(Task="Plant Gamma (Combustion)", Start='2025-06-01', Finish='2025-06-15', Resource="Region B"),
        dict(Task="Plant Delta (C-Inspection)", Start='2025-09-01', Finish='2025-10-01', Resource="Region B")
    ])
    
    fig_fleet = px.timeline(fleet_data, x_start="Start", x_end="Finish", y="Task", color="Resource", title="Global Fleet Schedule")
    st.plotly_chart(fig_fleet, use_container_width=True)

# --- SCREEN 2: OUTAGE DASHBOARD ---
elif selection == "2. Outage Dashboard (Unit View)":
    st.title("🏭 Unit 4 Major Inspection Dashboard")
    st.markdown("Combined Cycle (2x1) - T-0 Execution Phase")

    # Top Level KPI
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Schedule Variance", "-2 Days", "Critical Path Delay", delta_color="inverse")
    kpi2.metric("Budget Utilization", "42%", "On Track")
    kpi3.metric("Open Projects", "68 / 85", "12 Completed")
    kpi4.metric("Safety Incidents", "0", "15,000 Man-hours")

    st.markdown("---")
    
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.subheader("Critical Path Status")
        # Filter for critical path items
        cp_df = df_projects[df_projects["Critical Path"] == True].sort_values("Start Date")
        fig_cp = px.timeline(cp_df, x_start="Start Date", x_end="End Date", y="Name", color="Status", title="Critical Path Tasks")
        st.plotly_chart(fig_cp, use_container_width=True)
        
    with c2:
        st.subheader("Top Risks / Issues")
        st.warning("**Rotor Lift Crane**: Certification expiring in 2 days.")
        st.error("**BOP Valve**: Replacement part delayed by customs.")
        st.info("**Labor**: Night shift electrician shortage.")

# --- SCREEN 3: PROJECT MATRIX ---
elif selection == "3. The 85 Projects Matrix":
    st.title("The Project Matrix")
    st.markdown("Manage the 85 independent projects linked to this outage.")
    
    # Filter controls
    col1, col2 = st.columns(2)
    with col1:
        cat_filter = st.multiselect("Filter by Category", df_projects['Category'].unique(), default=df_projects['Category'].unique())
    with col2:
        status_filter = st.multiselect("Filter by Status", df_projects['Status'].unique(), default=df_projects['Status'].unique())
    
    filtered_df = df_projects[df_projects['Category'].isin(cat_filter) & df_projects['Status'].isin(status_filter)]
    
    # Interactive Dataframe
    st.dataframe(
        filtered_df,
        column_config={
            "Budget Labor": st.column_config.NumberColumn(format="$%d"),
            "Actual Labor": st.column_config.NumberColumn(format="$%d"),
            "Status": st.column_config.SelectboxColumn(options=['Not Started', 'In Progress', 'Completed']),
            "Start Date": st.column_config.DateColumn(format="D MMM YYYY"),
        },
        use_container_width=True,
        hide_index=True
    )
    
    st.caption("*Select a row to drill down into specific project details (Simulated).*")

# --- SCREEN 4: FINANCIALS ---
elif selection == "4. Financial & Budget Master":
    st.title("Financial Control Tower")
    st.markdown("Tracking Labor vs. Material across the lifecycle (T-24 to T+3).")
    
    # Calculate Totals
    total_labor_budget = df_projects['Budget Labor'].sum()
    total_labor_actual = df_projects['Actual Labor'].sum()
    total_mat_budget = df_projects['Budget Material'].sum()
    total_mat_actual = df_projects['Actual Material'].sum()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Labor Variance")
        fig_labor = go.Figure(data=[
            go.Bar(name='Budget', x=['Labor'], y=[total_labor_budget], marker_color='blue'),
            go.Bar(name='Actual + Committed', x=['Labor'], y=[total_labor_actual], marker_color='orange')
        ])
        st.plotly_chart(fig_labor, use_container_width=True)
        
    with col2:
        st.subheader("Material Variance")
        fig_mat = go.Figure(data=[
            go.Bar(name='Budget', x=['Material'], y=[total_mat_budget], marker_color='green'),
            go.Bar(name='Actual + Committed', x=['Material'], y=[total_mat_actual], marker_color='red')
        ])
        st.plotly_chart(fig_mat, use_container_width=True)

    st.markdown("### Cost Overrun Alert (Top 5 Projects)")
    df_projects['Variance'] = (df_projects['Actual Labor'] + df_projects['Actual Material']) - (df_projects['Budget Labor'] + df_projects['Budget Material'])
    overrun_df = df_projects.sort_values(by='Variance', ascending=False).head(5)
    st.table(overrun_df[['Name', 'Owner', 'Variance']])

# --- SCREEN 5: EXECUTION DRILL DOWN ---
elif selection == "5. Execution & Critical Path":
    st.title(" Execution & Asset Drill-Down")
    
    tab1, tab2 = st.tabs(["Asset View (GT/HRSG)", "Daily Shift Logs"])
    
    with tab1:
        st.subheader("Gas Turbine Section Review")
        col_img, col_data = st.columns([1, 2])
        with col_img:
            # Placeholder for Diagram
            st.markdown("""
            <div style="background-color:#ddd; height:300px; display:flex; align-items:center; justify-content:center;">
                [Diagram: GT Cross Section]
            </div>
            """, unsafe_allow_html=True)
        with col_data:
            st.markdown("**Component: Combustion Liner (Can 4)**")
            st.markdown("- **Status:** Removed for Inspection")
            st.markdown("- **Finding:** Thermal Barrier Coating (TBC) loss > 5%")
            st.markdown("- **Action:** Replace from strategic spares.")
            st.button("View QA Report #4402")
            
    with tab2:
        st.subheader("Daily Shift Log Input")
        with st.form("shift_log"):
            shift = st.selectbox("Shift", ["Day", "Night"])
            date = st.date_input("Date")
            notes = st.text_area("Shift Notes / Impediments")
            uploaded_file = st.file_uploader("Upload Site Photos")
            submitted = st.form_submit_button("Submit Log")
            if submitted:
                st.success("Log entry saved to central database.")

# --- SCREEN 6: CLOSEOUT ---
elif selection == "6. Closeout & Reconciliation":
    st.title("Outage Closeout (T+3 Months)")
    
    st.progress(80, text="Closeout Progress: 80%")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.success("Operations Returned")
    with c2:
        st.warning("4 Open Invoices")
    with c3:
        st.info(" Final Report Drafting")
        
    st.subheader("Pending Actions for Book Closing")
    st.checkbox("Reconcile Contractor Overtime Hours")
    st.checkbox("Return unused spares to Warehouse inventory")
    st.checkbox("Submit Regulatory Emissions Report")

    st.checkbox("Finalize Lessons Learned Session")

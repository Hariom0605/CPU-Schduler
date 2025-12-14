import streamlit as st
import sys
import os

# Add parent directory to path to import core module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.scheduling import fcfs, sjf, round_robin, priority_scheduling, calculate_metrics
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(page_title="CPU Scheduling Simulator", layout="wide")

st.title("🖥️ CPU Scheduling Algorithms Simulator")
st.markdown("---")

# Sidebar for input
st.sidebar.header("📋 Process Input")

# Initialize session state for processes
if 'processes' not in st.session_state:
    st.session_state.processes = []

# Input form
with st.sidebar.form("process_form"):
    st.subheader("Add Process")
    process_id = st.text_input("Process ID", value=f"P{len(st.session_state.processes)+1}")
    arrival_time = st.number_input("Arrival Time", min_value=0, value=0)
    burst_time = st.number_input("Burst Time", min_value=1, value=5)
    priority = st.number_input("Priority (lower = higher priority)", min_value=1, value=1)
    
    submit = st.form_submit_button("➕ Add Process")
    
    if submit:
        st.session_state.processes.append({
            'id': process_id,
            'arrival': arrival_time,
            'burst': burst_time,
            'priority': priority
        })
        st.success(f"Added {process_id}")

# Display current processes
if st.session_state.processes:
    st.sidebar.subheader("Current Processes")
    df = pd.DataFrame(st.session_state.processes)
    st.sidebar.dataframe(df, use_container_width=True)
    
    if st.sidebar.button("🗑️ Clear All Processes"):
        st.session_state.processes = []
        st.rerun()

# Algorithm selection
st.sidebar.markdown("---")
st.sidebar.header("⚙️ Algorithm Settings")
algorithm = st.sidebar.selectbox(
    "Select Algorithm",
    ["FCFS", "SJF", "Round Robin", "Priority Scheduling"]
)

quantum = None
if algorithm == "Round Robin":
    quantum = st.sidebar.number_input("Time Quantum", min_value=1, value=2)

run_button = st.sidebar.button("▶️ Run Simulation", type="primary", use_container_width=True)

# Main content area
if run_button and st.session_state.processes:
    st.header(f"Results: {algorithm}")
    
    # Run selected algorithm
    gantt_chart = []
    results = []
    
    try:
        if algorithm == "FCFS":
            gantt_chart, results = fcfs(st.session_state.processes)
        elif algorithm == "SJF":
            gantt_chart, results = sjf(st.session_state.processes)
        elif algorithm == "Round Robin":
            gantt_chart, results = round_robin(st.session_state.processes, quantum)
        elif algorithm == "Priority Scheduling":
            gantt_chart, results = priority_scheduling(st.session_state.processes)
        
        # Display metrics
        metrics = calculate_metrics(results)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Average Waiting Time", f"{metrics['avg_waiting']} units")
        with col2:
            st.metric("Average Turnaround Time", f"{metrics['avg_turnaround']} units")
        with col3:
            st.metric("Total Processes", metrics['total_processes'])
        
        st.markdown("---")
        
        # Gantt Chart
        st.subheader("📊 Gantt Chart")
        fig, ax = plt.subplots(figsize=(12, 4))
        
        colors = plt.cm.Set3(range(len(st.session_state.processes)))
        process_colors = {p['id']: colors[i] for i, p in enumerate(st.session_state.processes)}
        
        for item in gantt_chart:
            ax.barh(0, item['finish'] - item['start'], left=item['start'], 
                   height=0.5, color=process_colors[item['process']], 
                   edgecolor='black', linewidth=1.5)
            ax.text((item['start'] + item['finish'])/2, 0, item['process'], 
                   ha='center', va='center', fontweight='bold', fontsize=10)
        
        ax.set_ylim(-0.5, 0.5)
        ax.set_xlabel('Time', fontsize=12)
        ax.set_yticks([])
        ax.set_title(f'{algorithm} Gantt Chart', fontsize=14, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
        
        st.pyplot(fig)
        
        # Results Table
        st.subheader("📈 Process Details")
        results_df = pd.DataFrame(results)
        st.dataframe(results_df, use_container_width=True)
        
        # Performance Chart
        st.subheader("⏱️ Performance Metrics")
        fig2, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
        
        process_ids = [r['id'] for r in results]
        waiting_times = [r['waiting'] for r in results]
        turnaround_times = [r['turnaround'] for r in results]
        
        ax1.bar(process_ids, waiting_times, color='coral', edgecolor='black')
        ax1.set_xlabel('Process')
        ax1.set_ylabel('Time')
        ax1.set_title('Waiting Time per Process')
        ax1.grid(axis='y', alpha=0.3)
        
        ax2.bar(process_ids, turnaround_times, color='skyblue', edgecolor='black')
        ax2.set_xlabel('Process')
        ax2.set_ylabel('Time')
        ax2.set_title('Turnaround Time per Process')
        ax2.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        st.pyplot(fig2)
        
    except Exception as e:
        st.error(f"Error running simulation: {str(e)}")

elif run_button and not st.session_state.processes:
    st.warning("⚠️ Please add at least one process before running the simulation.")

else:
    st.info("👈 Add processes using the sidebar and click 'Run Simulation' to start.")

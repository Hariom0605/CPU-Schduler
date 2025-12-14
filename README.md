🧠 CPU Scheduling Simulator
An interactive visual simulator for classic CPU scheduling algorithms built with Python and Streamlit.
It helps understand how different algorithms schedule processes using Gantt charts, tables, and performance metrics.

🚀 Features
Supports four major scheduling algorithms:

🔹 FCFS (First Come First Serve)

🔹 SJF (Shortest Job First – Non‑preemptive)

🔹 Round Robin (with configurable time quantum)

🔹 Priority Scheduling (Non‑preemptive, lower number = higher priority)

📊 Gantt Chart visualization for execution order and timing

📋 Process detail table showing waiting time and turnaround time per process

📈 Performance charts:

Bar chart for waiting time of each process

Bar chart for turnaround time of each process

📉 Summary metrics:

Average waiting time

Average turnaround time

Total number of processes

💻 Simple, user‑friendly web UI built with Streamlit

🎯 Project Overview
This project simulates how the CPU schedules multiple processes using different algorithms from Operating Systems.
The user enters process information and instantly sees how each algorithm affects execution order and performance.

Objectives
Visualize CPU scheduling using clear and interactive Gantt charts.

Compare algorithms based on waiting time and turnaround time.

Provide an educational tool for students learning Operating Systems concepts.

🧩 System Design
1️⃣ Core Scheduling Module (core/scheduling.py)
Implements all scheduling algorithms:

FCFS

Processes are executed in the order of arrival.

SJF (Non‑preemptive)

Among available processes, the one with the smallest burst time is selected.

Round Robin

Each process gets CPU for a fixed time quantum in a cyclic manner.

Priority Scheduling (Non‑preemptive)

Process with highest priority (smallest priority value) is selected first.

Each algorithm returns:

Gantt chart data (process id, start time, finish time)

Per‑process metrics:

Start time

Finish time

Waiting time

Turnaround time

A helper function calculates:

Average waiting time

Average turnaround time

2️⃣ GUI Module (GUI/app.py)
Built using Streamlit:

Sidebar form to add processes:

Process ID

Arrival time

Burst time

Priority

Algorithm selection:

FCFS, SJF, Round Robin, Priority Scheduling

For Round Robin, user sets the time quantum

Buttons:

➕ Add Process

▶️ Run Simulation

🗑️ Clear All Processes

Main area shows:

Gantt chart

Key metrics (average times, total processes)

Process metrics table

Performance bar charts

🛠️ Tech Stack
Language: Python

Frontend / UI: Streamlit

Visualization: Matplotlib

Data handling: Pandas

Version control & hosting: Git & GitHub
def fcfs(processes):
    """First Come First Serve Scheduling"""
    processes = sorted(processes, key=lambda x: x['arrival'])
    current_time = 0
    gantt_chart = []
    results = []
    
    for process in processes:
        if current_time < process['arrival']:
            current_time = process['arrival']
        
        start_time = current_time
        finish_time = current_time + process['burst']
        
        gantt_chart.append({
            'process': process['id'],
            'start': start_time,
            'finish': finish_time
        })
        
        turnaround_time = finish_time - process['arrival']
        waiting_time = turnaround_time - process['burst']
        
        results.append({
            'id': process['id'],
            'arrival': process['arrival'],
            'burst': process['burst'],
            'start': start_time,
            'finish': finish_time,
            'waiting': waiting_time,
            'turnaround': turnaround_time
        })
        
        current_time = finish_time
    
    return gantt_chart, results


def sjf(processes):
    """Shortest Job First Scheduling (Non-preemptive)"""
    processes = sorted(processes, key=lambda x: x['arrival'])
    current_time = 0
    gantt_chart = []
    results = []
    remaining = processes.copy()
    
    while remaining:
        available = [p for p in remaining if p['arrival'] <= current_time]
        
        if not available:
            current_time = remaining[0]['arrival']
            continue
        
        process = min(available, key=lambda x: x['burst'])
        start_time = current_time
        finish_time = current_time + process['burst']
        
        gantt_chart.append({
            'process': process['id'],
            'start': start_time,
            'finish': finish_time
        })
        
        turnaround_time = finish_time - process['arrival']
        waiting_time = turnaround_time - process['burst']
        
        results.append({
            'id': process['id'],
            'arrival': process['arrival'],
            'burst': process['burst'],
            'start': start_time,
            'finish': finish_time,
            'waiting': waiting_time,
            'turnaround': turnaround_time
        })
        
        current_time = finish_time
        remaining.remove(process)
    
    return gantt_chart, results


def round_robin(processes, quantum):
    """Round Robin Scheduling"""
    processes = sorted(processes, key=lambda x: x['arrival'])
    current_time = 0
    gantt_chart = []
    results = {p['id']: {'arrival': p['arrival'], 'burst': p['burst'], 
                         'remaining': p['burst'], 'start': None, 'finish': 0} 
               for p in processes}
    queue = []
    index = 0
    
    while True:
        # Add newly arrived processes to queue
        while index < len(processes) and processes[index]['arrival'] <= current_time:
            queue.append(processes[index]['id'])
            index += 1
        
        if not queue:
            if index < len(processes):
                current_time = processes[index]['arrival']
                continue
            else:
                break
        
        process_id = queue.pop(0)
        if results[process_id]['start'] is None:
            results[process_id]['start'] = current_time
        
        execution_time = min(quantum, results[process_id]['remaining'])
        
        gantt_chart.append({
            'process': process_id,
            'start': current_time,
            'finish': current_time + execution_time
        })
        
        current_time += execution_time
        results[process_id]['remaining'] -= execution_time
        
        # Add newly arrived processes
        while index < len(processes) and processes[index]['arrival'] <= current_time:
            queue.append(processes[index]['id'])
            index += 1
        
        if results[process_id]['remaining'] > 0:
            queue.append(process_id)
        else:
            results[process_id]['finish'] = current_time
    
    # Calculate metrics
    final_results = []
    for process_id, data in results.items():
        turnaround_time = data['finish'] - data['arrival']
        waiting_time = turnaround_time - data['burst']
        final_results.append({
            'id': process_id,
            'arrival': data['arrival'],
            'burst': data['burst'],
            'start': data['start'],
            'finish': data['finish'],
            'waiting': waiting_time,
            'turnaround': turnaround_time
        })
    
    return gantt_chart, final_results


def priority_scheduling(processes):
    """Priority Scheduling (Non-preemptive, lower number = higher priority)"""
    processes = sorted(processes, key=lambda x: x['arrival'])
    current_time = 0
    gantt_chart = []
    results = []
    remaining = processes.copy()
    
    while remaining:
        available = [p for p in remaining if p['arrival'] <= current_time]
        
        if not available:
            current_time = remaining[0]['arrival']
            continue
        
        process = min(available, key=lambda x: (x['priority'], x['arrival']))
        start_time = current_time
        finish_time = current_time + process['burst']
        
        gantt_chart.append({
            'process': process['id'],
            'start': start_time,
            'finish': finish_time
        })
        
        turnaround_time = finish_time - process['arrival']
        waiting_time = turnaround_time - process['burst']
        
        results.append({
            'id': process['id'],
            'arrival': process['arrival'],
            'burst': process['burst'],
            'priority': process['priority'],
            'start': start_time,
            'finish': finish_time,
            'waiting': waiting_time,
            'turnaround': turnaround_time
        })
        
        current_time = finish_time
        remaining.remove(process)
    
    return gantt_chart, results


def calculate_metrics(results):
    """Calculate average metrics"""
    if not results:
        return {}
    
    avg_waiting = sum(r['waiting'] for r in results) / len(results)
    avg_turnaround = sum(r['turnaround'] for r in results) / len(results)
    
    return {
        'avg_waiting': round(avg_waiting, 2),
        'avg_turnaround': round(avg_turnaround, 2),
        'total_processes': len(results)
    }

import psutil
import subprocess
import json
import time
import os
from datetime import datetime
from flask import render_template, jsonify
from app import app

def get_system_info():
print("\n📡 Collecting system information...\n")

# CPU metrics
cpu_percent = psutil.cpu_percent(interval=1)
cpu_count = psutil.cpu_count()
cpu_freq = psutil.cpu_freq()
load_avg = os.getloadavg()
print(f"🧠 CPU: {cpu_percent}% used, {cpu_count} cores, {cpu_freq.current:.2f} MHz")
print(f"📊 Load Average (1, 5, 15 min): {load_avg}")

    # Memory values
memory = psutil.virtual_memory()
swap = psutil.swap_memory()
print(f"💾 Memory: {memory.percent}% used, {round(memory.used / (1024**3), 2)} GB used")
print(f"🔁 Swap: {swap.percent}% used")

    # For disk
disk = psutil.disk_usage('/')
disk_io = psutil.disk_io_counters()
print(f"📀 Disk: {disk.percent}% used, {round(disk.used / (1024**3), 2)} GB used")
print(f"🔄 Disk IO: {round(disk_io.read_bytes / (1024**2), 2)} MB read, {round(disk_io.write_bytes / (1024**2), 2)} MB written")

# for all network values
network = psutil.net_io_counters()
print(f"🌐 Network: {round(network.bytes_sent / (1024**2), 2)} MB sent, {round(network.bytes_recv / (1024**2), 2)} MB received")

# top proccesses 
processes = []
for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
try:
processes.append(proc.info)
except:
pass
top_processes = sorted(processes, key=lambda x: x['cpu_percent'] or 0, reverse=True)[:10]
print("🔥 Top 10 Processes by CPU:")
for p in top_processes:
print(f"   PID: {p['pid']} | Name: {p['name']} | CPU: {p['cpu_percent']}% | MEM: {p['memory_percent']:.2f}%")

# current services running
services = {}
service_list = ['apache2', 'mysql', 'smbd', 'nmbd', 'ssh']
print("\n🛠️ Checking service statuses:")
for service in service_list:
try:
status_result = subprocess.run(['systemctl', 'is-active', service], 
capture_output=True, text=True)
info_result = subprocess.run(['systemctl', 'show', service, '--property=ActiveEnterTimestamp'], 
capture_output=True, text=True)
services[service] = {
'status': status_result.stdout.strip(),
'info': info_result.stdout.strip()
}
status_emoji = "✅" if services[service]['status'] == 'active' else "❌"
print(f"   {status_emoji} {service}: {services[service]['status']}")
except:
services[service] = {'status': 'unknown', 'info': 'N/A'}
print(f"   ⚠️ {service}: unknown")

# whos logged in and system info 
boot_time = datetime.fromtimestamp(psutil.boot_time())
uptime = datetime.now() - boot_time
users = [user.name for user in psutil.users()]
print(f"\n🕒 System Uptime: {str(uptime).split('.')[0]}")
print(f"👥 Users logged in: {', '.join(set(users)) if users else 'None'}")
print(f"⏰ Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("-" * 60)

return {
'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
'cpu': {
'percent': cpu_percent,
'count': cpu_count,
'frequency': cpu_freq.current if cpu_freq else 0,
'load_avg': load_avg
        },
'memory': {
'percent': memory.percent,
'used_gb': round(memory.used / (1024**3), 2),
'total_gb': round(memory.total / (1024**3), 2),
'available_gb': round(memory.available / (1024**3), 2)
        },
'swap': {
'percent': swap.percent,
'used_gb': round(swap.used / (1024**3), 2),
'total_gb': round(swap.total / (1024**3), 2)
},
'disk': {
'percent': disk.percent,
'used_gb': round(disk.used / (1024**3), 2),
'total_gb': round(disk.total / (1024**3), 2),
'free_gb': round(disk.free / (1024**3), 2),
'read_mb': round(disk_io.read_bytes / (1024**2), 2) if disk_io else 0,
'write_mb': round(disk_io.write_bytes / (1024**2), 2) if disk_io else 0
},
'network': {
'bytes_sent_mb': round(network.bytes_sent / (1024**2), 2),
'bytes_recv_mb': round(network.bytes_recv / (1024**2), 2),
'packets_sent': network.packets_sent,
'packets_recv': network.packets_recv
        },
'processes': {
'total': len(processes),
'top_processes': top_processes
},
'services': services,
'system': {
'uptime': str(uptime).split('.')[0],
'boot_time': boot_time.strftime('%Y-%m-%d %H:%M:%S'),
'users': list(set(users))
}
}

@app.route('/api/data')
def api_data():
"""API endpoint that returns all system monitoring data as JSON"""
return jsonify(get_system_info())

@app.route('/')
def dashboard():
"""Main dashboard route - displays the full monitoring interface"""
data = get_system_info()
return render_template('dashboard.html', data=data)
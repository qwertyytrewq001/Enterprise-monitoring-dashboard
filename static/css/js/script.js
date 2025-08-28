function updateDashboard() {
const loading = document.getElementById('loading');
const errorMessage = document.getElementById('error-message');
loading.classList.add('active');
errorMessage.style.display = 'none';
    
fetch('/api/data')
.then(response => response.json())
.then(data => {
document.getElementById('cpu-percent').textContent = data.cpu.percent + '%';
document.getElementById('memory-percent').textContent = data.memory.percent + '%';
document.getElementById('disk-percent').textContent = data.disk.percent + '%';
document.getElementById('timestamp').textContent = data.timestamp;
document.getElementById('cpu-progress').style.width = data.cpu.percent + '%';
document.getElementById('memory-progress').style.width = data.memory.percent + '%';
document.getElementById('disk-progress').style.width = data.disk.percent + '%';
document.getElementById('network-sent').textContent = data.network.bytes_sent_mb;
document.getElementById('network-recv').textContent = data.network.bytes_recv_mb;
            
const processList = document.getElementById('process-list');
processList.innerHTML = data.processes.top_processes.map(process => `
<div class="process-item">
<div class="process-name">${process.name}</div>
<div class="process-stats">
CPU: ${process.cpu_percent.toFixed(1)}% | 
MEM: ${process.memory_percent.toFixed(1)}%
</div>
</div>
`).join('');
            
loading.classList.remove('active');
})
.catch(error => {
console.error('Error updating dashboard:', error);
loading.classList.remove('active');
errorMessage.textContent = 'Failed to update dashboard. Retrying...';
errorMessage.style.display = 'block';
});
}

let refreshInterval;
function setRefreshRate() {
const rate = parseInt(document.getElementById('refresh-rate').value);
clearInterval(refreshInterval);
refreshInterval = setInterval(updateDashboard, rate);
}

function toggleDarkMode() {
document.body.classList.toggle('dark-mode');
localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
}

document.addEventListener('DOMContentLoaded', () => {
if (localStorage.getItem('darkMode') === 'true') {
document.body.classList.add('dark-mode');
}
setRefreshRate();
updateDashboard();
    
document.querySelectorAll('.card, .service').forEach(element => {
element.addEventListener('keypress', (e) => {
if (e.key === 'Enter') {
element.classList.toggle('hovered');
}
});
});
});
from app import app

if __name__ == '__main__':
print("🚀 Starting Harjot's Enterprise Monitoring Dashboard...")
print("📊 Dashboard available at: http://192.168.100.234:5000")
print("🔗 API endpoint at: http://192.168.100.234:5000/api/data")
print("🔄 Real-time updates configurable (3s, 5s, 10s)")
print("🎨 Dark mode and accessibility enhancements enabled")
print("=" * 60)
app.run(host='0.0.0.0', port=5000, debug=True)
#!/usr/bin/env python3
"""
🌿 EcoLingua AI v3.0 - Professional Startup Script
Launch the professional environmental intelligence platform
"""

import subprocess
import sys
import os
import time
import webbrowser
from pathlib import Path

def print_banner():
    """Print professional startup banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║        🌿 EcoLingua AI v3.0 - Professional Edition          ║
    ║                                                              ║
    ║        Advanced Environmental Intelligence Platform          ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_requirements():
    """Check if required files and dependencies exist"""
    print("🔍 Checking system requirements...")
    
    required_files = [
        "app.py",
        "dashboard.html",
        "requirements.txt"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        return False
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    
    print("✅ System requirements check passed")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], check=True, capture_output=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_log_directory():
    """Create log directory if it doesn't exist"""
    log_dir = Path("logs")
    if not log_dir.exists():
        log_dir.mkdir()
        print("📁 Created logs directory")

def start_server():
    """Start the professional EcoLingua server"""
    print("🚀 Starting EcoLingua AI Professional Server...")
    print("=" * 60)
    
    # Server information
    host = "0.0.0.0"
    port = 5050
    
    print(f"🌐 Server Host: {host}")
    print(f"🔌 Server Port: {port}")
    print(f"🏠 Dashboard: http://localhost:{port}")
    print(f"📚 API Docs: http://localhost:{port}/api/docs")
    print(f"🔗 Health Check: http://localhost:{port}/api/health")
    print(f"📊 System Status: http://localhost:{port}/api/status")
    print("=" * 60)
    
    print("🧠 AI Systems: Initializing...")
    print("⚛️  Quantum Processor: Activating...")
    print("🌍 Environmental Monitoring: Starting...")
    print("📡 WebSocket Server: Preparing...")
    print("=" * 60)
    
    try:
        # Start the server
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "app:app",
            "--host", host,
            "--port", str(port),
            "--reload",
            "--log-level", "info"
        ])
        
    except KeyboardInterrupt:
        print("\n🛑 Server shutdown initiated...")
        print("🧠 AI systems safely disconnected")
        print("⚛️  Quantum processors powered down")
        print("🌍 Environmental monitoring stopped")
        print("📡 WebSocket connections closed")
        print("✅ EcoLingua AI Professional shutdown complete")
        
    except Exception as e:
        print(f"❌ Server startup error: {e}")
        print("\n💡 Troubleshooting:")
        print("   • Ensure port 5050 is available")
        print("   • Check if all dependencies are installed")
        print("   • Verify Python version (3.8+ required)")
        print("   • Run: pip install fastapi uvicorn")

def open_dashboard():
    """Open dashboard in browser after delay"""
    time.sleep(3)  # Wait for server to start
    try:
        webbrowser.open("http://localhost:5050")
        print("🌐 Dashboard opened in browser")
    except Exception as e:
        print(f"⚠️  Could not open browser: {e}")

def show_menu():
    """Show startup menu"""
    print("\n🎯 EcoLingua AI Professional - Startup Options:")
    print("1. 🚀 Start Professional Server")
    print("2. 🧪 Run Test Simulator")
    print("3. 📦 Install Dependencies")
    print("4. 🔍 System Check")
    print("5. 📚 View Documentation")
    print("6. 🚪 Exit")
    
    return input("\nSelect option (1-6): ").strip()

def run_test_simulator():
    """Run the professional test simulator"""
    if os.path.exists("test.py"):
        print("🧪 Starting Professional Test Simulator...")
        subprocess.run([sys.executable, "test.py"])
    else:
        print("❌ Test simulator not found (test.py)")

def show_documentation():
    """Show documentation information"""
    print("\n📚 EcoLingua AI v3.0 - Professional Documentation")
    print("=" * 60)
    print("🌐 Dashboard: http://localhost:5050")
    print("📖 API Documentation: http://localhost:5050/api/docs")
    print("🔄 Interactive API: http://localhost:5050/api/redoc")
    print("\n🔗 Key Endpoints:")
    print("   POST /api/sensor-data - Submit environmental data")
    print("   GET  /api/status - System status and metrics")
    print("   GET  /api/health - Health check")
    print("   WS   /ws - Real-time WebSocket updates")
    print("\n📊 Features:")
    print("   • Advanced AI Environmental Analysis")
    print("   • Quantum Processing Simulation")
    print("   • Real-time Species Recognition")
    print("   • Carbon Footprint Tracking")
    print("   • Professional Dashboard Interface")
    print("   • Comprehensive API Documentation")

def main():
    """Main startup function"""
    print_banner()
    
    # Check if we're in the right directory
    if not os.path.exists("app.py"):
        print("❌ Please run this script from the EcoLingua directory")
        print("💡 Make sure app.py is in the current directory")
        return
    
    create_log_directory()
    
    while True:
        choice = show_menu()
        
        if choice == "1":
            if check_requirements():
                print("🎯 Starting EcoLingua AI Professional Platform...")
                
                # Option to open browser
                open_browser = input("Open dashboard in browser? (y/n): ").lower().strip()
                if open_browser in ['y', 'yes']:
                    import threading
                    browser_thread = threading.Thread(target=open_dashboard)
                    browser_thread.daemon = True
                    browser_thread.start()
                
                start_server()
            else:
                print("❌ System requirements not met")
                
        elif choice == "2":
            run_test_simulator()
            
        elif choice == "3":
            install_dependencies()
            
        elif choice == "4":
            check_requirements()
            
        elif choice == "5":
            show_documentation()
            
        elif choice == "6":
            print("👋 Thank you for using EcoLingua AI Professional!")
            print("🌿 Protecting our environment with advanced AI")
            break
            
        else:
            print("❌ Invalid choice. Please select 1-6.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Startup interrupted by user")
    except Exception as e:
        print(f"❌ Startup error: {e}")
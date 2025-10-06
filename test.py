"""
🌿 EcoLingua AI v3.0 - Professional Test Simulator
Comprehensive testing suite for the professional environmental intelligence platform
"""

import requests
import json
import time
import random
import math
import logging
from datetime import datetime, timezone
from typing import Dict, Any, List
import threading
from dataclasses import dataclass

# Configure professional logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("EcoLingua-Test")

@dataclass
class TestResult:
    """Test result data structure"""
    test_name: str
    success: bool
    response_time: float
    status_code: int
    message: str

class ProfessionalEcoLinguaSimulator:
    """Professional test simulator for EcoLingua AI"""
    
    def __init__(self, server_url: str = "http://localhost:5050"):
        self.server_url = server_url.rstrip('/')
        self.device_id = "PROFESSIONAL_SIMULATOR_001"
        self.session = requests.Session()
        self.session.timeout = 15
        self.test_results: List[TestResult] = []
        
        # Professional headers
        self.session.headers.update({
            'User-Agent': 'EcoLingua-Professional-Simulator/3.0',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        
    def generate_realistic_environmental_data(self, scenario: str = "normal") -> Dict[str, Any]:
        """Generate realistic environmental data based on scenario"""
        
        current_time = datetime.now()
        hour = current_time.hour
        day_of_year = current_time.timetuple().tm_yday
        
        # Base temperature with seasonal and daily variation
        seasonal_temp = 20 + 15 * math.sin((day_of_year - 80) * 2 * math.pi / 365)
        daily_temp = seasonal_temp + 8 * math.sin((hour - 6) * math.pi / 12)
        
        if scenario == "optimal":
            temperature = 22.0 + random.uniform(-1, 1)
            humidity = 65.0 + random.uniform(-5, 5)
            air_quality = random.uniform(5, 25)
            co2_level = random.uniform(380, 400)
            audio_level = random.uniform(100, 300)
            vibration = random.uniform(5, 15)
            
        elif scenario == "stress":
            temperature = random.choice([45.0, -5.0]) + random.uniform(-2, 2)
            humidity = random.choice([15.0, 95.0]) + random.uniform(-5, 5)
            air_quality = random.uniform(150, 300)
            co2_level = random.uniform(500, 800)
            audio_level = random.uniform(800, 1000)
            vibration = random.uniform(150, 200)
            
        elif scenario == "extreme":
            temperature = random.choice([50.0, -15.0])
            humidity = random.choice([5.0, 98.0])
            air_quality = random.uniform(300, 500)
            co2_level = random.uniform(800, 1200)
            audio_level = random.uniform(900, 1000)
            vibration = random.uniform(180, 200)
            
        else:  # normal scenario
            temperature = max(-20, min(50, daily_temp + random.uniform(-3, 3)))
            humidity = max(10, min(95, 70 - (temperature - 20) * 1.5 + random.uniform(-15, 15)))
            air_quality = random.uniform(10, 100)
            co2_level = random.uniform(380, 450)
            
            # Audio varies by time of day
            if 6 <= hour <= 22:
                audio_level = random.uniform(200, 600)
            else:
                audio_level = random.uniform(50, 300)
                
            vibration = random.uniform(5, 50)
            if random.random() < 0.1:  # Occasional spikes
                vibration += random.uniform(20, 100)
        
        return {
            "temperature": round(temperature, 1),
            "humidity": round(max(0, min(100, humidity)), 1),
            "audio_level": round(max(0, min(1000, audio_level)), 1),
            "vibration": round(max(0, min(200, vibration)), 1),
            "air_quality_pm25": round(max(0, air_quality), 1),
            "co2_level": round(max(300, min(5000, co2_level)), 1),
            "device_id": self.device_id,
            "location": f"Test Site {scenario.title()}",
            "timestamp": current_time.isoformat()
        }
    
    def send_sensor_data(self, data: Dict[str, Any]) -> TestResult:
        """Send sensor data and measure performance"""
        start_time = time.time()
        
        try:
            response = self.session.post(
                f"{self.server_url}/api/sensor-data",
                json=data
            )
            
            response_time = (time.time() - start_time) * 1000  # Convert to ms
            
            if response.status_code == 200:
                result_data = response.json()
                
                # Extract key information
                ai_translation = result_data.get('ai_analysis', {}).get('ai_translation', 'No translation')
                consciousness = result_data.get('ai_analysis', {}).get('consciousness_level', 0)
                
                message = f"✅ Success | AI: {consciousness:.1%} | Translation: {ai_translation[:50]}..."
                
                return TestResult(
                    test_name="sensor_data",
                    success=True,
                    response_time=response_time,
                    status_code=response.status_code,
                    message=message
                )
            else:
                return TestResult(
                    test_name="sensor_data",
                    success=False,
                    response_time=response_time,
                    status_code=response.status_code,
                    message=f"❌ Server error: {response.status_code}"
                )
                
        except requests.exceptions.ConnectionError:
            return TestResult(
                test_name="sensor_data",
                success=False,
                response_time=0,
                status_code=0,
                message="❌ Connection error - Server not reachable"
            )
        except Exception as e:
            return TestResult(
                test_name="sensor_data",
                success=False,
                response_time=0,
                status_code=0,
                message=f"❌ Error: {str(e)}"
            )
    
    def test_system_health(self) -> TestResult:
        """Test system health endpoint"""
        start_time = time.time()
        
        try:
            response = self.session.get(f"{self.server_url}/api/health")
            response_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                health_data = response.json()
                status = health_data.get('status', 'unknown')
                version = health_data.get('version', 'unknown')
                
                return TestResult(
                    test_name="health_check",
                    success=True,
                    response_time=response_time,
                    status_code=response.status_code,
                    message=f"✅ Health: {status} | Version: {version}"
                )
            else:
                return TestResult(
                    test_name="health_check",
                    success=False,
                    response_time=response_time,
                    status_code=response.status_code,
                    message=f"❌ Health check failed: {response.status_code}"
                )
                
        except Exception as e:
            return TestResult(
                test_name="health_check",
                success=False,
                response_time=0,
                status_code=0,
                message=f"❌ Health check error: {str(e)}"
            )
    
    def test_system_status(self) -> TestResult:
        """Test system status endpoint"""
        start_time = time.time()
        
        try:
            response = self.session.get(f"{self.server_url}/api/status")
            response_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                status_data = response.json()
                ai_consciousness = status_data.get('ai_consciousness', 0)
                quantum_coherence = status_data.get('quantum_coherence', 0)
                
                return TestResult(
                    test_name="system_status",
                    success=True,
                    response_time=response_time,
                    status_code=response.status_code,
                    message=f"✅ AI: {ai_consciousness:.1%} | Quantum: {quantum_coherence:.1f}%"
                )
            else:
                return TestResult(
                    test_name="system_status",
                    success=False,
                    response_time=response_time,
                    status_code=response.status_code,
                    message=f"❌ Status check failed: {response.status_code}"
                )
                
        except Exception as e:
            return TestResult(
                test_name="system_status",
                success=False,
                response_time=0,
                status_code=0,
                message=f"❌ Status error: {str(e)}"
            )
    
    def run_comprehensive_test_suite(self) -> Dict[str, Any]:
        """Run comprehensive test suite"""
        print("🧪 EcoLingua AI v3.0 - Professional Test Suite")
        print("=" * 60)
        
        test_results = []
        
        # Test 1: System Health
        print("🏥 Testing system health...")
        health_result = self.test_system_health()
        test_results.append(health_result)
        print(f"   {health_result.message} ({health_result.response_time:.0f}ms)")
        
        # Test 2: System Status
        print("📊 Testing system status...")
        status_result = self.test_system_status()
        test_results.append(status_result)
        print(f"   {status_result.message} ({status_result.response_time:.0f}ms)")
        
        # Test 3: Normal Environmental Data
        print("🌿 Testing normal environmental data...")
        normal_data = self.generate_realistic_environmental_data("normal")
        normal_result = self.send_sensor_data(normal_data)
        test_results.append(normal_result)
        print(f"   {normal_result.message} ({normal_result.response_time:.0f}ms)")
        
        # Test 4: Optimal Conditions
        print("✨ Testing optimal environmental conditions...")
        optimal_data = self.generate_realistic_environmental_data("optimal")
        optimal_result = self.send_sensor_data(optimal_data)
        test_results.append(optimal_result)
        print(f"   {optimal_result.message} ({optimal_result.response_time:.0f}ms)")
        
        # Test 5: Stress Conditions
        print("⚠️  Testing stress environmental conditions...")
        stress_data = self.generate_realistic_environmental_data("stress")
        stress_result = self.send_sensor_data(stress_data)
        test_results.append(stress_result)
        print(f"   {stress_result.message} ({stress_result.response_time:.0f}ms)")
        
        # Calculate summary statistics
        successful_tests = sum(1 for result in test_results if result.success)
        total_tests = len(test_results)
        avg_response_time = sum(result.response_time for result in test_results if result.response_time > 0) / max(1, len([r for r in test_results if r.response_time > 0]))
        
        summary = {
            'total_tests': total_tests,
            'successful_tests': successful_tests,
            'success_rate': (successful_tests / total_tests) * 100,
            'average_response_time': avg_response_time,
            'test_results': test_results
        }
        
        print("\n" + "=" * 60)
        print("📈 Test Summary:")
        print(f"   Total Tests: {total_tests}")
        print(f"   Successful: {successful_tests}")
        print(f"   Success Rate: {summary['success_rate']:.1f}%")
        print(f"   Avg Response Time: {avg_response_time:.0f}ms")
        
        return summary
    
    def run_continuous_simulation(self, duration_minutes: int = 5, interval_seconds: int = 3):
        """Run continuous environmental simulation"""
        print(f"🚀 Starting Professional EcoLingua Simulation")
        print(f"⏱️  Duration: {duration_minutes} minutes")
        print(f"📡 Interval: {interval_seconds} seconds")
        print(f"🌐 Server: {self.server_url}")
        print("=" * 60)
        
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        
        success_count = 0
        total_count = 0
        response_times = []
        
        try:
            while time.time() < end_time:
                # Generate realistic data with some variation
                scenario = random.choices(
                    ["normal", "optimal", "stress"],
                    weights=[0.7, 0.2, 0.1]
                )[0]
                
                data = self.generate_realistic_environmental_data(scenario)
                
                print(f"\n⏰ {datetime.now().strftime('%H:%M:%S')} - Scenario: {scenario.title()}")
                print(f"   🌡️  Temperature: {data['temperature']}°C")
                print(f"   💧 Humidity: {data['humidity']}%")
                print(f"   🌬️  Air Quality: {data['air_quality_pm25']} PM2.5")
                print(f"   🌱 CO₂: {data['co2_level']} ppm")
                print(f"   🔊 Audio: {data['audio_level']} dB")
                
                result = self.send_sensor_data(data)
                total_count += 1
                
                if result.success:
                    success_count += 1
                    response_times.append(result.response_time)
                
                print(f"   {result.message}")
                
                time.sleep(max(1, interval_seconds))
                
        except KeyboardInterrupt:
            print("\n🛑 Simulation stopped by user")
        
        # Final statistics
        print(f"\n🏁 Simulation Complete")
        print("=" * 60)
        print(f"📊 Statistics:")
        print(f"   Total Requests: {total_count}")
        print(f"   Successful: {success_count}")
        print(f"   Success Rate: {(success_count/max(1,total_count))*100:.1f}%")
        
        if response_times:
            print(f"   Avg Response Time: {sum(response_times)/len(response_times):.0f}ms")
            print(f"   Min Response Time: {min(response_times):.0f}ms")
            print(f"   Max Response Time: {max(response_times):.0f}ms")
    
    def run_load_test(self, concurrent_requests: int = 5, duration_seconds: int = 30):
        """Run load testing with concurrent requests"""
        print(f"⚡ Load Testing - {concurrent_requests} concurrent requests for {duration_seconds}s")
        print("=" * 60)
        
        results = []
        threads = []
        
        def worker():
            end_time = time.time() + duration_seconds
            while time.time() < end_time:
                data = self.generate_realistic_environmental_data()
                result = self.send_sensor_data(data)
                results.append(result)
                time.sleep(0.5)
        
        # Start concurrent threads
        for i in range(concurrent_requests):
            thread = threading.Thread(target=worker)
            thread.start()
            threads.append(thread)
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Analyze results
        successful = sum(1 for r in results if r.success)
        total = len(results)
        avg_response = sum(r.response_time for r in results if r.response_time > 0) / max(1, len([r for r in results if r.response_time > 0]))
        
        print(f"📈 Load Test Results:")
        print(f"   Total Requests: {total}")
        print(f"   Successful: {successful}")
        print(f"   Success Rate: {(successful/max(1,total))*100:.1f}%")
        print(f"   Avg Response Time: {avg_response:.0f}ms")
        print(f"   Requests/Second: {total/duration_seconds:.1f}")

def main():
    """Main function with professional menu"""
    print("🌿 EcoLingua AI v3.0 - Professional Test Simulator")
    print("=" * 60)
    
    # Get server URL
    server_url = input("Server URL (default: http://localhost:5050): ").strip()
    if not server_url:
        server_url = "http://localhost:5050"
    
    simulator = ProfessionalEcoLinguaSimulator(server_url)
    
    while True:
        print("\n🎯 Professional Testing Options:")
        print("1. 🧪 Comprehensive Test Suite")
        print("2. 🚀 Continuous Simulation")
        print("3. ⚡ Load Testing")
        print("4. 🌿 Single Environmental Sample")
        print("5. ✨ Optimal Conditions Test")
        print("6. ⚠️  Stress Conditions Test")
        print("7. 🏥 Health Check Only")
        print("8. 📊 System Status Only")
        print("9. 🚪 Exit")
        
        try:
            choice = input("\nSelect option (1-9): ").strip()
            
            if choice == "1":
                simulator.run_comprehensive_test_suite()
                
            elif choice == "2":
                duration = input("Duration in minutes (default 5): ").strip()
                interval = input("Interval in seconds (default 3): ").strip()
                
                duration = max(1, min(60, int(duration) if duration.isdigit() else 5))
                interval = max(1, min(30, int(interval) if interval.isdigit() else 3))
                
                simulator.run_continuous_simulation(duration, interval)
                
            elif choice == "3":
                concurrent = input("Concurrent requests (default 5): ").strip()
                duration = input("Duration in seconds (default 30): ").strip()
                
                concurrent = max(1, min(20, int(concurrent) if concurrent.isdigit() else 5))
                duration = max(10, min(300, int(duration) if duration.isdigit() else 30))
                
                simulator.run_load_test(concurrent, duration)
                
            elif choice == "4":
                data = simulator.generate_realistic_environmental_data("normal")
                result = simulator.send_sensor_data(data)
                print(f"📊 Result: {result.message}")
                
            elif choice == "5":
                data = simulator.generate_realistic_environmental_data("optimal")
                result = simulator.send_sensor_data(data)
                print(f"✨ Result: {result.message}")
                
            elif choice == "6":
                data = simulator.generate_realistic_environmental_data("stress")
                result = simulator.send_sensor_data(data)
                print(f"⚠️  Result: {result.message}")
                
            elif choice == "7":
                result = simulator.test_system_health()
                print(f"🏥 Health: {result.message}")
                
            elif choice == "8":
                result = simulator.test_system_status()
                print(f"📊 Status: {result.message}")
                
            elif choice == "9":
                print("👋 Thank you for using EcoLingua Professional Test Simulator!")
                break
                
            else:
                print("❌ Invalid choice. Please select 1-9.")
                
        except KeyboardInterrupt:
            print("\n🛑 Test interrupted by user")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
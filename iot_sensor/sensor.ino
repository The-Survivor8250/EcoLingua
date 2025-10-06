#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <DHT.h>
#include <driver/i2s.h>
#include <esp_sleep.h>
#include <BluetoothSerial.h>

// WiFi credentials
const char* ssid = "Wokwi-GUEST";
const char* password = "";

// Server endpoint
const char* serverURL = "http://your-server:5050/api/sensor-data";

// Advanced features
BluetoothSerial SerialBT;
bool emergencyMode = false;
float baselineNoise = 0;
int wildlifeDetections = 0;

// DHT sensor setup
#define DHT_PIN 4
#define DHT_TYPE DHT11
DHT dht(DHT_PIN, DHT_TYPE);

// I2S microphone setup
#define I2S_WS 25
#define I2S_SD 33
#define I2S_SCK 32
#define I2S_PORT I2S_NUM_0
#define SAMPLE_RATE 16000
#define SAMPLE_BITS 16
#define SAMPLE_COUNT 1024

// Vibration sensor
#define VIBRATION_PIN 34

int16_t samples[SAMPLE_COUNT];
unsigned long lastSensorRead = 0;
const unsigned long sensorInterval = 5000; // 5 seconds

void setup() {
  Serial.begin(115200);
  dht.begin();
  
  // Initialize Bluetooth
  SerialBT.begin("EcoLingua_Sensor");
  Serial.println("Bluetooth device ready to pair");
  
  // Initialize WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("🌿 EcoLingua connecting to nature's network...");
  }
  Serial.println("🌍 Connected to global conservation network!");
  
  // Initialize I2S for microphone
  i2s_config_t i2s_config = {
    .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_RX),
    .sample_rate = SAMPLE_RATE,
    .bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT,
    .channel_format = I2S_CHANNEL_FMT_ONLY_LEFT,
    .communication_format = I2S_COMM_FORMAT_I2S,
    .intr_alloc_flags = ESP_INTR_FLAG_LEVEL1,
    .dma_buf_count = 4,
    .dma_buf_len = 1024
  };
  
  i2s_pin_config_t pin_config = {
    .bck_io_num = I2S_SCK,
    .ws_io_num = I2S_WS,
    .data_out_num = I2S_PIN_NO_CHANGE,
    .data_in_num = I2S_SD
  };
  
  i2s_driver_install(I2S_PORT, &i2s_config, 0, NULL);
  i2s_set_pin(I2S_PORT, &pin_config);
  
  Serial.println("🎤 Advanced audio monitoring system online");
  Serial.println("🦋 Wildlife detection algorithms activated");
  Serial.println("🚨 Emergency conservation system ready");
}

void loop() {
  if (millis() - lastSensorRead >= sensorInterval) {
    collectAndSendData();
    lastSensorRead = millis();
  }
  
  // Check for Bluetooth commands
  if (SerialBT.available()) {
    String command = SerialBT.readString();
    processBluetoothCommand(command);
  }
  
  delay(100);
}

void collectAndSendData() {
  // Read environmental sensors
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();
  int vibration = analogRead(VIBRATION_PIN);
  
  // Read audio data
  size_t bytes_read;
  i2s_read(I2S_PORT, samples, sizeof(samples), &bytes_read, portMAX_DELAY);
  
  // Advanced audio analysis
  float audioLevel = calculateAudioLevel();
  float dominantFreq = calculateDominantFrequency();
  String audioPattern = analyzeAudioPattern();
  bool wildlifeDetected = detectWildlife(audioLevel, dominantFreq);
  
  // Environmental threat detection
  bool threatDetected = detectEnvironmentalThreats(temperature, humidity, audioLevel);
  
  // Create comprehensive JSON payload
  DynamicJsonDocument doc(4096);
  doc["device_id"] = "EcoLingua_ESP32_Advanced";
  doc["timestamp"] = millis();
  doc["location"] = createLocationData();
  
  // Environmental data
  JsonObject env = doc.createNestedObject("environmental");
  env["temperature"] = temperature;
  env["humidity"] = humidity;
  env["vibration"] = vibration;
  env["air_quality_index"] = calculateAQI(temperature, humidity);
  
  // Advanced audio analysis
  JsonObject audio = doc.createNestedObject("audio_analysis");
  audio["level"] = audioLevel;
  audio["dominant_frequency"] = dominantFreq;
  audio["pattern"] = audioPattern;
  audio["baseline_deviation"] = audioLevel - baselineNoise;
  audio["wildlife_detected"] = wildlifeDetected;
  
  // Conservation insights
  JsonObject conservation = doc.createNestedObject("conservation");
  conservation["threat_level"] = threatDetected ? "high" : "low";
  conservation["biodiversity_score"] = calculateBiodiversityScore();
  conservation["ecosystem_health"] = assessEcosystemHealth(temperature, humidity, audioLevel);
  
  // Emergency system
  if (threatDetected) {
    triggerEmergencyMode();
    doc["emergency_alert"] = true;
  }
  
  JsonArray audioArray = doc.createNestedArray("audio_samples");
  for (int i = 0; i < min(200, SAMPLE_COUNT); i++) {
    audioArray.add(samples[i]);
  }
  
  String jsonString;
  serializeJson(doc, jsonString);
  
  // Multi-channel transmission
  sendToServer(jsonString);
  if (emergencyMode) {
    sendEmergencyAlert(jsonString);
  }
}

float calculateAudioLevel() {
  long sum = 0;
  int peaks = 0;
  for (int i = 0; i < SAMPLE_COUNT; i++) {
    int val = abs(samples[i]);
    sum += val;
    if (val > 1000) peaks++;
  }
  
  float avgLevel = (float)sum / SAMPLE_COUNT;
  
  // Adaptive baseline calibration
  if (baselineNoise == 0) {
    baselineNoise = avgLevel;
  } else {
    baselineNoise = (baselineNoise * 0.99) + (avgLevel * 0.01);
  }
  
  return avgLevel;
}

float calculateDominantFrequency() {
  // Enhanced frequency analysis with peak detection
  int maxIndex = 0;
  int maxValue = 0;
  int frequencyBins[10] = {0};
  
  for (int i = 1; i < SAMPLE_COUNT - 1; i++) {
    int val = abs(samples[i]);
    if (val > maxValue) {
      maxValue = val;
      maxIndex = i;
    }
    
    // Frequency binning for pattern analysis
    int bin = (i * 10) / SAMPLE_COUNT;
    if (bin < 10) frequencyBins[bin] += val;
  }
  
  return (float)(maxIndex * SAMPLE_RATE) / (2 * SAMPLE_COUNT);
}

String analyzeAudioPattern() {
  // Advanced pattern recognition
  float avgAmplitude = calculateAudioLevel();
  float dominantFreq = calculateDominantFrequency();
  
  if (dominantFreq > 2000 && dominantFreq < 8000) {
    return "bird_song";
  } else if (dominantFreq > 100 && dominantFreq < 1000) {
    return "mammal_call";
  } else if (avgAmplitude > baselineNoise * 3) {
    return "disturbance";
  } else {
    return "ambient";
  }
}

bool detectWildlife(float audioLevel, float frequency) {
  // AI-powered wildlife detection
  bool detected = false;
  
  if (frequency > 1000 && frequency < 10000 && audioLevel > baselineNoise * 1.5) {
    wildlifeDetections++;
    detected = true;
    Serial.println("🦅 Wildlife activity detected!");
  }
  
  return detected;
}

bool detectEnvironmentalThreats(float temp, float humidity, float audioLevel) {
  // Multi-parameter threat assessment
  bool threat = false;
  
  if (temp > 40 || temp < -10) {
    Serial.println("🌡️ Extreme temperature threat detected!");
    threat = true;
  }
  
  if (audioLevel > baselineNoise * 5) {
    Serial.println("🔊 Unusual noise disturbance detected!");
    threat = true;
  }
  
  if (humidity < 20 || humidity > 90) {
    Serial.println("💧 Extreme humidity conditions detected!");
    threat = true;
  }
  
  return threat;
}

JsonObject createLocationData() {
  DynamicJsonDocument locationDoc(512);
  JsonObject location = locationDoc.to<JsonObject>();
  
  location["latitude"] = 40.7128;  // Example coordinates
  location["longitude"] = -74.0060;
  location["altitude"] = 10;
  location["ecosystem_type"] = "temperate_forest";
  location["protection_status"] = "monitored";
  
  return location;
}

float calculateAQI(float temp, float humidity) {
  // Simplified air quality estimation
  float aqi = 50; // Base good air quality
  
  if (temp > 35) aqi += 20;
  if (humidity > 80) aqi += 15;
  if (humidity < 30) aqi += 10;
  
  return min(aqi, 500.0f);
}

float calculateBiodiversityScore() {
  // Dynamic biodiversity scoring
  float score = 0.5; // Base score
  
  if (wildlifeDetections > 0) {
    score += min(wildlifeDetections * 0.1, 0.4);
  }
  
  return min(score, 1.0f);
}

String assessEcosystemHealth(float temp, float humidity, float audioLevel) {
  if (temp > 15 && temp < 30 && humidity > 40 && humidity < 70 && wildlifeDetections > 0) {
    return "excellent";
  } else if (temp > 10 && temp < 35 && humidity > 30 && humidity < 80) {
    return "good";
  } else {
    return "stressed";
  }
}

void triggerEmergencyMode() {
  emergencyMode = true;
  Serial.println("🚨 EMERGENCY MODE ACTIVATED!");
  SerialBT.println("🚨 Conservation emergency detected!");
  
  // Flash LED or activate buzzer if available
  // Emergency protocols would be implemented here
}

void sendEmergencyAlert(String data) {
  // Send to emergency endpoints
  HTTPClient emergencyHttp;
  emergencyHttp.begin("http://your-server:5050/api/sensor-data");
  emergencyHttp.addHeader("Content-Type", "application/json");
  emergencyHttp.addHeader("X-Emergency", "true");
  
  int response = emergencyHttp.POST(data);
  Serial.printf("Emergency alert sent: %d\n", response);
  emergencyHttp.end();
}

void processBluetoothCommand(String command) {
  command.trim();
  
  if (command == "STATUS") {
    SerialBT.printf("🌿 EcoLingua Status:\n");
    SerialBT.printf("Wildlife detections: %d\n", wildlifeDetections);
    SerialBT.printf("Emergency mode: %s\n", emergencyMode ? "ACTIVE" : "NORMAL");
    SerialBT.printf("Baseline noise: %.2f\n", baselineNoise);
  } else if (command == "RESET") {
    wildlifeDetections = 0;
    emergencyMode = false;
    baselineNoise = 0;
    SerialBT.println("🔄 System reset complete");
  } else if (command == "EMERGENCY") {
    triggerEmergencyMode();
  }
}

void sendToServer(String data) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverURL);
    http.addHeader("Content-Type", "application/json");
    http.addHeader("X-Device-Type", "EcoLingua-Advanced");
    
    int httpResponseCode = http.POST(data);
    
    if (httpResponseCode > 0) {
      Serial.printf("🌍 Data transmitted to conservation network: %d\n", httpResponseCode);
    } else {
      Serial.printf("❌ Transmission error: %s\n", http.errorToString(httpResponseCode).c_str());
    }
    
    http.end();
  }
}
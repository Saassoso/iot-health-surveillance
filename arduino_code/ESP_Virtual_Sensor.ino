#include <WiFi.h>
#include <PubSubClient.h>

// WiFi credentials
const char* ssid = "Orange-CE5F";
const char* password = "36LG4061L9Y";

// MQTT broker
const char* mqtt_server = "192.168.1.154"; // Replace with Raspberry Pi IP
const int mqtt_port = 1883;
const char* heart_rate_topic =  "sensor/patient1/heart_rate";  // MQTT topic for heart rate
const char* temperature_topic = "sensor/patient1/temperature";  // MQTT topic for temperature
const char* spO2_topic =        "sensor/patient1/spo2";            // MQTT topic for SpO2
const char* sickness_topic =    "sensor/patient1/sickness";  // MQTT topic for sickness

WiFiClient espClient;
PubSubClient client(espClient);

int i = 1;
int sicknessCounter = 0; // Counter to simulate sickness duration
String currentSickness = ""; // Current sickness state

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to WiFi...");
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("Connected to WiFi");
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP32_Client")) {
      Serial.println("connected");
    } else {
      Serial.print("Failed, rc=");
      Serial.print(client.state());
      delay(5000);
    }
  }
}

float generateHeartRate() {
  if (sicknessCounter > 0) {
    return random(120, 160); // Abnormal heart rate during sickness
  }
  return random(60, 101);
}

float generateTemperature() {
  if (sicknessCounter > 0) {
    return random(390, 410) / 10.0; // Abnormal temperature during sickness
  }
  return random(365, 376) / 10.0;
}

float generateSpO2() {
  if (sicknessCounter > 0) {
    return random(85, 95); // Lower SpO2 during sickness
  }
  return random(95, 101);
}

void setup() {
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, mqtt_port);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  // Determine sickness state
  if (sicknessCounter == 0 && random(0, 100) < 5) { // 5% chance to simulate sickness
    int sicknessType = random(0, 3);
    if (sicknessType == 0) currentSickness = "Corona";
    else if (sicknessType == 1) currentSickness = "Flu";
    else if (sicknessType == 2) currentSickness = "Pneumonia";

    sicknessCounter = 6; // Sickness duration (30 seconds / 5-second loop)
    client.publish(sickness_topic, currentSickness.c_str());
    Serial.println("Sickness state activated: " + currentSickness);
  }

  // Simulate sensor readings
  float heartRate = generateHeartRate();
  float temperature = generateTemperature();
  float spO2 = generateSpO2();

  // Publish the sensor data to MQTT topics
  String heartRateMessage = String(heartRate);
  String temperatureMessage = String(temperature);
  String spO2Message = String(spO2);

  client.publish(heart_rate_topic, heartRateMessage.c_str());
  client.publish(temperature_topic, temperatureMessage.c_str());
  client.publish(spO2_topic, spO2Message.c_str());

  Serial.println("Published sensor data:");
  Serial.print("Heart Rate: ");
  Serial.println(heartRate);
  Serial.print("Temperature: ");
  Serial.println(temperature);
  Serial.print("SpO2: ");
  Serial.println(spO2);

  if (sicknessCounter > 0) {
    sicknessCounter--;
    if (sicknessCounter == 0) {
      currentSickness = "None";
      client.publish(sickness_topic, "None"); // End sickness state
      Serial.println("Sickness state ended.");
    }
  }

  i++;
  i = i % 30;
  // Delay to simulate real-time data update every 5 seconds
  delay(5000);
}


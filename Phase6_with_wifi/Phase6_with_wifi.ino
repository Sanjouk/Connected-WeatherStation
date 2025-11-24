#include <WiFi.h>
#include <HTTPClient.h>
#include "DHT.h"
#include <ArduinoJson.h>

// ------------------- Wi-Fi -------------------
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// ------------------- Server -------------------
const char* serverURL = "http://192.168.1.100:3000/telemetry"; // Replace with your server IP

// ------------------- Pins -------------------
#define DHTPIN        4
#define DHTTYPE       DHT22
#define LDR_PIN       36
#define POT_PIN       39
#define PIR_PIN       14

DHT dht(DHTPIN, DHTTYPE);

// ------------------- Setup -------------------
void setup() {
  Serial.begin(115200);
  dht.begin();
  
  pinMode(LDR_PIN, INPUT);
  pinMode(POT_PIN, INPUT);
  pinMode(PIR_PIN, INPUT);

  WiFi.begin(ssid, password);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected!");
}

// ------------------- Loop -------------------
void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();
    int ldrValue = analogRead(LDR_PIN);
    int potValue = analogRead(POT_PIN);
    int pirValue = digitalRead(PIR_PIN);

    if (isnan(temperature) || isnan(humidity)) {
      Serial.println("Failed to read DHT22!");
    } else {
      // Build JSON
      StaticJsonDocument<256> doc;
      doc["device_id"] = "ESP32_001";
      doc["temperature"] = temperature;
      doc["humidity"] = humidity;
      doc["ldr"] = ldrValue;
      doc["pot"] = potValue;
      doc["pir"] = pirValue;

      String jsonData;
      serializeJson(doc, jsonData);

      // Send HTTP POST
      HTTPClient http;
      http.begin(serverURL);
      http.addHeader("Content-Type", "application/json");

      int httpResponseCode = http.POST(jsonData);

      if (httpResponseCode > 0) {
        String response = http.getString();
        Serial.print("Server response: ");
        Serial.println(response);
      } else {
        Serial.print("Error on sending POST: ");
        Serial.println(httpResponseCode);
      }

      http.end();
    }
  } else {
    Serial.println("Wi-Fi disconnected, retrying...");
    WiFi.reconnect();
  }

  delay(10000); // Wait 10 seconds before next POST
}

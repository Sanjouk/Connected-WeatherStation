#include "DHT.h"
#include <ESP32Servo.h>

// ------------------- Pins -------------------
#define DHTPIN        4
#define DHTTYPE       DHT22

#define LDR_PIN       36
#define POT_PIN       39
#define PIR_PIN       14

#define SERVO_PIN     13
#define LED_PWM_PIN   2
#define BUZZER_PIN    12

// ------------------- Constants -------------------
#define TEMP_THRESHOLD    28.0   // °C, adjust as needed
#define LIGHT_THRESHOLD   500    // raw ADC value
bool securityMode = true;       // Security mode ON/OFF

// ------------------- Objects -------------------
DHT dht(DHTPIN, DHTTYPE);
Servo blindServo;

// ------------------- Setup -------------------
void setup() {
  Serial.begin(115200);

  // Sensors
  dht.begin();
  pinMode(LDR_PIN, INPUT);
  pinMode(POT_PIN, INPUT);
  pinMode(PIR_PIN, INPUT);

  // Actuators
  blindServo.attach(SERVO_PIN);
  pinMode(LED_PWM_PIN, OUTPUT);
  ledcSetup(0, 5000, 8);    // LED PWM channel
  ledcAttachPin(LED_PWM_PIN, 0);

  pinMode(BUZZER_PIN, OUTPUT);

  Serial.println("Phase 5: Local Automation Started");
}

// ------------------- Helper Functions -------------------
void updateServo(float temp) {
  if (temp > TEMP_THRESHOLD) {
    Serial.println("Temp high → Closing blinds (180°)");
    blindServo.write(180);
  }
}

void updateLED(int ldrValue, int potValue) {
  if (ldrValue < LIGHT_THRESHOLD) {
    Serial.println("Low light → LEDs ON");
    int brightness = map(potValue, 0, 4095, 0, 255);
    ledcWrite(0, brightness);
  } else {
    ledcWrite(0, 0); // Turn off LED
  }
}

void securityAlarm(bool pirDetected) {
  if (securityMode && pirDetected) {
    Serial.println("Security breach! Activating alarm");
    digitalWrite(BUZZER_PIN, HIGH);
    ledcWrite(0, 0);           // Lights OFF
    blindServo.write(180);     // Close blinds
  } else {
    digitalWrite(BUZZER_PIN, LOW);
  }
}

// ------------------- Main Loop -------------------
void loop() {
  // --- Read Sensors ---
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();
  int ldrValue = analogRead(LDR_PIN);
  int potValue = analogRead(POT_PIN);
  int pirState = digitalRead(PIR_PIN);

  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Failed to read DHT22!");
  } else {
    Serial.print("Temp: "); Serial.print(temperature);
    Serial.print(" °C, Humidity: "); Serial.println(humidity);
  }

  Serial.print("LDR: "); Serial.print(ldrValue);
  Serial.print(", Pot: "); Serial.print(potValue);
  Serial.print(", PIR: "); Serial.println(pirState);

  // --- Automation Logic ---
  updateServo(temperature);
  updateLED(ldrValue, potValue);
  securityAlarm(pirState);

  delay(1000);  // Loop interval
}

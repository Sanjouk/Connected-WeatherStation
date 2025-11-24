#include <ESP32Servo.h>

// ------------------- Pins -------------------
#define SERVO_PIN      13   // Servo for blinds
#define POT_PIN        39   // Potentiometer for brightness
#define LED_PWM_PIN    2    // Single LED
#define RGB_RED_PIN    25
#define RGB_GREEN_PIN  26
#define RGB_BLUE_PIN   27

// ------------------- Servo -------------------
Servo blindServo;

// ------------------- RGB Mode -------------------
enum RGBMode { RED, GREEN, BLUE, CYAN, MAGENTA, YELLOW, WHITE, OFF };
RGBMode currentMode = OFF;

// ------------------- Setup -------------------
void setup() {
  Serial.begin(115200);

  // Servo setup
  blindServo.attach(SERVO_PIN);

  // PWM LED setup
  ledcSetup(0, 5000, 8); // Channel 0, 5 kHz, 8-bit
  ledcAttachPin(LED_PWM_PIN, 0);

  // RGB setup
  ledcSetup(1, 5000, 8); ledcAttachPin(RGB_RED_PIN, 1);
  ledcSetup(2, 5000, 8); ledcAttachPin(RGB_GREEN_PIN, 2);
  ledcSetup(3, 5000, 8); ledcAttachPin(RGB_BLUE_PIN, 3);

  Serial.println("Phase 4: Actuator Test Started");
}

// ------------------- Functions -------------------
void setRGB(RGBMode mode) {
  switch(mode) {
    case RED:     ledcWrite(1, 255); ledcWrite(2, 0);   ledcWrite(3, 0); break;
    case GREEN:   ledcWrite(1, 0);   ledcWrite(2, 255); ledcWrite(3, 0); break;
    case BLUE:    ledcWrite(1, 0);   ledcWrite(2, 0);   ledcWrite(3, 255); break;
    case CYAN:    ledcWrite(1, 0);   ledcWrite(2, 255); ledcWrite(3, 255); break;
    case MAGENTA: ledcWrite(1, 255); ledcWrite(2, 0);   ledcWrite(3, 255); break;
    case YELLOW:  ledcWrite(1, 255); ledcWrite(2, 255); ledcWrite(3, 0); break;
    case WHITE:   ledcWrite(1, 255); ledcWrite(2, 255); ledcWrite(3, 255); break;
    case OFF:     ledcWrite(1, 0);   ledcWrite(2, 0);   ledcWrite(3, 0); break;
  }
}

// ------------------- Main Loop -------------------
void loop() {
  // --- Servo Test ---
  Serial.println("Servo: 0° (open blinds)");
  blindServo.write(0);
  delay(2000);

  Serial.println("Servo: 90° (half closed)");
  blindServo.write(90);
  delay(2000);

  Serial.println("Servo: 180° (fully closed)");
  blindServo.write(180);
  delay(2000);

  // --- LED Brightness Test ---
  int potValue = analogRead(POT_PIN);        // 0–4095 on ESP32 ADC
  int ledValue = map(potValue, 0, 4095, 0, 255);
  ledcWrite(0, ledValue);                    // Write PWM to LED
  Serial.print("LED Brightness: "); Serial.println(ledValue);

  // --- RGB Lamp Modes ---
  for (int i = RED; i <= OFF; i++) {
    currentMode = (RGBMode)i;
    setRGB(currentMode);
    Serial.print("RGB Mode: "); Serial.println(i);
    delay(1500);
  }
}

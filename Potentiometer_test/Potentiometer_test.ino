#define POT_PIN 39
#define ADC_MAX_VALUE 4095.0 // Max ADC value for 12-bit resolution (ESP32 standard)
#define VREF 3.3             // ESP32 operating voltage (Reference Voltage)

void setup() {
  // Initialize the Serial communication at a baud rate of 115200
  Serial.begin(115200);
}

void loop() {
  // 1. Read the raw analog value from the potentiometer pin (0 to 4095)
  int rawValue = analogRead(POT_PIN);

  // 2. Convert the raw ADC value to a normalized float value (0.0 to 1.0)
  float normalizedValue = (float)rawValue / ADC_MAX_VALUE;

  // 3. Convert the normalized value to the actual voltage (0.0 V to 3.3 V)
  float voltage = normalizedValue * VREF;

  // Print the raw reading
  Serial.print("Raw Value: ");
  Serial.print(rawValue);

  // Print the normalized value
  Serial.print(" | Normalized: ");
  Serial.print(normalizedValue);

  // Print the calculated voltage (with 2 decimal places)
  Serial.print(" | Voltage: ");
  Serial.print(voltage, 2); 
  Serial.println(" V");
  
  // Wait for 200 milliseconds before the next reading
  delay(200);
}
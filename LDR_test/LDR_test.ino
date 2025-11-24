#define LDR_PIN 36
#define ADC_MAX_VALUE 4095.0 // 12-bit resolution
#define VREF 3.3 // Reference voltage (VCC)

void setup() {
  Serial.begin(115200);
}

void loop() {
  // 1. Read the raw ADC value
  int rawValue = analogRead(LDR_PIN);

  // 2. Convert the raw value to voltage
  // Use floating-point math for precision
  float voltage = (float)rawValue / ADC_MAX_VALUE * VREF;

  // 3. Print the results
  Serial.print("LDR Raw Value: ");
  Serial.print(rawValue);
  
  Serial.print(" | Converted Voltage: ");
  Serial.print(voltage);
  Serial.println(" V");

  delay(500);
}
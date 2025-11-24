#define BUZZER_PIN 12

void setup() {
  Serial.begin(115200);
  pinMode(BUZZER_PIN, OUTPUT);
}

void loop() {
  Serial.println("Buzzing!");
  digitalWrite(BUZZER_PIN, HIGH);
  delay(1000);

  Serial.println("Silence.");
  digitalWrite(BUZZER_PIN, LOW);
  delay(1000);
}

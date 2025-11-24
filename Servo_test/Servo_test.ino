#include <ESP32Servo.h>

Servo myservo;

int servoPin = 27;
int potentiometre = 34;
int angle = 0;

void setup(){
  Serial.begin(115200);
  myservo.attach(servoPin);
  myservo.write(90);
  pinMode(potentiometre, INPUT);
}

void loop(){
  int raw = analogRead(potentiometre);      // 0..4095
  int angle = map(raw, 0, 4095, 0, 180);
  angle = constrain(angle, 0, 180);

  myservo.write(angle);

  Serial.print("ADC: ");   Serial.print(raw);
  Serial.print("  -> Angle: "); Serial.println(angle);

  delay(15); // petit délai pour la stabilité du servo
}
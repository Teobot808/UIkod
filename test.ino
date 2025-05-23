int counter = 0;

void setup() {
  Serial.begin(115200);
}

void loop() {
  // Loop every 100ms, reset every 100 counts (10s)
  counter = (counter + 1) % 100;

  float voltage = 11.0 + (counter % 16) * 0.1;  // 11.0 to 12.5V
  int speed = (counter * 2) % 100;              // 0–99
  int pwm = counter % 100;                      // 0–99
  int current = 1 + (counter % 3);              // 1–3A
  int laps = counter / 10;                      // one lap every second

  Serial.print("{\"time\": ");
  Serial.print(counter);
  Serial.print(", \"voltage\": ");
  Serial.print(voltage, 2);
  Serial.print(", \"current\": ");
  Serial.print(current);
  Serial.print(", \"speed\": ");
  Serial.print(speed);
  Serial.print(", \"pwm\": ");
  Serial.print(pwm);
  Serial.print(", \"laps\": ");
  Serial.print(laps);
  Serial.println(", \"status\": \"ok\"}");

  delay(100);
}

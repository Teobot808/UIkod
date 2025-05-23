// Arduino mock telemetry generator
void setup() {
  Serial.begin(115200);
}

void loop() {
  static int counter = 0;
  static unsigned long start = millis();

  int pwm = counter % 100;
  int speed = (counter * 2) % 40;
  int rpm = counter * 10;
  int warning = (counter % 50 == 0) ? 1 : 0;

  unsigned long now = millis();
  int elapsed = (now - start) / 1000;
  int lap_time = elapsed % 60;
  int laps = elapsed / 60;

  String data = "{";
  data += "\"V1\": " + String(12.1 + counter % 2) + ",";
  data += "\"V2\": " + String(12.3 + counter % 3) + ",";
  data += "\"V3\": " + String(11.9 + counter % 2) + ",";
  data += "\"V4\": " + String(4.9 + counter % 2) + ",";
  data += "\"V5\": " + String(5.1) + ",";
  data += "\"V6\": " + String(4.8) + ",";
  data += "\"V7\": " + String(5.0) + ",";
  data += "\"current\": " + String(1.2 + (counter % 3) * 0.3, 2) + ",";
  data += "\"temp1\": " + String(30 + counter % 5) + ",";
  data += "\"temp2\": " + String(28 + (counter % 7)) + ",";
  data += "\"temp3\": " + String(27 + (counter % 6)) + ",";
  data += "\"pwm\": " + String(pwm) + ",";
  data += "\"laps\": " + String(laps) + ",";
  data += "\"time\": " + String(elapsed) + ",";
  data += "\"lap_time\": " + String(lap_time) + ",";
  data += "\"rpm\": " + String(rpm) + ",";
  data += "\"speed\": " + String(speed) + ",";
  data += "\"mode\": " + String(1 + counter % 3) + ",";
  data += "\"warning\": " + String(warning) + ",";
  data += "\"debug\": " + String(counter % 10);
  data += "}";

  Serial.println(data);
  delay(200);
  counter++;
}

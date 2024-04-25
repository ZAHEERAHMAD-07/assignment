#include <WiFi.h>
#include <HTTPClient.h>
#include <ESP32Servo.h>

const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
const char* accountSid = "YOUR_TWILIO_ACCOUNT_SID";
const char* authToken = "YOUR_TWILIO_AUTH_TOKEN";
const char* twilioNumber = "YOUR_TWILIO_PHONE_NUMBER";
const char* recipientNumber = "RECIPIENT_PHONE_NUMBER";
const int doorSensorPin = 2; // GPIO pin for door sensor
const int servoPin = 4; // GPIO pin for servo motor
const int closedPosition = 0; // Angle for servo when door is closed
const int openPosition = 90; // Angle for servo when door is open

Servo doorLockServo;

void setup() {
  Serial.begin(115200);
  pinMode(doorSensorPin, INPUT_PULLUP);
  doorLockServo.attach(servoPin);
  connectToWiFi();
}

void loop() {
  if (isDoorOpen()) {
    Serial.println("Door is open");
    unlockDoor();
    sendSMS("Door alarm: The door has been opened!");
    delay(5000); // Wait for 5 seconds to avoid sending multiple alarms in quick succession
  } else {
    Serial.println("Door is closed");
    lockDoor();
  }
  delay(1000); // Check door status every 1 second
}

void connectToWiFi() {
  Serial.print("Connecting to WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("WiFi connected");
  Serial.println("IP address: " + WiFi.localIP().toString());
}

bool isDoorOpen() {
  return digitalRead(doorSensorPin) == HIGH;
}

void lockDoor() {
  doorLockServo.write(closedPosition);
  Serial.println("Door locked");
}

void unlockDoor() {
  doorLockServo.write(openPosition);
  Serial.println("Door unlocked");
}

void sendSMS(const char* message) {
  HTTPClient http;
  http.begin("https://api.twilio.com/2010-04-01/Accounts/" + String(accountSid) + "/Messages.json");
  http.setAuthorization(accountSid, authToken);
  http.addHeader("Content-Type", "application/x-www-form-urlencoded");

  String postData = "To=" + String(recipientNumber) + "&From=" + String(twilioNumber) + "&Body=" + String(message);
  int httpResponseCode = http.POST(postData);

  if (httpResponseCode > 0) {
    Serial.println("SMS sent successfully");
  } else {
    Serial.print("Error sending SMS. HTTP response code: ");
    Serial.println(httpResponseCode);
  }

  http.end();
}

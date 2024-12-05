#include "BluetoothSerial.h"

BluetoothSerial SerialBT;  // Initialize Bluetooth Serial

void setup() {
  Serial.begin(9600);        // For debugging and forwarding data
  //Serial2.begin(9600, SERIAL_8N1, 16, 17);
  SerialBT.begin("ESP32-Robot");  // Set Bluetooth device name
  Serial.println("Bluetooth Device is Ready to Pair");
}

void loop() {
  // Check for data from Bluetooth
  if (SerialBT.available()) {
    String input = SerialBT.readStringUntil('\n');  // Read input from Bluetooth
    input.trim();  // Remove any extra whitespace or newline

    // Map numeric input to commands
    if (input == "1") {
      Serial.println("FORWARD");
    } else if (input == "2") {
      Serial.println("REVERSE");
    } else if (input == "3") {
      Serial.println("STOP");
    } else if (input == "4") {
      Serial.println("TURN_LEFT");
    } else if (input == "5") {
      Serial.println("TURN_RIGHT");
    } else {
      // Forward any other input directly
      Serial.println(input);
    }
  }

  /*// Check for data from Serial Monitor (for debugging)
  if (Serial.available()) {
    String debugInput = Serial.readStringUntil('\n');  // Read from Serial Monitor
    debugInput.trim();
    SerialBT.println(debugInput);  // Send it to the Bluetooth device
    Serial.println("Sent to Bluetooth: " + debugInput);  // Debugging feedback
  }*/
}

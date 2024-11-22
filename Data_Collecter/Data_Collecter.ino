#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_HMC5883_U.h>
#include "BluetoothSerial.h" // Include Bluetooth Serial library

Adafruit_HMC5883_Unified mag = Adafruit_HMC5883_Unified(12345);
BluetoothSerial SerialBT;

// Function to calculate magnetic field intensity and heading
void calculateMagneticFieldAndHeading(float x, float y, float z, float &intensity, float &heading) {
    // Calculate the total magnetic field intensity
    intensity = sqrt(x * x + y * y + z * z);

    // Calculate the heading (in degrees)
    heading = atan2(y, x) * 180.0 / PI;


    // Ensure heading is in the range [0, 360]
    if (heading < 0) {
        heading += 360.0;
    }
}

void setup() {
    // Start Serial for debugging
    Serial.begin(115200);
    while (!Serial);

    // Initialize Bluetooth
    SerialBT.begin("ESP32_HMC5883L");
    Serial.println("Bluetooth ready. Pair with ESP32_HMC5883L.");

    // Initialize the HMC5883L module
    if (!mag.begin()) {
        Serial.println("Error: HMC5883L not detected. Check wiring.");
        while (1);
    }
    Serial.println("HMC5883L ready.");
}

void loop() {
    // Get magnetometer readings
    sensors_event_t event;
    mag.getEvent(&event);

    // Variables to store calculated values
    float intensity, heading;
    float horizontalField = sqrt(event.magnetic.x * event.magnetic.x + event.magnetic.y * event.magnetic.y); // Magnitude of horizontal component
    float inclinationRadians = atan2(event.magnetic.z, horizontalField); // Angle in radians
    float inclinationDegrees = inclinationRadians * 180.0 / PI; // Convert to degrees
    
    // Calculate magnetic field intensity and heading
    calculateMagneticFieldAndHeading(event.magnetic.x, event.magnetic.y, event.magnetic.z, intensity, heading);
    

    // Format the data
    String data1 = String(event.magnetic.x) + "," +  String(event.magnetic.y) + "," +  String(event.magnetic.z) + "," + String(intensity) + "," + String(heading) + "," + String(inclinationDegrees);
    //String data2 = "Intensity: " + String(intensity) + " uT, Heading: " + String(heading) + " degrees";

    // Send data over Bluetooth
    SerialBT.println(data1);
    //SerialBT.println(data2);

    // Debugging: Print data to Serial Monitor
    Serial.println(data1);

    delay(100); // Send data every second
}

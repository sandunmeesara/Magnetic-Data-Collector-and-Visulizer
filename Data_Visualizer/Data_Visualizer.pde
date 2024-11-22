import processing.serial.*;  // Import Serial library
import java.io.PrintWriter; // Import library for writing to file

Serial myPort;            // Serial port object
PrintWriter output;       // File writer object

float[][] dataPoints;     // 2D array to store data points (x, y, z, intensity, heading)
int maxDataPoints = 100;  // Number of points to display on the chart
float maxValue = 100.0;   // Maximum value for the chart scale (adjust as needed)
String[] serialPorts;     // List of available COM ports
boolean portSelected = false; // Flag to track if the port is selected

void setup() {
  size(1000, 600); // Set the window size

  // List available serial ports
  serialPorts = Serial.list();
  println("Available Serial Ports:");
  for (int i = 0; i < serialPorts.length; i++) {
    println(i + ": " + serialPorts[i]);
  }
  println("Please type the port number in the console to select it.");

  dataPoints = new float[maxDataPoints][5]; // Initialize the 2D array

  // Initialize file for recording data
  output = createWriter("data_log.csv");
  output.println("X,Y,Z,Intensity,Heading"); // Add header row to the CSV
}

void draw() {
  background(255);         // Clear the screen with white background
  stroke(0);               // Set line color to black
  fill(0);                 // Set text color to black

  if (!portSelected) {
    textAlign(CENTER, CENTER);
    textSize(20);
    text("Select the COM port in the console to start.", width / 2, height / 2);
    return;
  }

  // Draw the chart border
  line(50, height - 50, width - 50, height - 50); // X-axis
  line(50, height - 50, 50, 50);                 // Y-axis

  // Display the chart labels
  textAlign(CENTER);
  text("Data Over Time (Intensity)", width / 2, height - 10);
  textAlign(LEFT);
  text("Value", 10, height / 2);

  // Draw data points for intensity
  float xStep = (width - 100) / (maxDataPoints - 1); // Spacing between points
  for (int i = 0; i < maxDataPoints - 1; i++) {
    float x1 = 50 + i * xStep;
    float y1 = map(dataPoints[i][3], 0, maxValue, height - 50, 50); // Intensity
    float x2 = 50 + (i + 1) * xStep;
    float y2 = map(dataPoints[i + 1][3], 0, maxValue, height - 50, 50); // Intensity
    line(x1, y1, x2, y2); // Draw line between points
  }
}

void serialEvent(Serial myPort) {
  String data = myPort.readStringUntil('\n'); // Read incoming data until newline
  if (data != null) {
    data = trim(data); // Remove extra whitespace
    try {
      // Parse the CSV data (x, y, z, intensity, heading)
      String[] values = split(data, ",");
      if (values.length == 5) {
        float x = float(values[0]);
        float y = float(values[1]);
        float z = float(values[2]);
        float intensity = float(values[3]);
        float heading = float(values[4]);

        // Record the data to the file
        output.println(data);
        output.flush(); // Ensure data is saved immediately

        // Shift data points and add the new row
        for (int i = 0; i < maxDataPoints - 1; i++) {
          dataPoints[i] = dataPoints[i + 1];
        }
        dataPoints[maxDataPoints - 1] = new float[]{x, y, z, intensity, heading};
      }
    } catch (Exception e) {
      println("Invalid data: " + data); // Handle parsing errors
    }
  }
}

void keyPressed() {
  if (key == 'q' || key == 'Q') {
    output.close(); // Close the file when 'q' is pressed
    exit();         // Exit the program
  }
}

void keyTyped() {
  if (!portSelected) {
    // Allow user to select the serial port by typing the index
    int portIndex = int(key) - int('0'); // Convert key to number
    if (portIndex >= 0 && portIndex < serialPorts.length) {
      myPort = new Serial(this, serialPorts[portIndex], 115200);
      println("Connected to: " + serialPorts[portIndex]);
      portSelected = true;
    } else {
      println("Invalid port selection. Try again.");
    }
  }
}

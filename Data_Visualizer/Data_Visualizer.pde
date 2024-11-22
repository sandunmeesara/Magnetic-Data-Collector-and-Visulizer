import processing.serial.*;  // Import Serial library
import java.io.PrintWriter; // Import library for writing to file

Serial myPort;            // Serial port object
PrintWriter output;       // File writer object

float[] dataPoints;       // Array to store data points for the chart
int maxDataPoints = 100;  // Number of points to display on the chart
float maxValue = 100.0;   // Maximum value for the chart scale (adjust as needed)

void setup() {
  size(800, 400);         // Set the window size
  String portName = Serial.list()[0]; // Automatically select the first available serial port
  myPort = new Serial(this, portName, 115200); // Open the port with the correct baud rate
  myPort.bufferUntil('\n');  // Wait for new line character before processing data
  
  dataPoints = new float[maxDataPoints]; // Initialize data array
  
  // Initialize file for recording data
  output = createWriter("data_log.txt"); 
}

void draw() {
  background(255);         // Clear the screen with white background
  stroke(0);               // Set line color to black
  fill(0);                 // Set text color to black
  
  // Draw the chart border
  line(50, height - 50, width - 50, height - 50); // X-axis
  line(50, height - 50, 50, 50);                 // Y-axis
  
  // Display the chart labels
  textAlign(CENTER);
  text("Data Over Time", width / 2, height - 10);
  textAlign(LEFT);
  text("Value", 10, height / 2);
  
  // Draw data points
  float xStep = (width - 100) / (maxDataPoints - 1); // Spacing between points
  for (int i = 0; i < dataPoints.length - 1; i++) {
    float x1 = 50 + i * xStep;
    float y1 = map(dataPoints[i], 0, maxValue, height - 50, 50);
    float x2 = 50 + (i + 1) * xStep;
    float y2 = map(dataPoints[i + 1], 0, maxValue, height - 50, 50);
    line(x1, y1, x2, y2); // Draw line between points
  }
}

void serialEvent(Serial myPort) {
  String data = myPort.readStringUntil('\n'); // Read incoming data until newline
  if (data != null) {
    data = trim(data);      // Remove extra whitespace
    try {
      float value = Float.parseFloat(data); // Convert to a number
      output.println(value); // Record the value to the file
      output.flush();        // Ensure data is saved immediately
      
      // Add the value to the chart data array
      for (int i = 0; i < dataPoints.length - 1; i++) {
        dataPoints[i] = dataPoints[i + 1]; // Shift data points left
      }
      dataPoints[dataPoints.length - 1] = value; // Add new value to the end
    } catch (NumberFormatException e) {
      println("Invalid data: " + data); // Handle non-numeric data
    }
  }
}

void keyPressed() {
  if (key == 'q' || key == 'Q') {
    output.close(); // Close the file when 'q' is pressed
    exit();         // Exit the program
  }
}

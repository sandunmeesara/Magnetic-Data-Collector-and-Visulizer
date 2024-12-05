#define run_speed 100
#define turn_speed 100

// Pin definitions
const int leftEncoderPin = 2;    // Left encoder sensor
const int rightEncoderPin = 3;   // Right encoder sensor
const int motorLeftForward = 4;  // Left motor forward pin
const int motorLeftBackward = 5; // Left motor backward pin
const int motorRightForward = 6; // Right motor forward pin
const int motorRightBackward = 7;// Right motor backward pin
const int EN_A = 9;  // PWM pin for left motor
const int EN_B = 10; // PWM pin for right motor

volatile unsigned long leftPulseCount = 0;
volatile unsigned long rightPulseCount = 0;

float wheelDiameter = 0.065;    // Wheel diameter in meters (adjust for your robot)
int pulsesPerRevolution = 20;   // Adjust based on encoder specs
float totalDistance = 0.0;      // Accumulated distance in meters
bool movingForward = false;
bool movingBackward = false;

void setup() {
  Serial.begin(9600);  // Serial communication with ESP32
  pinMode(leftEncoderPin, INPUT_PULLUP);
  pinMode(rightEncoderPin, INPUT_PULLUP);
  
  attachInterrupt(digitalPinToInterrupt(leftEncoderPin), leftPulseISR, RISING);
  attachInterrupt(digitalPinToInterrupt(rightEncoderPin), rightPulseISR, RISING);

  pinMode(motorLeftForward, OUTPUT);
  pinMode(motorLeftBackward, OUTPUT);
  pinMode(motorRightForward, OUTPUT);
  pinMode(motorRightBackward, OUTPUT);
  pinMode(EN_A, OUTPUT);
  pinMode(EN_B, OUTPUT);

  Serial.println("Robot Ready");
}

void loop() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command == "1") { //FORWARD
      moveForward();
    } else if (command == "2") { //REVERSE
      moveBackward();
    } else if (command == "3") { //STOP
      stopMotors();
    } else if (command == "4") { //TURN_LEFT
      turnLeft();
    } else if (command == "5") { //TURN_RIGHT
      turnRight();
    }
  }

  //Serial.println("Test!");
  
  // Calculate and accumulate traveled distance when moving forward or backward
  if (movingForward || movingBackward) {
    float distanceLeft = (leftPulseCount * PI * wheelDiameter) / pulsesPerRevolution;
    float distanceRight = (rightPulseCount * PI * wheelDiameter) / pulsesPerRevolution;
    float averageDistance = (distanceLeft + distanceRight) / 2;
    totalDistance += averageDistance;

    leftPulseCount = 0;  // Reset pulse counts after calculation
    rightPulseCount = 0;

    Serial.print("Total Distance: ");
    Serial.print(totalDistance, 2);  // Display in meters
    Serial.println(" meters");
  }

  delay(1000);  // Update distance every second
}

void moveForward() {
  movingForward = true;
  movingBackward = false;
  leftPulseCount = 0;
  rightPulseCount = 0;

  digitalWrite(motorLeftForward, HIGH);
  digitalWrite(motorLeftBackward, LOW);
  digitalWrite(motorRightForward, HIGH);
  digitalWrite(motorRightBackward, LOW);
  analogWrite(EN_A, run_speed);
  analogWrite(EN_B, run_speed);
}

void moveBackward() {
  movingBackward = true;
  movingForward = false;
  leftPulseCount = 0;
  rightPulseCount = 0;

  digitalWrite(motorLeftForward, LOW);
  digitalWrite(motorLeftBackward, HIGH);
  digitalWrite(motorRightForward, LOW);
  digitalWrite(motorRightBackward, HIGH);
  analogWrite(EN_A, run_speed);
  analogWrite(EN_B, run_speed);
}

void stopMotors() {
  movingForward = false;
  movingBackward = false;

  digitalWrite(motorLeftForward, LOW);
  digitalWrite(motorLeftBackward, LOW);
  digitalWrite(motorRightForward, LOW);
  digitalWrite(motorRightBackward, LOW);
  analogWrite(EN_A, 0);
  analogWrite(EN_B, 0);
}

void turnLeft() {
  movingForward = false;
  movingBackward = false;

  digitalWrite(motorLeftForward, LOW);
  digitalWrite(motorLeftBackward, HIGH);
  digitalWrite(motorRightForward, HIGH);
  digitalWrite(motorRightBackward, LOW);
  analogWrite(EN_A, turn_speed);
  analogWrite(EN_B, turn_speed);

  //delay(100);  // Adjust time for a suitable turn duration
  //stopMotors();
}

void turnRight() {
  movingForward = false;
  movingBackward = false;

  digitalWrite(motorLeftForward, HIGH);
  digitalWrite(motorLeftBackward, LOW);
  digitalWrite(motorRightForward, LOW);
  digitalWrite(motorRightBackward, HIGH);
  analogWrite(EN_A, turn_speed);
  analogWrite(EN_B, turn_speed);

  //delay(100);  // Adjust time for a suitable turn duration
  //stopMotors();
}

void leftPulseISR() {
  if (movingForward || movingBackward) {
    leftPulseCount++;
  }
}

void rightPulseISR() {
  if (movingForward || movingBackward) {
    rightPulseCount++;
  }
}

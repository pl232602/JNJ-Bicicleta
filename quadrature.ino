// Define pins for encoder
const int encoderPinA = 2;
const int encoderPinB = 3;

volatile long encoderValue = 0;
volatile int lastEncoded = 0;
volatile long lastencoderValue = 0;

void setup() {
  Serial.begin(9600);
  
  // Set encoder pins as inputs
  pinMode(encoderPinA, INPUT_PULLUP);
  pinMode(encoderPinB, INPUT_PULLUP);
  
  // Attach interrupt handlers
  attachInterrupt(digitalPinToInterrupt(encoderPinA), updateEncoder, CHANGE);
  attachInterrupt(digitalPinToInterrupt(encoderPinB), updateEncoder, CHANGE);
}

void loop() {
  // Read encoder value
  long currEncoderValue;
  noInterrupts();
  currEncoderValue = encoderValue;
  interrupts();
  
  // Send encoder value over serial
  Serial.print("enca");
  Serial.println(currEncoderValue);
  
  delay(100); // Adjust delay according to your requirements
}

void updateEncoder() {
  int MSB = digitalRead(encoderPinA); //MSB = most significant bit
  int LSB = digitalRead(encoderPinB); //LSB = least significant bit

  int encoded = (MSB << 1) | LSB; //converting the 2 pin value to single number
  int sum  = (lastEncoded << 2) | encoded; //adding it to the previous encoded value

  if(sum == 0b1101 || sum == 0b0100 || sum == 0b0010 || sum == 0b1011) encoderValue++;
  if(sum == 0b1110 || sum == 0b0111 || sum == 0b0001 || sum == 0b1000) encoderValue--;

  lastEncoded = encoded; //store this value for next time
}

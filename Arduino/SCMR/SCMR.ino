long irLeftDistance = 0;  // variable to store the value coming from the sensor
long irMiddleDistance = 0;  // variable to store the value coming from the sensor
long irRightDistance = 0;  // variable to store the value coming from the sensor

int irLeftPin = A0;
int irMiddlePin = A1;
int irRightPin = A2;

int counter = 0;

void setup() 
{
  Serial.begin(9600);
}

void loop() 
{
  irLeftDistance = ((irLeftDistance * 95) + ((long)analogRead(irLeftPin) * 5))/100;
  irMiddleDistance = ((irMiddleDistance * 95) + ((long)analogRead(irMiddlePin) * 5))/100;
  irRightDistance = ((irRightDistance * 95) + ((long)analogRead(irRightPin) * 5))/100;

  if(counter++ > 100)
  {
    Serial.println(irLeftDistance);
    Serial.println(irMiddleDistance);
    Serial.println(irRightDistance);
    Serial.println();
    counter = 0;
  }
  delay(10);
}

void setupStepperMotors()
{
  TCCR0A = 0b11000010; 
  TCCR0B = 0b00000100;
  OCR0A = 128;
}

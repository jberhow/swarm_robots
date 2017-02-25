long irLeftDistance = 0;  // variable to store the value coming from the sensor
long irMiddleDistance = 0;  // variable to store the value coming from the sensor
long irRightDistance = 0;  // variable to store the value coming from the sensor

#define IR_LEFT_PIN     8
#define IR_MIDDLE_PIN   9
#define IR_RIGHT_PIN    10

int counter = 0;

char serialData[128];
char serialDataPointer;

uint16_t currentRotation;
uint16_t requiredRotation;
uint8_t robotSpeed;
uint8_t currentRobotSpeed;
int16_t rotationalDifference;

#define DIRECTION_DATA_START_BYTE  'D'

#define SERIAL_DATA_END_BYTE    'E'

#define TRUE 1
#define FALSE 0

uint8_t enableMotorsFlag;

#define LEFT_MOTOR_PWM 2
#define LEFT_MOTOR_DIR 5
#define RIGHT_MOTOR_PWM 4
#define RIGHT_MOTOR_DIR 7
#define ENABLE_PIN 8

void setup() 
{
  Serial.begin(9600);

  setupStepperMotors();
}

void loop() 
{
  rotationalDifference = currentRotation - requiredRotation;
   
  if(rotationalDifference > 5 and rotationalDifference < 180)
      rotateRight();
  else if(rotationalDifference > 5 and rotationalDifference >= 180)
      rotateLeft();
  else if(rotationalDifference < -5 and rotationalDifference > -180)
      rotateLeft();
  else if(rotationalDifference < -5 and rotationalDifference <= -180)
      rotateRight();
  else
      setMotorsForward();

  if(currentRobotSpeed != robotSpeed)
  { 
    OCR0A = robotSpeed;
    OCR0B = robotSpeed/2;
    OCR3A = robotSpeed;
    OCR3B = robotSpeed/2;

    if(currentRobotSpeed == 0)
    {
      enableMotors();
    }
    if(robotSpeed == 0)
    {
      disableMotors();
    }
    
    currentRobotSpeed = robotSpeed;
    TCNT0 = 0;
    TCNT3 = 0;
  }
  
  irLeftDistance = ((irLeftDistance * 99) + ((long)analogRead(IR_LEFT_PIN)) * 1)/100;
  irMiddleDistance = ((irMiddleDistance * 99) + ((long)analogRead(IR_MIDDLE_PIN)) * 1)/100;
  irRightDistance = ((irRightDistance * 99) + ((long)analogRead(IR_RIGHT_PIN)) * 1)/100;

  if(irMiddleDistance > 180)
  {
    if(irLeftDistance > 180)
    {
      rotateRight();
      delay(1000);
      setMotorsForward();
    }
    else if(irRightDistance > 180)
    {
      rotateLeft();
      delay(1000);
      setMotorsForward();
    }
    else
    {
      rotateLeft();
      delay(3000);
      setMotorsForward();
    }
  }
  else if(irLeftDistance > 230)
  {
    rotateRight();
    delay(1000);
    setMotorsForward();
  }
  else if(irRightDistance > 230)
  {
    rotateLeft();
    delay(1000);
    setMotorsForward();
  }
}

void setupStepperMotors()
{
  //Set step pins as outputs
  pinMode(LEFT_MOTOR_PWM, OUTPUT);
  pinMode(RIGHT_MOTOR_PWM, OUTPUT);

  //Set direction pins as outputs
  pinMode(LEFT_MOTOR_DIR, OUTPUT);
  pinMode(RIGHT_MOTOR_DIR, OUTPUT);

  //Set enable pin as output
  pinMode(ENABLE_PIN, OUTPUT);
  digitalWrite(ENABLE_PIN, HIGH);

  //Set direction forward
  digitalWrite(LEFT_MOTOR_DIR, LOW);
  digitalWrite(RIGHT_MOTOR_DIR, HIGH);

   //Z Step
  TCCR0A = (1 << COM0B1) | (1 << WGM01) | (1 << WGM00);
  TCCR0B = (1 << WGM02) | (1 << CS02) | (1 << CS00);
  OCR0A = 100;
  OCR0B = 50;

  //X Step
  TCCR3A = (1 << COM3B1) | (1 << WGM31) | (1 << WGM30);
  TCCR3B = (1 << WGM33) | (1 << WGM32) | (1 << CS32) | (1 << CS30);
  OCR3A = 100;
  OCR3B = 50;

  TCNT0 = 0;
  TCNT3 = 0;

  currentRobotSpeed = 0;

  enableMotors();
}

void enableMotors()
{
  digitalWrite(ENABLE_PIN, LOW);
}

void disableMotors()
{
  digitalWrite(ENABLE_PIN, HIGH);
}

void setMotorsForward()
{
  //Set directions forward
  digitalWrite(LEFT_MOTOR_DIR, LOW);
  digitalWrite(RIGHT_MOTOR_DIR, HIGH);
}

void rotateLeft()
{
  //Set directions forward
  digitalWrite(LEFT_MOTOR_DIR, HIGH);
  digitalWrite(RIGHT_MOTOR_DIR, HIGH);
}

void rotateRight()
{
  //Set directions forward
  digitalWrite(LEFT_MOTOR_DIR, LOW);
  digitalWrite(RIGHT_MOTOR_DIR, LOW);
}

/*
  SerialEvent occurs whenever a new data comes in the
 hardware serial RX.  This routine is run between each
 time loop() runs, so using delay inside loop can delay
 response.  Multiple bytes of data may be available.
 */
void serialEvent() 
{
  while (Serial.available())
  {
    char data = (char)Serial.read();

    Serial.println(data);

    //React to data type
    switch(data)
    {
      //Start bytes clear the buffer
      case DIRECTION_DATA_START_BYTE:
        Serial.println("1");
        serialDataPointer = 1;
        serialData[0] = DIRECTION_DATA_START_BYTE;
        break;
 
      //End bytes perform an action on the received data
      case SERIAL_DATA_END_BYTE:
        Serial.println("2");
        Serial.println(serialData[0]);
        switch(serialData[0])
        {
          case DIRECTION_DATA_START_BYTE:
            Serial.println("3");
            currentRotation = ((uint16_t)serialData[1] << 8) + ((uint16_t) serialData[2]);
            requiredRotation = ((uint16_t)serialData[3] << 8) + ((uint16_t) serialData[4]);
            robotSpeed = serialData[5];
            Serial.println(robotSpeed);
            break;

          default:
            serialDataPointer = 0;
            break;
        }
        break;

      //Default store data to buffer
      default:
        if(serialDataPointer < 128)
          serialData[serialDataPointer] = data;
          serialDataPointer++;
        break;
    }
    
  }
}

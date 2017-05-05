#include "TimerOne.h"
#include "Adafruit_HMC5883_U.h"

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

volatile uint8_t rotationDelay;
volatile uint8_t irRotation;

#define LEFT_MOTOR_PWM 2
#define LEFT_MOTOR_DIR 5
#define RIGHT_MOTOR_PWM 4
#define RIGHT_MOTOR_DIR 7
#define ENABLE_PIN 8

/* Assign a unique ID to this sensor at the same time */
//Adafruit_HMC5883_Unified mag = Adafruit_HMC5883_Unified(12345);

void setup() 
{
  Serial.begin(115200);

  setupStepperMotors();
  //mag.begin();

  Timer1.initialize(500000);
  Timer1.attachInterrupt(halfSecondTimer);
  rotationDelay = 0;
  robotSpeed = 0;
  currentRobotSpeed = 0;
  irRotation = FALSE;
}

void loop() 
{
  /* Get a new sensor event */ 
  //sensors_event_t event; 
  //mag.getEvent(&event);
 
  /* Display the results (magnetic vector values are in micro-Tesla (uT)) 
  Serial.print("X: "); Serial.print(event.magnetic.x); Serial.print("  ");
  Serial.print("Y: "); Serial.print(event.magnetic.y); Serial.print("  ");
  Serial.print("Z: "); Serial.print(event.magnetic.z); Serial.print("  ");Serial.println("uT");*/

  // Hold the module so that Z is pointing 'up' and you can measure the heading with x&y
  // Calculate heading when the magnetometer is level, then correct for signs of axis.
  //float heading = atan2(event.magnetic.y, event.magnetic.x);
  
  // Once you have your heading, you must then add your 'Declination Angle', which is the 'Error' of the magnetic field in your location.
  // Find yours here: http://www.magnetic-declination.com/
  // If you cannot find your Declination, comment out these two lines, your compass will be slightly off.
  //float declinationAngle = 0.20;
  //heading += declinationAngle;
  
  // Correct for when signs are reversed. (2nd and 4th quadrant)
  //if(heading < 0)
  //  heading += 2*PI;
    
  // Check for wrap due to addition of declination.
  //if(heading > 2*PI)
  //  heading -= 2*PI;
   
  // Convert radians to degrees for readability.
  //currentRotation = (uint16_t) (heading * 180/M_PI);
  //if(currentRotation > 180)
  //{
  //  currentRotation = (currentRotation - 360);
  //}
  
  rotationalDifference = currentRotation - requiredRotation;

  if(irRotation == FALSE)
  {
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
  }

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
      rotationDelay = 2;
      irRotation = TRUE;
      TCNT1 = 0;
      /*delay(1000);
      setMotorsForward();*/
    }
    else if(irRightDistance > 180)
    {
      rotateLeft();
      rotationDelay = 2;
      irRotation = TRUE;
      TCNT1 = 0;
      /*delay(1000);
      setMotorsForward();*/
    }
    else
    {
      rotateLeft();
      rotationDelay = 6;
      irRotation = TRUE;
      TCNT1 = 0;
      /*delay(3000);
      setMotorsForward();*/
    }
  }
  else if(irLeftDistance > 230)
  {
    rotateRight();
    rotationDelay = 6;
    irRotation = TRUE;
    TCNT1 = 0;
    /*delay(1000);
    setMotorsForward();*/
  }
  else if(irRightDistance > 230)
  {
    rotateLeft();
    rotationDelay = 6;
    irRotation = TRUE;
    TCNT1 = 0;
    /*delay(1000);
    setMotorsForward();*/
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

  //enableMotors();
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

void halfSecondTimer()
{
  if(rotationDelay > 0)
  {
    rotationDelay--;
  }
  if(rotationDelay == 0 && irRotation == TRUE)
  {
    setMotorsForward();
    irRotation = FALSE;
  }
}

/*
  SerialEvent occurs whenever a new data comes in the
 hardware serial RX.  This routine is run between each
 time loop() runs, so using delay inside loop can delay
 response.  Multiple bytes of data may be available.
 */
void serialEvent() 
{
  char data;
  if(!Serial.available())
    return;
    
  do
  {
    data = (char)Serial.read();
    /*Serial.write(robotSpeed);
    Serial.write(currentRobotSpeed);
    Serial.write(currentRotation);
    Serial.write(requiredRotation);*/
  }while(data != DIRECTION_DATA_START_BYTE);

  serialDataPointer = 1;
  serialData[0] = DIRECTION_DATA_START_BYTE;
  
  while (data != SERIAL_DATA_END_BYTE)
  {
    while(!Serial.available())
    {}
    data = (char)Serial.read();
    
    //React to data type
    switch(data)
    {
      //Start bytes clear the buffer
      case DIRECTION_DATA_START_BYTE:
        serialDataPointer = 1;
        serialData[0] = DIRECTION_DATA_START_BYTE;
        break;
 
      //End bytes perform an action on the received data
      case SERIAL_DATA_END_BYTE:
        switch(serialData[0])
        {
          case DIRECTION_DATA_START_BYTE:
            currentRotation = ((uint16_t)serialData[1] << 8) + ((uint16_t) serialData[2]);
            requiredRotation = ((uint16_t)serialData[3] << 8) + ((uint16_t) serialData[4]);
            robotSpeed = serialData[5];
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

  /*while (Serial.available())
  {
    Serial.read();
  }*/
}

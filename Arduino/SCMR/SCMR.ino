long irLeftDistance = 0;  // variable to store the value coming from the sensor
long irMiddleDistance = 0;  // variable to store the value coming from the sensor
long irRightDistance = 0;  // variable to store the value coming from the sensor

int irLeftPin = A0;
int irMiddlePin = A1;
int irRightPin = A2;

int counter = 0;

char serialData[128];
char serialDataPointer;

uint8_t rotationAmountDegrees;
uint8_t forwardAmount;
int8_t robotSpeed;

#define DIRECTION_DATA_START_BYTE  0xAA

#define SERIAL_DATA_END_BYTE    0xEE

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
  //Serial.begin(9600);

  setupStepperMotors();
}

void loop() 
{ 
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
  digitalWrite(LEFT_MOTOR_PWM, LOW);
  digitalWrite(RIGHT_MOTOR_PWM, HIGH);
}

void rotateLeft()
{
  
}

void rotateRight()
{

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

    //React to data type
    switch(data)
    {
      //Start bytes clear the buffer
      case DIRECTION_DATA_START_BYTE:
        serialDataPointer = 0;
        serialData[0] = DIRECTION_DATA_START_BYTE;
        break;
 
      //End bytes perform an action on the received data
      case SERIAL_DATA_END_BYTE:
        switch(serialData[0])
        {
          case DIRECTION_DATA_START_BYTE:
            rotationAmountDegrees = serialData[1];
            forwardAmount = serialData[2];
            robotSpeed = serialData[3];
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
        break;
    }
    
  }
}

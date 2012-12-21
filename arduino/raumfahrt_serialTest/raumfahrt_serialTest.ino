

/*-------Raumfahrt Angle Tester---------------------------------------------------

Maultashcen Modulator M6 to Ground Control



Serial Interrupt Code from http://arduino.cc/forum/index.php/topic,45076.0.html
*/

// Global variables needed

// to the pins used:
const int analogInPin = A0;  // Analog input pin that the potentiometer is attached to
const int analogOutPin = 9; // Analog output pin that the LED is attached to

int sensorValue = 0;        // value read from the pot
int outputValue = 0;        // value output to the PWM (analog out)
long int timeOrig;
long int timeNow;
long int timeSpent;

bool runMode;

// Sets the bed turning once the 'S' command is received from the python machine
const float motorTestVoltage = 4.5; // must be in the 0-5V range (below 2.5 turns it in other direction)

void setup() {
  // initialize serial communications at 9600 bps:
  Serial.begin(9600); 
   timeOrig = millis();
   runMode = false;
}

void loop() {
  if(!runMode)
  {
    char temp;
    while(Serial.available())
    {
      temp = Serial.read();
    }
    if(temp == 'S')
    {
      runMode = true;
      analogWrite(analogOutPin,motorTestVoltage* 51);
      //Serial.println("motorTestVoltage: ");
      //Serial.println(motorTestVoltage* 51);
    }
  }
  else
  {
  
    // read the sensor value:
    sensorValue = analogRead(analogInPin);            
    // leave the following lines commented for now
    //timeNow = millis();
    //timeSpent = timeNow - timeOrig;
  
    //Serial.print(timeSpent);
    //Serial.print(",");
    Serial.println(sensorValue);      

  // wait 2 milliseconds before the next loop
  // for the analog-to-digital converter to settle
  // after the last reading:
    delay(2);    
  }    
}


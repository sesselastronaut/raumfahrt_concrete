/*-------Raumfahrt Concrete---------------------------------------------------
Ground control to modelito-6

Serial Interrupt Code from http://arduino.cc/forum/index.php/topic,45076.0.html
decrease Kp
increase Ki 
*/

const int analogInPin = A0;
const int analogOutPin = 9;
float theta_current; 
float theta_desired;
float error = 0;
float error_Dot = 0;
float error_previous = 0;
float error_total;
const float Kd = 0.15;//3.5
const float Kp = 0.2;
const float Ki = 0; //0.001;
float analogVoltage; 
int digitalVoltage;// value output to the PWM (voltage out)
float corrected_analogVoltage;
char inputString [10];         // incoming serial byte
char inputNum[5];
float valueReceived;

// Volatile, since it is modified in an ISR.
volatile boolean inService;
boolean activeControlOn;

int loop_ctr;

int sensor_window[10];

boolean firstTime;

void setup() {
  Serial.begin(9600);
  pinMode(2, INPUT);
  digitalWrite(2, LOW);
  //attachInterrupt(0, serialInterrupt, CHANGE);
  // Used to signal that main loop is alive.
  pinMode(4, OUTPUT);
  digitalWrite(4, LOW);

  inService = true;
  activeControlOn = false;
  // Used to signal that Serial input was read.
  pinMode(5, OUTPUT);
  digitalWrite(5, LOW);
  analogVoltage = 0;
  digitalVoltage = 0;
  error_total = 0;
  firstTime=true;
}



void serialInterrupt()
{
  // Trick: since Serial I/O in interrupt driven, we must reenable interrupts while in this Interrupt Service Routine.
  // But doing so will cause the routine to be called nestedly, causing problems.
  // So we mark we are already in service.

  // Already in service? Do nothing.
  if (inService) return;

  // You was not in service. Now you are.
  inService = true;
  
  // Reenable interrupts, to allow Serial to work. We do this only if inService is false.
  interrupts();
  
  if (Serial.available() > 0) {
    // get incoming byte:
     Serial.readBytes(inputString,5);
     Serial.print("Received :");
     Serial.print(inputString);
     int i = 1;
    for (i==1;i<6;i++)
    {
      inputNum[i-1] = inputString[i];
    }
    valueReceived = (float)atoi(inputNum)/10; 
    // send sensor values:
    /*
    Serial.print(", Instruction : ");
    Serial.print(inputString[0]);
    Serial.print(" , Value :");
    Serial.println(valueReceived);
    */
    theta_desired = valueReceived;
 }   
  // Job done.
  inService = false;
  activeControlOn = true;
}


void ground_control(float theta_current)
{
      if(firstTime  == true)
    {
      theta_desired = theta_current;
      //buf[0] = theta_desired;
      Serial.println("reset");
      attachInterrupt(0, serialInterrupt, CHANGE);
      firstTime = false;
      inService = false;
    }
    else if (activeControlOn == true){
      if(theta_desired > 360){
        
//protecting for sensible values
        
        theta_desired = 360; 
      }
      else if (theta_desired < 0){
            theta_desired = 0;
      }
      activeControlOn = false;
    }
    /*else {
      theta_desired = theta_current;
    }*/
    int negator = -1; // this assumes motor positive voltage goes in clockwise otherwise error direction is wrong
    error = negator*(theta_desired - theta_current);
    error_total = error_total + error;
    
     
    if (error < -180) {
      error = error + 360;
    }
    
    
    error_Dot = (error_previous - error);
    if (error == 0 && error_Dot == 0 && error_total == 0){
      activeControlOn = false;
    }
    analogVoltage = (Kp * error) + (Kd*error_Dot)/10 +  (Ki*error_total); // Kd * error_Dot;
    corrected_analogVoltage = analogVoltage + 2.5;
    if (corrected_analogVoltage > 5){
      corrected_analogVoltage = 5;
    }
    else if (corrected_analogVoltage < 0){
      corrected_analogVoltage = 0;
    }
    digitalVoltage = corrected_analogVoltage * 51; 
    analogWrite(analogOutPin, digitalVoltage);
    
  //  Serial.print("desired = "); //coming from python through serial number between 0 and 360°
 //   Serial.print(buf[0]);   
    Serial.print("theta_desired = ");
    Serial.print(theta_desired);
    Serial.print(" | theta_current = ");      
    Serial.print(theta_current);
    Serial.print(" | error = ");
    Serial.print(error);
    Serial.print(" | error_previous = ");
    Serial.print(error_previous);
    Serial.print(" | error_Dot = ");
    Serial.print(error_Dot);
    Serial.print(" | error_Total = ");
    Serial.print(error_total);
    Serial.print(" | analogVoltage = ");
    Serial.println(analogVoltage);
   
    error_previous = error;
}


 
void loop(){
  
// see what value is coming in

// btween 0 to 1023
   
    int adc_current = analogRead(analogInPin); 
    
//calculate the current position in angle degrees
    
  sensor_window[loop_ctr] = adc_current * 0.3519;  
  
  loop_ctr = loop_ctr + 1;

  if(loop_ctr == 9) {
  loop_ctr = 0;  
  theta_current = 0.0;
  for( int i = 0; i<10; i++) {
      theta_current = theta_current + sensor_window[i];
    }
    theta_current = theta_current/10;
    ground_control(theta_current);
  }
  delay(10);
    
}



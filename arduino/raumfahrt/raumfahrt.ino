/*-------Raumfahrt Concrete---------------------------------------------------
Ground control to modelito-6

Serial Interrupt Code from http://arduino.cc/forum/index.php/topic,45076.0.html
decrease Kp
increase Ki 
*/


/*

Python Comm Protocol:
's9999'
s - character representing command

 'c' - current angle
 't' - target angle
 'r' - current reference
 'm' - reset display mode

stands for
9999 - value

*/


const int analogIn1Pin = A0;
const int analogIn2Pin = A1;
 
const int analogOutPin = 9;
const int resetNorthAnalogPin = A5;



int adc_current;
float theta_m1;
float theta_m2;

float theta_current; 
float theta_desired;
float theta_sensor;
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
float northAnalogVal;
float northReferenceAngle;
int adc_previous;
int negator = -1; // this assumes motor positive voltage goes in clockwise otherwise error direction is wrong

//hardhack
/*
const float sensor_deadZoneMin = 354;
const float sensor_deadZoneMax = 360;
const float sensor_deadZoneMid = 357;
*/
int resetNorthVal;
int serialPrintMode = 2; 
// 1 - Continous printing for human readable output, 
// 2 - Python serialcom mode

boolean beginSerialSending = false;
char inputString [10];         // incoming serial byte
char inputNum[5];
float valueReceived;

// Volatile, since it is modified in an ISR.
volatile boolean inService;
boolean activeControlOn;

int loop_ctr;

int sensor_window[10];
int resetNorthSensor_window[10];

boolean firstTime;





int adc1;
int adc2;

float v1;
float v2;

float theta1;
float theta2;

float t;
float theta1p1;
float theta1p2;

float thetaOut;
const float oneByM1 = 36;
const float oneByM2 = -36;


void setup() {
  Serial.begin(9600);
  pinMode(2, INPUT);
  digitalWrite(2, LOW);
  
  // ResertNorthPin - obsolete
  //pinMode(resetNorthPin,INPUT);
  //digitalWrite(resetNorthPin,HIGH);
 
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
  negator = -1;
  beginSerialSending = false;
}

String sendFormat(char type, int data)
{
  String newData = String(int(data));
  int numZerosReqd = 4-newData.length();
  
  String sentString;
  switch(numZerosReqd)
  {
    case 0: sentString = String(type) + String(data); break;
    
    case 1: sentString = String(type) + String('0') + String(data);break;
    
    case 2: sentString = String(type) + String("00") + String(data);break;
    
    case 3: sentString = String(type) + String("000") + String(data);break;
        
    case 4: sentString = String(type) + String("0000");break;
  }
  return(sentString);
}



void sendStatusOnSerial()
{
  if( beginSerialSending )
  {
    Serial.println(sendFormat('c',int(10*theta_current)));
    Serial.println(sendFormat('t',int(10*theta_desired)));
    Serial.println(sendFormat('r',int(10*northReferenceAngle)));
  }
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
     
      if(serialPrintMode == 1) {
       Serial.print("Received :");
       Serial.print(inputString);
      }
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
    
    switch(inputString[0]){
      case 't': theta_desired = valueReceived; beginSerialSending = true; break;
     // case 'r': northReferenceAngle = valueReceived;  beginSerialSending = true;break;
      case 'p': serialPrintMode = 2; break;
      case 'h' : serialPrintMode = 1;break;
      default: break;
    }
    
    /*
    if(theta_desired - northReferenceAngle >= sensor_deadZoneMin  && theta_desired - northReferenceAngle <= sensor_deadZoneMax) {
      if(theta_desired - northReferenceAngle > sensor_deadZoneMid){
        theta_desired = sensor_deadZoneMax + northReferenceAngle;
      }
      else{*/
     //   theta_desired = theta_desired + northReferenceAngle; 
 //     }
  //  }

 }   
  // Job done.
  inService = false;
  activeControlOn = true;
}


void ground_control(float theta_current)
{


//    if (activeControlOn == true){
  /*
      if(theta_desired > 360){
        
//protecting for sensible values
        
        theta_desired = 360; 
      }
        else if (theta_desired < 0){
            theta_desired = 0;
      }*/
  //    activeControlOn = false;
   // }
    /*else {
      theta_desired = theta_current;
    }*/
    
    error = negator*(theta_desired - theta_current);
 //   error_total = error_total + error;
    
     
    if (error < -180) {
      error = error + 360;
    }
    
    if(error>180) {
      error = error-360;
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
    if(serialPrintMode == 1) {
      Serial.print("theta_sensor_dig=");
      Serial.print(adc1);/*
      Serial.print("theta_sensor=");
      Serial.print(theta_sensor);/*
      Serial.print(" | theta_m1=");
      Serial.print(theta_m1);
      Serial.print(" | theta_m2=");        
      Serial.print(theta_m2);*/
      Serial.print(" | theta_current = ");      
      Serial.print(theta_current);
      Serial.print(" | theta_desired = ");
      Serial.print(theta_desired);
      Serial.print(" | north_current_dig = ");      
      Serial.print(northAnalogVal);
      
      Serial.print(" | north_current = ");      
      Serial.print(northReferenceAngle);
      Serial.print(" | error = ");
      Serial.print(error);
      Serial.print(" | error_Dot = ");
      Serial.print(error_Dot);;
      Serial.print(" | analogVoltage = ");
      Serial.println(analogVoltage);
    }
    else
    {  
      sendStatusOnSerial();
    }   

   error_previous = error;
    
}
float computeBedAngle()
{
  
  
  static int adc1Past = 0;
  static int adc2Past = 0;

    adc1 = analogRead(analogIn1Pin);//0.6* (float)analogRead(analogIn1Pin) + 0.4*adc1Past; 
    adc2 = analogRead(analogIn2Pin);//0.6* (float)analogRead(analogIn2Pin) + 0.4*adc2Past; 
    
    
    v1 = 5*((0.6*(float)adc1 + 0.4*(float)adc1Past) /1023.0);
    v2 = 5*((0.6*(float)adc2 + 0.4*(float)adc2Past )/1023.0);
    adc1Past = adc1;
    adc2Past = adc2;
    
    
    /*
     if(serialPrintMode == 1) {
       
       
      Serial.print(" | V1 : ");
      Serial.print(v1);

      Serial.print(" | V2 : ");
      Serial.print(v2);
     }*/
    
/*
    if(v1<=2.5 && v2 <=2.5)
    {
      // Quadrant 1
      Serial.print(" | Quad : 1");
    //    theta1 = oneByM1*v1;
     //   theta2 = oneByM2*(v2 - 2.5);        

    }
    else if (v1>2.5 && v2<=2.5)
    {
      // Quadrant 2
       Serial.print(" | Quad : 2");
    //    theta1 = 90.0 + oneByM1*(v1-2.5);
     //   theta2 = 90.0 + oneByM1*v2;
    }
    else if (v1>2.5 && v2>2.5)
    {
       // Quadrant 3
      Serial.print(" | Quad : 3");
     //   theta1 =180.0 + oneByM2*(v1 - 5.0);
      //  theta2 =180.0 + oneByM1*(v2 - 2.5);
    }
    else if (v1<=2.5 && v2>2.5)
    {
       // Quadrant 4
      Serial.print(" | Quad : 4");
      //  theta1 = 270 + oneByM2*(v1 - 2.5);
      //  theta2 = 270 + oneByM2*(v2 - 5.0);
    }
    */
    
      
    theta1p1 = (v1/5.0) * 180.0;
    theta1p2 = 180.0 + ((5.0-v1)/5.0)*180.0;
  /*
   if(serialPrintMode == 1) {
      Serial.print(" | theta1p1 :");
      Serial.print(theta1p1);
      Serial.print(" | theta1p2 :");
      Serial.print(theta1p2);

      Serial.print(" | Choice : ");
   }*/
    if(v2 < 2.54)
    {
      /*
       if(serialPrintMode == 1) {
        Serial.print("1 : ");
        Serial.println(theta1p1);
       }*/
        
        thetaOut = theta1p1;
    }
    else
    {
      /*
       if(serialPrintMode == 1) {
        Serial.print("2 : ");
        Serial.println(theta1p2);
       }*/
        thetaOut = theta1p2;
    }  

/*
    Serial.print(" | diff:");
    Serial.print(theta1-theta2);;
    Serial.print(" | avg:");
    Serial.println(thetaAvg);
  */  
    return(thetaOut);
    
}
 
void loop(){
  
     if(firstTime  == true)
    {
      //theta_desired = theta_current;
      //buf[0] = theta_desired;
      analogWrite(analogOutPin, 2.5*51);
      if(serialPrintMode == 1) {
        Serial.println("reset");
      }
      attachInterrupt(0, serialInterrupt, CHANGE);
      firstTime = false;
      inService = false;
      delay(1);
    }
   
  
// see what value is coming in

// btween 0 to 1023
  
  adc_previous = adc_current; 
  adc_current = computeBedAngle();
  
  
    
//calculate the current position in angle degrees
    
/*
  if(adc_previous - adc_current >10 || adc_current - adc_previous > 10)
  {
  //sensor_window[loop_ctr] = adc_current * 0.3519;  
  sensor_window[loop_ctr]= theta_m2;
  }
  else
  {
    sensor_window[loop_ctr] = theta_m1;
  }
  */
  sensor_window[loop_ctr] = adc_current;
  int northResetIn = analogRead(resetNorthAnalogPin);
  

  resetNorthSensor_window[loop_ctr] =   map(northResetIn, 0, 1023, 0, 1023);  ;
      
  loop_ctr = loop_ctr + 1;

    if(loop_ctr>9) {
      //Serial.print(loop_ctr);
    loop_ctr = 0;  
    theta_sensor = 0.0;
    northAnalogVal = 0.0;
      for( int i = 0; i<10; i++) {
        theta_sensor = theta_sensor + (float)sensor_window[i];
        northAnalogVal = northAnalogVal + (float)resetNorthSensor_window[i];
      }
      
      
      theta_sensor =  (theta_sensor/10.0);
      northAnalogVal = (northAnalogVal/10.0);
      
      /*
      Serial.print("| theta_sensor : ");
      Serial.print(theta_sensor);
      Serial.print("| northAnalogVal : ");
      Serial.println(northAnalogVal);      
*/       /*    
      resetNorthVal = digitalRead(resetNorthPin);*/
      northReferenceAngle = northAnalogVal * (0.35191); //value *(360*5)/1024

      //if(resetNorthVal == 0)
      //{
        
       theta_current = theta_sensor - northReferenceAngle;
       if(theta_current<0){
         theta_current = theta_current+360;
       }
       else if(theta_current>=360){
          theta_current = theta_current-360;
       }
        
        ground_control(theta_current);
        delay(10);
      /*} 
      else{ 
        digitalVoltage = 5;
        northReferenceAngle = theta_current;
        analogWrite(analogOutPin, digitalVoltage*51);
    
        if(serialPrintMode == 1) {
         Serial.print(" ResetingNorthMode | ");
         Serial.print(" NewNorthAngle = ");
         Serial.println(theta_current);
        }
        else
        {
          sendStatusOnSerial();
        }
      */
      
  }
}



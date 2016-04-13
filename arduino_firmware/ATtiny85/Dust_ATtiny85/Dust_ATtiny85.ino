//* Dust sensor reader
// *   Based on "Dusty's" code for SHARP's dust sensor
// *   Timing constants optimised (manually) for use with\
//     an ATtiny85 @8MHz with internal clock
//Dust Sensor constants and variables
int dustIN=1;  //Analog input Pin1 on ATtiny85
long int dust;  //Dust voltage
int dustTRIG=3;  //Trigger pin for Dust sensor 
int delay_tosample=280; //Microseconds after the trigger
int dustOUT=0; //PWM out for analog out of averaged signal
int Nsamples=200;
void setup(){
  pinMode(dustTRIG,OUTPUT);
  pinMode(dustOUT,OUTPUT);
  pinMode(4,OUTPUT);
  analogWrite(dustOUT,0); //Bring the output to ground
}
void loop(){
  dust=0;
  for (int i=0;i<Nsamples;i++){
    digitalWrite(dustTRIG,LOW);
    delayMicroseconds(delay_tosample);
    dust=dust+analogRead(dustIN);
    digitalWrite(dustTRIG,HIGH);
    delayMicroseconds(9500);
  }
  analogWrite(dustOUT,dust/Nsamples);
}

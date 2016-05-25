/* Dusty Air Corner sensor hub
 20160525
	- PMS3003 as Dust sensor 
	- No motion sensor
	- Distance with HC-SR04
	- CO2 with DFRobot unit
	- Timing controlled by Real Time Clock
	- No data saving ... moved to host PC to log
	- Time managed by Chronodot using Chronodot library by Stephanieplanet
	- Temperature from LM36
	- T&RH from DHT22
*/
//Add Libraries to work with the Real Time Clock
#include <RTClib.h>
#include <RTC_DS3231.h>
#include <Wire.h>
#define CLOCK_ADDRESS 0x68 // HW address for the RTC
//Add DHT library
#include <DHT.h>
#define DHT22_PIN 7 // Pin where the DHT22 is connected
//Ultrasonic range finder
#include <NewPing.h>
#define TRIGGER_PIN 5
#define ECHO_PIN 6
#define MAX_DISTANCE 100
//PMS3003 definitions
#define receiveDatIndex 32 // Sensor data payload size
//Analog channels definitions
#define TempPin 2
#define CO2Pin 0

//Variable declarations
byte receiveDat[receiveDatIndex]; //receive data from the air detector module
byte readbuffer[64];
unsigned int checkSum,checkresult;
unsigned int FrameLength,Data4,Data5,Data6;
unsigned int PM1,PM25,PM10,N300,N500,N1000,N2500,N5000,N10000;
unsigned int timer1,timer0;
int Temp,CO2;
boolean valid_data;
RTC_DS3231 RTC;
DateTime time;
dht DHT;
NewPing sonar(TRIGGER_PIN,ECHO_PIN,MAX_DISTANCE);
//Distance variable 
unsigned int Distance; //Distance
//CO2 variable
unsigned int CO2; //CO2 signal

boolean readDust(){
	while (Serial.peek()!=66){
		receiveDat[0]=Serial.read();
	}
	Serial.readBytes((char *)receiveDat,receiveDatIndex);
	checkSum = 0;
	for (int i = 0;i < receiveDatIndex;i++){
		checkSum = checkSum + receiveDat[i];
	}
	checkresult = receiveDat[receiveDatIndex-2]*256+receiveDat[receiveDatIndex-1]+receiveDat[receiveDatIndex-2]+receiveDat[receiveDatIndex-1];
	valid_data = (checkSum == checkresult);
	return valid_data;
}

int GetTemperature() {
	int dump = analogRead(TempPin);
	delay(10);
	dump = analogRead(TempPin);
	return dump;
}
int GetCO2() {
	int dump = analogRead(CO2Pin);
	delay(10);
	dump = analogRead(CO2Pin);
	return dump;
}
void SendData(DateTime xtime) {
	Serial.print(xtime.year());
	Serial.print("\t");
	Serial.print(xtime.month());
	Serial.print("\t");
	Serial.print(xtime.day());
	Serial.print("\t");
	Serial.print(xtime.hour());
	Serial.print("\t");
	Serial.print(xtime.minute());
	Serial.print("\t");
	Serial.print(xtime.second());
	Serial.print("\t");
	//Dust from Dust sensor
	while (!GetDust()){
		delay(10);
	}
	PM1 = (receiveDat[4]*256)+receiveDat[5];
	Serial.print(PM1);
	Serial.print("\t");
	PM25 = (receiveDat[6]*256)+receiveDat[7];
	Serial.print(PM25);
	Serial.print("\t");
	PM10 = (receiveDat[8]*256)+receiveDat[9];
	Serial.print(PM10);
	Serial.print("\t");
	Data4 = (receiveDat[10]*256)+receiveDat[11];
	Serial.print(Data4);
	Serial.print("\t");
	Data5 = (receiveDat[12]*256)+receiveDat[13];
	Serial.print(Data5);
	Serial.print("\t");
	Data6 = (receiveDat[14]*256)+receiveDat[15];
	Serial.print(Data6);
	Serial.print("\t");
	N300 = (receiveDat[16]*256)+receiveDat[17];
	Serial.print(N300);
	Serial.print("\t");
	N500 = (receiveDat[18]*256)+receiveDat[19];
	Serial.print(N500);
	Serial.print("\t");
	N1000 = (receiveDat[20]*256)+receiveDat[21];
	Serial.print(N1000);
	Serial.print("\t");
	N2500 = (receiveDat[22]*256)+receiveDat[23];
	Serial.print(N2500);
	Serial.print("\t");
	N5000 = (receiveDat[24]*256)+receiveDat[25];
	Serial.print(N5000);
	Serial.print("\t");
	N10000 = (receiveDat[26]*256)+receiveDat[27];
	Serial.print(N10000);
	Serial.print("\t");
	//Distance from Range Finder
	Distance=GetDistance();
	Serial.print(Distance);
	Serial.print("\t");
	//Serial.println("Distance Done");
	//Temperature from analog
	Temp=GetTemperature();
	Serial.print(Temp);
	Serial.print("\t");
	//Temperature and RH from DHT22
	Serial.print(DHT.temperature);
	Serial.print("\t");
	Serial.print(DHT.humidity);
	Serial.print("\t");
	//CO2 from analog
	CO2=GetCO2();
	Serial.println(CO2);
}

void setup(){
	//Set up serial comms
	Serial.begin(9600);
	//Set up RTC
	Wire.begin();
	RTC.begin();   // the function to get the time from the RTC
	if (! RTC.isrunning()) {
		Serial.println(F("RTC is NOT running! Setting time to compile time"));
		// following line sets the RTC to the date & time this sketch was compiled
		RTC.adjust(DateTime(__DATE__, __TIME__));
	}
	else {
		Serial.println(F("RTC running OK"));
	}
	time=RTC.now();
	//Set the analog read pin modes
	pinMode(A0,INPUT);
	pinMode(A1,INPUT);
	pinMode(A2,INPUT);
	Serial.println(F("Initialisation done."));
	//Initialise variables
	timer0=millis();
	delay(100);
}
void loop(){
	timer1 = millis();
	time=RTC.now();
	if  ((timer1 - timer0) > 1000) {
		timer0 = timer1;
		SendData(time);
		Serial.readBytes((char *)readbuffer,64);

	}
}

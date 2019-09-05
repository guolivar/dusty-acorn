/*
   PACMAN - lite (Unlocking Curious Minds Alexandra 2018)
   - PMS3003 as Dust sensor on Hardware Serial port 2 - NOT SLEEPING
   - T&RH with Sensiron SHT31-DIS (I2C @ 0x44)
   - CO2 with K30 sensor 
   - distance with HC-SR04?
 */
//Framework
 #include <Arduino.h>
 #include <esp_system.h>

//Add Libraries to work with the I2C devices
#include <Wire.h>
//SHT30 T&RH sensor
#include <WEMOS_SHT3X.h>

//I2C definitions
#define xsda 21
#define xscl 22
#define TRH_ADDRESS 0x44

//HC-SR04 library
#include <hcsr04.h>
#define TRIG_PIN 12
#define ECHO_PIN 13

//PMS3003 definitions
#define receiveDatIndex 24 // Sensor data payload size PMS3003

//Load assisting libraries

//Definitions
byte receiveDat[receiveDatIndex]; //receive data from the air detector module
byte readbuffer[64];
int checkSum,checkresult;
int FrameLength,Data4,Data5,Data6;
int PM1,PM25,PM10,PM1us,PM25us,PM10us;
int record_idx;

float t,rh; //main temperature and RH
bool valid_data,iamok,ready; ///Data health flags
String save_line,timestamp;
String dataline,serbuff,mac_add;

unsigned int interval,tic,toc;

// SHT30 T&RH sensor
SHT3X sht30(0x44);

//HC-SR04
HCSR04 hcsr04(TRIG_PIN,ECHO_PIN,20,2500);


//SoftwareSerial rxPIN, txPIN
HardwareSerial dustport(2);

void readDust(HardwareSerial _dustport){
        int panic = 0; // failsafe to avoid no-dust sensor lock
        while ((_dustport.peek()!=66) & (panic < 500)) {
                receiveDat[0]=_dustport.read();
                delay(5);
                panic = panic +1;
        }
        _dustport.readBytes((char *)receiveDat,receiveDatIndex);
        checkSum = 0;
        for (int i = 0; i < receiveDatIndex; i++) {
                checkSum = checkSum + receiveDat[i];
        }
        checkresult = receiveDat[receiveDatIndex-2]*256+receiveDat[receiveDatIndex-1]+receiveDat[receiveDatIndex-2]+receiveDat[receiveDatIndex-1];
        valid_data = (checkSum == checkresult);
        if (panic >= 499){
          valid_data = false;
        }
        if (valid_data) {
                FrameLength = (receiveDat[2]*256)+receiveDat[3];
                PM1 = (receiveDat[4]*256)+receiveDat[5];
                PM25 = (receiveDat[6]*256)+receiveDat[7];
                PM10 = (receiveDat[8]*256)+receiveDat[9];
                PM1us = (receiveDat[10]*256)+receiveDat[11];
                PM25us = (receiveDat[12]*256)+receiveDat[13];
                PM10us = (receiveDat[14]*256)+receiveDat[15];
                Data4 = (receiveDat[16]*256)+receiveDat[17];
                Data5 = (receiveDat[18]*256)+receiveDat[19];
                Data6 = (receiveDat[20]*256)+receiveDat[21];
        } else {
                FrameLength = 0;
                PM1 = -999;
                PM25 = -999;
                PM10 = -999;
                PM1us = -999;
                PM25us = -999;
                PM10us = -999;
                Data4 = -999;
                Data5 = -999;
                Data6 = -999;
        }
        //Clear receiving buffer
        for( int i = 0; i < sizeof(receiveDat); ++i )
                receiveDat[i] = (char)0;
}

void setup(){
        iamok = true;
        //Start HWserial for messages
        Serial.begin(115200);
        Serial.println(F("Starting the setup"));
        //Start SoftwareSerial for PMS3003
        dustport.begin(9600);
        dustport.setTimeout(20000);

        //Initialise i2c
        Serial.println(F("I2C begins!"));
        Wire.begin(xsda, xscl);

}

void loop(){
        valid_data = false;

        //Read Dust data
        //Serial.println(F("Reading Dust Data"));
        while ((!valid_data)) {
                readDust(dustport);
        }

        // Read from SHT31
        //Serial.println(F("Getting SHT30 data"));
        t=0;
        rh=0;
        byte _sht = 1;
        while (_sht!=0) {
                _sht = sht30.get();
                //Read T&RH data
                t = sht30.cTemp;
                rh = sht30.humidity;
                _sht = 0;
        }
        //Build line to save to file and to send to server
        save_line = String(PM1);
        save_line = save_line + ";" + String(PM25);
        save_line = save_line + ";" + String(PM10);
        save_line = save_line + ";" + String(t);
        save_line = save_line + ";" + String(rh);
        save_line = save_line + ";" + hcsr04.ToString();
        //Publish dataline
        Serial.println(save_line);

}

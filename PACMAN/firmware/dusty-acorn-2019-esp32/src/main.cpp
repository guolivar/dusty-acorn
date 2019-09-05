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
#define xsda 23
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

int readCO2(){

  int co2_value = 0; // Store the CO2 value inside this variable.
  //////////////////////////
  /* Begin Write Sequence */
  //////////////////////////
  const int co2Addr = 0x68;
  // This is the default address of the CO2 sensor, 7bits shifted left.
  Wire.beginTransmission(co2Addr);
  Wire.write(0x22);
  Wire.write(0x00);
  Wire.write(0x08);
  Wire.write(0x2A);
  Wire.endTransmission();
  /////////////////////////
  /* End Write Sequence. */
  /////////////////////////
  /*
  Wait 10ms for the sensor to process our command. The sensors's
  primary duties are to accurately measure CO2 values. Waiting 10ms
  ensures the data is properly written to RAM
  */
  delay(10);
  /////////////////////////
  /* Begin Read Sequence */
  /////////////////////////
  /*
  Since we requested 2 bytes from the sensor we must read in 4 bytes.
  This includes the payload, checksum, and command status byte.
  */
  Wire.requestFrom(co2Addr, 4);
  byte i = 0;
  byte buffer[4] = {0, 0, 0, 0};
  /*
  Wire.available() is not necessary. Implementation is obscure but we
  leave it in here for portability and to future proof our code
  */
  while (Wire.available()){
    buffer[i] = Wire.read();
    i++;
  }
  ///////////////////////
  /* End Read Sequence */
  ///////////////////////
  /*
  Using some bitwise manipulation we will shift our buffer
  into an integer for general consumption
  */
  co2_value |= buffer[1] & 0xFF;
  co2_value = co2_value << 8;
  co2_value |= buffer[2] & 0xFF;
  byte sum = buffer[0] + buffer[1] + buffer[2]; //Byte addition utilizes overflow
  if (sum == buffer[3]){
    // Success!
    return co2_value;
  }
  else{
    // Failure!
    return 0;
  }
}


void setup(){
        iamok = true;
        //Start HWserial for messages
        Serial.begin(9600);
        //Serial.println(F("Starting the setup"));
        //Start SoftwareSerial for PMS3003
        dustport.begin(9600);
        dustport.setTimeout(20000);

        //Initialise i2c
        //Serial.println(F("I2C begins!"));
        Wire.begin(xsda, xscl);

}

void loop(){
        valid_data = false;

        //Read Dust data
        //Serial.println(F("Reading Dust Data"));
        while ((!valid_data)) {
                readDust(dustport);
                valid_data = true;
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
        // Read from K30
        int co2_value = readCO2();
        //Build line
        Serial.print(PM1);
        Serial.print(";");
        Serial.print(PM25);
        Serial.print(";");
        Serial.print(PM10);
        Serial.print(";");
        Serial.print(t);
        Serial.print(";");
        Serial.print(rh);
        Serial.print(";");
        Serial.print(co2_value);
        Serial.print(";");
        Serial.println(String(hcsr04.distanceInMillimeters()));

}

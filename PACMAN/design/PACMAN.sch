EESchema Schematic File Version 2
LIBS:PACMAN-rescue
LIBS:power
LIBS:device
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
LIBS:microcontrollers
LIBS:dsp
LIBS:microchip
LIBS:analog_switches
LIBS:motorola
LIBS:texas
LIBS:intel
LIBS:audio
LIBS:interface
LIBS:digital-audio
LIBS:philips
LIBS:display
LIBS:cypress
LIBS:siliconi
LIBS:opto
LIBS:atmel
LIBS:contrib
LIBS:valves
LIBS:gus_work
LIBS:PACMAN-cache
EELAYER 25 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title "Dusty ACorn"
Date "2016-08-10"
Rev "1"
Comp "NIWA"
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L ARDUINO_PRO_MINI MC1
U 1 1 57731415
P 4700 3300
F 0 "MC1" H 4700 3300 60  0000 C CNN
F 1 "ARDUINO_PRO_MINI" H 4700 3300 60  0000 C CNN
F 2 "arduino:Halley-ARDUINO_PRO_MINI" H 4700 3300 60  0001 C CNN
F 3 "" H 4700 3300 60  0000 C CNN
	1    4700 3300
	1    0    0    -1  
$EndComp
$Comp
L CONN_02X20 P1
U 1 1 577316C5
P 1700 1900
F 0 "P1" H 1700 2950 50  0000 C CNN
F 1 "RPi connector" V 1700 1900 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_2x20" H 1700 950 50  0001 C CNN
F 3 "" H 1700 950 50  0000 C CNN
	1    1700 1900
	1    0    0    -1  
$EndComp
$Comp
L CONN_01X08 P5
U 1 1 57A9D4B3
P 8950 3450
F 0 "P5" H 8950 3900 50  0000 C CNN
F 1 "PMS3003" V 9050 3450 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x08" H 8950 3450 50  0001 C CNN
F 3 "" H 8950 3450 50  0000 C CNN
	1    8950 3450
	1    0    0    -1  
$EndComp
$Comp
L CONN_01X04 P4
U 1 1 57AB036E
P 8850 4800
F 0 "P4" H 8850 5050 50  0000 C CNN
F 1 "Sonar" V 8950 4800 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x04" H 8850 4800 50  0001 C CNN
F 3 "" H 8850 4800 50  0000 C CNN
	1    8850 4800
	1    0    0    -1  
$EndComp
$Comp
L CONN_01X04 P3
U 1 1 57AB06A5
P 8850 1800
F 0 "P3" H 8850 2050 50  0000 C CNN
F 1 "DHT22" V 8950 1800 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x04" H 8850 1800 50  0001 C CNN
F 3 "" H 8850 1800 50  0000 C CNN
	1    8850 1800
	1    0    0    -1  
$EndComp
$Comp
L CONN_01X03 P2
U 1 1 57AB0750
P 8800 5700
F 0 "P2" H 8800 5900 50  0000 C CNN
F 1 "CO2" V 8900 5700 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x03" H 8800 5700 50  0001 C CNN
F 3 "" H 8800 5700 50  0000 C CNN
	1    8800 5700
	1    0    0    -1  
$EndComp
Wire Wire Line
	8600 5600 8400 5600
Wire Wire Line
	8150 5700 8600 5700
Wire Wire Line
	8150 5800 8600 5800
Text Label 8400 5600 0    60   ~ 0
A0
$Comp
L +5V #PWR01
U 1 1 57AB14EF
P 8150 5700
F 0 "#PWR01" H 8150 5550 50  0001 C CNN
F 1 "+5V" H 8150 5840 50  0000 C CNN
F 2 "" H 8150 5700 50  0000 C CNN
F 3 "" H 8150 5700 50  0000 C CNN
	1    8150 5700
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR02
U 1 1 57AB1564
P 8150 5800
F 0 "#PWR02" H 8150 5550 50  0001 C CNN
F 1 "GND" H 8150 5650 50  0000 C CNN
F 2 "" H 8150 5800 50  0000 C CNN
F 3 "" H 8150 5800 50  0000 C CNN
	1    8150 5800
	1    0    0    -1  
$EndComp
$Comp
L +5V #PWR03
U 1 1 57AB170D
P 8450 4650
F 0 "#PWR03" H 8450 4500 50  0001 C CNN
F 1 "+5V" H 8450 4790 50  0000 C CNN
F 2 "" H 8450 4650 50  0000 C CNN
F 3 "" H 8450 4650 50  0000 C CNN
	1    8450 4650
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR04
U 1 1 57AB1820
P 8450 4950
F 0 "#PWR04" H 8450 4700 50  0001 C CNN
F 1 "GND" H 8450 4800 50  0000 C CNN
F 2 "" H 8450 4950 50  0000 C CNN
F 3 "" H 8450 4950 50  0000 C CNN
	1    8450 4950
	1    0    0    -1  
$EndComp
Wire Wire Line
	8650 4650 8450 4650
Wire Wire Line
	8650 4950 8450 4950
Wire Wire Line
	8650 4750 8450 4750
Wire Wire Line
	8650 4850 8450 4850
Text Label 8450 4750 2    60   ~ 0
D5
Text Label 8450 4850 2    60   ~ 0
D6
Wire Wire Line
	8750 3400 8550 3400
Text Label 8550 3400 2    60   ~ 0
D10
Wire Wire Line
	8750 3700 8550 3700
Wire Wire Line
	8750 3800 8550 3800
$Comp
L +5V #PWR05
U 1 1 57AB1CA1
P 8550 3800
F 0 "#PWR05" H 8550 3650 50  0001 C CNN
F 1 "+5V" H 8550 3940 50  0000 C CNN
F 2 "" H 8550 3800 50  0000 C CNN
F 3 "" H 8550 3800 50  0000 C CNN
	1    8550 3800
	-1   0    0    1   
$EndComp
$Comp
L GND #PWR06
U 1 1 57AB1CBE
P 8550 3700
F 0 "#PWR06" H 8550 3450 50  0001 C CNN
F 1 "GND" H 8550 3550 50  0000 C CNN
F 2 "" H 8550 3700 50  0000 C CNN
F 3 "" H 8550 3700 50  0000 C CNN
	1    8550 3700
	-1   0    0    1   
$EndComp
Wire Wire Line
	8650 1650 8450 1650
Wire Wire Line
	8650 1750 8450 1750
Wire Wire Line
	8650 1950 8450 1950
$Comp
L GND #PWR07
U 1 1 57AB1E41
P 8450 1950
F 0 "#PWR07" H 8450 1700 50  0001 C CNN
F 1 "GND" H 8450 1800 50  0000 C CNN
F 2 "" H 8450 1950 50  0000 C CNN
F 3 "" H 8450 1950 50  0000 C CNN
	1    8450 1950
	1    0    0    -1  
$EndComp
$Comp
L +5V #PWR08
U 1 1 57AB1E5E
P 8450 1650
F 0 "#PWR08" H 8450 1500 50  0001 C CNN
F 1 "+5V" H 8450 1790 50  0000 C CNN
F 2 "" H 8450 1650 50  0000 C CNN
F 3 "" H 8450 1650 50  0000 C CNN
	1    8450 1650
	1    0    0    -1  
$EndComp
Text Label 8450 1750 2    60   ~ 0
D7
Wire Wire Line
	4100 2500 3900 2500
Wire Wire Line
	4100 3200 3900 3200
Wire Wire Line
	4100 3300 3900 3300
Wire Wire Line
	4100 3400 3900 3400
Wire Wire Line
	4100 3700 3900 3700
Text Label 3900 3200 2    60   ~ 0
D5
Text Label 3900 3300 2    60   ~ 0
D6
Text Label 3900 3400 2    60   ~ 0
D7
Text Label 3900 3700 2    60   ~ 0
D10
Wire Wire Line
	5400 3500 5650 3500
Text Label 5650 3500 0    60   ~ 0
A0
Wire Wire Line
	5400 2700 5650 2700
Wire Wire Line
	5400 2600 5650 2600
$Comp
L +5V #PWR09
U 1 1 57AB220C
P 5650 2600
F 0 "#PWR09" H 5650 2450 50  0001 C CNN
F 1 "+5V" H 5650 2740 50  0000 C CNN
F 2 "" H 5650 2600 50  0000 C CNN
F 3 "" H 5650 2600 50  0000 C CNN
	1    5650 2600
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR010
U 1 1 57AB22A1
P 5650 2700
F 0 "#PWR010" H 5650 2450 50  0001 C CNN
F 1 "GND" H 5650 2550 50  0000 C CNN
F 2 "" H 5650 2700 50  0000 C CNN
F 3 "" H 5650 2700 50  0000 C CNN
	1    5650 2700
	1    0    0    -1  
$EndComp
Text Label 3900 2500 2    60   ~ 0
TX0
Wire Wire Line
	1950 950  2250 950 
Wire Wire Line
	1950 1050 2250 1050
Wire Wire Line
	2250 1050 2250 950 
$Comp
L +5V #PWR011
U 1 1 57AB24B1
P 2350 1000
F 0 "#PWR011" H 2350 850 50  0001 C CNN
F 1 "+5V" H 2350 1140 50  0000 C CNN
F 2 "" H 2350 1000 50  0000 C CNN
F 3 "" H 2350 1000 50  0000 C CNN
	1    2350 1000
	1    0    0    -1  
$EndComp
Wire Wire Line
	2250 1000 2350 1000
Connection ~ 2250 1000
$Comp
L GND #PWR012
U 1 1 57AB24EF
P 2350 1150
F 0 "#PWR012" H 2350 900 50  0001 C CNN
F 1 "GND" H 2350 1000 50  0000 C CNN
F 2 "" H 2350 1150 50  0000 C CNN
F 3 "" H 2350 1150 50  0000 C CNN
	1    2350 1150
	1    0    0    -1  
$EndComp
Wire Wire Line
	1950 1150 2350 1150
Wire Wire Line
	1950 1350 2150 1350
Text Label 2150 1350 2    60   ~ 0
TX0
$EndSCHEMATC

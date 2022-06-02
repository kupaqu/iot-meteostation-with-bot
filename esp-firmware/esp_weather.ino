#include "Config.h"
#include "WIFI.h"
#include "MQTT.h"
#include "Disp.h"
#include "RTClib.h"
#include <Wire.h>
#include <Adafruit_BMP085.h>
#include <DHT.h>
#include <NTPClient.h>
#include <WiFiUdp.h>

#define DHTTYPE DHT21 

DHT dht(DHTPIN, DHTTYPE);
RTC_DS1307 rtc;
Adafruit_BMP085 bmp;
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org", utcOffsetInSeconds);

float temp;
float humd;
float pres;

void setup(void){
  Serial.begin(9600);
  Display_init();
  WIFI_init(false);

  mqtt_cli.setServer(mqtt_broker, mqtt_port);
  mqtt_cli.setBufferSize(2048);
  mqtt_cli.setCallback(callback);
  MQTT_init();
  
  WiFi.begin(ssidCLI, passwordCLI);
  dht.begin();
  if (!rtc.begin()) {
    printMessage("RTC not\nfind");
    while(1) {}
  }
  if (!rtc.isrunning()) {
    printMessage("RTC not\nrunning");
    timeClient.begin();
    timeClient.update();
    time_t rawtime = timeClient.getEpochTime();
    struct tm * ti;
    ti = localtime (&rawtime);
    
    uint16_t year = ti->tm_year + 1900;
    uint8_t month = ti->tm_mon + 1;
    uint8_t day = ti->tm_mday;
    uint8_t hours = ti->tm_hour;
    uint8_t minutes = ti->tm_min;
    uint8_t seconds = ti->tm_sec;
    rtc.adjust(DateTime(year, month, day, hours, minutes, seconds));
  }
  if (!bmp.begin()) {
    printMessage("Could\nnot find\nBMP180");
    while(1) {}
  }
}

void loop(void){
  if (!mqtt_cli.connected()) {
    MQTT_init();
  }                
  mqtt_cli.loop();

  temp = dht.readTemperature();
  humd = dht.readHumidity();
  pres = bmp.readPressure()  * 0.00750062;

  String t = "T=" + String(temp) + " C\n";
  String h = "H=" + String(humd) + "%\n";
  String p = "P=" + String(pres) + " mmHg";
  
  DateTime now = rtc.now();
  char data2server[] = "DD/MM/YYYY-hh:mm:ss";
  char data2display[] = "hh:mm:ss";   
  now.toString(data2server);
  now.toString(data2display);
  
  String result2server = String(data2server) + "|" + temp + "|" + humd + "|" + pres;
  String result2display = String(data2display) + "\n" + t + "\n" + h + "\n" + p;
  
  mqtt_cli.publish("isu/iot/meteo", result2server.c_str());
  display.clearDisplay();
  display.setCursor(0,0);
  display.println(result2display);
  display.display();
  delay(5000);
}

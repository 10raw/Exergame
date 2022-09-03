
//MAX30100 ESP8266 WebServer
#include <ESP8266WebServer.h>
#include <Wire.h>
#include "MAX30100_PulseOximeter.h"
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <SPI.h>
#define REPORTING_PERIOD_MS     1000

float BPM, SpO2;

/*Put your SSID & Password*/
const char* ssid = "vivo 1904";  // Enter SSID here
const char* password = "998d6ac38b71";  //Enter Password here
    String servername="http://192.168.86.37:3000/";

PulseOximeter pox;
uint32_t tsLastReport = 0;

ESP8266WebServer server(80);

void setup() {
  Serial.begin(115200);
  pinMode(16, OUTPUT);
  delay(100);
 WiFi.begin(ssid, password);
 
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());
 
  Serial.print("Initializing pulse oximeter..");

  if (!pox.begin()) {
    Serial.println("FAILED");
    for (;;);
  } else {
    Serial.println("SUCCESS");
    
  }
}
void loop() {
  pox.update();
  if (millis() - tsLastReport > REPORTING_PERIOD_MS) {

    BPM = pox.getHeartRate();
    SpO2 = pox.getSpO2();

 
    Serial.print("BPM: ");
    Serial.println(BPM);

    Serial.print("SpO2: ");
    Serial.print(SpO2);
    Serial.println("%");

    Serial.println("*********************************");
    
    tsLastReport = millis();

     
    WiFiClient client;
    HTTPClient http;
    servername="http://192.168.86.37:3000/?sensor="+(String)BPM ;
    http.begin(client,servername);  
    int httpCode = http.GET();                                 
  Serial.print(httpCode);
  Serial.println();
    if (httpCode > 0) { 
 
      String payload = http.getString();  
      Serial.print(payload);            
 
    }
 
    http.end();   //Close connection
 
  }
 
  }

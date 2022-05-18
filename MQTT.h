#include <PubSubClient.h>
#include "Disp.h"

PubSubClient mqtt_cli(wifiClient);

void callback(char *topic, byte *payload, unsigned int length) {
    Serial.print("Message arrived in topic: ");
    Serial.println(topic);  
    if (strcmp(topic, "esp/weather") == 0) {
      Serial.println("connect!");
    }
    Serial.println("-----------------------");
}

void MQTT_init(){
  while (!mqtt_cli.connected()) {
      String client_id = "esp8266-" + String(WiFi.macAddress());
      Serial.print("The client " + client_id);
      Serial.println(" connects to the public mqtt broker\n");
      if (mqtt_cli.connect(client_id.c_str())){
          Serial.println("MQTT Connected");
          printMessage("MQTT\nConnected");
      } else {
          Serial.print("failed with state ");
          Serial.println(mqtt_cli.state());
          delay(2000);
      }
  }  
}

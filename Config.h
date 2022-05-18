String ssidAP = "ESP_WIFI"; // имя контроллера и точки доступа
String passwordAP = "ESP8266123"; // пароль точки доступа

//char* ssidCLI = "YOUR_SSID"; // имя контроллера и точки доступа
//char* passwordCLI = "YOUR_PASS"; // пароль точки доступа

//char* ssidCLI = "mx3";
//char* passwordCLI = "9021717614";

char* ssidCLI = "meteo";
char* passwordCLI = "meteo2022";

const long utcOffsetInSeconds = 28800;

char* mqtt_broker = "broker.emqx.io";

const int mqtt_port = 1883;

const int OLED_RESET = 0;

const int DHTPIN = 14;

#pragma once

#include <Wire.h>
#include <Adafruit_SSD1306.h>

Adafruit_SSD1306 display(OLED_RESET);

void printWelcomMessage();

void Display_init() {
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  display.setTextSize(1);
  display.setTextColor(WHITE);
  printWelcomMessage();
}

void printWelcomMessage() {
  display.clearDisplay();
  display.setCursor(12,18);
  display.println("Project");
  display.setCursor(32,28);
  display.println("METEO");
  display.display();
  delay(2000);
}

void printMessage(String msg) {
  display.clearDisplay();
  display.setCursor(0,18);
  display.println(msg);
  display.display();
  delay(1500);
}

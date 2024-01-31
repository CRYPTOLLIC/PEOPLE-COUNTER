#include <Servo.h>
#include <LiquidCrystal.h>

Servo myservo;  // Create a servo object to control the servo motor
const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);
String x;

void setup() {
  Serial.begin(9600);  // Start the serial communication
  myservo.attach(9);  // Attach the servo to pin 9
  lcd.begin(16,2);  // Initialize the LCD
  lcd.print("People Counter");  // Display a title
}

void loop() {
    while(!Serial.available());
    x = Serial.readString();
    lcd.print(x);
    Serial.println(x);
    if (x == "1" || x=="3") {
      // Rotate the servo motor 90 degrees when '1' is received
      myservo.write(90);
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Limit Exceeded!");
    }
    else{
      myservo.write(0);
    }
  }

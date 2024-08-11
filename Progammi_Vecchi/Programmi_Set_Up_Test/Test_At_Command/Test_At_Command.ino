// include the library code:
#include <LiquidCrystal.h>

// initialize the library by associating any needed LCD interface pin
// with the arduino pin number it is connected to
const int rs = 11;
const int en = 10;
const int d4 = 5;
const int d5 = 4;
const int d6 = 3;
const int d7 = 2;
const int p2 = 12;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);
// Dichiarazione dei comandi AT
const char* atCommands[] = {
  "ATI",
  "AT+CFUN=0",
  "AT+CFUN=1",
  "AT+CGDCONT=?",
  "AT+QENG=\"servingcell\"",
  "AT+QNWINFO",
  "AT+QPING=1,\"8.8.8.8\"",
  "AT+QCFG=\"usbnet\",0",
  "AT+CGDCONT=1,\"IP\",\"oai\",\"\",0,0,0",
  "AT+CGACT=1,1"
};
// Numero di comandi AT
const int numCommands = sizeof(atCommands) / sizeof(atCommands[0]);

int buttonState = 0;
void setup() {
  lcd.print("Inizializzazione..");
  Serial.begin(115200,SERIAL_8N1);
  pinMode(p2,INPUT);
  // set up the LCD's number of columns and rows:
  lcd.begin(16, 2);
  // Print a message to the LCD. 
}

void loop() {
  lcd.clear();
  // set the cursor to column 0, line 1
  // (note: line 1 is the second row, since counting begins with 0):
  lcd.setCursor(0, 0);
  // print the number of seconds since reset:
  lcd.print("AT command:");
  // Invio del comando AT corrispondente
  int command=selezione_atcommand();
  Serial.println(atCommands[command]);
  delay(500);
  while(digitalRead(p2)){
    String receivedMessage = Serial.readStringUntil('\n');
    lcd.clear();
    lcd.setCursor(0,0);
    lcd.println(receivedMessage);
  }
  delay(500);
}
int selezione_atcommand(){
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("AT command:");
  int appoggio=1;
  int commandIndex = 0;
  while(!digitalRead(p2)){
    int potValue = analogRead(A1);
    // Mappatura del valore del potenziometro al numero di comandi AT
    int commandIndex = map(potValue, 0, 1023, 0, numCommands - 1);
    if(commandIndex != appoggio){
      lcd.setCursor(0,1);
      lcd.print("                       ");
      lcd.setCursor(0,1);
      lcd.print(atCommands[commandIndex]);
      appoggio=commandIndex;
    }
    delay(500);
  }
  return appoggio;
}
#include <ReceiveOnlySoftwareSerial.h>
int PIN_TTL_RX = 3; //Green wire, Transmit Data Line from acceptor
int PIN_INTERRUPT_LINE = 4; //Orange wire, Request to send data to host
int PIN_SEND_LINE = 5; //White/Blue wire, Host Ready Signal
int i;
int output =0;
ReceiveOnlySoftwareSerial mySerial(PIN_TTL_RX); // RX
void setup()  
{
  Serial.begin(115200);
  while (!Serial) { }  // wait for Serial to become available
  Serial.println("Insert Bill");
  // set the data rate for the ReceiveOnlySoftwareSerial port
  mySerial.begin(9600);
  digitalWrite(PIN_TTL_RX, HIGH); //internal pull-up required
  pinMode(PIN_INTERRUPT_LINE, INPUT);
  pinMode(PIN_SEND_LINE, OUTPUT);
  pinMode(8, OUTPUT);
}
void loop() // run over and over
{
  if (digitalRead(PIN_INTERRUPT_LINE) == LOW){
    digitalWrite(PIN_SEND_LINE, LOW);
    digitalWrite(PIN_SEND_LINE, HIGH);  
  }
  if (mySerial.available()){
    int codeFromBillAcceptor = mySerial.read();
    if( codeFromBillAcceptor == 0x81){  
      for(i=0; i<10; i++){
        digitalWrite(8, HIGH);
        delay(10);
        digitalWrite(8, LOW);
        delay(10);    
      }
      int total = 20;
      output = output + total;
      Serial.println(output);                     
    }
    if( codeFromBillAcceptor == 0x82){
      for(i=0; i<25; i++){
        digitalWrite(8, HIGH);
        delay(10);
        digitalWrite(8, LOW);
        delay(10);      
      }
      int total = 50;
      output = output + total;
      Serial.println(output);                     
    }
    if( codeFromBillAcceptor == 0x83){
      for(i=0; i<50; i++){
        digitalWrite(8, HIGH);
        delay(10);
        digitalWrite(8, LOW);
        delay(10); 
      }
      int total = 100;
      output = output + total;
      Serial.println(output);                     
    }
    if( codeFromBillAcceptor == 0x84){
      for(i=0; i<100; i++){
        digitalWrite(8, HIGH);
        delay(10);
        digitalWrite(8, LOW);
        delay(10);        
      }
      int total = 200;
      output = output + total;
      Serial.println(output);                     
    }
    if( codeFromBillAcceptor == 0x85){
      for(i=0; i<250; i++){
        digitalWrite(8, HIGH);
        delay(10);
        digitalWrite(8, LOW);
        delay(10);        
      }
      int total = 500;
      output = output + total;
      Serial.println(output);                     
    }
    if( codeFromBillAcceptor == 0x86   ){
      for(i=0; i<500; i++){
        digitalWrite(8, HIGH);
        delay(10);
        digitalWrite(8, LOW);
        delay(10);   
      }
      int total = 1000;
      output = output + total;
      Serial.println(output); 
    }
  }
}

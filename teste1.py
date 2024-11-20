
from RPi.GPIO import Pin                         #| include <Arduino.h>
import time                                     #|
                                                #|
def medirDist (echo, trig):                     #| void medirDist( int echo, int trig) {
    nova_leitura = False                        #|    bool nova_leitura = false;
    contador = 0                                #|    int contador = 0;
    resultado = 0                               #|    float resultado = 0;
    duracao = 0                                 #|    int duracao = 0;
    echoPIN = Pin(echo, Pin.IN)                 #|    pinMode( echo, INPUT);
    trigPIN = Pin(trig, Pin.OUT)                #|    pinMode( trig, OUTPUT);
                                                #|
    trigPIN.value(0)                            #|    digitalWrite( trig, LOW);
    time.sleep_us(2)                            #|    delayMicroseconds(2)
    trigPIN.value(1)                            #|    digitalWrite( trig, HIGH);
    time.sleep_us(10)                           #|    delayMicroseconds(10)
    trigPIN.value(0)                            #|    digitalWrite( trig, LOW);
    time.sleep_us(2)                            #|    delayMicroseconds(2)
                                                #|
    while not echoPIN.value():                  #|    while (!digitalRead(echo)){
      pass                                      #|       contador++;
      contador += 1                             #|       if (contador == 5000) {
      if contador == 5000:                      #|          nova_Leitura = true;
         nova_leitura = True                    #|          break;
         break                                  #|       }
                                                #|    }
    if nova_leitura:                            #|    if (nova_leitura){
        return False                            #|       return False;
                                                #|    }
    inicio = time.ticks_us()/1000000            #|    unsigned long inicio = micros();
                                                #|
    while echoPIN.value(): pass                 #|    while (digitalRead(echo)) {;}
    retorno = time.ticks_us()/1000000           #|    unsigned long retorno = micros();
                                                #|
    if retorno == inicio:                       #|    if (retorno == incio) {
        resultado = "N/A"                       #|       resultado = -1;
    else:                                       #|    } else {
        duracao = retorno - inicio              #|       duracao = retorno - inicio;
                                                #|    }
    soundSpeed = 34300                          #|    int soundSpeed = 34300;
    resultado = duracao * soundSpeed / 2        #|    resultado = duracao * soundSpeed / 2;
    resultado = round(resultado, 1)             #|    resultado = round(resultado, 1);
    return resultado                            #|    return resultado;
                                                #| }
                                                #|
pinEcho = 15                                    #| int pinEcho = 15;
pinTrig = 14                                    #| int pinTrig = 14;
                                                #|
pinLedVd = 13                                   #| int pinLedVd = 13;
pinLedVm = 12                                   #| int pinLedVm = 12;
pinBuz   = 10                                   #| int pinBuz   = 10;
                                                #|
                                                #| void setup() {
LedVd = Pin(pinLedVd, Pin.OUT)                  #|    pinMode( pinLedVd, OUTPUT);
LedVm = Pin(pinLedVm, Pin.OUT)                  #|    pinMode( pinLedVm, OUTPUT);
Buzzer = Pin(pinBuz , Pin.OUT)                  #|    pinMode( pinBuz  , OUTPUT);
                                                #| }
                                                #|
while True:                                     #| void loop() {
    distancia = medirDist(pinEcho,pinTrig)      #|    float distancia = medirDist( pinEcho, pinTrig);
    print ("Dist: " + str(distancia), end='\r') #|    Serial.print("Dist: "); Serial.print(distancia); Serial.print("\r");
                                                #|    
    if distancia > 20.0 :                       #|    if (distancia > 40.0) {
        LedVm.value(0)                          #|       digitalWrite( pinLedVm, LOW);
        LedVd.value(1)                          #|       digitalWrite( pinLedVd, HIGH);
    else :                                      #|    } else {
        LedVd.value(0)                          #|       digitalWrite( pinLedVd, LOW);
        LedVm.value(1)                          #|       digitalWrite( pinLedVm, HIGH);
                                                #|    
    if distancia < 10.0 :                       #|    if (distancia < 20.0) {
        Buzzer.value(1)                         #|       digitalWrite( pinBuz, HIGH);
    else :                                      #|    } else {
        Buzzer.value(0)                         #|       digitalWrite( pinBuz, LOW);
                                                #|    
    time.sleep(0.5)                             #|    delay (5000);
                                                #|  
# Q0716_HCSR04.py
# Exibindo Q0716_HCSR04.py…
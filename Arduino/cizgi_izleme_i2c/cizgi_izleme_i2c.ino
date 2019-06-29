/*
  I2C Pinleri Nano

  SDA -> A4
  SCL -> A5
*/

#include <Wire.h>

#define SLAVE_ADDRESS 0x04

//Dc Motor Bağlantıları
#define pwmPinSol  9
#define Sol1Pin  7
#define Sol2Pin  8
#define pwmPinSag  3
#define Sag1Pin  5
#define Sag2Pin  4

//Çizgi İzlemek için Gerekli Bağlantılar
int refDeg = 800;
#define cizgi1 A0
#define cizgi2 A1
#define cizgi3 A2
bool cizgirengi = false; //False beyaz çizgi, true siyah çizgi
bool devamEt = true; // Veri beklemek için false, değilse true
bool cizgiIzle = false; //Direk çizgi izlemey başlamak için true, değilse false
int sonkonum = 1;
bool c1;
bool c2;
bool c3;

char Veri_ayar[20];
int durum = 0;

void setup() {
  Serial.begin(9600);
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveData);

  pinMode(pwmPinSol, OUTPUT);
  pinMode(Sol1Pin, OUTPUT);
  pinMode(Sol2Pin, OUTPUT);
  pinMode(pwmPinSag, OUTPUT);
  pinMode(Sag1Pin, OUTPUT);
  pinMode(Sag2Pin, OUTPUT);

  pinMode (cizgi1, INPUT);
  pinMode (cizgi2, INPUT);
  pinMode (cizgi3, INPUT);
}

void loop()
{

  if (devamEt == true)
  {
    motorKontrol(0, 0);
    Serial.print("Yolcu Aliniyor/Iniyor..");
    devamEt = false;
    cizgiIzle = !cizgiIzle;
  }
  if (cizgiIzle == true)
  {
    CizgiIzle();
    //Serial.println("Duraka gidiliyor.");
  }
}

void receiveData(int byteCount) {
  char karakter;
  while (Wire.available()) {
    karakter = Wire.read();
  }
  devamEt = true;
}

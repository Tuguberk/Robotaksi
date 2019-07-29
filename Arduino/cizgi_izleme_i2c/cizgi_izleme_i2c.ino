/*
  I2C Pinleri Nano

  SDA -> A4
  SCL -> A5
*/


#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
#define SLAVE_ADDRESS 0x04
#define SERVOMIN  125 // this is the 'minimum' pulse length count (out of 4096)
#define SERVOMAX  575 // this is the 'maximum' pulse length count (out of 4096)
uint8_t servonum = 1;
int kapiKapali = 40;
int kapiAcik = 160;
int yururaksamKapali = 170;
int yururaksamAcik = 40;

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
bool devamEt = false; // Veri beklemek için false, değilse true
bool cizgiIzle = false; //Direk çizgi izlemey başlamak için true, değilse false
int sonkonum = 1;
bool c1;
bool c2;
bool c3;

char Veri_ayar[20];
int durum = 0;

void setup() {
  Serial.begin(9600);
  pwm.begin();
  pwm.setPWMFreq(60);  // Analog servos run at ~60 Hz updates

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

  pwm.setPWM(0, 0, angleToPulse(kapiKapali));
  pwm.setPWM(1, 0, angleToPulse(yururaksamKapali));
}

void loop()
{

  if (devamEt == true)
  {
    motorKontrol(0, 0);
    Serial.print("Yolcu Aliniyor/Iniyor..");
    Yolcu();
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

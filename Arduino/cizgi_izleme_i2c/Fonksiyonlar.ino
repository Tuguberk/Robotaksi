void motorKontrol(int hizSol, int hizSag)
{
  boolean ters = true;
  if (hizSol < 0)
  {
    hizSol = abs(hizSol);
    analogWrite(pwmPinSol, hizSol);
    digitalWrite(Sol1Pin, ! ters);
    digitalWrite(Sol2Pin, ters);
  }
  else
  {
    analogWrite(pwmPinSol, hizSol);
    digitalWrite(Sol1Pin, ters);
    digitalWrite(Sol2Pin, ! ters);
  }

  if (hizSag < 0)
  {
    hizSag = abs(hizSag);
    analogWrite(pwmPinSag, hizSag);
    digitalWrite(Sag1Pin, ters);
    digitalWrite(Sag2Pin, ! ters);
  }
  else
  {
    analogWrite(pwmPinSag, hizSag);
    digitalWrite(Sag1Pin, ! ters);
    digitalWrite(Sag2Pin, ters);
  }
}

void Yolcu()
{

  pwm.setPWM(0, 0, angleToPulse(kapiAcik));
  pwm.setPWM(1, 0, angleToPulse(yururaksamAcik));
  delay(6000);
  pwm.setPWM(0, 0, angleToPulse(kapiKapali));
  pwm.setPWM(1, 0, angleToPulse(yururaksamKapali));
  delay(2000);
}

void CizgiIzle()
{
  if (analogRead(cizgi1) < refDeg) c1 = false; else c1 = true;
  if (analogRead(cizgi2) < refDeg) c2 = false; else c2 = true;
  if (analogRead(cizgi3) < refDeg) c3 = false; else c3 = true;
  Serial.print(c1);
  Serial.print('\t');
  Serial.print(c2);
  Serial.print('\t');
  Serial.print(c3);
  Serial.println();

  if (c1 != cizgirengi and c2 == cizgirengi and c3 != cizgirengi)
  {
    Serial.println("Duz");
    motorKontrol(70, 70);
    sonkonum = 1;
  }
  if (c1 != cizgirengi and c2 != cizgirengi and c3 == cizgirengi)
  {
    Serial.println("Sagdancikti");
    motorKontrol(-50, 130);
    sonkonum = 0;
  }
  if (c1 == cizgirengi and c2 != cizgirengi and c3 != cizgirengi)
  {
    Serial.println("Soldancikti");
    motorKontrol(130, -50);
    sonkonum = 2;
  }
  if (c1 == cizgirengi and c2 == cizgirengi and c3 != cizgirengi)
  {
    Serial.println("Soldancikti");
    motorKontrol(130, -50);
    sonkonum = 2;
  }
  if (c1 != cizgirengi and c2 == cizgirengi and c3 == cizgirengi)
  {
    Serial.println("Sagdancikti");
    motorKontrol(-50, 130);
    sonkonum = 0;
  }/*
  else if (c1 != cizgirengi and c2 != cizgirengi and c3 != cizgirengi)
  {
    switch (sonkonum)
    {
      case 0:
        motorKontrol(90, 0);
        break;
      case 1:
        motorKontrol(0, 90);
        break;
    }
  }*/
}

int angleToPulse(int ang) {
  return map(ang, 0, 180, SERVOMIN, SERVOMAX);
}

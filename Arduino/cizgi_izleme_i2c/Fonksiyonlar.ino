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

void CizgiIzle()
{
  if (analogRead(cizgi1)<refDeg) c1 = false; else c1 = true;
  if (analogRead(cizgi2)<refDeg) c2 = false; else c2 = true;
  if (analogRead(cizgi3)<refDeg) c3 = false; else c3 = true;
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
    motorKontrol(-40, 120);
    sonkonum = 0;
  }
  if (c1 == cizgirengi and c2 != cizgirengi and c3 != cizgirengi)
  {
    Serial.println("Soldancikti");
    motorKontrol(120, -40);
    sonkonum = 2;
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

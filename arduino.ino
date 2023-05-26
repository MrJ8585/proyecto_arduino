int SensorPIR = 2;
int LED=4;
int piezo=7;


void setup()
{
  Serial.begin(9600);
  pinMode(SensorPIR,INPUT);
  pinMode(LED,OUTPUT);
  pinMode(piezo, OUTPUT);
}

void loop()

{
  int valor = digitalRead(SensorPIR);
  if(valor==HIGH){
    Serial.print("Se detecto movimiento")
    digitalWrite(LED,HIGH);
    digitalWrite(piezo,HIGH);
    delay(1000);
    digitalWrite(piezo,LOW);
    delay(1000);
  } else{
    digitalWrite(LED,LOW);
    digitalWrite(piezo,LOW);
  }

  delay(10);
  Serial.print("estamos viendo...");
  Serial.println(valor);
  delay(250);
}
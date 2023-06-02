int SensorPIR = 2;
int LED = 4;
int piezo = 7;
bool sensor_encendido = false;  // Variable para controlar el estado del sensor
bool sistema_prendido = true;  // Variable para controlar el encendido/apagado del sistema
bool sensor_previo = false;  // Variable para almacenar el estado previo del sensor

void setup()
{
  Serial.begin(9600);
  pinMode(SensorPIR, INPUT);
  pinMode(LED, OUTPUT);
  pinMode(piezo, OUTPUT);
}

void loop()
{
  if (sistema_prendido && !sensor_encendido)
  {
    int valor = digitalRead(SensorPIR);

    if (valor == HIGH)
    {
      sensor_encendido = true;
      if (sistema_prendido)
      {
        Serial.println("Se detectó movimiento");
        digitalWrite(LED, HIGH);
        digitalWrite(piezo, HIGH);
      }
    }
  }
  else if (!sistema_prendido && sensor_encendido)
  {
    sensor_encendido = false;
    digitalWrite(LED, LOW);
    digitalWrite(piezo, LOW);
  }
  
  // Controlar encendido/apagado del sistema
  if (Serial.available() > 0)
  {
    char dato = Serial.read();
    if (dato == 'P')
    {
      sistema_prendido = !sistema_prendido;  // Cambiar el estado del sistema
      if (sistema_prendido)
      {
        Serial.println("Sistema prendido");
      }
      else
      {
        Serial.println("Sistema apagado");
        sensor_encendido = false;
        digitalWrite(LED, LOW);
        digitalWrite(piezo, LOW);
      }
    }
    else if (dato == 'A')
    {
      sensor_encendido = false;
      digitalWrite(LED, LOW);
      digitalWrite(piezo, LOW);
      Serial.println("No se ha detectado movimiento");
    }
  }
  
  sensor_previo = sensor_encendido;  // Almacenar estado previo del sensor
  delay(10);  // Pequeña pausa entre iteraciones
}

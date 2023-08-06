// Phi Version 4.0 ultrasonido
#include <NewPing.h> //sensor ultrasonido
#include <Servo.h> //servomotor

 
//variables globales
char caracter;
char data;
char parametro[8]; //utilizado para recibir los 8 bits del comando write
//char extendido[4]; //puertos extendidos
char parametro_pwm[2]; //puertos extendidos
String lectura; //arma el string de enviuio a python
int pin; //recibe el estado del puerto digital de lectura 

//Sensor ultrasonido en puertos 11 y 12
#define TRIGGER_PIN  12  // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHO_PIN     11  // Arduino pin tied to echo pin on the ultrasonic sensor.
#define MAX_DISTANCE 200 // Maximum distance we want to ping for (in centimeters). Maximum sensor distance is rated at 400-500cm.
NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE); // NewPing setup of pins and maximum distance.

//Servo en pin 10
Servo servoMotor; 

void setup() 
{
   Serial.begin(9600);
   //Serial.setTimeout(50);
   
   //definicion 
   for (int i=2; i <= 9 ; i++){
      pinMode(i, OUTPUT);
   }

   //seteamos todo a nivel bajo
   for (int i=2; i <= 9; i++){
      digitalWrite(i, LOW);
   }
   
   for (int i=14; i <= 19 ; i++){
      pinMode(i, INPUT_PULLUP);
   }
    
   
  servoMotor.attach(10); // Iniciamos el servo para que empiece a trabajar con el pin 10
  servoMotor.write(0); // Inicializamos al ángulo 0 el servomotor
}
 
void loop()
{
 
   if (Serial.available()>0) 
   {
     
      caracter = Serial.read();
      delay(1);
      if (caracter == 'L' ) //escribe low en el puerto que viene enviado despues
      {
          //recibimos 2 parametros el puerto y estado
          char b = Serial.read();
          b -= '0'; //se recibe el ascii del numero entre 0 y 9 que es del 48 al 47, si le resto el cero(48 ascii) me da el valor enviado
          digitalWrite(b+2, LOW); 
          
          
       }

      if (caracter == 'H') //escribe high en el puerto que viene enviado despues
      {
          //recibimos 2 parametros el puerto y estado
          char b = Serial.read();
          b -= '0';
          digitalWrite(b+2, HIGH);   
          
       }


      if (caracter == 'P') //pwm sobre el puerto indicado(1,3,4,7,8 correspondiemtes a 3,5,6,9,10 de arduino)
                           // el segundo parametro es un numero de 0 a 9 que se multtiplica por 25 para sacar la potencia(0 minima, 9 maxima)
      {
          //recibimos 2 parametros el puerto y estado
          int bytesleidos = Serial.readBytes(parametro_pwm,2);
          int puerto = parametro_pwm[0] - '0';
          int valor =  parametro_pwm[1] - '0';
          analogWrite(puerto+2, valor*25);
             
               
          
       }
      
      if (caracter == 'W') //escribir en todos s
      {
          //Si recubimos una W sabemos que lo que sigue es un numero entero entre 0 y 255 ya en binario de 8 posiciones
          //por ejemplo 00001001

          int bytesleidos = Serial.readBytes(parametro,8);
           
           for (int i=0; i <= 7 ; i++){
                
                if (parametro[i] == '0' ){ 
                   digitalWrite(9-i, LOW); 
                }
                else
                {
                   digitalWrite(9-i, HIGH);
                  
                }
             }
       }

      
       
        if (caracter == 'D'){   //setea todo a down
            for (int i=13; i >= 2; i--)
            {
                digitalWrite(i, LOW);
            }
        }
       
        if (caracter == 'U'){   //setea todo a up
            for (int i=13; i >= 2; i--)
            {
                digitalWrite(i, HIGH);

            }
        }

        if (caracter == 'R'){   //lee los puertos del 14 al 19 y los envia en un formato binario 01100000
            lectura = "";
            for (int i=14; i <= 19; i++)
            {
                lectura = lectura +  String(digitalRead(i));
                
            }
            Serial.println(lectura);
        }


      

        if (caracter == 'S') //lee el ultrasonido, calcula distancia y envia dato
      {
          float t = sonar.ping_median(10);         
          Serial.println(sonar.convert_cm(t));   
                
       }

        if (caracter == 'M') //mueve el servomotor
      {
              //Recibe un numero de 0 a 180 grados
              String angulo = Serial.readStringUntil('#'); //leo datos hasta el #
              servoMotor.write(angulo.toInt());
           
                
       }
        
    }
    delay(1);
}


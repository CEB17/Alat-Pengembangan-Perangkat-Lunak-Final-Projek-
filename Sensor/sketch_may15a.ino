unsigned int rpm;
volatile byte pulses;
unsigned long timeold;
unsigned int ppr = 20;
int encoder = 3; // pin de conexiòn del encoder derecho 

// mendefinisikan pin 
const int trigPin = 4; 
const int echoPin = 5; 

// defining variables 
long duration; 
int distance; 

//Standard PWM DC control
int E1 = 5;     //M1 Speed Control
int E2 = 6;     //M2 Speed Control
int M1 = 4;    //M1 Direction Control
int M2 = 7;    //M1 Direction Control

static int speed;

void counter(){
  pulses++;
}

void stop(void)                    //Stop
{
  digitalWrite(E1,LOW);
  digitalWrite(E2,LOW);
}
void advance(char a,char b)          //Move forward
{
  analogWrite (E1,a);      //PWM Speed Control
  digitalWrite(M1,HIGH);
  analogWrite (E2,b);
  digitalWrite(M2,HIGH);
}
void back_off (char a,char b)          //Move backward
{
  analogWrite (E1,a);
  digitalWrite(M1,LOW);
  analogWrite (E2,b);
  digitalWrite(M2,LOW);
}
void turn_L (char a,char b)             //Turn Left
{
  analogWrite (E1,a);
  digitalWrite(M1,LOW);
  analogWrite (E2,b);
  digitalWrite(M2,HIGH);
}
void turn_R (char a,char b)             //Turn Right
{
  analogWrite (E1,a);
  digitalWrite(M1,HIGH);
  analogWrite (E2,b);
  digitalWrite(M2,LOW);
}

void jarak(){ 
pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output 
pinMode(echoPin, INPUT); // Sets the echoPin as an Input 
// Clears the trigPin 
digitalWrite(trigPin, LOW); 
delayMicroseconds(2); 

// Sets the trigPin on HIGH state for 10 micro seconds 
digitalWrite(trigPin, HIGH); 
delayMicroseconds(10); 
digitalWrite(trigPin, LOW); 
// Reads the echoPin, returns the sound wave travel time in microseconds 
duration = pulseIn(echoPin, HIGH); 

// Calculating the distance 
distance= duration*0.034/2; 
} 

void CRPM(){
  if(millis() - timeold>=1000){
    detachInterrupt(0);
    rpm = (60*1000 / ppr)/(millis()-timeold)*pulses;
    timeold = millis();
    pulses = 0;
    }
}

void setup(void)
{
  Serial.begin(9600);
  pinMode(encoder, INPUT);
  attachInterrupt(0, counter, FALLING);
  pulses = 0;
  rpm = 0;
  timeold = 0;
  int i;
  for(i=4;i<=7;i++)
  pinMode(i, OUTPUT);
  Serial.begin(115200);      //Set Baud Rate
  Serial.println("Run keyboard control");
}
void loop(void)
{
  if(Serial.available()){
    char val = Serial.read();
    if(val != -1)
    {
      switch(val)
      {
      case 'i':   //speed up
        speed++;
        if(speed>5)
          speed = 5;
        break;
      case 'k':   //speed down
        speed--;
        if(speed<0)
          speed = 0;
        break;
      case 'w'://Move Forward
        advance( (255*speed)/5, (255*speed)/5 );   //move forward in max speed
        break;
      case 's'://Move Backward
        back_off( (255*speed)/5,(255*speed)/5 );   //move back in max speed
        break;
      case 'a'://Turn Left
        turn_L (100,100);
        break;
      case 'd'://Turn Right
        turn_R (100,100);
        break;
      case 'x':
        stop();
        break;
      }
    }
    else stop();
  }

jarak();
CRPM(); 
Serial.print("jarak = "); 
Serial.print(distance); 

Serial.print(" "); 
Serial.print("Speed = "); 
Serial.println(rpm, DEC); 
attachInterrupt(0, counter, FALLING);

}

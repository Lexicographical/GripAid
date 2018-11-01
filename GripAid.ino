#include <Servo.h>
#include <Wire.h>
#include "U8glib.h"

#define DS3231_I2C_ADDRESS 0x68

Servo gripServo;
U8GLIB_SH1106_128X64 u8g(U8G_I2C_OPT_NONE); 

 int xlength;
int flexVal;
String newBPM;
int pulsePin = A1;
boolean center = true;
int normalVal;

int bpm, sig, ibi=600, pulse=false, qs=false;

static boolean debug = true;

int bpmCache = 0;
int rate[10];
unsigned long sampleCounter = 0, lastBeatTime=0;
int P=512, T=512, thresh=525, amp=100;
boolean firstBeat = true, secondBeat = false;
bool drawBig = true;
bool flexAct = false;

byte decToBcd(byte val)
{
  return ( (val / 10 * 16) + (val % 10) );
}

// Convert binary coded decimal to normal decimal numbers
byte bcdToDec(byte val)
{
  return ( (val / 16 * 10) + (val % 16) );
}

void readDS3231time(byte *second,
                    byte *minute,
                    byte *hour,
                    byte *dayOfWeek,
                    byte *dayOfMonth,
                    byte *month,
                    byte *year)
{
  Wire.beginTransmission(DS3231_I2C_ADDRESS);
  Wire.write(0); // set DS3231 register pointer to 00h
  Wire.endTransmission();
  Wire.requestFrom(DS3231_I2C_ADDRESS, 7);
  // request seven bytes of data from DS3231 starting from register 00h
  *second = bcdToDec(Wire.read() & 0x7f);
  *minute = bcdToDec(Wire.read());
  *hour = bcdToDec(Wire.read() & 0x3f);
  *dayOfWeek = bcdToDec(Wire.read());
  *dayOfMonth = bcdToDec(Wire.read());
  *month = bcdToDec(Wire.read());
  *year = bcdToDec(Wire.read());
}


void automatic()
{
  gripServo.write(0);
  delay(1500);
  gripServo.write(180);
  delay(1500);
}

void manual()
{
  

    flexVal = analogRead(A0);
  Serial.println(flexVal);
    if(flexVal < normalVal-60)
  {
    flexAct = false;
    gripServo.write(0);
  }
  else
  {
    flexAct = true;
    gripServo.write(175);
  }
  
  
}

void display()
{
    u8g.firstPage();  
  do {
    draw();
  } while( u8g.nextPage() );

  if(flexVal > normalVal-60)
  {
    xlength = 90;
  }
  else
  {
    xlength = 40;
  }
}

void startupPage() {
  String text = "GripAid";
  for (int i = 0; i < 7; i++) {
    u8g.firstPage();
    String sub = text.substring(0, i + 1);
    do {
      u8g.drawStr(30, 30, sub.c_str());
      u8g.drawLine(30, 35, 40 + 8*i, 35);
    } while (u8g.nextPage());
//    Serial.println(sub);
    delay(250);
  }
  delay(500);
}

int beatCount = 0;
int beats[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};

void draw()
{
    
    
  // graphic commands to redraw the complete screen should be placed here  

//  u8g.drawStr( 0, 20, "Hello World!");
//    u8g.drawBox(10,10,xlength,20);

    if (qs) {
      if (bpm > 60 && bpm < 100) {
         bpmCache = bpm;
      }
    }
    if (bpmCache == 0) {
      u8g.drawStr(0, 20, String("---").c_str());
    } else {
      u8g.drawStr(0, 20, String(bpmCache).c_str());
    }
    u8g.drawStr(0, 70, "BPM");

    if (drawBig) {
    u8g.drawDisc(53, 20, 8);
    u8g.drawDisc(69, 20, 8);
    u8g.drawBox(59, 20, 8, 8);
    u8g.drawTriangle(47, 26, 76, 26, 61, 40);
  } else {
    u8g.drawDisc(55, 20, 5);
    u8g.drawDisc(65, 20, 5);
    u8g.drawBox(60, 20, 5, 5);
    u8g.drawTriangle(51, 24, 69, 24, 60, 34);
  }

  if (flexAct) {
    u8g.drawBox(45, 50, 31, 5);
  } else {
    u8g.drawBox(53, 50, 16, 5);
  }

  byte second, minute, hour, dayOfWeek, dayOfMonth, month, year;
  readDS3231time(&second, &minute, &hour, &dayOfWeek, &dayOfMonth, &month,
                 &year);
  

  u8g.drawStr(100, 35, "");
    
//    u8g.drawStr(0, 20, String(newBPM).c_str() );

// heart
   

//    u8g.drawBox(50, 30, 10, 10);

//    beatGraph
//  beatCount++;
//  if (beatCount == 4) {
//    beatCount = 0;
//    int val = 0;
//    if (qs) {
//       val = constrain(bpm, 0, 150);
//       val = map(val, 0, 150, 0, 15);
//    } else if (beats[14] > 0) {
//      val = -beats[14];
//    }
//    for (int i = 1; i < 15; i++) {
//      beats[i-1] = beats[i];
//    }
//    beats[14] = val;
//  }
//  for (int i = 1; i < 15; i++) {
//    int x1 = 50 + 4 * (i-1);
//    int y1 = 30 + beats[i-1];
//    int x2 = 50 + 4 * i;
//    int y2 = 30 + beats[i];
//    u8g.drawLine(x1,y1, x2,y2);
//  }

}

void interruptSetup() {
  TCCR2A = 0x02;     // DISABLE PWM ON DIGITAL PINS 3 AND 11, AND GO INTO CTC MODE
  TCCR2B = 0x06;     // DON'T FORCE COMPARE, 256 PRESCALER 
  OCR2A = 0X7C;      // SET THE TOP OF THE COUNT TO 124 FOR 500Hz SAMPLE RATE
  TIMSK2 = 0x02;     // ENABLE INTERRUPT ON MATCH BETWEEN TIMER2 AND OCR2A
  sei(); 
}

void serialOutputOnBeat() {
  if (debug) {
//    Serial.println("=== Heart beat detected! ===");
//    Serial.print("BPM: ");
//    Serial.println(bpm);
  }
  qs = true;
}

ISR(TIMER2_COMPA_vect) //triggered when Timer2 counts to 124
{  
  cli();                                      // disable interrupts while we do this
  sig = analogRead(pulsePin);              // read the pulse Sensor 
  sampleCounter += 2;                         // keep track of the time in mS with this variable
  int N = sampleCounter - lastBeatTime;       // monitor the time since the last beat to avoid noise
                                              //  find the peak and trough of the pulse wave
  if(sig < thresh && N > (ibi/5)*3) // avoid dichrotic noise by waiting 3/5 of last IBI
    {      
      if (sig < T) // T is the trough
      {                        
        T = sig; // keep track of lowest point in pulse wave 
      }
    }

  if(sig > thresh && sig > P)
    {          // thresh condition helps avoid noise
      P = sig;                             // P is the peak
    }                                        // keep track of highest point in pulse wave

  //  NOW IT'S TIME TO LOOK FOR THE HEART BEAT
  // sig surges up in value every time there is a pulse
  if (N > 250)
  {                                   // avoid high frequency noise
    if ( (sig > thresh) && (pulse == false) && (N > (ibi/5)*3) )
      {        
        pulse = true;                               // set the pulse flag when we think there is a pulse
        //digitalWrite(blinkPin,HIGH);                // turn on pin 13 LED
        ibi = sampleCounter - lastBeatTime;         // measure time between beats in mS
        lastBeatTime = sampleCounter;               // keep track of time for next pulse
  
        if(secondBeat)
        {                        // if this is the second beat, if secondBeat == TRUE
          secondBeat = false;                  // clear secondBeat flag
          for(int i=0; i<=9; i++) // seed the running total to get a realisitic BPM at startup
          {             
            rate[i] = ibi;                      
          }
        }
  
        if(firstBeat) // if it's the first time we found a beat, if firstBeat == TRUE
        {                         
          firstBeat = false;                   // clear firstBeat flag
          secondBeat = true;                   // set the second beat flag
          sei();                               // enable interrupts again
          return;                              // IBI value is unreliable so discard it
        }   
      // keep a running total of the last 10 IBI values
      word runningTotal = 0;                  // clear the runningTotal variable    

      for(int i=0; i<=8; i++)
        {                // shift data in the rate array
          rate[i] = rate[i+1];                  // and drop the oldest IBI value 
          runningTotal += rate[i];              // add up the 9 oldest IBI values
        }

      rate[9] = ibi;                          // add the latest IBI to the rate array
      runningTotal += rate[9];                // add the latest IBI to runningTotal
      runningTotal /= 10;                     // average the last 10 IBI values 
      bpm = 60000/runningTotal;               // how many beats can fit into a minute? that's BPM!
      qs = true;                              // set Quantified Self flag 
      // QS FLAG IS NOT CLEARED INSIDE THIS ISR
    }                       
  }

  if (sig < thresh && pulse == true)
    {   // when the values are going down, the beat is over
      //digitalWrite(blinkPin,LOW);            // turn off pin 13 LED
      pulse = false;                         // reset the pulse flag so we can do it again
      amp = P - T;                           // get amplitude of the pulse wave
      thresh = amp/2 + T;                    // set thresh at 50% of the amplitude
      P = thresh;                            // reset these for next time
      T = thresh;
    }

  if (N > 2500)
    {                           // if 2.5 seconds go by without a beat
      thresh = 512;                          // set thresh default
      P = 512;                               // set P default
      T = 512;                               // set T default
      lastBeatTime = sampleCounter;          // bring the lastBeatTime up to date        
      firstBeat = true;                      // set these to avoid noise
      secondBeat = false;                    // when we get the heartbeat back
    }

  sei();                                   // enable interrupts when youre done!
}



void setup() {
  // put your setup code here, to run once:
  Wire.begin();
  Serial.begin(9600);
  pinMode(A0,INPUT);
  pinMode(A1, INPUT);
  gripServo.attach(9);

  normalVal = analogRead(A0);
  

  u8g.setRot180();
  u8g.setColorIndex(1); // pixel on
  u8g.setFont(u8g_font_unifont);
  interruptSetup();
  startupPage();

//  newBPM = String(random(80,90)).c_str();
  
}
const int beatThresh = 5;
int count = beatThresh - 1;
void loop() {
  // put your main code here, to run repeatedly:
  if (qs) {
    serialOutputOnBeat();
    qs = false;
  }
  count++;
  if (count == beatThresh) {
    drawBig = !drawBig;
    count = 0;
  }
  delay(20);

//automatic();
manual();
display();
//  Serial.println(flexVal);
}

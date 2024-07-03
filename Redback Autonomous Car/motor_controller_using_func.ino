//declaring global variables
int rightmotorlogicpin1 = 10;
int rightmotorlogicpin2 = 11;
int leftmotorlogicpin1 = 5;
int leftmotorlogicpin2 = 6;
int pwmDutyCycle = 100;
char ip = 0;

//configures motor pins to output
void initialiseMotorPins(){
  pinMode(rightmotorlogicpin1, OUTPUT);
  pinMode(rightmotorlogicpin2, OUTPUT);
  pinMode(leftmotorlogicpin1, OUTPUT);
  pinMode(leftmotorlogicpin2, OUTPUT);
}

void setup() {
  //set baud rate
  Serial.begin(9600);

  //displaying program name and other details
  Serial.println("--------------------------------------------------------------------------------------");
  Serial.println("Program name: Motor Controller");
  Serial.println("--------------------------------------------------------------------------------------");
  Serial.println("Initializing...");
  
  delay(900);

  //configuring the motor pins
  initialiseMotorPins();
  
  //printing motor pin configuration for wiring
  Serial.println("Right Motor Pin 1 = 5");
  Serial.println("Right Motor Pin 2 = 6");
  Serial.println("Left Motor Pin 1 = 10");
  Serial.println("Left Motor Pin 2 = 11");
  
  Serial.println("Initialization complete!");
  Serial.println("--------------------------------------------------------------------------------------");
  Serial.println("Enter instruction:");
}

//sets value of motor pins according to the direction
void setmotorpins(int rightpin1num, int leftpin1num, int rightpin2num, int leftpin2num){
  analogWrite(rightmotorlogicpin1,rightpin1num);
  analogWrite(leftmotorlogicpin1,leftpin1num);
  analogWrite(rightmotorlogicpin2,rightpin2num);
  analogWrite(leftmotorlogicpin2,leftpin2num);
}

//sends different values of motor pins according to instruction
void forward(){
  Serial.println("Forward!");
  setmotorpins(0,0,pwmDutyCycle,pwmDutyCycle);
}

void backward(){
  Serial.println("Backward!");
  setmotorpins(pwmDutyCycle,pwmDutyCycle,0,0);
}

void left(){
  Serial.println("Turning left!");
  setmotorpins(0,pwmDutyCycle,pwmDutyCycle,0);
}

void right(){
  Serial.println("Turning right!");
  setmotorpins(pwmDutyCycle,0,0,pwmDutyCycle);
}

void stop(){
  Serial.println("Stop!");
  pwmDutyCycle = 0;
  setmotorpins(pwmDutyCycle,0,0,pwmDutyCycle);
}

void exitProgram(){
  Serial.println("Program Terminated!");
  pwmDutyCycle = 0;
  setmotorpins(pwmDutyCycle,0,0,pwmDutyCycle);
}

//prints new changed speed
void changespeed(){
  Serial.print("Speed = ");
  Serial.print(pwmDutyCycle);
  Serial.println("%");
}

void loop() {
  //checking if there is any incoming data
  if (Serial.available() > 0) {
    //reading first character of input data
    char ip = Serial.read();

    //move forward if "f" is entered
    if (ip == 'f' or ip == 'F') {
      forward();
    }

    //move backward if "b" is entered
    else if (ip == 'b' or ip == 'B') {
      backward();
    }

    //turn left if "l" is entered
    else if (ip == 'l' or ip == 'L') {
      left();
    }

    //turn right if "r" is entered
    else if (ip == 'r' or ip == 'R') {
      right();
    }

    //stop robot if "0" is entered
    else if (ip == '0') {
      stop();
    }

    //change speed of robot for next instruction if input is between 1 and 5
    else if(ip == '1'||ip == '2'||ip == '3'||ip == '4'||ip == '5'){
      pwmDutyCycle = ((int(ip)-48)*10);
      changespeed();
    }

    //terminate program if "x" is entered
    else if(ip=='x'){
      // makes robot stop & terminates program
      exitProgram();
      delay(100);
      exit(0);
    }

    //wait for next character to arrive
    delay(1000);
  }
}
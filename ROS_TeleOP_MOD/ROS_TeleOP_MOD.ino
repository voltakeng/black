#define ena 5
#define in1 6
#define in2 7
#define enb 11
#define in3 9
#define in4 10

#include <RedBot.h>
#include <ArduinoHardware.h>
#include <ros.h> 
#include <geometry_msgs/Twist.h> 
#include <std_msgs/Float32.h> 
//#include <Encoder.h>

//Encoder myEncL(2, 27);
//Encoder myEncR(19, 23);
RedBotEncoder encoder = RedBotEncoder(A1,A0);
long oldPositionL  = 0;
long oldPositionR  = 0;
ros::NodeHandle nh;


geometry_msgs::Twist msg;
std_msgs::Float32 encL_msg;
std_msgs::Float32 encR_msg;

ros::Publisher EncL("Enc_L", &encL_msg);
ros::Publisher EncR("Enc_R", &encR_msg);

long newPositionL;
long newPositionR;


  
void roverCallBack(const geometry_msgs::Twist& cmd_vel)
{

	double x = cmd_vel.linear.x;
  double z = cmd_vel.angular.z;

	double moveL = x+(z/2);
	double moveR = x-(z/2);

  
if (moveL>0.0){
        //analogWrite(ena,max(min(moveL*100,60),35));
        analogWrite(ena,(moveL*100));
        digitalWrite(in1,0);digitalWrite(in2,1);
    }else if (moveL<0.0){
	      analogWrite(ena,max(min(abs(moveL)*100,60),35));
        digitalWrite(in1,1);digitalWrite(in2,0);
    }else{ 
	      analogWrite(ena,0);
        digitalWrite(in1,0);digitalWrite(in2,0);
	}

if (moveR>0.0){
        //analogWrite(enb,max(min(moveR*100,60),35)-20);
        analogWrite(enb,(moveR*100)-20);
        digitalWrite(in4,1);digitalWrite(in3,0);
    }else if (moveR<0.0){
	      analogWrite(enb,max(min(abs(moveR)*100,60),35));
        digitalWrite(in4,0);digitalWrite(in3,1);
    }else{ 
	      analogWrite(enb,0);
        digitalWrite(in4,0);digitalWrite(in3,0);
  }

// if(cmd_vel.linear.y>=1.0){ 
// digitalWrite(42,1);
// } else  {
// digitalWrite(42,0);
// }
}
ros::Subscriber <geometry_msgs::Twist> Motor("/cmd_vel", roverCallBack);

void setup()
{
  pinMode(ena,OUTPUT);  pinMode(in1,OUTPUT); pinMode(in2,OUTPUT);
  pinMode(enb,OUTPUT);  pinMode(in3,OUTPUT); pinMode(in4,OUTPUT);
  
//  pinMode(42,OUTPUT); 
//  digitalWrite(42,1); delay(100);
//  digitalWrite(42,0); delay(100);
//  digitalWrite(42,1); delay(100);
//  digitalWrite(42,0); delay(100);

  nh.initNode();
  nh.subscribe(Motor);
  nh.advertise(EncL);
  nh.advertise(EncR);
} 

void loop()
{
//    newPositionL = myEncL.read();
//    newPositionR = myEncR.read()*-1;
    newPositionL = encoder.getTicks(LEFT);
    newPositionR = encoder.getTicks(RIGHT)*-1;
  
  if (newPositionL != oldPositionL) {
      oldPositionL = newPositionL;
      encL_msg.data = newPositionL;
  }
  if (newPositionR != oldPositionR) {
      oldPositionR = newPositionR;
      encR_msg.data = newPositionR;
  }
  
  if((newPositionL>1000000)||(newPositionR>1000000)||(newPositionL<-1000000)||(newPositionR<-1000000)){
//    myEncL.write(0);
//    myEncR.write(0);
      encoder.clearEnc(BOTH);  
  }
  
  EncL.publish( &encL_msg );
  EncR.publish( &encR_msg );
  nh.spinOnce();
  delay(10);
}

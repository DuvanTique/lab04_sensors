/*
 * UltraSoundROS.ino
 * Publica distancias del HC-SR04 como sensor_msgs/Range en ROS
 * Pines: Trig=12, Echo=11
 */

#include <ros.h>
#include <sensor_msgs/Range.h>

// Pines del sensor
#define PIN_TRIG 12
#define PIN_ECHO 11

ros::NodeHandle nh;

sensor_msgs::Range range_msg;
ros::Publisher pub_range("/UltraSound", &range_msg);

// Función de medición
float measureDistance() {
  digitalWrite(PIN_TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(PIN_TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(PIN_TRIG, LOW);

  long duration = pulseIn(PIN_ECHO, HIGH, 30000); // timeout 30 ms
  float distance_m = (duration * 0.000343) / 2.0; // velocidad sonido = 343 m/s
  return distance_m;
}

void setup() {
  pinMode(PIN_TRIG, OUTPUT);
  pinMode(PIN_ECHO, INPUT);

  nh.initNode();
  nh.advertise(pub_range);

  // Rellene los campos estáticos del mensaje
  range_msg.radiation_type = sensor_msgs::Range::ULTRASOUND;
  range_msg.header.frame_id = "/ultrasound";
  range_msg.field_of_view = 0.26;  // ~15 grados en radianes
  range_msg.min_range = 0.02;      // 2 cm mínimo
  range_msg.max_range = 4.00;      // 4 m máximo
}

void loop() {
  range_msg.range = measureDistance();
  range_msg.header.stamp = nh.now();
  pub_range.publish(&range_msg);
  nh.spinOnce();
  delay(100);  // 10 Hz
}

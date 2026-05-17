#!/usr/bin/env python3
"""
Suscriptor de cámara: convierte la imagen ROS a OpenCV,
aplica detección de bordes Canny y la republica.
"""
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

bridge = CvBridge()

def callback(msg):
    # Convertir mensaje ROS → imagen OpenCV
    frame = bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
    
    # Procesamiento: escala de grises + detección de bordes
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    
    # Mostrar en ventana local
    cv2.imshow("Camara original", frame)
    cv2.imshow("Bordes detectados", edges)
    cv2.waitKey(1)

rospy.init_node('image_detector')
rospy.Subscriber('/usb_cam/image_raw', Image, callback)
rospy.spin()

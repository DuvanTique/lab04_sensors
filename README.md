# Laboratorio 04 — Sensores con ROS

**Universidad Nacional de Colombia**  
**Robótica 2026-I**

## Integrantes

- Duvan Stiven Tique Osorio
- Juan Carlos Gonzalez Ibarra
- Àngel Rivera Amòrtegui
- Jesùs Manuel Aragòn Buitrago


## Descripción
Integración de sensores (HC-SR04, cámara web, RPLIDAR C1) con ROS Noetic. 
Incluye procesamiento de datos, visualización en tiempo real y mapeo con Hector SLAM.

## Estructura del repositorio

lab04_sensors/
├── scripts/               # Nodos Python
├── launch/                # Archivos .launch
├── arduino/               # Código Arduino
├── maps/                  # Mapas generados con Hector SLAM
└── resultados/            # Capturas y gráficas

## Actividades realizadas
1. Integración de sensor HC-SR04 con Arduino + rosserial
2. Implementación de cámara web con OpenCV
3. Configuración y análisis del RPLIDAR C1
4. Conversión de datos polares a cartesianos y validación
5. Mapeo con Hector SLAM

## Instrucciones de uso

### Actividad 1 — HC-SR04
```bash
rosrun rosserial_python serial_node.py /dev/ttyACM0
rosrun lab04_sensors ultrasound_validator.py
```

### Actividad 2 — Cámara web
```bash
rosrun usb_cam usb_cam_node
rosrun lab04_sensors image_detector.py
```

### Actividad 3 y 4 — LIDAR
```bash
roslaunch rplidar_ros rplidar_c1.launch
rosrun lab04_sensors lidar_cartesian.py
rosrun lab04_sensors lidar_validator.py
```

### Actividad 5 — Hector SLAM
```bash
roslaunch lab04_sensors hector_slam_c1.launch
```

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
- scripts/               # Nodos Python
-  launch/                # Archivos .launch
- arduino/               # Código Arduino
- maps/                  # Mapas generados con Hector SLAM
- resultados/            # Capturas y gráficas

## Actividades realizadas
1. Integración de sensor HC-SR04 con Arduino + rosserial
2. Implementación de cámara web con OpenCV
3. Configuración y análisis del RPLIDAR C1
4. Conversión de datos polares a cartesianos y validación
5. Mapeo con Hector SLAM

## Actividad 1 — Integración del sensor HC-SR04 mediante comunicación serial
 
### Objetivo
 
Conectar el sensor ultrasónico HC-SR04 a ROS a través de un Arduino UNO usando `rosserial`, publicar las medidas de distancia en un tópico ROS y compararlas con medidas de referencia.
 
### Material necesario
 
- Arduino UNO + cable USB-B
- Sensor HC-SR04
- 3 cables tipo dupont (macho-hembra)
- Regla o cinta métrica (patrón de referencia)
### 1.1 Conexión física del HC-SR04
 
| Pin HC-SR04 | Pin Arduino UNO |
|-------------|-----------------|
| VCC         | 5V              |
| GND         | GND             |
| Trig        | Pin 12          |
| Echo        | Pin 11          |

### Tipo de mensaje usado
 
El sensor publica en el tópico `/UltraSound` mensajes de tipo `sensor_msgs/Range`:
 
| Campo            | Descripción                              | Unidad   |
|------------------|------------------------------------------|----------|
| `header.stamp`   | Timestamp del mensaje                    | s        |
| `header.frame_id`| Marco de referencia del sensor           | —        |
| `radiation_type` | ULTRASOUND (0) o INFRARED (1)            | —        |
| `field_of_view`  | Ángulo del cono de detección             | rad      |
| `min_range`      | Distancia mínima medible                 | m        |
| `max_range`      | Distancia máxima medible                 | m        |
| `range`          | **Distancia medida** (valor principal)   | m        |
 
Frecuencia de publicación: **10 Hz** (configurable en el `delay()` del Arduino).
 
---



```bash
rosrun rosserial_python serial_node.py /dev/ttyACM0
rosrun lab04_sensors ultrasound_validator.py
```

## Actividad 2 — Implementación de cámara web
 
### Objetivo
 
Integrar una cámara web estándar al workspace de ROS, visualizar la imagen en tiempo real y demostrar que el flujo es idéntico para cualquier cámara de mayor prestación.

### Explorar los tópicos disponibles
 
```bash
rostopic list
```
 
Los tópicos principales publicados son:
 
| Tópico                        | Tipo de mensaje              | Descripción                     |
|-------------------------------|------------------------------|---------------------------------|
| `/usb_cam/image_raw`          | `sensor_msgs/Image`          | Imagen cruda sin comprimir      |
| `/usb_cam/image_raw/compressed` | `sensor_msgs/CompressedImage`| Imagen JPEG comprimida         |
| `/usb_cam/camera_info`        | `sensor_msgs/CameraInfo`     | Parámetros intrínsecos cámara   |
 
La estructura del mensaje de imagen es:
```bash
rostopic echo /usb_cam/image_raw | head -40
```
 
Campos principales de `sensor_msgs/Image`:
 
| Campo       | Descripción                         | Unidades |
|-------------|-------------------------------------|----------|
| `height`    | Filas de píxeles                    | px       |
| `width`     | Columnas de píxeles                 | px       |
| `encoding`  | Formato de color (bgr8, rgb8, mono8)| —        |
| `step`      | Bytes por fila                      | bytes    |
| `data`      | Arreglo plano de valores de píxel   | uint8[]  |
 
Frecuencia típica: **30 Hz**.

```bash
rosrun usb_cam usb_cam_node
rosrun lab04_sensors image_detector.py
```

## Actividad 3 — Configuración y análisis de datos del LIDAR (RPLIDAR C1)
### Tópicos activos y tipos de mensaje
 
```bash
rostopic list
rostopic info /scan
```
 
Tópicos publicados por el RPLIDAR C1:
 
| Tópico   | Tipo de mensaje        | Descripción                              |
|----------|------------------------|------------------------------------------|
| `/scan`  | `sensor_msgs/LaserScan`| Barrido completo 360° del LIDAR          |


#### Estructura de `sensor_msgs/LaserScan`
 
```
sensor_msgs/LaserScan
  Header header
    uint32 seq
    time stamp
    string frame_id          # "laser" por defecto
  float32 angle_min          # Ángulo inicio del barrido [rad]
  float32 angle_max          # Ángulo fin del barrido [rad]
  float32 angle_increment    # Resolución angular [rad/muestra]
  float32 time_increment     # Tiempo entre muestras [s]
  float32 scan_time          # Duración de un barrido completo [s]
  float32 range_min          # Distancia mínima válida [m]
  float32 range_max          # Distancia máxima válida [m]
  float32[] ranges           # Arreglo de distancias medidas [m]
  float32[] intensities      # Intensidades de retorno (si disponible)
```
 
| Parámetro típico RPLIDAR C1 | Valor               |
|-----------------------------|---------------------|
| `angle_min`                 | −π (−3.1416 rad)    |
| `angle_max`                 | +π (+3.1416 rad)    |
| `angle_increment`           | ~0.0175 rad (~1°)   |
| `scan_time`                 | ~0.1 s (10 Hz)      |
| `range_min`                 | 0.15 m              |
| `range_max`                 | 12.0 m              |
| Número de muestras          | ~360 por barrido    |
| Frecuencia de actualización | **10 Hz**           |

## Actividad 4 — Procesamiento de datos y validación de medidas
 
### 4.1 Crear el entorno controlado (laberinto)
 
Construya un recinto rectangular sencillo con cartón o madera. Coloque un objeto de geometría conocida (ej.: una caja cuadrada de 20 cm × 20 cm o una regla plana de 30 cm) dentro del campo de visión del LIDAR y tome sus medidas reales con un pie de rey o cinta métrica.

### Nodo de conversión LaserScan → coordenadas cartesianas
 
El modelo matemático de la transformación polar → cartesiana es:
 
```
x_i = r_i · cos(θ_i)
y_i = r_i · sin(θ_i)
 
donde:
  r_i = ranges[i]        (distancia al punto i, en metros)
  θ_i = angle_min + i · angle_increment   (ángulo del punto i, en radianes)
```


```bash
roslaunch rplidar_ros rplidar_c1.launch
rosrun lab04_sensors lidar_cartesian.py
rosrun lab04_sensors lidar_validator.py
```

### Actividad 5 — Hector SLAM
```bash
roslaunch lab04_sensors hector_slam_c1.launch
```

#!/usr/bin/env python3
"""
Captura N muestras del LIDAR en la dirección de un objeto
y calcula el error respecto a la medida real.

Objeto: ubíquelo frente al LIDAR (ángulo ~0 rad = dirección X+)
"""
import rospy
import numpy as np
from sensor_msgs.msg import LaserScan

muestras = []
CAPTURAR = True
N_MUESTRAS = 50            # Número de barridos a promediar
ANGULO_OBJETO_DEG = 0.0    # Cambie al ángulo donde está el objeto (grados)

def callback(msg):
    global muestras, CAPTURAR
    if not CAPTURAR:
        return

    angle_rad = np.deg2rad(ANGULO_OBJETIVO_DEG)
    angle_min = msg.angle_min
    angle_inc = msg.angle_increment

    # Índice del ángulo objetivo
    idx = int((angle_rad - angle_min) / angle_inc)
    idx = max(0, min(idx, len(msg.ranges) - 1))

    # Promediar 5 rayos alrededor del índice central (±2)
    ventana = msg.ranges[max(0, idx-2):idx+3]
    validos = [r for r in ventana if msg.range_min <= r <= msg.range_max]

    if validos:
        muestras.append(np.mean(validos))
        rospy.loginfo(f"Muestra {len(muestras)}/{N_MUESTRAS}: {np.mean(validos)*100:.2f} cm")

    if len(muestras) >= N_MUESTRAS:
        CAPTURAR = False

ANGULO_OBJETIVO_DEG = ANGULO_OBJETO_DEG

def main():
    rospy.init_node('lidar_validator')
    real_cm = float(input("Ingrese la distancia real al objeto (cm): "))

    rospy.Subscriber('/scan', LaserScan, callback)

    print(f"\nCapturando {N_MUESTRAS} muestras...")
    while not rospy.is_shutdown() and CAPTURAR:
        rospy.sleep(0.1)

    if muestras:
        media   = np.mean(muestras) * 100
        std_dev = np.std(muestras)  * 100
        error   = abs(media - real_cm) / real_cm * 100

        print("\n╔══════════════════════════════════════════╗")
        print(  "║     TABLA COMPARATIVA LIDAR vs PIE REY  ║")
        print(  "╠══════════════════════════════════════════╣")
        print(f"║  Distancia real (pie de rey)  : {real_cm:7.2f} cm ║")
        print(f"║  Media LIDAR ({N_MUESTRAS} muestras) : {media:7.2f} cm ║")
        print(f"║  Desviación estándar          : {std_dev:7.2f} cm ║")
        print(f"║  Error porcentual             : {error:7.2f} %  ║")
        print(  "╚══════════════════════════════════════════╝")

if __name__ == '__main__':
    main()
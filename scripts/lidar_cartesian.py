#!/usr/bin/env python3
import rospy
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from sensor_msgs.msg import LaserScan

xs_global, ys_global = [], []
datos_nuevos = False

def laserscan_callback(msg):
    global xs_global, ys_global, datos_nuevos

    angle_min = msg.angle_min
    angle_inc = msg.angle_increment
    rng_min   = msg.range_min
    rng_max   = msg.range_max

    xs, ys = [], []
    for i, r in enumerate(msg.ranges):
        if rng_min <= r <= rng_max:
            theta = angle_min + i * angle_inc
            x = r * np.cos(theta)
            y = r * np.sin(theta)
            xs.append(x)
            ys.append(y)

    xs_global = xs
    ys_global = ys
    datos_nuevos = True

def main():
    global datos_nuevos

    rospy.init_node('lidar_cartesian', anonymous=True)
    rospy.Subscriber('/scan', LaserScan, laserscan_callback)

    plt.ion()
    fig, ax = plt.subplots(figsize=(8, 8))
    scatter = ax.scatter([], [], s=1, c='cyan')
    ax.set_xlim(-6, 6)
    ax.set_ylim(-6, 6)
    ax.set_xlabel('X [m]')
    ax.set_ylabel('Y [m]')
    ax.set_title('RPLIDAR C1 — Coordenadas Cartesianas')
    ax.set_facecolor('#111111')
    fig.patch.set_facecolor('#222222')
    ax.tick_params(colors='white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.title.set_color('white')
    ax.plot(0, 0, 'ro', markersize=6, label='LIDAR')

    legend = ax.legend(facecolor='#333333')
    for text in legend.get_texts():
        text.set_color('white')

    ax.grid(True, color='#444444')

    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        if datos_nuevos and xs_global:
            scatter.set_offsets(np.c_[xs_global, ys_global])
            fig.canvas.draw()
            fig.canvas.flush_events()
            datos_nuevos = False
        rate.sleep()

    plt.ioff()
    plt.show()

if __name__ == '__main__':
    main()

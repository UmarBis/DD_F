#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class ApproachWall:
    def __init__(self):
        # Целевое расстояние до стены (50 см = 0.5 м)
        self.target_distance = 0.5
        
        # Максимальная скорость (м/с)
        self.max_speed = 0.22
        
        # Инициализация ноды
        rospy.init_node('approach_wall_node', anonymous=True)
        
        # Издатель для управления движением
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        
        # Подписчик на данные лидара
        rospy.Subscriber('/scan', LaserScan, self.callback)
        
        rospy.loginfo("Робот начал движение к стене...")
        rospy.loginfo(f"Целевое расстояние: {self.target_distance} м")
    
    def callback(self, scan):
        # Берем расстояние перед роботом (центральный луч - 0 градусов)
        # Обычно scan.ranges[0] или scan.ranges[len(scan.ranges)//2]
        front_distance = scan.ranges[0]
        
        # Создаем сообщение скорости
        vel = Twist()
        
        # Если расстояние больше целевого - едем вперед
        if front_distance > self.target_distance:
            vel.linear.x = self.max_speed
            rospy.loginfo(f"Расстояние до стены: {front_distance:.2f} м -> Едем вперед")
        else:
            vel.linear.x = 0.0
            rospy.loginfo(f"Расстояние до стены: {front_distance:.2f} м -> СТОП! Цель достигнута")
        
        # Публикуем команду скорости
        self.pub.publish(vel)

if __name__ == '__main__':
    try:
        wall_approach = ApproachWall()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass

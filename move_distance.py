#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

class MoveDistance:
    def __init__(self):
        # Целевое расстояние (2 м 30 см = 2.3 м)
        self.target_distance = 2.3
        
        # Минимальная скорость (м/с)
        self.min_speed = 0.05
        
        # Начальная позиция
        self.start_x = None
        
        # Флаг достижения цели
        self.goal_reached = False
        
        # Инициализация ноды
        rospy.init_node('move_distance_node', anonymous=True)
        
        # Издатель для управления движением
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        
        # Подписчик на данные одометрии
        rospy.Subscriber('/odom', Odometry, self.callback)
        
        rospy.loginfo(f"Робот начал движение...")
        rospy.loginfo(f"Целевое расстояние: {self.target_distance} м")
        rospy.loginfo(f"Скорость: {self.min_speed} м/с")
    
    def callback(self, odom):
        # Получаем текущую позицию по X
        current_x = odom.pose.pose.position.x
        
        # Запоминаем стартовую позицию при первом получении данных
        if self.start_x is None:
            self.start_x = current_x
            rospy.loginfo(f"Стартовая позиция: {self.start_x:.2f} м")
        
        # Вычисляем пройденное расстояние
        distance_traveled = current_x - self.start_x
        
        # Создаем сообщение скорости
        vel = Twist()
        
        # Если цель не достигнута - едем
        if not self.goal_reached:
            if distance_traveled < self.target_distance:
                vel.linear.x = self.min_speed
                rospy.loginfo(f"Пройдено: {distance_traveled:.2f} / {self.target_distance} м")
            else:
                vel.linear.x = 0.0
                self.goal_reached = True
                rospy.loginfo(f"Цель достигнута! Пройдено: {distance_traveled:.2f} м")
        else:
            vel.linear.x = 0.0
        
        # Публикуем команду скорости
        self.pub.publish(vel)

if __name__ == '__main__':
    try:
        mover = MoveDistance()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass

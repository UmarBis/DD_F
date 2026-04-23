#!/usr/bin/env python3

import rospy
from std_msgs.msg import Int32
import random

def numbers_publisher():
    # Инициализация ноды
    rospy.init_node('numbers_publisher_node', anonymous=True)
    
    # Создание издателя для топика /numbers с типом Int32
    pub = rospy.Publisher('/numbers', Int32, queue_size=10)
    
    # Частота публикации: 5 Гц (0.2 секунды)
    rate = rospy.Rate(5)
    
    rospy.loginfo("Начата публикация случайных чисел в топик /numbers")
    
    while not rospy.is_shutdown():
        # Генерация случайного числа от 1 до 99
        random_number = random.randint(1, 99)
        
        # Создание сообщения
        msg = Int32()
        msg.data = random_number
        
        # Публикация сообщения
        pub.publish(msg)
        
        # Логирование для отладки
        rospy.loginfo(f"Опубликовано число: {random_number}")
        
        # Пауза для поддержания частоты 5 Гц
        rate.sleep()

if __name__ == '__main__':
    try:
        numbers_publisher()
    except rospy.ROSInterruptException:
        pass

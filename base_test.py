#!/usr/bin/env python3

import rospy
from std_msgs.msg import Int32

class NumbersProcessor:
    def __init__(self):
        # Инициализация ноды
        rospy.init_node('numbers_processor_node', anonymous=True)
        
        # Список для хранения полученных чисел
        self.numbers_buffer = []
        
        # Подписчик на топик /numbers
        self.subscriber = rospy.Subscriber('/numbers', Int32, self.callback)
        
        rospy.loginfo("Подписчик на топик /numbers запущен")
        rospy.loginfo("Ожидание получения 5 чисел для расчета среднего...")
    
    def callback(self, msg):
        # Добавляем полученное число в буфер
        self.numbers_buffer.append(msg.data)
        rospy.loginfo(f"Получено число: {msg.data} (в буфере: {len(self.numbers_buffer)}/5)")
        
        # Проверяем, набралось ли 5 чисел
        if len(self.numbers_buffer) == 5:
            # Расчет среднего арифметического
            average = sum(self.numbers_buffer) / len(self.numbers_buffer)
            
            # Вывод результата
            rospy.loginfo("=" * 50)
            rospy.loginfo(f"Получена последовательность: {self.numbers_buffer}")
            rospy.loginfo(f"Среднее арифметическое: {average:.2f}")
            rospy.loginfo("=" * 50)
            
            # Очищаем буфер для следующей последовательности
            self.numbers_buffer = []
            rospy.loginfo("Начинаем расчет новой последовательности...")

if __name__ == '__main__':
    try:
        processor = NumbersProcessor()
        rospy.spin()  # Держит программу запущенной
    except rospy.ROSInterruptException:
        pass

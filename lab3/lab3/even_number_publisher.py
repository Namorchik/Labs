import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

class EvenNumberPublisher(Node):
    def __init__(self):
        super().__init__('even_pub')
        
        # Объявляем параметры
        self.declare_parameter('publish_frequency', 10.0)
        self.declare_parameter('overflow_threshold', 100)
        self.declare_parameter('topic_name', 'even_numbers')
        
        # Читаем их
        self.freq = self.get_parameter('publish_frequency').value
        self.threshold = self.get_parameter('overflow_threshold').value
        self.topic = self.get_parameter('topic_name').value

        self.publisher_ = self.create_publisher(Int32, self.topic, 10)
        self.overflow_publisher_ = self.create_publisher(Int32, 'overflow', 10)
        
        self.current_number = 0
        self.timer = self.create_timer(1.0 / self.freq, self.timer_callback)
        self.get_logger().info(f"Узел запущен! Частота: {self.freq} Гц, Порог: {self.threshold}")

    def timer_callback(self):
        msg = Int32()
        msg.data = self.current_number
        self.publisher_.publish(msg)
        self.get_logger().info(f'Публикую: {msg.data}')
        
        self.current_number += 2
        
        if self.current_number >= self.threshold:
            overflow_msg = Int32()
            overflow_msg.data = self.current_number
            self.overflow_publisher_.publish(overflow_msg)
            self.current_number = 0

def main(args=None):
    rclpy.init(args=args)
    node = EvenNumberPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
#!/usr/bin/env python3
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    # 1. Объявляем аргумент mode
    mode_arg = DeclareLaunchArgument(
        'mode',
        default_value='fast',
        description='Режим работы: fast или slow'
    )

    # 2. Получаем значение аргумента
    mode = LaunchConfiguration('mode')

    # 3. Настраиваем параметры на основе режима
    # В launch-файлах мы не можем использовать обычные if/else для LaunchConfiguration напрямую,
    # поэтому используем PythonExpression (встроенная функция запуска).
    # Но проще сделать это через словарь параметров, который ROS 2 умеет обрабатывать.
    # Однако, для простоты и наглядности, мы сделаем два разных узла (один запустится, другой нет), 
    # либо используем PythonExpression.
    
    # Простой и надежный способ для учебной задачи:
    # Мы передадим параметры через PythonExpression, чтобы они вычислялись на лету.
    from launch.substitutions import PythonExpression

    frequency = PythonExpression(["20.0 if '", mode, "' == 'fast' else 5.0"])
    threshold = PythonExpression(["50 if '", mode, "' == 'fast' else 150"])
    topic = PythonExpression(["'/even_numbers_fast' if '", mode, "' == 'fast' else '/even_numbers_slow'"])

    return LaunchDescription([
        mode_arg,
        Node(
            package='lab3',
            executable='even_publisher',
            name='even_pub',
            output='screen',
            parameters=[
                {'publish_frequency': frequency},
                {'overflow_threshold': threshold},
                {'topic_name': topic},
            ]
        ),
        Node(
            package='lab3',
            executable='overflow_listener',
            name='overflow_listener',
            output='screen',
            parameters=[
                # Для слушателя мы тоже можем динамически менять топик,
                # но в задании сказано просто слушать переполнение. 
                # По умолчанию он слушает 'overflow'. 
                # В режиме fast топик публикатора /even_numbers_fast, но overflow остается 'overflow'.
                # Если хотите, чтобы слушатель тоже менял имя топика, можно добавить логику.
                # Оставим стандартный.
                {'overflow_topic': 'overflow'} 
            ]
        ),
    ])
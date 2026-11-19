from setuptools import find_packages, setup

package_name = 'lab3'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Добавляем путь к launch-файлам:
        ('share/' + package_name + '/launch', ['launch/robot_system.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='namor',
    maintainer_email='namor@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'even_publisher = lab3.even_number_publisher:main',
            'overflow_listener = lab3.overflow_listener:main',
        ],
    },
)
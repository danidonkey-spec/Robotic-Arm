from setuptools import find_packages, setup
from glob import glob
import os
package_name = 'ur5_lab_world'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*.py')),
        ('share/' + package_name + '/worlds', glob('worlds/*.sdf')),
        ('share/' + package_name + '/models/table', glob('models/table/*')),
        ('share/' + package_name + '/models/realsense_rgbd', glob('models/realsense_rgbd/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='daniel',
    maintainer_email='daniel.zioni8@gmail.com',
    description='UR5 lab world for Gazebo simulation',
    license='Apache-2.0',
    
)

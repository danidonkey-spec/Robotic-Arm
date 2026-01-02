import os
from launch import LaunchDescription
from launch.actions import SetEnvironmentVariable, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node

def generate_launch_description():
    pkg_world = get_package_share_directory('ur5_lab_world')
    pkg_ur_sim = get_package_share_directory('ur_simulation_gz')

    # 1) Gazebo resource path (כדי שימצא model://table וכו')
    gz_path = os.pathsep.join([
        os.path.join(pkg_world, 'models'),
        os.path.join(pkg_world, 'worlds'),
        os.environ.get('GZ_SIM_RESOURCE_PATH', ''),
    ]).strip(os.pathsep)

    set_gz = SetEnvironmentVariable('GZ_SIM_RESOURCE_PATH', gz_path)

    # 2) UR5 + MoveIt + Gazebo (אבל עם world_file שלך)
    ur_moveit = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ur_sim, 'launch', 'ur_sim_moveit.launch.py')
        ),
        launch_arguments={
            'ur_type': 'ur5',
            'world_file': os.path.join(pkg_world, 'worlds', 'lab.sdf'),
        }.items()
    )

    # 3) Bridge למצלמה (Gazebo <-> ROS) — לפי התחביר הרשמי /TOPIC@ROS@GZ :contentReference[oaicite:4]{index=4}
    camera_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/camera/camera_info@sensor_msgs/msg/CameraInfo@gz.msgs.CameraInfo',
            '/camera/depth_image@sensor_msgs/msg/Image@gz.msgs.Image',
            '/camera/points@sensor_msgs/msg/PointCloud2@gz.msgs.PointCloudPacked',
        ],
        output='screen'
    )

    return LaunchDescription([
        set_gz,
        ur_moveit,
        camera_bridge,
    ])

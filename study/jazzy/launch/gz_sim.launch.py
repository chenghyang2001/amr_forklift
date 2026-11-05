"""
gz_sim.launch.py
================
amr_forklift（nebula_agv）在 ROS 2 Jazzy + Gazebo Harmonic（gz sim 8）的模擬啟動檔。
對應原作者 Humble + Gazebo Classic 版的 launch/gazebo.launch.py。

用法：
  ros2 launch amr_forklift gz_sim.launch.py
  ros2 launch amr_forklift gz_sim.launch.py gz_flags:="-r -s" use_rviz:=false   # 只開伺服器
"""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

# gz ↔ ROS 橋接清單：'[' 表示 gz→ROS，']' 表示 ROS→gz（只有 cmd_vel 是往模擬器送）
BRIDGE_TOPICS = [
    '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
    '/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
    '/left_sensor/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
    '/right_sensor/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
    '/imu/data_raw@sensor_msgs/msg/Imu[gz.msgs.IMU',
    '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry',
    '/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V',
    '/joint_states@sensor_msgs/msg/JointState[gz.msgs.Model',
    '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',
]


def generate_launch_description():
    pkg_share = get_package_share_directory('amr_forklift')
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')

    world_path = os.path.join(pkg_share, 'worlds', 'nebula_arena_gz.world')
    xacro_file = os.path.join(pkg_share, 'models', 'nebula_urdf', 'model_gz.xacro')
    rviz_config = os.path.join(pkg_share, 'rviz', 'config.rviz')

    use_rviz = LaunchConfiguration('use_rviz')
    gz_flags = LaunchConfiguration('gz_flags')

    # gz 解析 package://amr_forklift/... 時是在資源路徑下找「amr_forklift」資料夾，
    # 所以要加的是 share 的上一層，而不是套件 share 本身
    existing_resource_path = os.environ.get('GZ_SIM_RESOURCE_PATH', '')
    resource_paths = [os.path.dirname(pkg_share)]
    if existing_resource_path:
        resource_paths.append(existing_resource_path)
    set_gz_resource = SetEnvironmentVariable('GZ_SIM_RESOURCE_PATH', os.pathsep.join(resource_paths))

    declared_arguments = [
        DeclareLaunchArgument('use_rviz', default_value='true',
                              description='是否開啟 RViz2'),
        DeclareLaunchArgument('gz_flags', default_value='-r',
                              description='傳給 gz sim 的旗標；"-r -s" 只開伺服器（無 GUI）'),
    ]

    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')),
        launch_arguments={
            'gz_args': [gz_flags, ' ', world_path],
            'on_exit_shutdown': 'true',
        }.items(),
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': ParameterValue(Command(['xacro ', xacro_file]), value_type=str),
            'use_sim_time': True,
        }],
    )

    # 生成位置與原 Classic 版 spawn_entity 相同，確保兩版地圖座標一致
    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-topic', 'robot_description',
            '-name', 'nebula_agv',
            '-x', '-6.0',
            '-y', '-3.8',
            '-z', '0.15',
            '-Y', '-1.5708',
        ],
        output='screen',
    )

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=BRIDGE_TOPICS,
        parameters=[{'use_sim_time': True}],
        output='screen',
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config],
        condition=IfCondition(use_rviz),
        parameters=[{'use_sim_time': True}],
        output='screen',
    )

    # Nav2 costmap 吃的是 /scan_filtered，沒有這個節點導航會看不到障礙物
    scan_filter_node = Node(
        package='amr_forklift',
        executable='scan_filter_node',
        name='scan_filter_node',
        parameters=[{'use_sim_time': True}],
        output='screen',
    )

    return LaunchDescription(declared_arguments + [
        set_gz_resource,
        gz_sim,
        robot_state_publisher,
        spawn_robot,
        bridge,
        rviz_node,
        scan_filter_node,
    ])

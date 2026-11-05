"""
slam_nav_gz.launch.py
=====================
SLAM + Nav2 一起跑（Jazzy 版），對應原作者的 launch/slam_nav.launch.py。

slam_toolbox 持續做雷射比對產生 map→odom，所以不需要 AMCL、也不用手動 2D Pose Estimate。
Nav2 參數改用 config/navigation_jazzy.yaml（以 Jazzy 官方 nav2_params.yaml 為底），
因為原 Humble 版參數缺 Jazzy 新增節點的設定，lifecycle manager 會起不來。

用法（gz_sim.launch.py 已經在跑時）：
  ros2 launch amr_forklift slam_nav_gz.launch.py
"""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    pkg_amr_forklift = get_package_share_directory('amr_forklift')
    pkg_slam = get_package_share_directory('slam_toolbox')
    pkg_nav2 = get_package_share_directory('nav2_bringup')

    use_sim_time = LaunchConfiguration('use_sim_time')
    nav2_params = os.path.join(pkg_amr_forklift, 'config', 'navigation_jazzy.yaml')
    slam_params = os.path.join(pkg_amr_forklift, 'config', 'slam_toolbox_mapping.yaml')

    # 1) SLAM Toolbox：發布 /map 並持續提供 map→odom
    slam = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(pkg_slam, 'launch', 'online_async_launch.py')),
        launch_arguments={
            'slam_params_file': slam_params,
            'use_sim_time': use_sim_time,
        }.items(),
    )

    # 2) Nav2 導航（只有規劃／控制，不含 amcl 與 map_server，地圖由 SLAM 提供）
    navigation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(pkg_nav2, 'launch', 'navigation_launch.py')),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'params_file': nav2_params,
            'autostart': 'true',
        }.items(),
    )

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='true',
                              description='模擬用 true，實車用 false'),
        slam,
        navigation,
    ])

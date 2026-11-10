import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    use_sim_time_arg = DeclareLaunchArgument(
        "use_sim_time",
        default_value="true",
        description="Use simulation (Gazebo) clock if true",
    )

    use_sim_time = LaunchConfiguration("use_sim_time")
    pkg_share = get_package_share_directory("volcanibot_localization")
    ekf_config = os.path.join(pkg_share, "config", "ekf.yaml")

    imu_republisher_node = Node(
        package="volcanibot_localization",
        executable="imu_republisher.py",
        name="imu_republisher_node",
        output="screen",
        parameters=[{"use_sim_time": use_sim_time}],
    )

    robot_localization_node = Node(
        package="robot_localization",
        executable="ekf_node",
        name="ekf_filter_node",
        output="screen",
        parameters=[
            ekf_config,
            {"use_sim_time": use_sim_time},
        ],
    )

    return LaunchDescription([
        use_sim_time_arg,
        imu_republisher_node,
        robot_localization_node,
    ])

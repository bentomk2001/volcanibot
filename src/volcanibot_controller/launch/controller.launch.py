from launch import LaunchDescription
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():

    use_sim_time_arg = DeclareLaunchArgument(
        "use_sim_time",
        default_value="True",
    )

    use_sim_time = LaunchConfiguration("use_sim_time")
    pkg_share = get_package_share_directory("volcanibot_controller")
    params_file = os.path.join(pkg_share, "config", "volcanibot_controllers.yaml")

    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "--controller-manager", "/controller_manager"],
        parameters=[{"use_sim_time": use_sim_time}],
    )

    base_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "volcanibot_controller", 
            "--controller-manager", 
            "/controller_manager",
            "--param-file", params_file
        ],
        parameters=[{"use_sim_time": use_sim_time}],
    )

    return LaunchDescription([
        use_sim_time_arg,
        joint_state_broadcaster_spawner,
        base_controller_spawner,
    ])
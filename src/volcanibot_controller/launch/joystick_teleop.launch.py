import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.actions import IncludeLaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    
    volcanibot_controller_pkg = get_package_share_directory('volcanibot_controller')

    use_sim_time_arg = DeclareLaunchArgument(name="use_sim_time", default_value="True",
                                      description="Use simulated time"
    )
    
    joy_teleop = Node(
        package="joy_teleop",
        executable="joy_teleop",
        parameters=[os.path.join(volcanibot_controller_pkg, "config", "joy_teleop.yaml"),
                    {"use_sim_time": LaunchConfiguration("use_sim_time")}],
    )

    joy_node = Node(
        package="joy",
        executable="joy_node",
        name="joystick",
        parameters=[os.path.join(volcanibot_controller_pkg, "config", "joy_config.yaml"),
                    {"use_sim_time": LaunchConfiguration("use_sim_time")}]
    )
    
    twist_mux_node = Node(
        package="twist_mux",
        executable="twist_mux",
        name="twist_mux",
        output="screen",
        remappings=[("/cmd_vel_out", "/volcanibot_controller/cmd_vel")],
        parameters=[
            os.path.join(volcanibot_controller_pkg, "config", "twist_mux_locks.yaml"),
            os.path.join(volcanibot_controller_pkg, "config", "twist_mux_topics.yaml"),
            {"use_sim_time": LaunchConfiguration("use_sim_time")},
            {"use_stamped": True},
        ],
    )

    return LaunchDescription(
        [
            use_sim_time_arg,
            joy_teleop,
            joy_node,
            twist_mux_node,
        ]
    )
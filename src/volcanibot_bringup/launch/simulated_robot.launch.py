import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition, UnlessCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    use_sim_time_arg = DeclareLaunchArgument(
        "use_sim_time",
        default_value="true",
        description="Use simulation (Gazebo) clock if true",
    )

    world_name_arg = DeclareLaunchArgument(
        "world_name",
        default_value="small_house",
        description="Gazebo world name (empty, small_house, small_warehouse)",
    )

    use_slam_arg = DeclareLaunchArgument(
        "use_slam",
        default_value="true",
        description="Whether to run SLAM (true) or localization on a saved map (false)",
    )

    use_rviz_arg = DeclareLaunchArgument(
        "use_rviz",
        default_value="true",
        description="Whether to launch RViz2",
    )

    use_sim_time = LaunchConfiguration("use_sim_time")
    world_name = LaunchConfiguration("world_name")
    use_slam = LaunchConfiguration("use_slam")
    use_rviz = LaunchConfiguration("use_rviz")

    # 1. Gazebo Simulation + Robot State Publisher + ROS-Gazebo Bridge
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("volcanibot_description"),
                "launch",
                "gazebo.launch.py",
            )
        ),
        launch_arguments={
            "world_name": world_name,
        }.items(),
    )

    # 2. ros2_control Spawners (joint_state_broadcaster & volcanibot_controller)
    controller = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("volcanibot_controller"),
                "launch",
                "controller.launch.py",
            )
        ),
        launch_arguments={
            "use_sim_time": use_sim_time,
        }.items(),
    )

    # 3. Joystick Teleop + Twist Mux
    joystick = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("volcanibot_controller"),
                "launch",
                "joystick_teleop.launch.py",
            )
        ),
        launch_arguments={
            "use_sim_time": use_sim_time,
        }.items(),
    )

    # 4. Local Localization (IMU Republisher + EKF for odom -> base_footprint)
    local_localization = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("volcanibot_localization"),
                "launch",
                "local_localization.launch.py",
            )
        ),
        launch_arguments={
            "use_sim_time": use_sim_time,
        }.items(),
    )

    # 5a. SLAM Mapping (runs when use_slam:=true)
    slam = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("volcanibot_mapping"),
                "launch",
                "slam.launch.py",
            )
        ),
        launch_arguments={
            "use_sim_time": use_sim_time,
            "use_rviz": use_rviz,
        }.items(),
        condition=IfCondition(use_slam),
    )

    # 5b. Global Localization / AMCL & Nav2 (to be uncommented when implemented, runs when use_slam:=false)
    # global_localization = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource(
    #         os.path.join(
    #             get_package_share_directory("volcanibot_localization"),
    #             "launch",
    #             "global_localization.launch.py",
    #         )
    #     ),
    #     launch_arguments={
    #         "use_sim_time": use_sim_time,
    #     }.items(),
    #     condition=UnlessCondition(use_slam),
    # )

    return LaunchDescription([
        use_sim_time_arg,
        world_name_arg,
        use_slam_arg,
        use_rviz_arg,
        gazebo,
        controller,
        joystick,
        local_localization,
        slam,
        # global_localization,
    ])


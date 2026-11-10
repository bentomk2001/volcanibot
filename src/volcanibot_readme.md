# VolcaniBot Workspace

4-wheeled differential-drive autonomous agricultural robot utilizing encoders, IMU, and LiDAR.

## Environment & Build Commands

* Simulator: Gazebo

* Build workspace: `colcon build`

* Build specific package: `colcon build --packages-select <pkg_name>`

* Source environment: `source install/setup.bash`

* Launch Simulation: `ros2 launch volcanibot_description gazebo.launch.py use_sim_time:=true`

* Launch Controllers: `ros2 launch volcanibot_controller controller.launch.py use_sim_time:=true`

* Launch Localization (EKF): `ros2 launch volcanibot_localization local_localization.launch.py use_sim_time:=true`

## Workspace Package Map (`src/`)

* `volcanibot_description` (CMake): URDF/Xacro robot models, Gazebo launch files, maps, and worlds.

* `volcanibot_controller` (CMake): Core control logic and differential drive control, with nodes written in Python.

* `volcanibot_localization` (CMake): Sensor fusion and state estimation using `robot_localization` (Extended Kalman Filter fusing wheel odometry and IMU) and Python IMU covariance preprocessing.

## Coding Conventions & AI Prompting Rules

* **Models:** Always edit `.xacro` files; never hardcode changes into raw `.urdf` files.

* **Languages & Build System:** Both packages use `ament_cmake`. Python nodes inside the controller package must be properly installed via `CMakeLists.txt`.

* **Simulation Time:** All Gazebo-related launch files and nodes *must* run with `use_sim_time: true`.

* **Dependency Management:** Whenever generating or adding new code, ALWAYS automatically add the required dependencies to the corresponding `CMakeLists.txt` and `package.xml` files.

* **Description Config:** Ensure `launch`, `urdf`, `worlds`, `maps`, and `meshes` directories are installed in `CMakeLists.txt`.

* **Terminal Commands:** Never execute terminal commands (`run_command`) without explicit user permission.

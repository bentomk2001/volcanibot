#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu


class ImuRepublisher(Node):
    """Republishes Gazebo IMU messages with explicit frame_id and covariance matrices for EKF."""

    def __init__(self):
        super().__init__("imu_republisher_node")

        self.declare_parameter("frame_id", "imu_link")
        self.declare_parameter("orientation_variance", 1.0e-4)
        self.declare_parameter("angular_velocity_variance", 4.0e-8)      # (2e-4 rad/s)^2
        self.declare_parameter("linear_acceleration_variance", 2.89e-4)  # (1.7e-2 m/s^2)^2

        self.frame_id = self.get_parameter("frame_id").value
        ori_var = float(self.get_parameter("orientation_variance").value)
        ang_vel_var = float(self.get_parameter("angular_velocity_variance").value)
        lin_acc_var = float(self.get_parameter("linear_acceleration_variance").value)

        # 3x3 diagonal covariance matrices flattened in row-major order
        self.orientation_cov = [
            ori_var, 0.0, 0.0,
            0.0, ori_var, 0.0,
            0.0, 0.0, ori_var,
        ]
        self.angular_velocity_cov = [
            ang_vel_var, 0.0, 0.0,
            0.0, ang_vel_var, 0.0,
            0.0, 0.0, ang_vel_var,
        ]
        self.linear_acceleration_cov = [
            lin_acc_var, 0.0, 0.0,
            0.0, lin_acc_var, 0.0,
            0.0, 0.0, lin_acc_var,
        ]

        self.imu_pub = self.create_publisher(Imu, "imu_ekf", 10)
        self.imu_sub = self.create_subscription(Imu, "imu", self.imu_callback, 10)

        self.get_logger().info(
            f"IMU Republisher started: /imu -> /imu_ekf (frame_id='{self.frame_id}')"
        )

    def imu_callback(self, msg: Imu):
        msg.header.frame_id = self.frame_id
        msg.orientation_covariance = self.orientation_cov
        msg.angular_velocity_covariance = self.angular_velocity_cov
        msg.linear_acceleration_covariance = self.linear_acceleration_cov
        self.imu_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = ImuRepublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()

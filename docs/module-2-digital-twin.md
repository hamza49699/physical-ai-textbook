---
sidebar_position: 2
---

# Module 2: The Digital Twin (Gazebo & Unity)

## Overview

A **Digital Twin** is a virtual replica of your robot in a simulated environment. You can test algorithms, train behaviors, and generate synthetic data without risking expensive hardware.

**What you'll learn:**
- Physics simulation using Gazebo
- High-fidelity 3D rendering with Unity
- Simulating realistic sensors (LiDAR, Depth Cameras, IMUs)
- Human-robot interaction scenarios

---

## 2.1 Introduction to Gazebo

Gazebo is the industry standard for robotics simulation, featuring realistic physics and sensor models.

### Installation

```bash
# Ubuntu 22.04
sudo apt-get update
sudo apt-get install gazebo-11 ros-humble-gazebo-ros-pkgs
source /opt/ros/humble/setup.bash
```

### Launch Your First Simulation

```bash
gazebo --verbose  # Starts with 3D view
```

**Resources:**
- [Gazebo Tutorials](http://gazebosim.org/tutorials)
- [ROS 2 + Gazebo Integration](https://github.com/ros-simulation/gazebo_ros_pkgs)

---

## 2.2 Physics Simulation

### Key Physics Concepts

| Concept | Definition | Example |
|---------|-----------|---------|
| **Gravity** | Force pulling objects down (9.81 m/s²) | Robot falls when unsupported |
| **Collision** | Physical objects can't overlap | Robot can't walk through walls |
| **Friction** | Resistance between surfaces | Robot feet grip the ground |
| **Inertia** | Resistance to acceleration | Heavy robots accelerate slowly |

### Creating a Simulated Environment

**gazebo_world.sdf (Simulation Description Format)**

```xml
<?xml version="1.0" ?>
<sdf version="1.8">
  <world name="robot_world">
    
    <!-- Physics Configuration -->
    <physics name="default_physics" type="ode">
      <max_step_size>0.001</max_step_size>
      <real_time_factor>1.0</real_time_factor>
      <gravity>0 0 -9.81</gravity>
    </physics>

    <!-- Ground Plane -->
    <model name="ground_plane">
      <static>true</static>
      <link name="link">
        <collision name="collision">
          <geometry>
            <plane>
              <normal>0 0 1</normal>
              <size>100 100</size>
            </plane>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <plane>
              <normal>0 0 1</normal>
              <size>100 100</size>
            </plane>
          </geometry>
          <material>
            <ambient>0.8 0.8 0.8 1</ambient>
            <diffuse>0.8 0.8 0.8 1</diffuse>
          </material>
        </visual>
      </link>
    </model>

    <!-- Obstacles -->
    <model name="wall">
      <static>true</static>
      <pose>5 0 1 0 0 0</pose>
      <link name="link">
        <collision name="collision">
          <geometry>
            <box>
              <size>0.1 10 2</size>
            </box>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <box>
              <size>0.1 10 2</size>
            </box>
          </geometry>
          <material>
            <ambient>0.5 0.5 0.5 1</ambient>
            <diffuse>0.5 0.5 0.5 1</diffuse>
          </material>
        </visual>
      </link>
    </model>

  </world>
</sdf>
```

### Launching Gazebo with ROS 2

```bash
# In one terminal: Gazebo
gazebo gazebo_world.sdf

# In another: ROS 2 bridge
ros2 run gazebo_ros gazebo_ros_init
```

---

## 2.3 Sensor Simulation

### LiDAR (Light Detection and Ranging)

LiDAR creates a 3D map by shooting laser beams and measuring reflections.

**Gazebo URDF with LiDAR Plugin:**

```xml
<link name="lidar_link">
  <visual>
    <geometry>
      <cylinder radius="0.05" length="0.07"/>
    </geometry>
  </visual>
  <collision>
    <geometry>
      <cylinder radius="0.05" length="0.07"/>
    </geometry>
  </collision>
  <sensor name="lidar_sensor" type="ray">
    <plugin filename="libgazebo_ros_ray_sensor.so" name="gazebo_ros_ray_sensor">
      <ros>
        <remapping>~/out:=/scan</remapping>
      </ros>
      <output_type>sensor_msgs/LaserScan</output_type>
    </plugin>
    <ray>
      <scan>
        <horizontal>
          <samples>360</samples>
          <resolution>1.0</resolution>
          <min_angle>-3.14159</min_angle>
          <max_angle>3.14159</max_angle>
        </horizontal>
      </scan>
      <range>
        <min>0.08</min>
        <max>10.0</max>
        <resolution>0.01</resolution>
      </range>
    </ray>
  </sensor>
</link>
```

### Depth Camera

Depth cameras measure distance using infrared or structured light.

```xml
<link name="depth_camera_link">
  <sensor name="depth_camera" type="camera">
    <camera>
      <horizontal_fov>1.047</horizontal_fov>
      <image>
        <width>640</width>
        <height>480</height>
        <format>R8G8B8</format>
      </image>
      <clip>
        <near>0.02</near>
        <far>300</far>
      </clip>
    </camera>
    <plugin filename="libgazebo_ros_camera.so" name="depth_camera_controller">
      <ros>
        <remapping>image_raw:=/depth_camera/image</remapping>
        <remapping>camera_info:=/depth_camera/info</remapping>
      </ros>
      <camera_name>depth_camera</camera_name>
      <frame_name>depth_camera_link</frame_name>
    </plugin>
  </sensor>
</link>
```

### IMU (Inertial Measurement Unit)

IMU measures acceleration and rotation.

```xml
<link name="imu_link">
  <sensor name="imu_sensor" type="imu">
    <plugin filename="libgazebo_ros_imu_sensor.so" name="imu_plugin">
      <ros>
        <remapping>imu:=/imu/data</remapping>
      </ros>
      <initial_orientation_as_reference>false</initial_orientation_as_reference>
    </plugin>
  </sensor>
</link>
```

### Reading Sensor Data in ROS 2

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan, Image
from sensor_msgs.msg import Imu

class SensorReader(Node):
    def __init__(self):
        super().__init__('sensor_reader')
        
        # LiDAR subscriber
        self.lidar_sub = self.create_subscription(
            LaserScan, '/scan', self.lidar_callback, 10)
        
        # Depth camera subscriber
        self.depth_sub = self.create_subscription(
            Image, '/depth_camera/image', self.depth_callback, 10)
        
        # IMU subscriber
        self.imu_sub = self.create_subscription(
            Imu, '/imu/data', self.imu_callback, 10)

    def lidar_callback(self, msg):
        self.get_logger().info(f"LiDAR: {len(msg.ranges)} rays")
        closest = min(msg.ranges)
        self.get_logger().info(f"Closest obstacle: {closest:.2f}m")

    def depth_callback(self, msg):
        self.get_logger().info(f"Depth camera: {msg.width}x{msg.height}")

    def imu_callback(self, msg):
        accel = msg.linear_acceleration
        self.get_logger().info(f"Acceleration: x={accel.x:.2f}, y={accel.y:.2f}, z={accel.z:.2f}")

def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(SensorReader())
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

---

## 2.4 Unity for High-Fidelity Rendering

Unity provides photorealistic graphics and can interact with ROS 2 via bridges.

### Setting Up ROS 2 in Unity

1. **Install Unity** (2022 LTS recommended)
2. **Install ROS 2 For Unity** package:
   - Asset Store → Search "ROS 2"
   - Import official ROS 2 For Unity plugin

3. **Connect to ROS 2:**

```csharp
using UnityEngine;
using ROS2;

public class ROS2Controller : MonoBehaviour
{
    private ROS2Node ros2Node;
    private ISubscription<sensor_msgs.msg.LaserScan> lidarSub;

    void Start()
    {
        ros2Node = GetComponent<ROS2Node>();
        lidarSub = ros2Node.CreateSubscription<sensor_msgs.msg.LaserScan>(
            "/scan",
            OnLidarData
        );
    }

    void OnLidarData(sensor_msgs.msg.LaserScan msg)
    {
        Debug.Log($"LiDAR data received: {msg.ranges.Length} rays");
    }
}
```

**Resources:**
- [Unity + ROS 2 Tutorial](https://github.com/RobotecAI/ROS2-for-Unity)

---

## 2.5 Human-Robot Interaction Scenarios

### Simulating a Robot Greeting Visitor

```python
# interactive_scenario.py
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time

class InteractiveRobot(Node):
    def __init__(self):
        super().__init__('interactive_robot')
        self.cmd_publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        
    def greet_visitor(self):
        """Robot detects visitor and waves"""
        self.get_logger().info("Visitor detected! Waving...")
        
        # Wave arm: rotate joint
        twist = Twist()
        twist.angular.z = 0.5  # Wave animation
        
        for _ in range(5):
            self.cmd_publisher.publish(twist)
            time.sleep(0.2)
            twist.angular.z *= -1  # Alternate direction
        
        # Return to rest position
        twist.angular.z = 0.0
        self.cmd_publisher.publish(twist)
        self.get_logger().info("Greeting complete!")

def main(args=None):
    rclpy.init(args=args)
    robot = InteractiveRobot()
    robot.greet_visitor()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

---

## Key Takeaways

✅ **Gazebo** = Physics-accurate robotics simulation  
✅ **Sensors** = LiDAR, Depth cameras, IMUs in simulation  
✅ **Unity** = High-fidelity rendering and visualization  
✅ **Digital Twin** = Test before deploying to real robots  

**Next:** Module 3 - AI-Robot Brain (NVIDIA Isaac)

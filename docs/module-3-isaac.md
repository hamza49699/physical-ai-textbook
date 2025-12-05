---
sidebar_position: 3
---

# Module 3: The AI-Robot Brain (NVIDIA Isaac™)

## Overview

NVIDIA Isaac provides the perception and AI stack for autonomous robotics. It combines photorealistic simulation (Isaac Sim), hardware-accelerated vision (Isaac ROS), and path planning (Nav2).

**What you'll learn:**
- Photorealistic simulation with Isaac Sim
- Synthetic data generation for training
- Hardware-accelerated VSLAM (Visual SLAM)
- Path planning for humanoid navigation

---

## 3.1 NVIDIA Isaac Ecosystem

### Three Core Components

```
┌─────────────────────────────────────────┐
│         Isaac Sim (Simulation)          │
│  - Photorealistic rendering             │
│  - Physics simulation                   │
│  - Synthetic data generation            │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│       Isaac ROS (Perception)            │
│  - GPU-accelerated VSLAM                │
│  - Real-time perception                 │
│  - Hardware integration                 │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│        Nav2 (Path Planning)             │
│  - Motion planning                      │
│  - Navigation                           │
│  - Obstacle avoidance                   │
└─────────────────────────────────────────┘
```

### Installation

```bash
# Install Isaac Sim (Omniverse platform required)
# Download: https://www.nvidia.com/en-us/omniverse/download/

# Install Isaac ROS
git clone https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_common.git
cd isaac_ros_common
./scripts/run_dev.sh

# Install Nav2
sudo apt install ros-humble-navigation2 ros-humble-nav2-bringup
```

**Resources:**
- [NVIDIA Isaac Documentation](https://docs.nvidia.com/isaac/)
- [Isaac ROS GitHub](https://github.com/NVIDIA-ISAAC-ROS)

---

## 3.2 Isaac Sim: Photorealistic Simulation

### Creating a Simulation Environment

Isaac Sim runs on NVIDIA Omniverse and provides tools to build synthetic worlds.

**Python API Example:**

```python
import omni.graph.core as og
from omni.isaac.kit import SimulationApp

# Initialize Isaac Sim
simulation_app = SimulationApp({"headless": False})
simulation_context = simulation_app.context

from omni.isaac.core import World

# Create world
world = World(stage_units_in_meters=1.0)

# Add robot to scene
from omni.isaac.manipulators import SingleArm
from omni.isaac.core.utils.stage import add_reference_to_stage

# Load humanoid robot
add_reference_to_stage(
    usd_path="omniverse://nvidia/Assets/Isaac/4.0/Isaac/Robots/Humanoids/G1/g1.usd",
    prim_path="/World/Robot"
)

# Play simulation
simulation_context.play()

# Step simulation at 60 Hz
for frame in range(1000):
    simulation_context.step(render=True)

simulation_app.close()
```

### Synthetic Data Generation

Generate labeled datasets for training perception models:

```python
from omni.isaac.synthetic_utils import SyntheticDataHelper
import cv2
import numpy as np

class DatasetGenerator:
    def __init__(self, world):
        self.world = world
        self.helper = SyntheticDataHelper()
        
    def generate_dataset(self, num_frames=1000):
        """Generate RGB, depth, and segmentation data"""
        
        dataset = {
            'rgb': [],
            'depth': [],
            'segmentation': []
        }
        
        for frame in range(num_frames):
            # Randomize lighting and camera angle
            self.randomize_environment()
            
            # Capture RGB image
            rgb = self.helper.get_rgb()
            dataset['rgb'].append(rgb)
            
            # Capture depth
            depth = self.helper.get_depth()
            dataset['depth'].append(depth)
            
            # Capture semantic segmentation
            seg = self.helper.get_segmentation()
            dataset['segmentation'].append(seg)
            
            self.world.step(render=False)
        
        return dataset
    
    def randomize_environment(self):
        """Randomize lighting, textures, and object positions"""
        # Randomize lighting
        light_intensity = np.random.uniform(0.5, 2.0)
        
        # Randomize camera position
        camera_x = np.random.uniform(-2, 2)
        camera_y = np.random.uniform(-2, 2)
        
        self.world.update_camera_position([camera_x, camera_y, 1.5])
```

---

## 3.3 Isaac ROS: Hardware-Accelerated VSLAM

### Visual SLAM (Simultaneous Localization and Mapping)

VSLAM uses camera images to build a map while tracking the robot's position.

**Launch Isaac ROS VSLAM:**

```bash
# Terminal 1: Start ROS 2 bridge from Isaac Sim
python3 isaac_sim_ros2_bridge.py

# Terminal 2: Launch VSLAM
ros2 launch isaac_ros_visual_slam isaac_ros_visual_slam.launch.py

# Terminal 3: Visualize
rviz2 -d vslam_config.rviz
```

**VSLAM Configuration (vslam.yaml):**

```yaml
vslam_node:
  ros__parameters:
    # Camera parameters
    camera_topic: "/camera/image_rect"
    camera_info_topic: "/camera/camera_info"
    
    # Detector and descriptor settings
    detector_type: "sift"  # or "orb", "akaze"
    descriptor_type: "sift"
    max_keypoints: 500
    
    # Matching parameters
    match_ratio: 0.7
    max_matches: 100
    
    # Pose estimation
    min_tracked_features: 20
    
    # Output
    pose_topic: "/visual_odometry/pose"
    map_topic: "/visual_odometry/map"
```

### Using VSLAM Data for Navigation

```python
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist

class VSLAMNavigator(Node):
    def __init__(self):
        super().__init__('vslam_navigator')
        
        # Subscribe to VSLAM odometry
        self.odom_sub = self.create_subscription(
            Odometry,
            '/visual_odometry/pose',
            self.odometry_callback,
            10
        )
        
        # Publish movement commands
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        
        self.robot_pose = None
        
    def odometry_callback(self, msg):
        """Update robot pose from VSLAM"""
        self.robot_pose = msg.pose.pose
        x = self.robot_pose.position.x
        y = self.robot_pose.position.y
        self.get_logger().info(f"Robot position: ({x:.2f}, {y:.2f})")
        
    def move_to_target(self, target_x, target_y):
        """Navigate to target using VSLAM feedback"""
        if self.robot_pose is None:
            self.get_logger().warning("Waiting for VSLAM data...")
            return
        
        # Calculate distance to target
        current_x = self.robot_pose.position.x
        current_y = self.robot_pose.position.y
        
        dx = target_x - current_x
        dy = target_y - current_y
        distance = (dx**2 + dy**2)**0.5
        
        if distance < 0.1:
            self.get_logger().info("Target reached!")
            return
        
        # Send movement command
        twist = Twist()
        twist.linear.x = 0.3  # Move forward
        self.cmd_pub.publish(twist)
```

---

## 3.4 Nav2: Path Planning for Humanoids

Nav2 (Navigation 2) provides autonomous navigation with obstacle avoidance.

### Launch Nav2

```bash
ros2 launch nav2_bringup bringup_launch.py use_sim_time:=true use_rviz:=true
```

### Path Planning Example

```python
import rclpy
from rclpy.node import Node
from nav2_simple_commander.robot_navigator import BasicNavigator
from geometry_msgs.msg import PoseStamped
import tf_transformations

class HumanoidNavigator(Node):
    def __init__(self):
        super().__init__('humanoid_navigator')
        self.navigator = BasicNavigator()
        
    def navigate_to_pose(self, x, y, theta):
        """Navigate to a target pose"""
        
        # Create goal pose
        goal_pose = PoseStamped()
        goal_pose.header.frame_id = 'map'
        goal_pose.header.stamp = self.get_clock().now().to_msg()
        
        goal_pose.pose.position.x = x
        goal_pose.pose.position.y = y
        
        # Convert angle to quaternion
        q = tf_transformations.quaternion_from_euler(0, 0, theta)
        goal_pose.pose.orientation.x = q[0]
        goal_pose.pose.orientation.y = q[1]
        goal_pose.pose.orientation.z = q[2]
        goal_pose.pose.orientation.w = q[3]
        
        # Navigate
        self.navigator.goToPose(goal_pose)
        self.get_logger().info(f"Navigating to ({x}, {y})")

def main(args=None):
    rclpy.init(args=args)
    navigator = HumanoidNavigator()
    
    # Navigation sequence
    navigator.navigate_to_pose(1.0, 0.0, 0.0)  # Move forward
    navigator.navigate_to_pose(1.0, 1.0, 1.57)  # Turn and move
    
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Waypoint Following

```python
from nav2_simple_commander.robot_navigator import BasicNavigator

class WaypointNavigator:
    def __init__(self):
        self.navigator = BasicNavigator()
        
    def follow_waypoints(self, waypoints):
        """Follow a sequence of waypoints"""
        for i, (x, y, theta) in enumerate(waypoints):
            goal_pose = PoseStamped()
            goal_pose.header.frame_id = 'map'
            goal_pose.pose.position.x = x
            goal_pose.pose.position.y = y
            
            q = tf_transformations.quaternion_from_euler(0, 0, theta)
            goal_pose.pose.orientation.x = q[0]
            goal_pose.pose.orientation.y = q[1]
            goal_pose.pose.orientation.z = q[2]
            goal_pose.pose.orientation.w = q[3]
            
            print(f"Going to waypoint {i+1}: ({x}, {y})")
            self.navigator.goToPose(goal_pose)

# Define waypoints (x, y, angle)
waypoints = [
    (0.0, 0.0, 0.0),    # Start
    (2.0, 0.0, 0.0),    # Move forward
    (2.0, 2.0, 1.57),   # Turn right and move
    (0.0, 2.0, 3.14),   # Turn right and move
    (0.0, 0.0, 0.0),    # Return to start
]

navigator = WaypointNavigator()
navigator.follow_waypoints(waypoints)
```

---

## Key Takeaways

✅ **Isaac Sim** = Photorealistic simulation with synthetic data generation  
✅ **VSLAM** = GPU-accelerated visual localization and mapping  
✅ **Nav2** = Production-grade autonomous navigation  
✅ **Integration** = Seamless workflow from simulation to real robots  

**Next:** Module 4 - Vision-Language-Action (VLA) and Capstone

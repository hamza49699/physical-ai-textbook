---
sidebar_position: 1
---

# Module 1: The Robotic Nervous System (ROS 2)

## Overview

ROS 2 (Robot Operating System 2) is the middleware layer that enables robots to perceive, reason, and act. Think of it as the nervous system of a robot—carrying signals between sensors, processors, and actuators.

**What you'll learn:**
- How ROS 2 nodes communicate via Topics and Services
- Writing Python agents using `rclpy`
- Describing robot structure with URDF
- Bridging AI agents to physical robot controllers

---

## 1.1 ROS 2 Architecture Basics

### The Three-Layer Model

```
┌─────────────────────────────────────┐
│  Application Layer (Your AI Brain)  │
├─────────────────────────────────────┤
│  Middleware Layer (ROS 2)           │
├─────────────────────────────────────┤
│  Hardware Layer (Motors, Sensors)   │
└─────────────────────────────────────┘
```

ROS 2 connects these layers through:
- **Nodes**: Independent Python/C++ processes
- **Topics**: Asynchronous message channels (Pub/Sub)
- **Services**: Synchronous request/reply calls

### Installation

```bash
# Ubuntu 22.04 (Recommended)
curl -sSL https://raw.githubusercontent.com/ros/rosdep/master/rosdep/sources.list.d/20-default.list | sudo tee /etc/apt/sources.list.d/ros-latest.list
curl -sSL https://repo.ros2.org/ros.key | sudo apt-key add -
sudo apt update
sudo apt install ros-humble-desktop
source /opt/ros/humble/setup.bash
```

**Resources:**
- [ROS 2 Installation Guide](https://docs.ros.org/en/humble/Installation.html)
- [ROS 2 Documentation](https://docs.ros.org/en/humble/)

---

## 1.2 Nodes and Communication

### Creating Your First Node

A ROS 2 node is a Python script that runs independently and communicates with other nodes.

**Example: Simple Publisher Node**

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class HelloPublisher(Node):
    def __init__(self):
        super().__init__('hello_publisher')
        self.publisher_ = self.create_publisher(String, 'hello_topic', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.count = 0

    def timer_callback(self):
        msg = String()
        msg.data = f'Hello World: {self.count}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: {msg.data}')
        self.count += 1

def main(args=None):
    rclpy.init(args=args)
    node = HelloPublisher()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**Run it:**
```bash
python3 hello_publisher.py
```

**Check messages:**
```bash
ros2 topic list              # See all topics
ros2 topic echo hello_topic  # Listen to messages
```

### Creating a Subscriber Node

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class HelloSubscriber(Node):
    def __init__(self):
        super().__init__('hello_subscriber')
        self.subscription = self.create_subscription(
            String,
            'hello_topic',
            self.listener_callback,
            10
        )

    def listener_callback(self, msg):
        self.get_logger().info(f'Received: {msg.data}')

def main(args=None):
    rclpy.init(args=args)
    node = HelloSubscriber()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**Run in another terminal:**
```bash
python3 hello_subscriber.py
```

---

## 1.3 Topics vs Services

| Feature | Topics | Services |
|---------|--------|----------|
| **Pattern** | Publisher → Subscriber | Client → Server (Request/Reply) |
| **Speed** | Asynchronous (fire & forget) | Synchronous (waits for response) |
| **Use Case** | Continuous data (sensor streams) | One-time requests (move to position) |
| **Example** | `/camera/image` topic | `/move_arm` service |

### Service Example: Robot Arm Controller

```python
# Server: arm_server.py
import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool

class ArmServer(Node):
    def __init__(self):
        super().__init__('arm_server')
        self.srv = self.create_service(SetBool, 'move_arm', self.move_callback)

    def move_callback(self, request, response):
        if request.data:
            self.get_logger().info('Moving arm UP')
            response.success = True
            response.message = 'Arm moved successfully'
        else:
            self.get_logger().info('Moving arm DOWN')
            response.success = True
            response.message = 'Arm retracted'
        return response

def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(ArmServer())
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

```python
# Client: arm_client.py
import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool

class ArmClient(Node):
    def __init__(self):
        super().__init__('arm_client')
        self.cli = self.create_client(SetBool, 'move_arm')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for service...')

    def send_request(self, direction):
        req = SetBool.Request()
        req.data = direction  # True for UP, False for DOWN
        future = self.cli.call_async(req)
        rclpy.spin_until_future_complete(self, future)
        return future.result()

def main(args=None):
    rclpy.init(args=args)
    client = ArmClient()
    response = client.send_request(True)  # Move UP
    print(f"Response: {response.message}")
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

---

## 1.4 Understanding URDF (Unified Robot Description Format)

URDF is an XML format that describes a robot's structure, joints, and links.

### Basic URDF Structure

```xml
<?xml version="1.0" ?>
<robot name="humanoid_robot">
  
  <!-- Base Link (torso) -->
  <link name="torso">
    <inertial>
      <mass value="30.0"/>
      <inertia ixx="1.0" ixy="0.0" ixz="0.0" 
               iyy="1.0" iyz="0.0" izz="1.0"/>
    </inertial>
    <visual>
      <geometry>
        <box size="0.3 0.3 0.6"/>
      </geometry>
      <material name="white">
        <color rgba="1 1 1 1"/>
      </material>
    </visual>
  </link>

  <!-- Left Shoulder Joint -->
  <joint name="left_shoulder" type="revolute">
    <parent link="torso"/>
    <child link="left_arm"/>
    <origin xyz="0.15 0.0 0.25" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="-3.14" upper="3.14" effort="100" velocity="1.0"/>
  </joint>

  <!-- Left Arm Link -->
  <link name="left_arm">
    <inertial>
      <mass value="3.0"/>
      <inertia ixx="0.1" ixy="0.0" ixz="0.0" 
               iyy="0.1" iyz="0.0" izz="0.1"/>
    </inertial>
    <visual>
      <geometry>
        <cylinder radius="0.05" length="0.5"/>
      </geometry>
    </visual>
  </link>

</robot>
```

### Visualize URDF

```bash
# Install URDF tools
sudo apt install liburdfdom-tools

# Check URDF validity
check_urdf humanoid.urdf

# Convert to graph
urdf_to_graphviz humanoid.urdf > humanoid.gv
```

**Resources:**
- [URDF Specification](http://wiki.ros.org/urdf)
- [URDF Tutorials](https://wiki.ros.org/urdf/Tutorials)

---

## 1.5 Bridging AI Agents to ROS Controllers

### Architecture: LLM → ROS 2 Bridge

```
┌──────────────────┐
│  LLM Agent       │ (receives: "Move forward")
└────────┬─────────┘
         │ (calls ROS service)
         ▼
┌──────────────────────────┐
│  ROS 2 Action Server     │ (translates to motor commands)
│  /robot/move_base        │
└────────┬─────────────────┘
         │ (publishes to motor topics)
         ▼
┌──────────────────┐
│  Motor Controller│
└──────────────────┘
```

### Example: LLM-Commanded Robot Movement

```python
# nlp_to_ros_bridge.py
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import openai

class NLPBridge(Node):
    def __init__(self):
        super().__init__('nlp_bridge')
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        openai.api_key = "your-api-key"

    def send_command(self, command_text):
        """Translate natural language to robot commands"""
        
        # Use GPT to interpret command
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a robot command interpreter. Respond ONLY with JSON."
                },
                {
                    "role": "user",
                    "content": f"Convert this to robot motion: '{command_text}'. Return JSON with linear_x, linear_y, angular_z values."
                }
            ]
        )
        
        # Parse response and create Twist message
        motion = response['choices'][0]['message']['content']
        twist = Twist()
        twist.linear.x = motion['linear_x']
        twist.linear.y = motion['linear_y']
        twist.angular.z = motion['angular_z']
        
        self.publisher.publish(twist)
        self.get_logger().info(f"Command executed: {command_text}")

def main(args=None):
    rclpy.init(args=args)
    bridge = NLPBridge()
    
    # Example commands
    bridge.send_command("Move forward 2 meters")
    bridge.send_command("Turn left 90 degrees")
    
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

---

## 1.6 Practical Exercise

**Task:** Create a robot that responds to voice commands

```python
# voice_controlled_robot.py
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import openai
import speech_recognition as sr

class VoiceControlledRobot(Node):
    def __init__(self):
        super().__init__('voice_robot')
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.recognizer = sr.Recognizer()

    def listen_and_command(self):
        with sr.Microphone() as source:
            audio = self.recognizer.listen(source)
            try:
                text = self.recognizer.recognize_google(audio)
                self.get_logger().info(f"Heard: {text}")
                self.send_robot_command(text)
            except sr.UnknownValueError:
                self.get_logger().info("Could not understand audio")

    def send_robot_command(self, command):
        twist = Twist()
        if "forward" in command.lower():
            twist.linear.x = 0.5
        elif "backward" in command.lower():
            twist.linear.x = -0.5
        elif "left" in command.lower():
            twist.angular.z = 0.5
        elif "right" in command.lower():
            twist.angular.z = -0.5
        elif "stop" in command.lower():
            twist.linear.x = 0.0
            twist.angular.z = 0.0
        
        self.publisher.publish(twist)
```

---

## Key Takeaways

✅ **Nodes** = Independent processes that communicate  
✅ **Topics** = Continuous data streams (sensors)  
✅ **Services** = One-time requests (actions)  
✅ **URDF** = Robot structure definition  
✅ **Bridges** = Connect AI to physical controllers  

**Next:** Module 2 - Digital Twin environments (Gazebo & Unity)

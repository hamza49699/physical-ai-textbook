---
sidebar_position: 4
---

# Module 4: Vision-Language-Action (VLA)

## Overview

Vision-Language-Action (VLA) is where robotics meets large language models. A robot receives voice commands, understands them with AI, plans a sequence of actions, and executes them in the real world.

**What you'll learn:**
- Converting voice to text with OpenAI Whisper
- Cognitive planning with LLMs (GPT-4)
- Grounding language in robot actions
- The capstone: Autonomous Humanoid Robot

---

## 4.1 Voice-to-Action Pipeline

### Architecture

```
┌──────────────┐
│  Voice Input │ (microphone)
└──────┬───────┘
       │
       ▼
┌─────────────────┐
│  Whisper (STT)  │ (speech-to-text)
└──────┬──────────┘
       │
       ▼
┌─────────────────────────┐
│  NLP Understanding      │ (parse intent)
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│  LLM Planning (GPT-4)   │ (generate action plan)
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│  ROS 2 Execution        │ (execute actions)
└──────┬──────────────────┘
       │
       ▼
┌──────────────┐
│ Robot Action │
└──────────────┘
```

---

## 4.2 Speech Recognition with OpenAI Whisper

### Installation

```bash
pip install openai-whisper pyaudio
```

### Basic Voice Input

```python
import whisper
import pyaudio
import numpy as np

class VoiceInput:
    def __init__(self):
        self.model = whisper.load_model("base")  # or "tiny", "small", "medium", "large"
        
    def record_audio(self, duration=5):
        """Record audio from microphone"""
        CHUNK = 1024
        FORMAT = pyaudio.paFloat32
        CHANNELS = 1
        RATE = 16000
        
        p = pyaudio.PyAudio()
        
        stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK
        )
        
        print("Recording...")
        frames = []
        for _ in range(0, int(RATE / CHUNK * duration)):
            data = stream.read(CHUNK)
            frames.append(np.frombuffer(data, dtype=np.float32))
        
        stream.stop_stream()
        stream.close()
        p.terminate()
        
        audio = np.concatenate(frames)
        return audio
    
    def transcribe(self, audio):
        """Convert audio to text"""
        result = self.model.transcribe(
            audio,
            language="en",
            task="transcribe"
        )
        return result["text"]
    
    def listen_and_transcribe(self, duration=5):
        """Record and transcribe voice"""
        audio = self.record_audio(duration)
        text = self.transcribe(audio)
        return text

# Usage
voice_input = VoiceInput()
command = voice_input.listen_and_transcribe()
print(f"Heard: {command}")
```

### Real-time Streaming with OpenAI API

```python
import openai
import pyaudio

openai.api_key = "your-api-key"

class StreamingVoiceInput:
    def __init__(self):
        self.buffer = b""
        
    def stream_and_transcribe(self):
        """Stream audio to Whisper API"""
        
        CHUNK = 1024
        FORMAT = pyaudio.paFloat32
        CHANNELS = 1
        RATE = 16000
        
        p = pyaudio.PyAudio()
        stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK
        )
        
        print("Listening...")
        
        # Record until silence
        silence_duration = 0
        max_silence = 3
        
        while silence_duration < max_silence:
            data = stream.read(CHUNK)
            self.buffer += data
            
            # Simple silence detection
            audio_data = np.frombuffer(data, dtype=np.float32)
            if np.abs(audio_data).mean() < 0.01:
                silence_duration += CHUNK / RATE
            else:
                silence_duration = 0
        
        stream.stop_stream()
        stream.close()
        p.terminate()
        
        # Send to Whisper
        with open("temp_audio.wav", "wb") as f:
            f.write(self.buffer)
        
        with open("temp_audio.wav", "rb") as f:
            transcript = openai.Audio.transcribe("whisper-1", f)
        
        return transcript["text"]
```

---

## 4.3 Cognitive Planning with LLMs

### Using GPT-4 for Action Planning

```python
import openai
import json

openai.api_key = "your-api-key"

class CognitivePlanner:
    def __init__(self):
        self.system_prompt = """
You are a robot planning system. Convert natural language commands into a sequence of robot actions.
Respond ONLY with valid JSON in this format:
{
    "actions": [
        {"action": "move_forward", "distance": 1.0, "duration": 5},
        {"action": "rotate", "angle": 90, "direction": "left"},
        {"action": "grasp", "object": "cup"}
    ],
    "reasoning": "explanation of the plan"
}

Available actions:
- move_forward: Move forward (distance in meters)
- move_backward: Move backward (distance in meters)
- rotate: Rotate (angle in degrees, direction: "left" or "right")
- grasp: Grasp object (object name)
- release: Release held object
- look_for: Search for object (object name)
- identify: Identify what the robot sees
- speak: Say something (text)
"""
    
    def plan_action(self, command):
        """Convert natural language to action plan"""
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"Command: {command}"}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        plan_text = response['choices'][0]['message']['content']
        
        try:
            plan = json.loads(plan_text)
            return plan
        except json.JSONDecodeError:
            return {"actions": [], "error": "Failed to parse plan"}
    
    def execute_plan(self, plan, robot_controller):
        """Execute action plan on robot"""
        for action in plan.get("actions", []):
            action_type = action.get("action")
            
            if action_type == "move_forward":
                robot_controller.move_forward(action.get("distance", 1.0))
            elif action_type == "move_backward":
                robot_controller.move_backward(action.get("distance", 1.0))
            elif action_type == "rotate":
                robot_controller.rotate(
                    action.get("angle", 90),
                    action.get("direction", "left")
                )
            elif action_type == "grasp":
                robot_controller.grasp(action.get("object", ""))
            elif action_type == "release":
                robot_controller.release()
            elif action_type == "speak":
                robot_controller.speak(action.get("text", ""))

# Example usage
planner = CognitivePlanner()
command = "Pick up the cup and place it on the table"
plan = planner.plan_action(command)
print(f"Action Plan: {json.dumps(plan, indent=2)}")
```

### Multi-step Reasoning with Chain-of-Thought

```python
class AdvancedPlanner:
    def __init__(self):
        pass
    
    def plan_with_reasoning(self, command):
        """Use chain-of-thought for complex tasks"""
        
        # Step 1: Understand the task
        understand_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "user",
                    "content": f"Understand this robot task: {command}\n\nBreak it down into subtasks."
                }
            ]
        )
        
        subtasks = understand_response['choices'][0]['message']['content']
        print(f"Subtasks:\n{subtasks}")
        
        # Step 2: Plan each subtask
        plan_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "user",
                    "content": f"For these subtasks:\n{subtasks}\n\nGenerate robot actions in JSON format."
                }
            ]
        )
        
        actions = plan_response['choices'][0]['message']['content']
        return actions
```

---

## 4.4 Grounding Language in Robot Actions

### Semantic Understanding for Objects

```python
class SemanticGrounding:
    def __init__(self):
        self.object_database = {
            "cup": {"grasp_type": "cylindrical", "force": 5},
            "ball": {"grasp_type": "spherical", "force": 3},
            "book": {"grasp_type": "flat", "force": 7},
            "bottle": {"grasp_type": "cylindrical", "force": 4}
        }
    
    def get_grasp_strategy(self, object_name):
        """Get how to grasp an object"""
        if object_name in self.object_database:
            return self.object_database[object_name]
        else:
            # Query GPT for unknown objects
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "user",
                        "content": f"How should a robot grasp a {object_name}? (grasp_type and force)"
                    }
                ]
            )
            return response['choices'][0]['message']['content']
    
    def plan_manipulation(self, action_description):
        """Convert description to manipulation command"""
        # Example: "carefully pick up the fragile vase"
        
        # Extract object and modifiers
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "user",
                    "content": f"Parse this action: '{action_description}'\nExtract: object_name, care_level, grip_strength"
                }
            ]
        )
        
        return response['choices'][0]['message']['content']
```

---

## 4.5 Capstone Project: The Autonomous Humanoid

### Full System Integration

```python
import rclpy
from rclpy.node import Node
import json
import openai

class AutonomousHumanoid(Node):
    def __init__(self):
        super().__init__('autonomous_humanoid')
        
        # Initialize components
        self.voice_input = VoiceInput()
        self.planner = CognitivePlanner()
        
        # ROS publishers/subscribers
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.grasp_pub = self.create_publisher(JointCommand, '/gripper_cmd', 10)
        
        # Vision integration
        self.vision_sub = self.create_subscription(Image, '/camera/image', self.process_image, 10)
        
        self.main_loop()
    
    def main_loop(self):
        """Main execution loop"""
        
        print("🤖 Autonomous Humanoid Robot Ready")
        print("Voice control enabled. Speak a command...")
        
        while True:
            try:
                # 1. Listen to voice command
                print("\n📢 Listening...")
                command = self.voice_input.listen_and_transcribe(duration=3)
                print(f"✅ Heard: '{command}'")
                
                # 2. Plan actions
                print("\n🧠 Planning actions...")
                plan = self.planner.plan_action(command)
                print(f"📋 Plan: {json.dumps(plan['actions'], indent=2)}")
                
                # 3. Execute plan
                print("\n🤖 Executing plan...")
                self.execute_action_plan(plan['actions'])
                
                print("✨ Task complete!")
                
            except KeyboardInterrupt:
                print("\n🛑 Shutting down...")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def execute_action_plan(self, actions):
        """Execute a sequence of actions"""
        for action in actions:
            action_type = action.get("action")
            
            if action_type == "move_forward":
                self.move_forward(action.get("distance", 1.0))
            elif action_type == "rotate":
                self.rotate(action.get("angle", 90))
            elif action_type == "look_for":
                self.look_for_object(action.get("object", ""))
            elif action_type == "grasp":
                self.grasp_object(action.get("object", ""))
            elif action_type == "release":
                self.release_object()
            elif action_type == "identify":
                self.identify_object()
    
    def move_forward(self, distance):
        """Move forward (in meters)"""
        print(f"  ➡️  Moving forward {distance}m...")
        twist = Twist()
        twist.linear.x = 0.3
        for _ in range(int(distance * 10)):
            self.cmd_pub.publish(twist)
            self.get_clock().sleep_for(0.1)
        twist.linear.x = 0.0
        self.cmd_pub.publish(twist)
    
    def rotate(self, angle):
        """Rotate (in degrees)"""
        print(f"  🔄 Rotating {angle} degrees...")
        twist = Twist()
        twist.angular.z = 0.5
        for _ in range(int(abs(angle) / 3)):
            self.cmd_pub.publish(twist)
            self.get_clock().sleep_for(0.1)
        twist.angular.z = 0.0
        self.cmd_pub.publish(twist)
    
    def grasp_object(self, object_name):
        """Grasp an object"""
        print(f"  ✋ Grasping {object_name}...")
        msg = JointCommand()
        msg.name = ["gripper_left", "gripper_right"]
        msg.position = [0.8, 0.8]
        self.grasp_pub.publish(msg)
    
    def release_object(self):
        """Release held object"""
        print(f"  👐 Releasing object...")
        msg = JointCommand()
        msg.name = ["gripper_left", "gripper_right"]
        msg.position = [0.0, 0.0]
        self.grasp_pub.publish(msg)
    
    def look_for_object(self, object_name):
        """Search for an object"""
        print(f"  👀 Looking for {object_name}...")
        # Rotate to search
        for angle in [-45, -20, 0, 20, 45]:
            twist = Twist()
            twist.angular.z = float(angle) / 10
            self.cmd_pub.publish(twist)
    
    def identify_object(self):
        """Identify what the robot sees"""
        print(f"  🔍 Identifying objects...")
        # Use vision model
        pass
    
    def process_image(self, msg):
        """Process camera images"""
        # TODO: Implement vision processing
        pass

def main(args=None):
    rclpy.init(args=args)
    robot = AutonomousHumanoid()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Complete Example Commands

```bash
# The robot can now understand and execute:

"Move forward and look for a cup"
# → Moves forward, scans environment, identifies cup

"Pick up the cup and place it on the table"
# → Locates cup, grasps it carefully, navigates to table, releases

"Clean up the room"
# → Plans entire cleanup sequence with Nav2 pathfinding

"What do you see?"
# → Uses vision to describe the environment

"Follow me"
# → Tracks person using VSLAM, follows at safe distance
```

---

## Key Takeaways

✅ **Whisper** = Robust speech recognition  
✅ **GPT-4** = Intelligent task planning  
✅ **Semantic Grounding** = Understanding objects and actions  
✅ **Integration** = End-to-end autonomous robotics  
✅ **Scalability** = From simulation to real robots  

---

## Resources

- [OpenAI Whisper](https://github.com/openai/whisper)
- [OpenAI API Documentation](https://platform.openai.com/docs/)
- [ROS 2 Best Practices](https://docs.ros.org/en/humble/Concepts.html)
- [Robotics Community](https://discourse.ros.org/)

**🎉 Congratulations! You've mastered the complete Physical AI stack!**

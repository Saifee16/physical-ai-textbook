#!/usr/bin/env python3
"""
Content Generation Helper Script

This script helps generate chapter templates for all remaining weeks.
You can use AI (Claude/GPT-4) to fill in the detailed content.
"""

import os
from pathlib import Path

# Chapter templates
CHAPTER_TEMPLATE = """---
sidebar_position: {position}
---

# {title}

## Introduction

{intro}

## Learning Objectives

By the end of this chapter, you will be able to:

{objectives}

## Core Concepts

### Concept 1

[Add detailed explanation]

### Concept 2

[Add detailed explanation]

## Practical Example

```python
# Code example
# Add practical implementation
```

## Hands-On Exercise

### Exercise 1: {exercise_title}

**Objective**: {exercise_objective}

**Steps**:
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Expected Output**: [Describe what students should see]

## Key Takeaways

1. 📌 [Key point 1]
2. 📌 [Key point 2]
3. 📌 [Key point 3]

## Next Steps

👉 **Next**: [{next_chapter}]({next_link})

## Discussion Questions

1. [Question 1]
2. [Question 2]
3. [Question 3]

## Further Reading

- **Documentation**: [Link]
- **Tutorials**: [Link]
- **Research Papers**: [Link]
"""

# Course structure
COURSE_STRUCTURE = {
    "week1-2": {
        "title": "Week 1-2: Introduction to Physical AI",
        "chapters": [
            {
                "filename": "digital-to-physical.md",
                "title": "From Digital to Physical: The Transition",
                "intro": "Exploring the fundamental shift from software-only AI to embodied intelligence.",
                "objectives": "- Understand the limitations of digital-only AI\n- Learn about embodied intelligence\n- Explore the challenges of physical AI",
                "exercise_title": "Simulate vs Real World",
                "exercise_objective": "Compare a simple task in simulation vs physical execution"
            },
            {
                "filename": "humanoid-landscape.md",
                "title": "Overview of Humanoid Robotics Landscape",
                "intro": "Survey of current humanoid robots and their capabilities.",
                "objectives": "- Identify major humanoid robot platforms\n- Compare different approaches to humanoid design\n- Understand the state of the art",
                "exercise_title": "Robot Comparison",
                "exercise_objective": "Research and compare 3 humanoid robot platforms"
            },
            {
                "filename": "sensor-systems.md",
                "title": "Sensor Systems: LIDAR, Cameras, IMUs",
                "intro": "Understanding the sensing capabilities that give robots perception.",
                "objectives": "- Learn about different sensor modalities\n- Understand sensor fusion\n- Explore sensor data processing",
                "exercise_title": "Sensor Data Visualization",
                "exercise_objective": "Visualize data from different sensor types"
            }
        ]
    },
    "week3-5": {
        "title": "Week 3-5: ROS 2 Fundamentals",
        "chapters": [
            {
                "filename": "nodes-topics-services.md",
                "title": "Nodes, Topics, and Services",
                "intro": "Deep dive into ROS 2 communication patterns.",
                "objectives": "- Create and manage ROS 2 nodes\n- Implement publishers and subscribers\n- Build service clients and servers",
                "exercise_title": "Build a Publisher-Subscriber System",
                "exercise_objective": "Create nodes that communicate via topics"
            },
            {
                "filename": "python-packages.md",
                "title": "Building ROS 2 Packages with Python",
                "intro": "Learn to structure and build ROS 2 Python packages.",
                "objectives": "- Create ROS 2 packages\n- Write setup.py and package.xml\n- Build and install packages",
                "exercise_title": "Create Your First Package",
                "exercise_objective": "Build a complete ROS 2 Python package from scratch"
            },
            {
                "filename": "launch-parameters.md",
                "title": "Launch Files and Parameter Management",
                "intro": "Manage complex robot systems with launch files.",
                "objectives": "- Write launch files in Python\n- Configure parameters\n- Manage multi-node systems",
                "exercise_title": "Multi-Node Launch",
                "exercise_objective": "Create a launch file for a multi-node system"
            }
        ]
    },
    "week6-7": {
        "title": "Week 6-7: Robot Simulation with Gazebo",
        "chapters": [
            {
                "filename": "gazebo-setup.md",
                "title": "Gazebo Simulation Environment Setup",
                "intro": "Setting up and configuring Gazebo for robot simulation.",
                "objectives": "- Install and configure Gazebo\n- Understand the simulation architecture\n- Create basic worlds",
                "exercise_title": "First Simulation",
                "exercise_objective": "Launch a simple robot in Gazebo"
            },
            {
                "filename": "urdf-sdf-formats.md",
                "title": "URDF and SDF Robot Description Formats",
                "intro": "Describing robots in machine-readable formats.",
                "objectives": "- Write URDF files\n- Understand SDF format\n- Convert between formats",
                "exercise_title": "Create Robot Description",
                "exercise_objective": "Write a URDF file for a simple robot"
            },
            {
                "filename": "physics-simulation.md",
                "title": "Physics Simulation and Sensor Simulation",
                "intro": "Realistic physics and sensor modeling in simulation.",
                "objectives": "- Configure physics engines\n- Simulate sensors (cameras, lidar, IMU)\n- Tune simulation parameters",
                "exercise_title": "Sensor Simulation",
                "exercise_objective": "Add and configure sensors in Gazebo"
            },
            {
                "filename": "unity-visualization.md",
                "title": "Introduction to Unity for Robot Visualization",
                "intro": "High-quality visualization using Unity.",
                "objectives": "- Set up Unity for robotics\n- Import robot models\n- Create visualizations",
                "exercise_title": "Unity Visualization",
                "exercise_objective": "Visualize a robot in Unity"
            }
        ]
    },
    "week8-10": {
        "title": "Week 8-10: NVIDIA Isaac Platform",
        "chapters": [
            {
                "filename": "isaac-sdk-sim.md",
                "title": "NVIDIA Isaac SDK and Isaac Sim",
                "intro": "Introduction to NVIDIA's robotics platform.",
                "objectives": "- Install Isaac Sim\n- Understand the architecture\n- Create basic simulations",
                "exercise_title": "Isaac Sim Setup",
                "exercise_objective": "Set up and run first Isaac Sim example"
            },
            {
                "filename": "ai-perception.md",
                "title": "AI-Powered Perception and Manipulation",
                "intro": "Using AI for robot perception and manipulation.",
                "objectives": "- Implement object detection\n- Use semantic segmentation\n- Grasp planning with AI",
                "exercise_title": "Object Detection Pipeline",
                "exercise_objective": "Build an object detection pipeline"
            },
            {
                "filename": "reinforcement-learning.md",
                "title": "Reinforcement Learning for Robot Control",
                "intro": "Training robots with reinforcement learning.",
                "objectives": "- Understand RL basics\n- Implement PPO for robotics\n- Train a simple policy",
                "exercise_title": "Train a Walking Policy",
                "exercise_objective": "Use RL to train a bipedal walking controller"
            },
            {
                "filename": "sim-to-real.md",
                "title": "Sim-to-Real Transfer Techniques",
                "intro": "Bridging the gap between simulation and reality.",
                "objectives": "- Understand domain randomization\n- Apply reality gap techniques\n- Deploy sim-trained models to real robots",
                "exercise_title": "Domain Randomization",
                "exercise_objective": "Implement domain randomization in Isaac Sim"
            }
        ]
    },
    "week11-12": {
        "title": "Week 11-12: Humanoid Robot Development",
        "chapters": [
            {
                "filename": "kinematics-dynamics.md",
                "title": "Humanoid Robot Kinematics and Dynamics",
                "intro": "Mathematical foundations of humanoid robots.",
                "objectives": "- Understand forward/inverse kinematics\n- Compute dynamics\n- Implement kinematic chains",
                "exercise_title": "IK Solver",
                "exercise_objective": "Implement inverse kinematics for an arm"
            },
            {
                "filename": "bipedal-locomotion.md",
                "title": "Bipedal Locomotion and Balance Control",
                "intro": "Making humanoids walk and balance.",
                "objectives": "- Understand ZMP and balance\n- Implement gait generation\n- Control bipedal walking",
                "exercise_title": "Walking Controller",
                "exercise_objective": "Implement a simple walking controller"
            },
            {
                "filename": "manipulation-grasping.md",
                "title": "Manipulation and Grasping with Humanoid Hands",
                "intro": "Dexterous manipulation with humanoid hands.",
                "objectives": "- Plan grasps\n- Control multi-fingered hands\n- Implement manipulation primitives",
                "exercise_title": "Grasp Planning",
                "exercise_objective": "Plan and execute grasps for different objects"
            },
            {
                "filename": "human-robot-interaction.md",
                "title": "Natural Human-Robot Interaction Design",
                "intro": "Designing intuitive interactions between humans and robots.",
                "objectives": "- Understand HRI principles\n- Design interaction patterns\n- Implement safety measures",
                "exercise_title": "HRI Scenario",
                "exercise_objective": "Design and implement a human-robot collaboration task"
            }
        ]
    },
    "week13": {
        "title": "Week 13: Conversational Robotics",
        "chapters": [
            {
                "filename": "gpt-integration.md",
                "title": "Integrating GPT Models for Conversational AI",
                "intro": "Adding language understanding to robots.",
                "objectives": "- Integrate GPT models\n- Process natural language commands\n- Generate robot actions from text",
                "exercise_title": "Voice Command System",
                "exercise_objective": "Build a system that executes GPT-interpreted commands"
            },
            {
                "filename": "speech-recognition.md",
                "title": "Speech Recognition and Natural Language Understanding",
                "intro": "Understanding spoken commands.",
                "objectives": "- Implement speech recognition\n- Process audio streams\n- Integrate with robot control",
                "exercise_title": "Speech Pipeline",
                "exercise_objective": "Build end-to-end speech to action pipeline"
            },
            {
                "filename": "multimodal-interaction.md",
                "title": "Multi-Modal Interaction: Speech, Gesture, Vision",
                "intro": "Combining multiple interaction modalities.",
                "objectives": "- Fuse multiple input modalities\n- Implement gesture recognition\n- Build multimodal interfaces",
                "exercise_title": "Multimodal System",
                "exercise_objective": "Create a system that uses speech + gesture + vision"
            }
        ]
    },
    "hardware": {
        "title": "Hardware & Lab Setup",
        "chapters": [
            {
                "filename": "workstation-requirements.md",
                "title": "Workstation Requirements",
                "intro": "Hardware needed for development.",
                "objectives": "- Understand GPU requirements\n- Choose appropriate CPU/RAM\n- Set up development environment",
                "exercise_title": "System Benchmark",
                "exercise_objective": "Benchmark your system for Isaac Sim"
            },
            {
                "filename": "edge-ai-kits.md",
                "title": "Edge AI Kits (Jetson)",
                "intro": "Deploying AI on edge devices.",
                "objectives": "- Set up Jetson Orin\n- Deploy models to edge\n- Optimize for inference",
                "exercise_title": "Edge Deployment",
                "exercise_objective": "Deploy a model to Jetson"
            },
            {
                "filename": "robot-options.md",
                "title": "Robot Hardware Options",
                "intro": "Choosing the right robot platform.",
                "objectives": "- Compare robot platforms\n- Understand trade-offs\n- Match robots to applications",
                "exercise_title": "Robot Selection",
                "exercise_objective": "Choose appropriate robot for a given task"
            },
            {
                "filename": "lab-architecture.md",
                "title": "Complete Lab Architecture",
                "intro": "Designing a complete robotics lab.",
                "objectives": "- Plan lab layout\n- Set up networking\n- Integrate all components",
                "exercise_title": "Lab Design",
                "exercise_objective": "Design a complete lab setup"
            }
        ]
    },
    "capstone": {
        "title": "Capstone Project",
        "chapters": [
            {
                "filename": "project-overview.md",
                "title": "Capstone Project Overview",
                "intro": "Building an autonomous humanoid robot.",
                "objectives": "- Understand project requirements\n- Plan implementation\n- Set milestones",
                "exercise_title": "Project Planning",
                "exercise_objective": "Create detailed project plan"
            },
            {
                "filename": "implementation-guide.md",
                "title": "Implementation Guide",
                "intro": "Step-by-step implementation guidance.",
                "objectives": "- Implement each component\n- Integrate subsystems\n- Test and debug",
                "exercise_title": "System Integration",
                "exercise_objective": "Integrate all capstone components"
            },
            {
                "filename": "evaluation-criteria.md",
                "title": "Evaluation Criteria",
                "intro": "How your capstone will be evaluated.",
                "objectives": "- Understand grading rubric\n- Meet requirements\n- Excel in presentation",
                "exercise_title": "Self-Evaluation",
                "exercise_objective": "Evaluate your project against criteria"
            }
        ]
    }
}

def generate_chapter(week_dir, chapter, position, next_chapter=None):
    """Generate a chapter file from template"""
    content = CHAPTER_TEMPLATE.format(
        position=position,
        title=chapter["title"],
        intro=chapter["intro"],
        objectives=chapter["objectives"],
        exercise_title=chapter["exercise_title"],
        exercise_objective=chapter["exercise_objective"],
        next_chapter=next_chapter["title"] if next_chapter else "Next Module",
        next_link=f"../{next_chapter['filename']}" if next_chapter else "../"
    )
    
    filepath = week_dir / chapter["filename"]
    with open(filepath, 'w') as f:
        f.write(content)
    
    print(f"  ✅ Created: {filepath.name}")

def main():
    """Generate all chapter templates"""
    docs_dir = Path(__file__).parent.parent / "book" / "docs"
    
    print("=" * 60)
    print("Physical AI Textbook - Content Template Generation")
    print("=" * 60)
    
    for week_key, week_data in COURSE_STRUCTURE.items():
        week_dir = docs_dir / week_key
        week_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"\n📁 {week_data['title']}")
        
        chapters = week_data["chapters"]
        for i, chapter in enumerate(chapters):
            next_chapter = chapters[i + 1] if i + 1 < len(chapters) else None
            generate_chapter(week_dir, chapter, i + 1, next_chapter)
    
    print("\n" + "=" * 60)
    print("✅ All chapter templates generated!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Review generated templates in book/docs/")
    print("2. Fill in detailed content using AI assistance")
    print("3. Add code examples and diagrams")
    print("4. Test all exercises")
    print("\nTip: Use Claude or GPT-4 to help expand each chapter!")

if __name__ == "__main__":
    main()
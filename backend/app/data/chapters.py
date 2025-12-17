from app.schemas.chapter import Chapter, Section

chapters = [

    Chapter(
        id=1,
        title="Introduction to Physical AI",
        description="Core concepts of Physical AI and embodied intelligence",
        sections=[
            Section(
                title="Definition of Physical AI",
                content="Physical AI systems are intelligent agents that sense, reason, and act within the physical world using embodied mechanisms."
            ),
            Section(
                title="Embodiment and Intelligence",
                content="Embodiment allows intelligence to emerge from interaction with the environment rather than pure computation."
            ),
        ]
    ),

    Chapter(
        id=2,
        title="Humanoid Robotics Architecture",
        description="System-level design of humanoid robots",
        sections=[
            Section(
                title="Mechanical Structure",
                content="Humanoid robots are designed with articulated joints and actuators to mimic human motion."
            ),
            Section(
                title="Sensors and Actuators",
                content="Sensors provide perception while actuators execute physical actions in humanoid robots."
            ),
        ]
    ),

    Chapter(
        id=3,
        title="Perception in Physical AI",
        description="Sensing and environment understanding",
        sections=[
            Section(
                title="Vision Systems",
                content="Cameras and depth sensors allow robots to interpret their surroundings."
            ),
            Section(
                title="Sensor Fusion",
                content="Multiple sensor inputs are fused to create a reliable perception model."
            ),
        ]
    ),

    Chapter(
        id=4,
        title="Decision Making and Control",
        description="Planning, learning, and control strategies",
        sections=[
            Section(
                title="Motion Planning",
                content="Planning algorithms generate safe and efficient movement trajectories."
            ),
            Section(
                title="Feedback Control",
                content="Control systems ensure stability and accuracy during physical interaction."
            ),
        ]
    ),

]


# Problem Formulation

## 1. System Setting

The paper considers a planar multi-robot system in 2D space. The system may contain three types of agents:

- landmarks,
- leaders,
- followers.

All of them are treated as agents, but they have different capabilities.

## 2. Agent Types

### Landmarks

Landmarks are static agents. They do not communicate with other agents.

### Leaders

Leaders are mobile agents. They also do not communicate with other agents.

### Followers

Followers are mobile agents with sensing and communication capabilities. Each follower can:

- measure its own self-displacement in its local coordinate frame,
- measure interior angles with respect to neighboring agents,
- communicate with neighboring followers.

## 3. Local Coordinate Frames

Each robot has its own local coordinate frame. The global frame is assumed to be fixed but unknown. A major difficulty is that different robot coordinate frames may have different orientations.

The paper considers both:

1. aligned coordinate frames,
2. unaligned coordinate frames.

The aligned case is simpler because all self-displacements can be described in a common orientation. The unaligned case is harder because self-displacements measured in different local frames must be related by unknown rotations.

## 4. Measurements

The paper mainly introduces the theory using inter-robot angle measurements, then discusses extensions to distance and bearing measurements.

The two most important measurements are:

### Signed Interior Angle

For robots i, j, and m, robot i can measure the signed interior angle with respect to robots j and m. This angle is measured counterclockwise and lies in the interval [-pi, pi).

This signed angle is independent of the orientation of robot i's local coordinate frame. This property is important for handling unaligned coordinate frames.

### Self-Displacement

Each follower i can measure its self-displacement between two consecutive time instants in its own local coordinate frame.

This can be obtained from wheel odometry, visual-inertial odometry, optical flow combined with IMU, or similar sensing methods.

## 5. Goal

The goal is to determine:

1. when relative localization is possible,
2. how to compute inter-agent relative positions,
3. how to handle unaligned coordinate frames,
4. how to improve localization accuracy under measurement noise.

The first question corresponds to relative localizability.

The second question corresponds to relative localization.

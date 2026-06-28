# Monte Carlo Laser-Based Robot Localization

<p align="center">
  <img src="docs/montecarlo-demo.gif" width="750">
</p>

<p align="center">

Particle Filter (Monte Carlo Localization) implementation developed using the Robotics Academy platform.

</p>

---

# Overview

This project implements a **Monte Carlo Localization (MCL)** algorithm for estimating the pose of a mobile robot in a known environment.

The localization process combines:

- Odometry-based motion model
- Laser sensor observation model
- Particle weighting
- Multinomial resampling
- Pose estimation from weighted particles

The implementation was developed as part of the **Introduction to Mobile Robotics** course.

---

# Algorithm Pipeline

```
Robot Motion
      │
      ▼
Motion Update
      │
      ▼
Laser Observation
      │
      ▼
Weight Update
      │
      ▼
Resampling
      │
      ▼
Pose Estimation
```

---

# Features

- Random particle initialization
- Motion model using odometry
- Ray Casting simulation
- Laser likelihood model
- Weight normalization
- Multinomial resampling
- Weighted pose estimation
- Real-time visualization in Robotics Academy

---

# Technologies

- Python 3
- Robotics Academy
- ROS 2 Humble
- Gazebo
- Docker

---

# Project Structure

```text
.
├── academy.py
├── README.md
└── docs
    └── montecarlo-demo.gif
```

---

# Results

The particle cloud gradually converges toward the robot's real position after successive prediction and correction steps.

The estimated pose is continuously computed using the weighted particle distribution.

---

# How to Run

1. Install Docker.
2. Run the Robotics Academy container.
3. Open the Montecarlo Laser Loc exercise.
4. Replace the template with `academy.py`.
5. Run the simulation.

---

# Theory

This implementation follows the Monte Carlo Localization algorithm described in:

- Probabilistic Robotics — Sebastian Thrun
- Chapter 8 – Particle Filters
- Robotics Academy – Monte Carlo Laser Localization

---

# Author

**Mariana Lins**

Federal University of Alagoas (UFAL)

Introduction to Mobile Robotics — 2026

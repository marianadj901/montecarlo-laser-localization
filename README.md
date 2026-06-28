# 🚗 Monte Carlo Laser-Based Robot Localization

<p align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![ROS2](https://img.shields.io/badge/ROS2-Humble-22314E?logo=ros)
![Gazebo](https://img.shields.io/badge/Gazebo-Simulator-orange)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![Status](https://img.shields.io/badge/Status-Completed-success)

</p>

<p align="center">
  <img src="docs/montecarlo-demo.gif" width="800"/>
</p>

<p align="center">
Particle Filter (Monte Carlo Localization) implemented using Robotics Academy.
</p>

---

## 📖 Overview

This project implements the **Monte Carlo Localization (MCL)** algorithm to estimate the pose of a mobile robot in a known environment using:

- Odometry
- Laser Scanner
- Particle Filter
- Multinomial Resampling

The implementation was developed for the **Introduction to Mobile Robotics** course at **Federal University of Alagoas (UFAL)**.

---

## ⚙️ Algorithm Pipeline

```text
🚗 Robot
      │
      ▼
📍 Motion Update
      │
      ▼
📡 Laser Observation
      │
      ▼
⚖️ Weight Update
      │
      ▼
🔄 Resampling
      │
      ▼
📌 Pose Estimation
```

---

## ✨ Features

- ✅ Random particle initialization
- ✅ Motion model using odometry
- ✅ Ray Casting sensor simulation
- ✅ Laser likelihood model
- ✅ Weight normalization
- ✅ Multinomial resampling
- ✅ Pose estimation
- ✅ Real-time particle visualization

---

## 🛠 Technologies

| Technology | Version |
|------------|---------|
| Python | 3 |
| Robotics Academy | Latest |
| ROS 2 | Humble |
| Gazebo | Included |
| Docker | Latest |

---

## 📂 Project Structure

```text
.
├── academy.py
├── README.md
└── docs
    └── montecarlo-demo.gif
```

---

## 📈 Results

The particle cloud converges toward the robot's real position after successive prediction and correction steps.

The estimated pose is continuously computed from the weighted particle distribution.

---

## ▶️ Running

```bash
1. Install Docker

2. Start Robotics Academy

3. Open the MonteCarlo Laser Loc exercise

4. Replace the template with academy.py

5. Run the simulation
```

---

## 📚 References

- Sebastian Thrun, *Probabilistic Robotics*
- Chapter 8 — Particle Filters
- Robotics Academy — Monte Carlo Laser Localization

---

## 👩‍💻 Author

**Mariana Lins**

Federal University of Alagoas (UFAL)

Introduction to Mobile Robotics — 2026

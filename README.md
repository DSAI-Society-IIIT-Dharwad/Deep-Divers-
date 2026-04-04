# DRL Autonomous Navigation

This project now supports two environment backends behind the same Gymnasium-style interface:

- `mock`: the lightweight Python environment already used for local DRL iteration.
- `ros2_gazebo`: a ROS 2 + Gazebo bridge that consumes `/odom` and `/scan`, publishes `/cmd_vel`, and can reset Gazebo through `/reset_simulation`.

## Quick start

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Train with the default mock environment:

```bash
python -m src.main --config configs/default.yaml
```

Evaluate a trained policy:

```bash
python -m src.main evaluate --config configs/default.yaml --model models/ppo_model.zip --episodes 20
```

## ROS 2 / Gazebo simulation

System dependencies are required outside Python:

- ROS 2 Humble or newer
- Gazebo with `gazebo_ros`
- `robot_state_publisher`, `joint_state_publisher`
- A Linux ROS 2 environment with `source /opt/ros/<distro>/setup.bash`

Use the simulation config:

```bash
python -m src.main --config configs/ros2_gazebo.yaml
```

Starter simulation assets are included under `simulation/ros2/`:

- `launch/sim.launch.py`
- `worlds/navigation.world`
- `urdf/diff_drive_bot.urdf`

The bridge environment expects these topics/services by default:

- `/cmd_vel`
- `/odom`
- `/scan`
- `/reset_simulation`

Update `configs/ros2_gazebo.yaml` if your robot uses namespaced topics.

## Project scope from the PDF

This repo is set up as an MVP for the project described in `DRL_Robot_Final.pdf`:

- Observations: LiDAR-like distance readings + odometry state
- Policy: DRL agent chooses navigation actions
- Objectives: reach goal quickly, avoid collisions, improve reward
- Evaluation: time to goal, collision rate, average reward

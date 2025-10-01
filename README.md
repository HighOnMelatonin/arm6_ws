# 6 Motor Arm

## Table of contents
- [6 Motor Arm](#6-motor-arm)
  - [Table of contents](#table-of-contents)
  - [About](#about)
  - [Dependencies](#dependencies)
  - [Repository Structure](#repository-structure)
  - [URDF](#urdf)
  - [Launchers](#launchers)
    - [Gazebo Launcher](#gazebo-launcher)
    - [View Launcher](#view-launcher)
    - [Controller Launcher](#controller-launcher)
  - [Start Here](#start-here)
  - [startup.sh](#startupsh)
  - [Credits](#credits)

## About
Package to simulate a 6 motor arm, 1 motor for waist rotation, 1 motor for pinching toolhead, 1 motor for toolhead rotation and 3 motors for joints

## Dependencies
This project assumes you have a working ROS2 jazzy install, gazebo harmonic and the normal dependencies of these frameworks.

## Repository Structure

## URDF

## Launchers
### Gazebo Launcher
### View Launcher
### Controller Launcher

## Start Here
To automate some of the repetitive tasks (because I'm lazy), run `startup.sh` in bash. Refer to
[startup.sh](#startupsh)<br>

## startup.sh
startup.sh takes in an argument to run various launchers related to the arm6 package.

Example of use:
`. startup.sh g` will execute `colcon build` and `. install/local_setup.sh`, parameter "g" triggers the execution of `ros2 launch arm6 gazebo.launch.py`

Arguments:
```
st runs send_trajectory.launch.py
g runs gazebo.launch.py
v runs view_r6bot.launch.py
c runs r6bot_controller.launch.py
no args will not run any launchers and will display this message
```

## Credits
This project was built on top of [6 DOF bot](https://control.ros.org/rolling/doc/ros2_control_demos/example_7/doc/userdoc.html), [gazebo](https://control.ros.org/rolling/doc/ros2_control_demos/example_9/doc/userdoc.html) and [carlikebot](https://control.ros.org/rolling/doc/ros2_control_demos/example_11/doc/userdoc.html)

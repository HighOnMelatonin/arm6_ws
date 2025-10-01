# 6 Motor Arm

## About

## Dependencies
This project assumes you have a working ROS2 jazzy install, gazebo harmonic and the normal dependencies of these frameworks

## Repository Structure

## URDF

## Launchers

## Start Here
To automate some of the repetitive tasks, run `startup.sh` in bash. <br>

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

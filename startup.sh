#!/bin/bash

#Startup for arm6


build () {
	export GZ_SIM_RESOURCE_PATH=/home/ruianh/arm6_ws/install/arm6/share
	colcon build
	. install/local_setup.sh
	echo "Built and installed locally"
	echo ""
}


case $1 in
	st)
		build
		echo "Sending trajectory"
		echo ""
		ros2 launch arm6 send_trajectory.launch.py
		;;

	g)
		build
		echo "running with gazebo"
		ros2 launch arm6 gazebo.launch.py
		;;

	v)
		build
		echo "running with rviz only"
		ros2 launch arm6 view_r6bot.launch.py
		;;

	c)
		build
		echo "running with controller"
		ros2 launch arm6 r6bot_controller.launch.py
		;;

	*)
		echo "Startup will build and install arm6 locally"
		echo "Run with arguments to run different launchers"
		echo ""
		echo "st runs send_trajectory.launch.py"
		echo "g runs gazebo.launch.py"
		echo "v runs view_r6bot.launch.py"
		echo "c runs r6bot_controller.launch.py"
		echo "no args will not run any launchers and will display this message"
		;;
esac



import serial
import time
import rclpy
import threading
import os
from typing import List
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
from sensor_msgs.msg import JointState
from std_msgs.msg import String

## Set up listener to listen to website for commands

class ArmController(Node):
    def __init__(self):
        super().__init__('arm_controller')

        ## Parameters
        self.declare_parameter('serial_port', '/dev/ttyUSB0')
        self.declare_parameter('baud_rate', 115200)

        ## Get parameters
        self.serial_port = self.get_parameter('serial_port').value
        self.baud_rate = self.get_parameter('baud_rate').value

        self.joint_names = [
            'joint0',
            'joint1',
            'joint2',
            'joint3',
            'joint4',
            'joint5'
        ]

        ## Initialise serial connection
        self.serial_connnection = None
        self.connect_serial()

        ## Joint state tracking
        self.current_joint_positions = [0.0] * len(self.joint_names)
        self.target_joint_positions = [0.0] * len(self.joint_names)

        self.joint_state_pub = self.create_publisher(
            JointState,
            '/hand/joint_states',
            10
        )

        self.connection_status_pub = self.create_publisher(
            String,
            '/hand_connection_status',
            10
        )

        self.timer = self.create_timer(0.02, self.publish_joint_states)

        self.serial_thread = threading.Thread(target=self.serial_communication_loop)
        self.serial_thread.daemon = True
        self.serial_thread.start()

        self.get_logger().set_level(rclpy.logging.LoggingSeverity.DEBUG)
        self.get_logger().info('Dexterous Hand Controller initialised')

        self.carCommands = {
            "FORWARD":"QJ",
            "BACKWARD":"HT",
            "LEFT":"ZZ",
            "RIGHT":"YZ",
            "LEFT ISH":"ZPY",
            "RIGHT ISH":"YPY",
            "STOP":"TZ",
            "TRACKING":"ZNXJ",
            "AVOID OBS":"ZYBZ",
            "FOLLOW":"GSGN"
        }

        self.movetime = 1000 # Default move time in ms (for arm servos)

    def connect_serial(self):
        try:
            self.serial_connnection = serial.Serial(self.serial_port, self.baud_rate, timeout=1.0)
            self.get_logger().info(f'Serial connection established on {self.serial_port}')
        
        except Exception as e:
            self.get_logger().error(f'Failed to connect to serial port: {e}')
            self.serial_connection = None

    def send_joint_commands(self, joint_positions: List[int]):
        """
        Craft commands to the arm servos
        """
        if not self.serial_connection:
            return
        
        servo0, servo1, servo2, servo3, servo4, servo5 = joint_positions
        command = f"{{#000P{servo0:0>4d}T{self.movetime:0>4d}!#001P{servo1:0>4d}T{self.movetime:0>4d}!#002P{servo2:0>4d}T{self.movetime:0>4d}!#003P{servo3:0>4d}T{self.movetime:0>4d}!#004P{servo4:0>4d}T{self.movetime:0>4d}!#005P{servo5:0>4d}T{self.movetime:0>4d}!}}"
        self.send_command(command)

    def send_move_commands(self, command:str):
        """
        Craft commands to the car component for movement

        Legal commands:
            "FORWARD"
            "BACKWARD"
            "LEFT"
            "RIGHT"
            "LEFT ISH"
            "RIGHT ISH"
            "STOP"
            "TRACKING"
            "AVOID OBS"
            "FOLLOW"
        """
        if not self.serial_connection:
            return
        
        if command in self.carCommands:
            command_to_send = f"${self.carCommands[command]}!"
            self.send_command(command_to_send)

    def send_command(self, command:str):
        if self.serial_connection and self.serial_connection.is_open:
            try:
                self.serial_connection.write(command.encode('utf-8'))
                self.get_logger().debug(f'Sent command: {command}')
            except Exception as e:
                self.get_logger().error(f'Error sending command: {e}')
                self.reconnect_serial()

    def serial_communication_loop(self):
        ## Handle incoming serial data (arm shouldn't send much back)
        while rclpy.ok():
            if self.serial_connection and self.serial_connection.is_open:
                try:
                    line = self.serial_connection.readline().decode('utf-8').strip()
                    if line:
                        self.get_logger().debug(f'Received: {line}')
                        self.process_serial_data(line)
                except Exception as e:
                    self.get_logger().error(f'Error reading from serial: {e}')
                    self.reconnect_serial()

            time.sleep(0.01)

    def publish_joint_states(self):
        joint_state = JointState()
        joint_state.header.stamp = self.get_clock().now().to_msg()
        joint_state.name = self.joint_names
        joint_state.position = self.current_joint_positions

        self.joint_state_pub.publish(joint_state)

        status_msg = String()
        if self.serial_connection and self.serial_connection.is_open:
            status_msg.data = "Connected"
        else:
            status_msg.data = "Disconnected"
        
        self.connection_status_pub.publish(status_msg)

    def reconnect_serial(self):
        if self.serial_connection:
            try:
                self.serial_connection.close()
            except:
                pass
        
        os.system("reset_usb")
        while self.serial_connection is None:
            self.get_logger().info('Attempting to reconnect to serial port...')
            self.connect_serial()
            if self.serial_connection:
                self.logger().info('Reconnected to serial port')
                break
            else:
                self.get_logger().info('Reconnection failed, retrying in 2 seconds...')
                time.sleep(2)

    def destroy_node(self):
        if self.serial_connection and self.serial_connection.is_open:
            self.send_move_commands("STOP")
            self.send_joint_commands([1500]*6)  # Move to neutral position
            self.serial_connection.close()
        super().destroy_node()


def main(args=None):
    try:
        with rclpy.init(args=args):
            arm_controller = ArmController()
            rclpy.spin(arm_controller)

    except ExternalShutdownException:
        pass

    finally:
        if 'arm_controller' in locals():
            arm_controller.destroy_node()
        
        rclpy.shutdown()

if __name__ == '__main__':
    main()
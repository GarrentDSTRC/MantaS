import rospy
from sensor_fish.msg import Warmdepth
from motion_control.msg import MotorCommandMsg

class DepthController:
    def __init__(self, target_depth):
        self.target_depth = target_depth
        self.current_depth = 0.0
        self.kp = 1.0  # 比例增益
        self.kd = 0.1  # 微分增益
        self.previous_error = 0.0
        self.previous_time = None

        # 发布器，控制推进器
        self.motor_pub = rospy.Publisher('motor_commands', MotorCommandMsg, queue_size=10)

        # 订阅深度传感器数据
        rospy.Subscriber('depth_sensor_data', Warmdepth, self.depth_callback)

    def depth_callback(self, msg):
        self.current_depth = msg.depth

    def start_depth_control(self):
        rate = rospy.Rate(10)  # 10Hz 控制频率
        while not rospy.is_shutdown():
            self.control_step()
            rate.sleep()

    def control_step(self):
        error = self.target_depth - self.current_depth
        current_time = rospy.get_time()
        derivative = 0.0

        if self.previous_time is not None:
            delta_time = current_time - self.previous_time
            derivative = (error - self.previous_error) / delta_time

        control_signal = self.kp * error + self.kd * derivative
        control_signal = max(min(control_signal, 255), -255)

        self.send_motor_commands(control_signal)

        self.previous_error = error
        self.previous_time = current_time

    def send_motor_commands(self, command):
        for pid in [2, 3, 4]:
            motor_msg = MotorCommandMsg(ID=pid, command=int(command))
            self.motor_pub.publish(motor_msg)
            rospy.loginfo(f"Sent command {command} to propeller {pid}")

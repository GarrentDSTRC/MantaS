#!/usr/bin/env python3

import rospy
from manta.msg import CommandMsg  # 导入新的通用消息类型
import json
import os
import sys
import time


# 确保当前脚本目录在 sys.path 中
script_dir = os.path.dirname(__file__)
if script_dir not in sys.path:
    sys.path.append(script_dir)

def load_config(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)
    return config

def send_command(topic, ID, command):
    # 初始化ROS节点（如果尚未初始化）
    if not rospy.core.is_initialized():
        rospy.init_node('actuation_loco_node', anonymous=True)
    
    # 创建一个Publisher对象，发布到指定的主题
    pub = rospy.Publisher(topic, CommandMsg, queue_size=10)

    # 创建CommandMsg消息实例
    command_msg = CommandMsg()

    # 等待节点准备好发布消息
    rospy.sleep(0.01)

    # 发送指定ID和命令的消息
    command_msg.ID = ID
    command_msg.command = command
    pub.publish(command_msg)
    rospy.loginfo("Sent command to topic %s with ID %s and command %s" % (topic, ID, command))

    # 保持节点运行一段时间，以便命令被处理
    rospy.sleep(0.01)

def execute_config(config_file):
    # 加载配置文件
    config = load_config(config_file)

    if 'time' in config:
        durance = config['time']
        start = time.time()
        while time.time() - start < durance:
            # 发布推进器命令
            for propeller in config['propellers']:
                send_command('propeller_commands', propeller['id'], propeller['command'])
            # 发布电机命令
            for motor in config['motors']:
                send_command('motor_commands', motor['id'], motor['command'])
            time.sleep(durance)

        for _ in range(2):
            # 发布推进器命令
            for propeller in config['propellers']:
                send_command('propeller_commands', propeller['id'], 0)
            # 发布电机命令
            for motor in config['motors']:
                send_command('motor_commands', motor['id'], 0)
            time.sleep(0.5)
    else:
        for _ in range(2):
            # 发布推进器命令
            for propeller in config['propellers']:
                send_command('propeller_commands', propeller['id'], propeller['command'])

            # 发布电机命令
            for motor in config['motors']:
                send_command('motor_commands', motor['id'], motor['command'])
            time.sleep(0.5)

def main():
    config_files = {
        '1': os.path.join(script_dir, '../config/config1.json'),
        '2': os.path.join(script_dir, '../config/config2.json'),
        '3': os.path.join(script_dir, '../config/config3.json'),
        '4': os.path.join(script_dir, '../config/config4.json'),

        '5': os.path.join(script_dir, '../config/config5.json'),
        '6': os.path.join(script_dir, '../config/config6.json'),
        '7': os.path.join(script_dir, '../config/config7.json'),
        '8': os.path.join(script_dir, '../config/config8.json'),
        '9': os.path.join(script_dir, '../config/config9.json'),
    }

    while not rospy.is_shutdown():
        # 提示用户选择配置文件
        print("Please select a config file:")
        print("1: config1.json")
        print("2: config2.json")
        print("3: config3.json")
        print("4: config4.json")
        print("5: config5.json")
        print("6: config6.json")
        print("7: config7.json")
        print("8: config8.json")
        print("9: Execute config8 and config9 in sequence")
        
        config_id = input("Enter the number of the config file you want to use: ")

        if config_id == '9':
            for _ in range(2):
            # 执行config8.json和config9.json
                execute_config(config_files['8'])
                execute_config(config_files['9'])
        elif config_id in config_files:
            config_file = config_files[config_id]
            execute_config(config_file)
        else:
            print("Invalid config ID. Please specify a valid number.")
            continue

        # # 提示用户是否继续
        # continue_choice = input("Do you want to continue? (y/n): ")
        # if continue_choice.lower() != 'y':
        #     break

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass

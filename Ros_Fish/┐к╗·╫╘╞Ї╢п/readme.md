#配置

1.脚本目录：/home/jetson/network_checker.py

2.更新服务配置文件：
确保服务配置文件正确。以下是示例：

sudo nano /etc/systemd/system/network_checker.service

[Unit]
Description=Start Actuation Control Script
After=network.target

[Service]
User=jetson
Group=jetson
WorkingDirectory=/home/jetson/Dayu_Scripts
ExecStart=/home/jetson/Dayu_Scripts/motor_protect.sh
Restart=on-failure
Environment="ROS_MASTER_URI=http://192.168.50.10:11311"
Environment="ROS_IP=192.168.50.11"
Environment="PYTHONUNBUFFERED=1"

[Install]
WantedBy=multi-user.target



#重新加载并启动服务，检查服务状态：
sudo systemctl daemon-reload
sudo systemctl start network_checker.service
sudo systemctl status network_checker.service

#停止正在运行的服务：
sudo systemctl stop network_checker.service

#############################

sudo gedit /etc/systemd/system/IO_node.service


重新加载并启动服务
sudo systemctl daemon-reload
sudo systemctl enable IO_node.service
sudo systemctl disable IO_node.service
sudo systemctl stop IO_node.service 
sudo systemctl stop actuation_control.service
sudo systemctl start IO_node.service
sudo systemctl start actuation_control.service

#############################

tail -f IO_node.log 

禁用服务：
sudo systemctl enable actuation_control.service
sudo systemctl disable actuation_control.service
sudo systemctl start actuation_control.service
sudo systemctl stop actuation_control.service
sudo systemctl status actuation_control.service


服务：
sudo systemctl enable IO_node.service
sudo systemctl enable actuation_control.service

禁用服务：
sudo systemctl disable actuation_control.service
sudo systemctl disable IO_node.service


传文件
scp -r sys test@192.168.50.10:~/

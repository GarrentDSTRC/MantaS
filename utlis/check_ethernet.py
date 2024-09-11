import subprocess
import re
import time
import logging
from datetime import datetime, timezone

def setup_logging():
    logging.basicConfig(
        filename='interface_status.log',
        level=logging.INFO,
        format='%(asctime)s %(message)s',
        datefmt='%Y-%m-%dT%H:%M:%SZ'
    )

def get_interface_status(interface):
    try:
        result = subprocess.run(['ifconfig', interface], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print(f"Error: {result.stderr.strip()}")
            return None

        output = result.stdout
        return output
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def parse_interface_status(output):
    # 正则表达式匹配
    flags_match = re.search(r'flags=\d+<(.+?)>', output)
    rx_packets_match = re.search(r'RX packets (\d+)', output)
    tx_packets_match = re.search(r'TX packets (\d+)', output)

    if flags_match and rx_packets_match and tx_packets_match:
        flags = flags_match.group(1).split(',')
        rx_packets = int(rx_packets_match.group(1))
        tx_packets = int(tx_packets_match.group(1))

        return {
            'flags': flags,
            'rx_packets': rx_packets,
            'tx_packets': tx_packets
        }
    return None

def check_interface_communication(interface):
    while True:
        output = get_interface_status(interface)
        if output:
            status = parse_interface_status(output)
            if status:
                if 'UP' in status['flags'] and 'RUNNING' in status['flags']:
                    if status['rx_packets'] > 0 or status['tx_packets'] > 0:
                        print("The network interface is up and communicating.")
                    else:
                        print("The network interface is up but not communicating.")
                else:
                    print("The network interface is down.")
            else:
                print("Failed to parse interface status.")
        else:
            print("Failed to get interface status.")
        
        time.sleep(1)  # 每10秒检测一次

if __name__ == "__main__":
    setup_logging()
    interface = 'enx00e04c6013c8'  # 替换为你的以太网接口名
    check_interface_communication(interface)

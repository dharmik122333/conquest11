from scapy.all import sniff
from collections import defaultdict
import time
from logger import log_alert
from vendor import get_vendor
import socket

traffic = defaultdict(int)
mac_map = {}
known_devices = set()
blocked_devices = set()

shared_data = {}

start_time = time.time()
local_ip = socket.gethostbyname(socket.gethostname())

def is_local_ip(ip):
    return ip.startswith(("192.168.", "10.", "172."))

def process_packet(packet):
    global traffic, mac_map, start_time, known_devices, blocked_devices, shared_data

    if packet.haslayer("IP"):
        src_ip = packet["IP"].src

        traffic[src_ip] += 1

    current_time = time.time()
    elapsed = current_time - start_time

    if elapsed >= 5:

        local_traffic = {
            ip: count for ip, count in traffic.items()
            if is_local_ip(ip)
        }

        if local_traffic:
            shared_data.clear()
            shared_data.update(local_traffic)

            print("📊 Updated shared data:", shared_data)

        traffic.clear()
        start_time = time.time()

def start_monitoring():
    print("🚀 Monitoring started...")

    # 🔥 IMPORTANT: specify interface
    sniff(prn=process_packet, store=False, iface="Wi-Fi")

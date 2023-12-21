from scapy.all import *
import time

correspondence = {"6":"fuel","7":"refuel","24":"enery_speed","40":"order_rub","54":"phy_l_rub","56":"phy_r_rub","108":"l_rub","109":"r_rub"}
table_min_max = {"fuel":{"min":0,"max":100},"refuel":{"min":0,"max":1},"enery_speed":{"min":0,"max":80},"order_rub":{"min":0,"max":80},"phy_l_rub":{"min":0,"max":80},"phy_r_rub":{"min":0,"max":80},"l_rub":{"min":0,"max":80},"r_rub":{"min":0,"max":80}}

SCADA_IP = "192.168.15.2"
CC_IP = "192.168.15.1"
NTP_IP = "192.168.15.3"

whitelist = [SCADA_IP, CC_IP, NTP_IP]

# dictionnary with IP as key and a list containing each request time as a value
ratelimit_list = {}
deltatime = 10           # seconds interval used for ratelimiting
ratelimit_deltatime = 10 # number of request in 'deltatime' second which will trigger the ratelimit logs

def find_too_old_times(current_time, ip_times_list):
    for idx, time in enumerate(ip_times_list):
        if current_time - time > deltatime:
            return idx
    return 0

def refresh_ratelimit_list(current_time):
    global ratelimit_list
    for ip in ratelimit_list.keys():
        find_too_old_idx = find_too_old_times(current_time, ratelimit_list[ip])
        ratelimit_list[ip] = ratelimit_list[ip][find_too_old_idx:]

def capture_modbus_traffic(interface="vboxnet2"):
    sniff(iface=interface, prn=process_modbus_packet, store=0, filter="port 502")
    
def process_modbus_packet(packet):
    global ratelimit_list
    if packet[IP].src not in whitelist:
        generate_security_alert(f"Wrong IP Address try to send ModBus request ({packet[IP].src})")
    
    # ratelimiting security
    current_time = time.time()
    refresh_ratelimit_list(current_time)
    try:
        ratelimit_list[packet[IP].src].append(current_time)
    except KeyError:
        ratelimit_list[packet[IP].src] = [current_time]
    for k in ratelimit_list.keys():
        if len(ratelimit_list[k]) > ratelimit_deltatime:
            generate_security_alert(f"Too much requests sent ({len(ratelimit_list[k])}) in {deltatime} seconds by {packet[IP].src}")


    if Raw in packet:
        data_b = bytes(packet[Raw].load)[-2:]
        data = int.from_bytes(data_b,"big")
        
        register_b = bytes(packet[Raw].load)[-4:-2]
        register = int.from_bytes(register_b,"big")
        
        if(str(register) in correspondence):
            name_register = correspondence[str(register)]
            min_data = table_min_max[name_register]["min"]
            max_data = table_min_max[name_register]["max"]
        
            if(data < min_data or data > max_data):
                generate_security_alert("data : " + str(data) + " of register : " + str(register) + " is out of range. Expect value between " + str(min_data) + " and " + str(max_data))

def generate_security_alert(message):
    
    print(f"Security Alert: {message}")

# Dans la fonction process_modbus_packet, ajoutez la logique de détection d'anomalies et générez des alertes en conséquence.

if __name__ == "__main__":
    capture_modbus_traffic()

from scapy.all import *

correspondence = {"6":"fuel","7":"refuel","24":"enery_speed","40":"order_rub","54":"phy_l_rub","56":"phy_r_rub","108":"l_rub","109":"r_rub"}
table_min_max = {"fuel":{"min":0,"max":100},"refuel":{"min":0,"max":1},"enery_speed":{"min":0,"max":80},"order_rub":{"min":0,"max":80},"phy_l_rub":{"min":0,"max":80},"phy_r_rub":{"min":0,"max":80},"l_rub":{"min":0,"max":80},"r_rub":{"min":0,"max":80}}

SCADA_IP = "192.168.15.2"
CC_IP = "192.168.15.1"
NTP_IP = "192.168.15.3"

def capture_modbus_traffic(interface="vboxnet0"):
    sniff(iface=interface, prn=process_modbus_packet, store=0, filter="port 502")
    
def process_modbus_packet(packet):
    if packet[IP].src != SCADA_IP and packet[IP].src != CC_IP and packet[IP].src != NTP_IP:
        generate_security_alert("Wrong IP Address try to send ModBus request")
    
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
                generate_security_alert("data : " + data + " of register : " + register + " is out of range. Expect value between " + min_data + " and " + max_data)

def generate_security_alert(message):
    
    print(f"Security Alert: {message}")

# Dans la fonction process_modbus_packet, ajoutez la logique de détection d'anomalies et générez des alertes en conséquence.

if __name__ == "__main__":
    capture_modbus_traffic()

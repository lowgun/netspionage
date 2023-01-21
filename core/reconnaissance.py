import requests 
import json
import re
import scapy.all as scapy
from pick import pick

def recon_choice(choice, target, manual_input):
    if choice == '1':
        choose_mac_address(target)
        return()
    elif choice == '2':
        input_mac_address(manual_input)
        return()
    else:
        exit()

def choose_mac_address(target):
    scan_addresses(target)
    return()

def input_mac_address(manual_input):
    address_api_call(manual_input)
    return()

# Helper Functions

def address_api_call(address):
    url = ("https://macvendors.co/api/" + address)
    response=requests.get(url)
    result=response.json()
    if result["result"]:
        json_object=result['result']
        if "error" in json_object:
            print("No MAC Address Found!")
            return()
        transcribe_api_results(json_object)
    else:
        print("Error: Something Went Wrong")

def transcribe_api_results(json_object):
    for key in json_object:
        value = json_object[key]
        print(f"\n {snake_case_to_normal(key)}: {value}")

def snake_case_to_normal(snake_text):
    temp = snake_text.split('_')
    res = temp[0].upper() + ''.join(' ' + ele.title().upper() for ele in temp[1:])
    return res

# Display MAC Address List

def scan_addresses(target):
    broadcast_packets = create_packet(target)
    success_packets = transmit_packet(broadcast_packets)
    entries = parse_response(success_packets)
    display_picker(entries)

def create_packet(ip):
    arp_request = scapy.ARP(pdst=ip)  # create a ARP request object by scapy
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")  # We have set the destination
    arp_request_broadcast = broadcast / arp_request
    return (arp_request_broadcast)

def transmit_packet(packet):
    success_list, failure_list = scapy.srp(packet, timeout=1, verbose=False)
    return success_list

def parse_response(success_list):
    targets = []
    for success in success_list:
        entry = {'mac': success[1].hwsrc}
        targets.append(entry)
    return targets

def display_picker(element_entries):
    mac_list = [el['mac'] for el in element_entries]
    option, index = pick(mac_list, 'SELECT MAC Address', indicator='=>', default_index=0)


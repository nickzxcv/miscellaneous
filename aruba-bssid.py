import argparse
import re

# based on
# https://community.arubanetworks.com/blogs/anandkumar-sukumar1/2020/10/20/how-is-the-bssid-derived-from-the-access-point-ethernet-mac-address
parser = argparse.ArgumentParser(description='Convert Aruba AP MAC to BSSID.')
parser.add_argument('mac', metavar='MAC', type=str, help='AP Ethernet MAC')
args = parser.parse_args()

def to_bssid(my_mac):
    oui = my_mac >> 24
    
    least20bits = my_mac % (2**20)
    least20bitsplus16 = least20bits << 4
    most4oftheleast20 = least20bitsplus16 >> 20
    xoredmost4 = most4oftheleast20 ^ 8
    newleast20 = least20bitsplus16 % (2**20)
    
    firstbssid = (oui << 24) + (xoredmost4 << 20) + newleast20
    
    return firstbssid

def hex_to_int(hex_mac):
    return int(hex_mac.replace(":", ""), 16)

def int_to_hex(int_mac):
    hex_mac = ""
    pop = 48
    while pop > 0:
        pop -= 8
        octet = (int_mac >> pop) & 255
        hex_mac += "{:02x}".format(octet)
        if pop > 0:
            hex_mac += ":"
    return hex_mac
        
if re.match('^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$', args.mac):
    int_mac = hex_to_int(args.mac)
    new_int_mac = to_bssid(int_mac)
    
    print(int_to_hex(new_int_mac))
else:
    print("Invalid MAC address format. Use all digits and use colons.")

 

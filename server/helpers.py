from ipaddress import ip_address, IPv4Address
import re
  
def validIPAddress(IP: str) -> str:
    try:
        return "ipv4" if type(ip_address(IP)) is IPv4Address else "ipv6"
    except ValueError:
        return "Invalid"
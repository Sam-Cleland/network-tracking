''' network capture

This script allows the user to capture network packets through a specified
port over a duration of time. The source and destination IP addresses are
extracted and converted to a geo location (longitude/latitude) and returned
as a kml string which can be displayed by GIS software.

This script requires that Tshark be installed, https://tshark.dev/, and the
GeoLiteCity database, https://github.com/mbcc2006/GeoLiteCity-data, be in the
root folder for the project.
'''

import dpkt
import socket
import pygeoip
import os
import pyshark

gi = pygeoip.GeoIP('GeoLiteCity.dat')

interface_name = 'xxxx'
capture_time = 300
output_name = "kml_out"
user = "xxxx"


def capture_packets(interface_name: str, capture_time: int) -> list:
    ''' Captures source and destination IP addresses captured
        through specifed port for the specified time duration.
        
        Args:
            interface_name (str): The name of the port to capture
                network traffic.
            capture_time (int): The time to capture network traffic
                in seconds.
        
        Returns:
            List: a list of pairs of source and destination IP address
                for each network packet. 
    '''
    
    packet_list = []
    capture = pyshark.LiveCapture(
        interface=interface_name
        )
    capture.sniff(timeout=capture_time)
    packets = [pkt for pkt in capture._packets]
    capture.close()
    try:
        for packet in packets:
            source_ip = packet.ip.src
            destination_ip = packet.ip.dst
            packet_list.append([source_ip, destination_ip])
    except AttributeError:
        pass
    finally:
        return packet_list
    
    
def plotIPs(pcap: list) -> str:
    ''' Creates a string of kml text for each unique destination
        IP address in the list returned by capture_packets().
        
        Args:
            pcap (list): list of source/destiantion IP address pairs.
            
        Returns:
            str: kml body text containing line information for plotting.
    '''
    
    kmlPts = ''
    dst_list = []
    for row in pcap:
        dst = str(row[1])
        if dst not in dst_list:
            KML = retKML(dst)
            kmlPts = kmlPts + KML
            dst_list.append(dst)
        else:
            pass
    return kmlPts


def retKML(dstip: str) -> str:
    ''' Converts IP addresses to a geo location (longitude/latitude)
        and places this information into kml text. This requres a home
        IP address.
        
        Args:
            dstip (str): Destination IP address
            
        Returns:
            str: kml text with plotting information
    '''
    
    dst = gi.record_by_name(dstip)
    src = gi.record_by_name('xxx.xx.xxx.xx')  # add your home IP here
    try:
        dstlongitude = dst['longitude']
        dstlatitude = dst['latitude']
        srclongitude = src['longitude']
        srclatitude = src['latitude']
        city = dst['city']
        count = dst['country_name']
        kml = (
            '<Placemark>\n'
            '<name>%s, %s, %s</name>\n'
            '<extrude>1</extrude>\n'
            '<tessellate>1</tessellate>\n'
            '<styleUrl>#transBluePoly</styleUrl>\n'
            '<LineString>\n'
            '<coordinates>%6f,%6f\n%6f,%6f</coordinates>\n'
            '</LineString>\n'
            '</Placemark>\n'
        )%(
            dstip,
            city,
            count,
            dstlongitude,
            dstlatitude,
            srclongitude,
            srclatitude
            )
        return kml
    except:
        return ''


def main():
    f = capture_packets(interface_name, capture_time)
    kmlheader = '<?xml version="1.0" encoding="UTF-8"?> \n' \
        '<kml xmlns="http://www.opengis.net/kml/2.2">\n<Document>\n' \
        '<Style id="transBluePoly">' \
                '<LineStyle>' \
                '<width>1.5</width>' \
                '<color>501400E6</color>' \
                '</LineStyle>' \
                '</Style>'
    kmlfooter = '</Document>\n</kml>\n'
    kmldoc=kmlheader + plotIPs(f) + kmlfooter
    with open(f"{output_name}.kml", "w") as text_file:
        text_file.write(kmldoc)
    
    
if __name__ == '__main__':
    main()

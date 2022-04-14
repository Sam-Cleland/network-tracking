import pyshark

def capture_packets(interface_name: str, capture_time: int):
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
            
        



    
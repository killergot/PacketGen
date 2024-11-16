from scapy.layers.inet import ICMP, UDP,IP,TCP
from scapy.all import *
from decor import except_catch_packet,except_catch
from functools import reduce
import psutil

class PacketGenerator:
    @except_catch
    def __init__(self):
        self.setInterface(self.getInterfaceList()[0])
        self.list_packet : list[list[int|str]] = list()

    @except_catch_packet('IP')
    def getIpPacket(self,
                         src : str = '192.168.0.56',
                         dst : str = '8.8.8.8',
                         id_ip : int|str = 13559,
                         ttl : int|str = 56) -> IP:
        ip_packet = IP(src=src, dst=dst, ttl=int(ttl), id=int(id_ip))
        return ip_packet

    @except_catch_packet('ICMP')
    def getIcmpPacket(self,
                           type : int = 8,
                           code : int = 0,
                           id : int = 135,
                           ) -> ICMP:

        icmp_packet = ICMP(type=int(type), code=int(code), id=int(id))
        return icmp_packet

    @except_catch_packet('TCP')
    def getTcpPacket(self,
                           sport: int = 12345,
                           dport: int = 80,
                           flags: str = '',
                           seq: int = 1000,
                           ack: int = 0,
                           window: int = 1024,
                           payload: str = 'test payload'
                           ) -> TCP:

        tcp_layer = TCP(sport=sport, dport=dport, flags=flags, seq=seq, ack=ack, window=window)
        if 'P' in flags or flags == 'A':
            return tcp_layer / payload
        else:
            return tcp_layer


    @except_catch_packet('UDP')
    def getUdpPacket(self,
                           sport: int = 12345,
                           dport: int = 12366,
                           payload: str = 'test payload'
                           ) -> UDP:
        udp_layer = UDP(sport=sport, dport=dport)
        return udp_layer / payload

    @except_catch
    def sendPacket(self,*args : IP|ICMP|TCP|UDP) -> None:
        full_packet = reduce(lambda x, y: x / y, args)
        print(full_packet)
        send(full_packet)
        self.list_packet.append(self.extractPacketData(full_packet))

    @except_catch
    def getInterfaceList(self) -> list[str]:
        interfaces = list(psutil.net_if_addrs().keys())[1:]
        return list(map(str,interfaces))

    @except_catch
    def extractPacketData(self,packet : IP|TCP|ICMP|UDP) -> list[int|str] :
        """Преобразовывает сетевой пакет в массив с иформацией """
        packet_data : list[int|str] = list()
        protocol : str|int = packet[IP].proto
        if packet.haslayer(IP):
            if protocol == 0:
                protocol = 'IP'
            elif protocol == 1:
                protocol = 'ICMP'
            elif protocol == 6:
                protocol = 'TCP'
            elif protocol == 17:
                protocol = 'UDP'
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
        else:
            protocol = None
            src_ip = None
            dst_ip = None

        src_port, dst_port, flags = None, None, None
        if packet.haslayer(TCP):
            src_port = packet[TCP].sport
            dst_port = packet[TCP].dport
            flags = packet[TCP].flags
        elif packet.haslayer(UDP):
            src_port = packet[UDP].sport
            dst_port = packet[UDP].dport
        elif packet.haslayer(ICMP):
            id = packet[ICMP].id
            code = packet[ICMP].code

        payload = packet[Raw].load if packet.haslayer(Raw) else None
        print(payload)

        if protocol == 'TCP':
            packet_data.extend([protocol, src_ip,dst_ip,f'[{dst_port} -> {src_port}], {flags}', payload])
        elif protocol == 'UDP':
            packet_data.extend([protocol, src_ip,dst_ip,f'[{dst_port} -> {src_port}]', payload])
        elif protocol == 'IP':
            packet_data.extend([protocol, src_ip, dst_ip,'Just IP', payload])
        else:
            packet_data.extend([protocol, src_ip, dst_ip,f'id = {id}, code = {code}' , payload])
        print(packet_data)
        return packet_data


    @except_catch
    def setInterface(self, new_interface : str) -> None:
        if new_interface not in self.getInterfaceList():
            print(f'Интерфейс {new_interface} не был найден')
        else:
            print(new_interface)
            conf.iface = new_interface

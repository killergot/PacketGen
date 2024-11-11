from scapy.layers.inet import ICMP, UDP,IP,TCP
from scapy.all import *
from decor import except_catch_packet,except_catch
from functools import reduce
import psutil

class PacketGenerator:
    @except_catch
    def __init__(self):
        self.setInterface(self.getInterfaceList()[0])
        self.list_packet : list[IP|ICMP|UDP|TCP] = list()

    @except_catch_packet('IP')
    def getIpPacket(self,
                         src : str = '192.168.0.56',
                         dst : str = '8.8.8.8',
                         id_ip : int = 13559,
                         ttl : int = 56) -> IP:
        ip_packet = IP(src=src, dst=dst, ttl=ttl, id=id_ip)
        return ip_packet

    @except_catch_packet('ICMP')
    def getIcmpPacket(self,
                           type : int = 8,
                           code : int = 0,
                           id : int = 135,
                           ) -> ICMP:

        icmp_packet = ICMP(type=type, code=code, id=id)
        return icmp_packet

    @except_catch_packet('TCP')
    def getTcpPacket(self,
                           sport: int = 12345,
                           dport: int = 80,
                           flags: str = 'a',
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
        # self.addPacketInList(full_packet)

    @except_catch
    def getInterfaceList(self) -> list[str]:
        interfaces = list(psutil.net_if_addrs().keys())[1:]
        return list(map(str,interfaces))

    @except_catch
    def addPacketInList(self,packet: IP|ICMP|TCP|UDP) -> None:
        temp = []
        temp.append(packet.protocol)


    @except_catch
    def setInterface(self, new_interface : str) -> None:
        if new_interface not in self.getInterfaceList():
            print(f'Интерфейс {new_interface} не был найден')
        else:
            print(new_interface)
            conf.iface = new_interface

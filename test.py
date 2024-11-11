from PacketGen import PacketGenerator

temp = PacketGenerator()

a = temp.getIpPacket()
a = a / temp.getTcpPacket(flags='AP')
print(temp.list_packet)
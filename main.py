from PacketGen import PacketGenerator
from decor import except_catch

from UI import Ui_MainWindow
from PyQt6 import QtCore,QtGui, QtWidgets

class MyClass(Ui_MainWindow):
    def __init__(self):
        self.temp = PacketGenerator()

    def setupUi(self, PacketGen):
        super().setupUi(PacketGen)
        self.MyInit()


    @except_catch
    def MyInit(self) -> None:
        _translate = QtCore.QCoreApplication.translate
        self.create.clicked.connect(lambda: self.createPacket())
        self.int_list.clear()
        for i, v in enumerate(self.temp.getInterfaceList()):
            self.int_list.addItem("")
            self.int_list.setItemText(i, _translate("PacketGen", v))
        self.int_list.currentTextChanged.connect(lambda: self.temp.setInterface(self.int_list.currentText()))
        self.model = QtGui.QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['proto','src','dst','info'])
        self.Packet_view.setModel(self.model)
        self.Packet_view.setColumnWidth(0, 30)  # Ширина первого столбца 100 пикселей
        self.Packet_view.setColumnWidth(1, 100)  # Ширина второго столбца 150 пикселей
        self.Packet_view.setColumnWidth(2, 100)
        self.Packet_view.setColumnWidth(3, 130)
        self.selection_packet_model = self.Packet_view.selectionModel()
        self.selection_packet_model.selectionChanged.connect(self.on_selection_changed)


    @except_catch
    def on_selection_changed(self, selected, deselected):
        # Получаем индексы выбранных строк
        indexes = self.selection_packet_model.selectedRows()
        if indexes:  # Если есть выбранные строки
            selected_row = indexes[0].row()  # Берем первую выбранную строку
            self.label234 = QtWidgets.QLabel("Ваш текст здесь", self.centralwidget)
            self.label234.setGeometry(QtCore.QRect(10, 440, 381, 121))
            self.label234.setObjectName("label")
            print('asdfsdaf')

    @except_catch
    def add_data_to_table(self, data):
        '''Выводит отправленные пакеты в таблице'''
        items = [QtGui.QStandardItem(str(cell)) for cell in data[:-1]]
        self.model.appendRow(items)


    @except_catch
    def getFlags(self) -> str:
        flags: str = ''
        if self.SYN.isChecked():
            flags += 'S'
        if self.RST.isChecked():
            flags += 'R'
        if self.URG.isChecked():
            flags += 'U'
        if self.ACK.isChecked():
            flags += 'A'
        if self.ECN.isChecked():
            flags += 'E'
        if self.CWR.isChecked():
            flags += 'C'
        if self.PSH.isChecked():
            flags += 'P'
        if self.FIN.isChecked():
            flags += 'F'
        return flags

    @except_catch
    def createPacket(self) -> None:
        '''Обрабатывает нажатие кнопки Create
           - Создает пакет на основе веденных данных в разные поля
           - Если поля пустые, то не вносит их в создание пакета
                Тогда беруться дефолтные значения, чтоб пакет коректно был сформирован'''
        ip_layer = None
        kwargs: dict[str, str | int] = dict()
        if self.ip_src_box.isChecked():
            kwargs['src'] = self.ip_src_text.text()
        if self.ip_dst_box.isChecked():
            kwargs['dst'] = self.ip_dst_text.text()
        kwargs['id_ip'] = self.ip_id_text.text()
        kwargs['ttl'] = self.ip_ttl_text.text()
        kwargs = {k: v for k, v in kwargs.items() if len(str(v))}
        ip_layer = self.temp.getIpPacket(**kwargs)

        if self.just_ip.isChecked():
            self.temp.sendPacket(ip_layer)
        elif self.icmp.isVisible():
            kwargs.clear()
            kwargs['type'] = self.icmp_type_text.toPlainText()
            if self.icmp_code_box.isChecked():
                kwargs['code'] = self.icmp_code_text.toPlainText()
            if self.icmp_id_box.isChecked():
                kwargs['id'] = self.icmp_id_text.toPlainText()
            kwargs = {k: int(v) for k, v in kwargs.items() if len(v)}

            icmp_layer = self.temp.getIcmpPacket(**kwargs)
            self.temp.sendPacket(ip_layer, icmp_layer)
        elif self.TCP.isVisible():
            kwargs.clear()
            kwargs['sport'] = self.tcp_src_port.text()
            kwargs['dport'] = self.tcp_dst_port.text()
            kwargs['seq'] = self.tcp_seq.text()
            kwargs['ack'] = self.tcp_ack.text()
            kwargs['window'] = self.tcp_window.text()
            kwargs = {k: int(v) for k, v in kwargs.items() if len(v)}

            kwargs['payload'] = self.tcp_data_text_edit.toPlainText()
            kwargs['flags'] = self.getFlags()

            tcp_layer = self.temp.getTcpPacket(**kwargs)
            self.temp.sendPacket(ip_layer, tcp_layer)
        elif self.UDP.isVisible():
            kwargs.clear()
            kwargs['sport'] = self.udp_src_port.text()
            kwargs['dport'] = self.udp_dst_port.text()
            kwargs = {k: int(v) for k, v in kwargs.items() if len(v)}
            kwargs['payload'] = self.udp_data_text.toPlainText()

            udp_layer = self.temp.getUdpPacket(**kwargs)
            self.temp.sendPacket(ip_layer, udp_layer)


        self.add_data_to_table(self.temp.list_packet[-1])


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    PacketGenWin = QtWidgets.QMainWindow()
    ui = MyClass()
    ui.setupUi(PacketGenWin)
    PacketGenWin.show()
    sys.exit(app.exec())
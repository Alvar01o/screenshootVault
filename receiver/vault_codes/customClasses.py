#represent th port status and file receiver
class TransferInfo:
    BUSY = False
    AVAILABLE = True
    def __init__(self, status, udpInfo):
        self.status = status
        self.udpInfo = udpInfo
        pass
# store every packet received
class CustomPacket:
    def __init__(self, identifier, data):
        self.identifier = identifier
        self.data = data

#file transfired on port - data and file information
class UdpInfo:
    exit_flag = 0 #check

    def __init__(self, img_length = 0, file_name = '', buffer_size = 0, filehash = ''):
        if img_length is None:
            self.img_length = img_length
        if filehash is None:
            self.filehash = filehash
        if file_name is None:
            self.file_name = file_name
        if buffer_size is None:
            self.buffer_size = buffer_size

    @property
    def img_length(self):
        return self._img_length
    
    @img_length.setter
    def img_length(self, valor):
        self._img_length = valor

    @property
    def file_name(self):
        return self._file_name
    
    @file_name.setter
    def file_name(self, valor):
        self._file_name = valor

    @property
    def buffer_size(self):
        return self._buffer_size
    
    @buffer_size.setter
    def buffer_size(self, valor):
        n = int(self.img_length / valor)
        obj_array = []
        #get index correctly - todo
        for i in range(n):
            customPacket = CustomPacket(i, None)
            obj_array.append(customPacket)
        self.packet_status_array = obj_array
        self._buffer_size = valor

    def __str__(self):
        status_str = 0;
        for package_status in self.packet_status_array:
                print(type(package_status));
                status_str += 1
        return f"UdpInfo(file_name={self.file_name}, buffer_size={self.buffer_size}, img_length={self.img_length}, packet_status_array={status_str})"
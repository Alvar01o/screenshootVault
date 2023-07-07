#represent th port status and file receiver
class TransferInfo:
    BUSY = 0
    AVAILABLE = 1
    DEAD = 2
    
    def __init__(self, status, udpInfo):
        self.status = status
        self.udpInfo = udpInfo
        pass
    def __str__(self):
        return f"TransferInfo(status={self.status}, " + self.udpInfo.__str__() + ")"
# store every packet received
class CustomPacket:
    def __init__(self, identifier, data):
        self.identifier = identifier
        self.data = data
    def __str__(self):
        return f"CustomPacket(identifier={self.identifier})"
#file transfired on port - data and file information
class UdpInfo:
    exit_flag = 0 #check

    def __init__(self, img_length=0, file_name=None, buffer_size=None, filehash=None):
        self.packet_status_array = []
        self.img_length = img_length
        self.filehash = filehash
        self.file_name = file_name
        self.buffer_size = buffer_size
        self.bytes_received = 0
    
    def add_custom_package(self,identifier, data):
        self.packet_status_array.append(CustomPacket(identifier, data))
        self.bytes_received += len(data)
    
    def get_bytes_received(self):
        return self.bytes_received

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
        n = 0
        if valor is not None:
            n = self._img_length // valor
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
                print(package_status.__str__());
                status_str += 1
        return f"UdpInfo(file_name={self.file_name}, buffer_size={self.buffer_size}, img_length={self.img_length}, packet_status_array={status_str})"
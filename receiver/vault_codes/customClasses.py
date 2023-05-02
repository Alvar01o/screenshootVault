class CustomPacket:
    def __init__(self, identifier, data):
        self.identifier = identifier
        self.data = data


class UdpInfo:
    def __init__(self, img_length = 0, file_name = '', buffer_size = 0, package_amount = 0):
        self.img_length = img_length
        self.file_name = file_name
        self.buffer_size = buffer_size
        self.package_amount = package_amount

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
        self._buffer_size = valor

    @property
    def package_amount(self):
        return self._package_amount
    
    @package_amount.setter
    def package_amount(self, valor):
        self._package_amount = valor

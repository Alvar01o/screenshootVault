class CustomPacket:
    def __init__(self, identifier, data):
        self.identifier = identifier
        self.data = data


class UdpInfo:
    def __init__(self, img_length, file_name, buffer_size, package_amount):
        self.img_length = img_length
        self.file_name = file_name
        self.buffer_size = buffer_size
        self.package_amount = package_amount
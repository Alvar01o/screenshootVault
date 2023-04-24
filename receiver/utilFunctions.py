def custom_progress_bar(percentage, length=40):
    filled = int(length * percentage)
    empty = length - filled
    return f"[{'#' * filled}{'-' * empty}]"

def calculate_buffer_size(image_size_bytes): 
    # Definir los límites del tamaño del buffer en bytes
    MIN_BUFFER_SIZE = 1024       # 1 KB
    MAX_BUFFER_SIZE = 32768  # 32 KB
    # Establecer un factor de relación entre el tamaño del buffer y el tamaño de la imagen
    BUFFER_SIZE_FACTOR = 0.05    # Por ejemplo, 5% del tamaño de la imagen
    
    # Calcular el tamaño del buffer en función del tamaño de la imagen y el factor de relación
    buffer_size = int(image_size_bytes * BUFFER_SIZE_FACTOR)
    
    # Asegurar que el tamaño del buffer esté dentro de los límites permitidos
    buffer_size = max(MIN_BUFFER_SIZE, buffer_size)
    buffer_size = min(MAX_BUFFER_SIZE, buffer_size)
    
    return buffer_size

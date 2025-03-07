import ctypes
from ctypes import (
    POINTER, byref, c_void_p, c_int32, c_uint32, c_char_p, c_int8
)

import numpy as np

from imaqbindings.enumerations import (
    IMAQAttribute, BufferLocation, BufferElement, BufferCommand
)
from imaqbindings import enumerations as imenum


# Load the IMAQ DLL
try:
    imaq = ctypes.CDLL("imaq.dll")
except OSError as e:
    raise RuntimeError(f"Could not find 'imaq.dll'. Check whether NI-IMAQ software is properly installed.")


# Define error checking function
imaq.imgShowError.restype = c_int32
imaq.imgShowError.argtypes = [c_int32, POINTER(ctypes.c_char * 256)]
def check_error(result, func, arguments):
    """ 
    Check return value from NI IMAQ C API and raise Exception if error with
    information as Exception. """
    if result != 0:
        str_buffer = ctypes.create_string_buffer(256)
        imaq.imgShowError(result, byref(str_buffer))
        imaq_error_str = str_buffer.value.decode()
        raise Exception(
            f"Error calling function {func.__name__} with arguments {arguments} : {imaq_error_str}"
        )


def ctypes_sig(argtypes, restype=c_int32, errcheck=check_error):
    """
    Automates setting wrapped ctypes function signature fields
    """
    def decorator(func):
        func_name = "img"
        acronyms = ["sdk", "id", "io", "cpld", "fpga", "led"] # TODO, copied from Alazar wrapper, check what's needed
        for x in func.__name__.split('_'):
            if x in acronyms: 
                x = x.upper()
            else:
                x = x.capitalize()
            func_name += x
        
        ctypes_func = getattr(imaq, func_name)
        ctypes_func.restype = restype
        ctypes_func.argtypes = argtypes
        if errcheck is not None:
            ctypes_func.errcheck = errcheck

        # Wrapped function to call the actual ctypes function
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator




class Board:
    """
    Interface to an NI IMAQ framegrabber.
    Args:
      device_name (int): The name identified in NI MAX. Defaults to "img0".
      timeout (float): Amount of time to wait for serial response.
    """
    def __init__(self, device_name:str = "img0", timeout:float = 0.5):
        self._ifid = None # Interface ID
        self._sid = None # Session ID
        self._bid = None # Buffer list ID
        self.buffers = []
        self.serial_timeout = timeout # in seconds
        
        # Open the interface & session
        device_name = device_name.encode()
        self._ifid = self._interface_open(device_name) # prefer 'device name' over 'interface name'
        self._sid = self._session_open()

    @ctypes_sig([c_char_p, POINTER(c_uint32)])
    def _interface_open(self, interface_name: str):
        """
        Opens an interface by name as specified in Measurement & Automation 
        Explorer (MAX). If it is successful, this function returns an 
        INTERFACE_ID.
        """
        ifid = c_uint32() # Interface ID
        imaq.imgInterfaceOpen(interface_name, byref(ifid))
        return ifid

    @ctypes_sig([c_uint32, POINTER(c_uint32)])
    def _session_open(self):
        """
        Opens a session and returns a session ID. This function inherits all 
        data associated with the given interface.
        """
        sid = c_uint32() # Session ID
        imaq.imgSessionOpen(self._ifid, byref(sid))
        return sid

    @ctypes_sig([c_uint32, c_uint32, POINTER(c_uint32)])
    def get_attribute(self, attr: IMAQAttribute):
        """
        Returns an attribute value.
        """
        value = c_uint32() # may need to make this a void pointer
        imaq.imgGetAttribute(self._sid, attr, byref(value))
        return value.value
    
    @ctypes_sig([c_uint32, c_uint32, c_uint32])
    def set_attribute(self, attr: IMAQAttribute, value: int):
        """
        Sets an attribute value.

        Not implemented: setting uint64 or double values.
        """
        imaq.imgSetAttribute(self._sid, attr, value)

    @ctypes_sig([c_uint32, POINTER(c_uint32)])
    def create_buf_list(self, num_elements: int):
        """
        Creates a buffer list. You must initialize the buffer list before 
        calling imgSessionConfigure. Use imgSetBufferElement to initialize the 
        buffer list.
        """
        bid = c_uint32()
        imaq.imgCreateBufList(num_elements, byref(bid))       
        print(f"Buffer list with {num_elements} buffers created.")
        return bid

    @ctypes_sig([c_uint32, c_uint32, c_uint32, POINTER(c_uint32)])
    def get_buffer_element(self, element: int, item_type: BufferElement):
        """
        Gets the value for a specified itemType for a buffer in a buffer list.
        """
        item_value = c_uint32()
        imaq.imgGetBufferElement(self._bid, element, item_type, byref(item_value))
        return item_value.value
    
    @ctypes_sig([c_uint32, c_uint32, c_uint32, c_uint32])
    def set_buffer_element(self, element: int, item_type: BufferElement, item_value):
        """ 
        Sets the value for a specified itemType for a buffer in a buffer list.
        
        This is part of the initialization process for the buffer list and new 
        buffers.Use convenience methods set_buffer_element_address(), 
        set_buffer_element_size(), and set_buffer_element_command().
        """
        imaq.imgSetBufferElement(self._bid, element, item_type, item_value)
    
    def set_buffer_element_address(self, element: int, address):
        """
        Sets buffer list element pointer to allocated buffer memory.        
        Convenience method: calls set_buffer_element()
        """
        self.set_buffer_element(element, BufferElement.IMG_BUFF_ADDRESS, address)
                                  
    def set_buffer_element_size(self, element: int, size_bytes: int):
        """
        Sets buffer list element size.
        Convenience method: calls set_buffer_element()
        """
        self.set_buffer_element(element, BufferElement.IMG_BUFF_SIZE, size_bytes)

    def set_buffer_element_command(self, element: int, command: str):
        """
        Sets the buffer command. Must be either "next", "loop", "pass", 
        or "stop" (caps insensitive).
        Convenience method: calls set_buffer_element()
        """
        command = command.lower()
        if command == "next":
            buf_cmd = BufferCommand.IMG_CMD_NEXT
        elif command == "loop":
            buf_cmd = BufferCommand.IMG_CMD_LOOP
        elif command == "pass":
            buf_cmd = BufferCommand.IMG_CMD_PASS
        elif command == "stop":
            buf_cmd = BufferCommand.IMG_CMD_STOP
        else:
            raise TypeError("Unrecognized buffer element command")
        self.set_buffer_element(element, BufferElement.IMG_BUFF_COMMAND, buf_cmd)

    @ctypes_sig([c_uint32, c_uint32])
    def session_configure(self):
        """
        Configures the hardware in preparation for an acquisition.
        
        A buffer list must exist and elements must be initialized.
        """
        imaq.imgSessionConfigure(self._sid, self._bid)

    @ctypes_sig([c_uint32, c_uint32, c_void_p])
    def session_acquire(self, async_flag: bool):
        """
        Starts an acquisition, synchronously or asynchronously, to the buffers 
        in the associated session buffer list.

        If async_flag is false, this function does not return until the 
        acquisition completes.

        Not implemented: callback function
        """
        imaq.imgSessionAcquire(self._sid, async_flag, None)
    
    @ctypes_sig([c_uint32])
    def session_serial_flush(self):
        """
        Clears the internal serial buffer. In a serial write/read sequence, call 
        imgSessionSerialFlush before calling imgSessionSerialWrite to clear the 
        internal serial buffer for the next read. 
        """
        imaq.imgSessionSerialFlush(self._sid)

    @ctypes_sig([c_uint32, c_void_p, POINTER(c_uint32), c_uint32])
    def session_serial_write(self, command: str):
        """
        Writes command string to the serial port.
        """
        buffer = command.encode('ascii')
        buf_size = c_uint32(len(buffer))
        buf_size_p = POINTER(c_uint32)(buf_size)
        timeout_ms = round(self.serial_timeout*1000)

        self.session_serial_flush()
        imaq.imgSessionSerialWrite(self._sid, buffer, buf_size_p, timeout_ms)

    def session_serial_read(self, buffer_size: int = 256):
        """
        Reads in data from the serial port on devices that support serial 
        communication. This function fills the buffer with characters received 
        from the serial port until either a termination character has been 
        received or the timeout period has elapsed.
        """
        buffer = ctypes.create_string_buffer(buffer_size)
        buf_size = c_uint32(buffer_size)
        buf_size_p = POINTER(c_uint32)(buf_size)
        timeout_ms = round(self.serial_timeout*1000)

        imaq.imgSessionSerialRead(self._sid, buffer, buf_size_p, timeout_ms)

        return buffer.raw[:buf_size.value].decode('ascii')
    
    def session_serial_read_bytes(self, buffer_size: int = 8):
        """
        Reads in an expected number of bytes from the serial port on image 
        acquisition devices that support serial communication. This function 
        fills the buffer with characters received from the serial port until 
        either the buffer is full or the timeout period has elapsed. When you 
        use this function, the serial termination string attribute is ignored. 
        """
        buffer = ctypes.create_string_buffer(buffer_size)
        buf_size = c_uint32(buffer_size)
        buf_size_p = POINTER(c_uint32)(buf_size)
        timeout_ms = round(self.serial_timeout*1000)

        imaq.imgSessionSerialReadBytes(self._sid, buffer, buf_size_p, timeout_ms)

        return buffer.raw[:buf_size.value].decode('ascii')
    
    def close(self, free_resources: bool = True):
        """ Close the session and interface."""
        if self._sid:
            self._close(self._sid, free_resources) 
            self._sid = None
        
        # Close the interface
        if self._ifid:
            self._close(self._ifid, free_resources) 
            self._ifid = None
        
        print("Board closed successfully.")

    @ctypes_sig([c_uint32, c_uint32])
    def _close(self, xid: c_uint32, free_resources: bool):
        imaq.imgClose(xid, free_resources)
    
    def __del__(self):
        # Automatically close hardware
        self.close()


class Buffer:
    """
    Buffer for data transfer.
    """
    def __init__(self, board: Board, shape: tuple[int], bytes_per_pixel: int):
        self._size_bytes = np.prod(shape) * bytes_per_pixel
        self._sid = board._sid

        # Make a null pointer to byte array
        self._ptr = POINTER(c_int8)()

        self._create_buffer(
            sid=self._sid, 
            where=BufferLocation.IMG_HOST_FRAME,
            buffer_size=self._size_bytes,
            buffer_ptr_addr=byref(self._ptr)
        )

        self._adr = ctypes.addressof(self._ptr.contents)

        ctypes_array = (c_int8 * self._size_bytes).from_address(self._adr)
        if bytes_per_pixel == 1:
            dtype = np.uint8
        elif bytes_per_pixel == 2:
            dtype = np.uint16
        elif (bytes_per_pixel == 3) or (bytes_per_pixel == 4):
            dtype = np.uint8
            shape = (shape[0], shape[1], bytes_per_pixel)

        self.buffer = np.frombuffer(ctypes_array, dtype=dtype)
        self.buffer.shape = shape
        self.ctypes_buffer = ctypes_array
    
    @ctypes_sig([c_uint32, c_uint32, c_uint32, POINTER(POINTER(ctypes.c_int8))])
    def _create_buffer(self, sid: int, where: BufferLocation, buffer_size: int, buffer_ptr_addr):
        imaq.imgCreateBuffer(sid, where, buffer_size, buffer_ptr_addr)
    
    def __del__(self):
        self._dispose_buffer(self._ptr)
        print("Disposed buffer")

    @ctypes_sig([c_void_p])
    def _dispose_buffer(self, ptr):
        imaq.imgDisposeBuffer(ptr)

    def close(self):
        """ Explicitly dispose the buffer. """
        self.__del__()



# TEST
if __name__ == "__main__":

    board = Board()
    sn = board.get_attribute(imenum.DeviceInformation.IMG_ATTR_GETSERIAL)
    sn_hex = f"{sn:08X}"
    print(sn)
    print(sn_hex)

    blist = board.create_buf_list(100)
from enum import Enum, IntEnum

"""
This module provides enumerations for use with the wrapper functions.

NI-IMAQ documentation refers to these as attributes, for example device 
information attributes will be Enum DeviceInformation
"""


_BASE = 0x3FF60000

class IMAQAttribute(IntEnum):
    """A common base class for all NI-IMAQ 'attribute' enums."""
    pass


class DeviceInformation(IMAQAttribute):
    """
    Device information attributes return information concerning the image 
    acquisition device.
    
    Enumeration Members:
        IMG_ATTR_CLOCK_FREQ: Returns the maximum pixel clock frequency of the device
        IMG_ATTR_COLOR: Returns TRUE if the interface device supports color processing
        IMG_ATTR_CURRENT_PORT_NUM: Returns the current port number that the opened interface is accessing
        IMG_ATTR_GETSERIAL: Returns the serial number of the device (format this result as hex to match NI MAX)
        IMG_ATTR_HASRAM: Returns TRUE if the interface device has onboard memory
        IMG_ATTR_INTERFACE_TYPE: Returns the type of the interface in hex. For example, this attribute returns 0x1424 for the NI PCI-1424
        IMG_ATTR_LINESCAN: Returns TRUE if the camera attached to the interface is a line scan camera
        IMG_ATTR_NUM_EXT_LINES: Returns the number of External trigger lines available to the device
        IMG_ATTR_NUM_ISO_IN_LINES: Returns the number of Iso In trigger lines available to the device
        IMG_ATTR_NUM_ISO_OUT_LINES: Returns the number of Iso Out trigger lines available to the device
        IMG_ATTR_NUM_PORTS: Returns the number of ports the device supports
        IMG_ATTR_NUM_RTSI_LINES: Returns the number of RTSI trigger lines available to the device
        IMG_ATTR_RAMSIZE: Returns the size of the RAM on the interface device
    """
    IMG_ATTR_CLOCK_FREQ         = _BASE + 0x00BB
    IMG_ATTR_COLOR              = _BASE + 0x0003
    IMG_ATTR_CURRENT_PORT_NUM   = _BASE + 0x01AE
    IMG_ATTR_GETSERIAL          = _BASE + 0x00C0
    IMG_ATTR_HASRAM             = _BASE + 0x0004
    IMG_ATTR_INTERFACE_TYPE     = _BASE + 0x0001
    IMG_ATTR_LINESCAN           = _BASE + 0x000C
    IMG_ATTR_NUM_EXT_LINES      = _BASE + 0x0012
    IMG_ATTR_NUM_ISO_IN_LINES   = _BASE + 0x01A8
    IMG_ATTR_NUM_ISO_OUT_LINES  = _BASE + 0x01A9
    IMG_ATTR_NUM_PORTS          = _BASE + 0x01AD
    IMG_ATTR_NUM_RTSI_LINES     = _BASE + 0x0013
    IMG_ATTR_RAMSIZE            = _BASE + 0x0005
    

class SessionInformation(IMAQAttribute):
    """
    Enumerates session information attributes.

    Enumeration Members:
        IMG_ATTR_ACQWINDOW_HEIGHT: Gets/sets the acquisition window height of the camera/channel associated with this session
        IMG_ATTR_ACQWINDOW_LEFT: Gets/sets the acquisition window left offset of the camera/channel associated with this session
        IMG_ATTR_ACQWINDOW_TOP: Gets/sets the acquisition window top offset of the camera/channel associated with this session
        IMG_ATTR_ACQWINDOW_WIDTH: Gets/sets the acquisition window width of the camera/channel associated with this session
        (IMG_ATTR_ENCODER* not implemented)
        IMG_ATTR_EXT_TRIG_LINE_FILTER: Enables/disables the noise filter for external trigger lines
        IMG_ATTR_NUM_POST_TRIGGER_BUFFERS: Gets/sets the number of buffers to be acquired after the assertion edge of the stop trigger. 
            This attribute is only used when a stop trigger has been registered for the acquisition.
        IMG_ATTR_RTSI_LINE_FILTER: Enables/disables the noise filter for RTSI trigger lines
        IMG_ATTR_VHA_MODE: Enables Variable Height Acquisition (VHA) mode
    """
    IMG_ATTR_ACQWINDOW_HEIGHT           = _BASE + 0x006B
    IMG_ATTR_ACQWINDOW_LEFT             = _BASE + 0x0068
    IMG_ATTR_ACQWINDOW_TOP              = _BASE + 0x0069
    IMG_ATTR_ACQWINDOW_WIDTH            = _BASE + 0x006A
    IMG_ATTR_EXT_TRIG_LINE_FILTER       = _BASE + 0x01AB
    IMG_ATTR_NUM_POST_TRIGGER_BUFFERS   = _BASE + 0x01AA
    IMG_ATTR_RTSI_LINE_FILTER           = _BASE + 0x01AC
    IMG_ATTR_VHA_MODE                   = _BASE + 0x00C4


class Image(IMAQAttribute):
    """
    Image attributes define parameters that affect an image acquisition, such as 
    region of interest.

    Enumeration Members:
        IMG_ATTR_ACQUIRE_FIELD: Gets/sets the field acquired when IMG_ATTR_FRAME_FIELD is set to FIELD_MODE. 
            When you are using FRAME_MODE, this attribute is the first field that is acquired in time.
        IMG_ATTR_BIN_THRESHOLD_HIGH: The upper limit for the binary threshold LUT
        IMG_ATTR_BIN_THRESHOLD_LOW: The lower limit for the binary threshold LUT
        IMG_ATTR_BITSPERPIXEL: Returns the bits per pixel value of the camera associated with this session
        IMG_ATTR_BYTESPERPIXEL: Returns the bytes per pixel value of the camera/channel associated with this session.
        IMG_ATTR_CHANNEL: Programs the current channel selected on the interface (0-3)
        IMG_ATTR_FRAME_FIELD: Gets/sets the current mode of the interlace (Frame or Field)
        IMG_ATTR_FRAMEWAIT_MSEC: Gets/sets the timeout value for a frame, in milliseconds
        (IMG_ATTR_*SCALE not implemented)
        IMG_ATTR_INVERT: Sets/gets the invert image mode. If this property is set to invert, the image will be upside down in memory.
        IMG_ATTR_LUT: Programs the look up table (LUT) for the given interface. Pass a constant to indicate the LUT you want to use.
        IMG_ATTR_ROI_HEIGHT: Gets/sets the region of interest (ROI) height of the camera/channel associated with this session
        IMG_ATTR_ROI_LEFT: Gets/sets the region of interest left of the camera/channel associated with this session
        IMG_ATTR_ROI_TOP: Gets/sets the region of interest top of the camera/channel associated with this session.
        IMG_ATTR_ROI_WIDTH: Gets/sets the region of interest left of the camera/channel associated with this session.
        IMG_ATTR_ROWPIXELS: Gets/sets the number of pixels in a row of an image. 
            This attribute value may be larger than the width of the image.
        IMG_ATTR_START_FIELD: For interlaced acquisitions, this attribute specifies the field that occupies line 0 of the image buffer
    """
    IMG_ATTR_ACQUIRE_FIELD          = _BASE + 0x00C2
    IMG_ATTR_BIN_THRESHOLD_HIGH     = _BASE + 0x00C6
    IMG_ATTR_BIN_THRESHOLD_LOW      = _BASE + 0x00C5
    IMG_ATTR_BITSPERPIXEL           = _BASE + 0x0066
    IMG_ATTR_BYTESPERPIXEL          = _BASE + 0x0067 
    IMG_ATTR_CHANNEL                = _BASE + 0x0006
    IMG_ATTR_FRAME_FIELD            = _BASE + 0x0007
    IMG_ATTR_FRAMEWAIT_MSEC         = _BASE + 0x007D
    IMG_ATTR_INVERT                 = _BASE + 0x0082
    IMG_ATTR_LUT                    = _BASE + 0x000B
    IMG_ATTR_ROI_HEIGHT             = _BASE + 0x01A7 
    IMG_ATTR_ROI_LEFT               = _BASE + 0x01A4
    IMG_ATTR_ROI_TOP                = _BASE + 0x01A5
    IMG_ATTR_ROI_WIDTH              = _BASE + 0x01A6
    IMG_ATTR_ROWPIXELS              = _BASE + 0x00C1 
    IMG_ATTR_START_FIELD            = _BASE + 0x0075


class Color(IMAQAttribute):
    """
    Color attributes set parameters associated with a color acquisition. Most
    attributes are not implemented because they are exclusive to PCI-1405 or 
    PCI/PXI-1411.

    Enumeration Members:
        IMG_ATTR_COLOR_IMAGE_REP: Specifies the type of image data returned when a color image is acquired
        (many attributes exclusive to PCI-1405 & PCI/PXI-1411 not implemented)
    """
    IMG_ATTR_COLOR_IMAGE_REP    = _BASE + 0x00AE


class ColorRepresentations(IntEnum):
    """
    Enumeration Members:
        IMG_COLOR_REP_RGB32: 32 bits RGB
        IMG_COLOR_REP_RED8: 8 bits Red
        IMG_COLOR_REP_GREEN8: 8 bits Green
        IMG_COLOR_REP_BLUE8: 8 bits Blue
        IMG_COLOR_REP_LUM8: 8 bits Light
        IMG_COLOR_REP_HUE8: 8 bits Hue
        IMG_COLOR_REP_SAT8: 8 bits Saturation
        IMG_COLOR_REP_INT8: 8 bits Intensity
        IMG_COLOR_REP_LUM16: 16 bits Light
        IMG_COLOR_REP_HUE16: 16 bits Hue
        IMG_COLOR_REP_SAT16: 16 bits Saturation
        IMG_COLOR_REP_INT16: 16 bits Intensity
        IMG_COLOR_REP_RGB48: 48 bits RGB
        IMG_COLOR_REP_RGB24: 24 bits RGB
        IMG_COLOR_REP_RGB16: 16 bits RGB (x555)
        IMG_COLOR_REP_HSL32: 32 bits HSL
        IMG_COLOR_REP_HSI32: 32 bits HSI
        IMG_COLOR_REP_NONE: No color information. Use bit-depth
        IMG_COLOR_REP_MONO10: 10 bit Monochrome
    """
    IMG_COLOR_REP_RGB32     = 0
    IMG_COLOR_REP_RED8      = 1
    IMG_COLOR_REP_GREEN8    = 2
    IMG_COLOR_REP_BLUE8     = 3  
    IMG_COLOR_REP_LUM8      = 4
    IMG_COLOR_REP_HUE8      = 5
    IMG_COLOR_REP_SAT8      = 6
    IMG_COLOR_REP_INT8      = 7
    IMG_COLOR_REP_LUM16     = 8
    IMG_COLOR_REP_HUE16     = 9
    IMG_COLOR_REP_SAT16     = 10
    IMG_COLOR_REP_INT16     = 11
    IMG_COLOR_REP_RGB48     = 12
    IMG_COLOR_REP_RGB24     = 13
    IMG_COLOR_REP_RGB16     = 14
    IMG_COLOR_REP_HSL32     = 15
    IMG_COLOR_REP_HSI32     = 16
    IMG_COLOR_REP_NONE      = 17
    IMG_COLOR_REP_MONO10    = 18

class StatusInformation(IMAQAttribute):
    """
    Status information attributes return status information about an acquisition.

    Enumeration Members:
        IMG_ATTR_ACQ_IN_PROGRESS: Returns TRUE if an acquisition is in progress on the camera associated with this session
        IMG_ATTR_FRAME_COUNT: Returns the number of frames acquired since the start of an acquisition
        IMG_ATTR_LAST_VALID_BUFFER: Returns the last available buffer list index
        IMG_ATTR_LAST_VALID_FRAME: Returns the last available cumulative buffer number
        IMG_ATTR_LOST_FRAMES: Returns the total number of lost frames in a continuous acquisition
        IMG_ATTR_POCL_STATUS: Returns the status of the Power Over Camera Link (PoCL) circuitry
        IMG_ATTR_POCL_STATUS_BASE: Returns the status of the PoCL circuitry for the Base connector
        IMG_ATTR_POCL_STATUS_MED_FULL: Returns the status of the PoCL circuitry for the Medium/Full connector

    """
    IMG_ATTR_ACQ_IN_PROGRESS        = _BASE + 0x0074 
    IMG_ATTR_FRAME_COUNT            = _BASE + 0x0076 
    IMG_ATTR_LAST_VALID_BUFFER      = _BASE + 0x0077 
    IMG_ATTR_LAST_VALID_FRAME       = _BASE + 0x00BA 
    IMG_ATTR_LOST_FRAMES            = _BASE + 0x0088 
    IMG_ATTR_POCL_STATUS            = _BASE + 0x01C6 
    IMG_ATTR_POCL_STATUS_BASE       = _BASE + 0x01D3 
    IMG_ATTR_POCL_STATUS_MED_FULL   = _BASE + 0x01D4


class BufferElement(IntEnum):
    """
    Enumerates buffer element specifiers.

    All should be uInt32 type, except for IMG_BUFF_ADDRESS which should be void*
    """
    IMG_BUFF_ADDRESS        = _BASE + 0x007E
    IMG_BUFF_COMMAND        = _BASE + 0x007F 
    IMG_BUFF_SKIPCOUNT      = _BASE + 0x0080
    IMG_BUFF_SIZE           = _BASE + 0x0082
    IMG_BUFF_TRIGGER        = _BASE + 0x0083
    IMG_BUFF_NUMBUFS        = _BASE + 0x00B0
    IMG_BUFF_CHANNEL        = _BASE + 0x00BC
    IMG_BUFF_ACTUALHEIGHT   = _BASE + 0x0400


class BufferCommand(IntEnum):
    """
    Enumerations buffer commands.
    
    Enumeration Members:
        IMG_CMD_NEXT: Proceed to next list entry
        IMG_CMD_LOOP: Loop back to start of buffer list and continue processing - RING ACQUISITION
        IMG_CMD_PASS: Do nothing here
        IMG_CMD_STOP: Stop
    """
    IMG_CMD_NEXT    = 0x01
    IMG_CMD_LOOP    = 0x02
    IMG_CMD_PASS    = 0x04
    IMG_CMD_STOP    = 0x08


class BufferLocation(IntEnum):
    """
    Enumerates location of buffer (host vs. device).
    """
    IMG_HOST_FRAME      = 0
    IMG_DEVICE_FRAME    = 1


class SignalType(IntEnum):
    """
    Enumerates signal types (external, RTSI, etc.)
    """
    IMG_SIGNAL_NONE                 = 0xFFFFFFFF
    IMG_SIGNAL_EXTERNAL             = 0
    IMG_SIGNAL_RTSI                 = 1
    IMG_SIGNAL_ISO_IN               = 2
    IMG_SIGNAL_ISO_OUT              = 3
    IMG_SIGNAL_STATUS               = 4
    IMG_SIGNAL_SCALED_ENCODER       = 5
    IMG_SIGNAL_SOFTWARE_TRIGGER     = 6


class TriggerPolarity(IntEnum):
    """
    Enumerates trigger polarities (active high, active low)
    """
    IMG_TRIG_POLAR_ACTIVEH  = 0
    IMG_TRIG_POLAR_ACTIVEL  = 1
import libsub
from exception import DeviceException

class Sub20:
    # Constants
    FPWM_ENABLE     = 0x0001
    FPWM_EN0        = 0x8000
    FPWM_EN1        = 0x2000
    FPWM_EN2        = 0x0800
    
    def __init__(self, dev = 0, pinNames = 0):
        res = libsub.sub_find_devices(dev)
        if res == 0:
            raise DeviceException(self.getError())
        
        self.device = libsub.sub_open(res)
        if self.device == 0:
            raise DeviceException(self.getError())
        
        code, port = libsub.sub_gpio_config(self.device, 0, 0)
        self.gpioPort = self._hex2binary(port)
        self.pinNames = pinNames
        self.pinArray = [17, 18, 19, 20, 21, 22, 23, 24, 1, 2, 3, 4, 5, 6, 7, 8, 32, 31, 30, 29, 28, 27, 26, 25, 9, 10, 11, 12, 13, 14, 15, 16]
        self.fpwmStatus = 0
        
        return res
            
    def __del__(self):
        libsub.sub_close(self.device)
        
    def getError(self):
        return libsub.sub_get_errno()
        
    def _hex2binary(self, byte):
        ''' Converts hex string to binary array '''
        tar = int(byte.encode('hex_codec'), 16)
        tar = bin(tar)
        l = []
        for i in range(2, len(tar)):
            l.append((tar[i]))
        return l
    
    def _binary2int(self, array):
        st = '0b'
        for i in array:
            st+=str(i)
        return int(st, 2)
    
    def _getPin(self, pin):
        if self.pinNames == 0:
            return pin
        elif self.pinNames == 1:
            return self.pinArray[pin]
        else:
            return self.pinArray[pin-1]
    
    def getProductId(self):
        code, prodid = libsub.sub_get_version(self.device, 255)
        return prodid
    
    def getSerialNumber(self):    
        code, serial = libsub.sub_get_serial_number(self.device, 255)
        return serial
    
    def writeLCD(self, string):
        ret = libsub.sub_lcd_write(self.device, string)
        if ret > 0:
            raise DeviceException(self.getError())
        return ret
    
    def gpioMask(self):
        return [0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0]
    
    def gpioConfig(self, set_array = [], mask_array = []):
        code, string = libsub.sub_gpio_config(self.device, self._binary2int(set_array), self._binary2int(mask_array))
        print self._binary2int(set_array)
        print self._binary2int(mask_array)
        if code > 0:
            raise DeviceException(self.getError())
        return string
    
    def gpioDirection(self, pin, val):
        pin_ = self._getPin(pin)
        set = mask = self.gpioMask()
        mask[pin_-1] = 1
        set[pin_-1] = val
        code, port = libsub.sub_gpio_config(self.device, self._binary2int(set), self._binary2int(mask))
        self.gpioPort = self._hex2binary(port)
    
    def gpioWrite(self, pin, val):
        pin_ = self._getPin(pin)
        set = self.gpioMask()
        mask = self.gpioMask()
        mask[pin_-1] = 1
        set[pin_-1] = val
        code, port = libsub.sub_gpio_write(self.device, self._binary2int(set), self._binary2int(mask))
        return self._hex2binary(port)
    
    def gpioRead(self, pin):
        lip = []
        for i in range(32):
            lip.append(libsub.sub_gpio_read_pin(self.device, i))
        lip.reverse()
        return lip[self._getPin(pin)-1]
    
    def fpwmEnable(self):
        ret = libsub.sub_fpwm_config(self.device, 0, self.FPWM_ENABLE)
        if ret > 0:
            raise DeviceException(self.getError())
        return ret
    
    def fpwmDisable(self):
        ret = libsub.sub_fpwm_config(self.device, 0, 0)
        if ret > 0:
            raise DeviceException(self.getError())
        return ret
    
    def fpwmConfig(self, fnum, freq):
        if fnum == 0: num = self.FPWM_EN0
        if fnum == 1: num = self.FPWM_EN1
        if fnum == 2: num = self.FPWM_EN2
        ret = libsub.sub_fpwm_config(self.device, freq, self.FPWM_ENABLE | num)
        if ret > 0:
            raise DeviceException(self.getError())
        return ret
    
    def fpwmSet(self, fnum, duty):
        ret = libsub.sub_fpwm_set(self.device, fnum, duty)
        if ret > 0:
            raise DeviceException(self.getError())
        return ret

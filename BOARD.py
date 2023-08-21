import RPi.GPIO as GPIO
import spidev
from constantes import *
import time
from EnvioJSON import *


class BOARD:
    """ Board initialisation/teardown and pin configuration is kept here.
        Also, information about the RF module is kept here.
        This is the Raspberry Pi board with one LED and a Ra-02 Lora.
    """
    # Note that the BCOM numbering for the GPIOs is used.
    DIO0 = 4   # RaspPi GPIO 4
    DIO1 = 17   # RaspPi GPIO 17
    DIO2 = 18   # RaspPi GPIO 27
    RST  = 22   # RaspPi GPIO 22
    LED  = 13   # RaspPi GPIO 13 connects to the LED and a resistor (1kohm or 330ohm)
    #SWITCH = 4  # RaspPi GPIO 4 connects to a switch - not necessary
    GPIO.setmode(BOARD.DIO0)
    GPIO.setmode(BOARD.DIO1)
    GPIO.setmode(BOARD.DIO2)
    # The spi object is kept here
    spi = None
    SPI_BUS=0
    SPI_CS=0
    
    # tell pySX127x here whether the attached RF module uses low-band (RF*_LF pins) or high-band (RF*_HF pins).
    # low band (called band 1&2) are 137-175 and 410-525
    # high band (called band 3) is 862-1020
    low_band = False

    @staticmethod
    def setup():
        """ Configure the Raspberry GPIOs
        :rtype : None
        """
        GPIO.setmode(GPIO.BCM)
        
        GPIO.setup(BOARD.RST, GPIO.OUT)
        GPIO.output(BOARD.RST, 1)
        # switch
        #GPIO.setup(BOARD.SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
        # DIOx
        for gpio_pin in [BOARD.DIO0, BOARD.DIO1, BOARD.DIO2]:
            GPIO.setup(gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    @staticmethod
    def teardown():
        """ Cleanup GPIO and SpiDev """
        GPIO.cleanup()
        BOARD.spi.close()

    @staticmethod
    def SpiDev():
        """ Init and return the SpiDev object
        :return: SpiDev object
        :param spi_bus: The RPi SPI bus to use: 0 or 1
        :param spi_cs: The RPi SPI chip select to use: 0 or 1
        :rtype: SpiDev
        """
        spi_bus=BOARD.SPI_BUS
        spi_cs=BOARD.SPI_CS
        BOARD.spi = spidev.SpiDev()
        BOARD.spi.open(spi_bus, spi_cs)
        BOARD.spi.max_speed_hz = 5000000    # SX127x can go up to 10MHz, pick half that to be safe
        return BOARD.spi

    @staticmethod
    def add_event_detect(dio_number, callback):
        """ Wraps around the GPIO.add_event_detect function
        :param dio_number: DIO pin 0...5
        :param callback: The function to call when the DIO triggers an IRQ.
        :return: None
        """
        GPIO.add_event_detect(dio_number, GPIO.RISING, callback=callback)

    @staticmethod
    def add_events(cb_dio0, cb_dio1, cb_dio2, switch_cb=None):
        BOARD.add_event_detect(BOARD.DIO0, callback=cb_dio0)
        BOARD.add_event_detect(BOARD.DIO1, callback=cb_dio1)
        BOARD.add_event_detect(BOARD.DIO2, callback=cb_dio2)
        # the modtronix inAir9B does not expose DIO4 and DIO5
        if switch_cb is not None:
            GPIO.add_event_detect(BOARD.SWITCH, GPIO.RISING, callback=switch_cb, bouncetime=300)    
    @staticmethod
    def reset():
        """ manual reset
        :return: 0
        """
        GPIO.output(BOARD.RST, 0)
        time.sleep(.01)
        GPIO.output(BOARD.RST, 1)
        time.sleep(.01)
        return 0
    
    def __init__(self, verbose=False, do_calibration=False, calibration_freq=868):
        """ Init the object
        
        Send the device to sleep, read all registers, and do the calibration (if do_calibration=True)
        :param verbose: Set the verbosity True/False
        :param calibration_freq: call rx_chain_calibration with this parameter. Default is 868
        :param do_calibration: Call rx_chain_calibration, default is False.
        """
        self.verbose = verbose
        # set the callbacks for DIO0..5 IRQs.
        BOARD.add_events(self._dio0, self._dio1, self._dio2)
        # set mode to sleep and read all registers
        self.set_mode(MODE.SLEEP)
        self.backup_registers = self.get_all_registers()
        # more setup work:
        if do_calibration:
            self.rx_chain_calibration(calibration_freq)
        # the FSK registers are set up exactly as modtronix do it:
        lookup_fsk = [
            #[REG.FSK.LNA            , 0x23],
            #[REG.FSK.RX_CONFIG      , 0x1E],
            #[REG.FSK.RSSI_CONFIG    , 0xD2],
            #[REG.FSK.PREAMBLE_DETECT, 0xAA],
            #[REG.FSK.OSC            , 0x07],
            #[REG.FSK.SYNC_CONFIG    , 0x12],
            #[REG.FSK.SYNC_VALUE_1   , 0xC1],
            #[REG.FSK.SYNC_VALUE_2   , 0x94],
            #[REG.FSK.SYNC_VALUE_3   , 0xC1],
            #[REG.FSK.PACKET_CONFIG_1, 0xD8],
            #[REG.FSK.FIFO_THRESH    , 0x8F],
            #[REG.FSK.IMAGE_CAL      , 0x02],
            #[REG.FSK.DIO_MAPPING_1  , 0x00],
            #[REG.FSK.DIO_MAPPING_2  , 0x30]
        ]
        self.set_mode(MODE.FSK_STDBY)
        for register_address, value in lookup_fsk:
            self.set_register(register_address, value)
        self.set_mode(MODE.SLEEP)
        # set the dio_ mapping by calling the two get_dio_mapping_* functions
        self.get_dio_mapping_1()
        self.get_dio_mapping_2()
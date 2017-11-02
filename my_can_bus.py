import can
import threading
import time
import datetime
from can.listener import Listener
import logging
import socket
import math

log = logging.getLogger('can.io.stdout')

def receive_can_message():
    bus = can.interface.Bus(bustype='socketcan_native', channel='can0')
    notifier = can.Notifier(bus, [MyListener()], 0.1)

def ac_front_power_on_off():
    bus = can.interface.Bus(bustype='socketcan_native', channel='can0')
    msg_362 = can.Message(arbitration_id=0x362,
                          data=[0x00, 0x5C, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                          extended_id=False)
    bus.send(msg_362)

if __name__ == "__main__":
    #ac_front_power_on_off()
    receive_can_message()
    while True:
        print('.')


class MyListener(Listener):
    """
    The Printer class is a subclass of :class:`~can.Listener` which simply prints
    any messages it receives to the terminal.

    :param output_file: An optional file to "print" to.
    """


    def __init__(self, output_file=None):
        if output_file is not None:
            log.info("Creating log file '{}' ".format(output_file))
            output_file = open(output_file, 'wt')
        self.output_file = output_file

    def on_message_received(self, msg):

        if self.output_file is not None:
            # self.output_file.write(str(msg) + "\n")
            print('1')
        else:
            # data = ["{:02X}".format(byte) for byte in msg.data]

            arb_id = hex(msg.arbitration_id)
            print(arb_id)
            if 0x361 == msg.arbitration_id:
                print(hex(msg.arbitration_id))
                for byte in msg.data:
                    print("{:02X}".format(byte), end='')

    def stop(self):
        if self.output_file:
            self.output_file.write("\n")
            self.output_file.close()
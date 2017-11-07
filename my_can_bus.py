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
    msg_362_normal = can.Message(arbitration_id=0x362,
                                 data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                                 extended_id=False)
    msg_362 = can.Message(arbitration_id=0x362,
                          data=[0x00, 0x5C, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                          extended_id=False)
    bus.send(msg_362_normal)
    time.sleep(1)
    bus.send(msg_362)
    time.sleep(1)
    bus.send(msg_362_normal)
    time.sleep(1)


def ac_temp_add():
    bus = can.interface.Bus(bustype='socketcan_native', channel='can0')
    msg_362_normal = can.Message(arbitration_id=0x362,
                          data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                          extended_id=False)
    msg_362 = can.Message(arbitration_id=0x362,
                          data=[0x00, 0x1C, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                          extended_id=False)

    bus.send(msg_362_normal)
    time.sleep(1)
    bus.send(msg_362)
    time.sleep(1)
    bus.send(msg_362_normal)
    time.sleep(1)


def ac_temp_minus():
    bus = can.interface.Bus(bustype='socketcan_native', channel='can0')
    msg_362_normal = can.Message(arbitration_id=0x362,
                          data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                          extended_id=False)
    msg_362 = can.Message(arbitration_id=0x362,
                          data=[0x00, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                          extended_id=False)

    bus.send(msg_362_normal)
    time.sleep(1)
    bus.send(msg_362)
    time.sleep(1)
    bus.send(msg_362_normal)
    time.sleep(1)


def open_trunk():
    bus = can.interface.Bus(bustype='socketcan_native', channel='can0')
    msg_100 = can.Message(arbitration_id=0x100,
                          data=[0x0A, 0x0F, 0x00, 0x01, 0x02, 0x00, 0x33, 0xE3],
                          extended_id=False)
    bus.send(msg_100)
    time.sleep(0.2)
    bus.send(msg_100)
    time.sleep(0.2)


if __name__ == "__main__":
    # ac_front_power_on_off()
    receive_can_message()
    while True:
        print('.')

ac_temp = 0
gear_d_pos = 0
tire_lf = 0
tire_rf = 0
tire_rr = 0
tire_lr = 0

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

            # arb_id = hex(msg.arbitration_id)

            if 0x361 == msg.arbitration_id:

                global ac_temp
                ac_temp_digit3 = (msg.data[0] & 0x0C) >> 2
                print('msg.data[4]='+ str(msg.data[4]))
                ac_temp_digit1 = chr(msg.data[4])
                ac_temp_digit2 = chr(msg.data[5])

                if ac_temp_digit1 != ' ':
                    if ac_temp_digit3 == 2:
                        ac_temp = ac_temp_digit1 + ac_temp_digit2 + '.5'
                    else:
                        ac_temp = ac_temp_digit1 + ac_temp_digit2 + '.0'
                else:
                    ac_temp = 'Close'
                print("ac_temp_digit1=" + ac_temp_digit1)
                print("ac_temp_digit2=" + ac_temp_digit2)
                print("ac_temp_digit3=" + str(ac_temp_digit3))

            elif 0x109 == msg.arbitration_id:
                global gear_d_pos
                gear_d_pos = (msg.data[2] & 0xF0) >> 4
                print("gear_d_pos=" + str(gear_d_pos))

            elif 0x3B5 == msg.arbitration_id:
                tire_lf_0 = msg.data[0]
                tire_lf_1 = msg.data[1]
                global tire_lf
                tire_lf = tire_lf_0*16 + tire_lf_1

                tire_rf_0 = msg.data[2]
                tire_rf_1 = msg.data[3]
                global tire_rf
                tire_rf = tire_rf_0 * 16 + tire_rf_1

                tire_rr_0 = msg.data[4]
                tire_rr_1 = msg.data[5]
                global tire_rr
                tire_rr = tire_rr_0 * 16 + tire_rr_1

                tire_lr_0 = msg.data[6]
                tire_lr_1 = msg.data[7]
                global tire_lr
                tire_lr = tire_lr_0 * 16 + tire_lr_1

                print("tire_lf=" + str(tire_lf))
                print("tire_rf=" + str(tire_rf))
                print("tire_rr=" + str(tire_rr))
                print("tire_lr=" + str(tire_lr))

    def stop(self):
        if self.output_file:
            self.output_file.write("\n")
            self.output_file.close()

## Project Plannning:

# Make a bunch of classes that represent the messages we can send
# Specify object/functions to run checks on the attributes of each class
# Message class structure:
# Attributes list: stores tuple/object? that contains a name, value, and a checker Object???

import json

byte_size = 255
two_byte_size = 65535

class CANMessage:
    name = [{"config_mode": "Message Mode Configuration"},
            {"total_send": "Total Send Message Count"},
            {"total_receive": "Total Receive Message Count"},
            {"transmission_rate": "Transmission Rate"},
            ]
    desc = [{"config_mode": "The 'Free CAN message configuration' is activated with the value 1."},
            {"total_send": "Maximum of 10 send messages."},
            {"total_receive": "Maximum of 10 receive messages."},
            {"transmission_rate": "Transmission rate in kBaud (thousands of symbol changes per second)"},
            ]
    
    # update methods:
    def update_config_mode(self, config_mode):
        if config_mode != 1:
            raise Exception("Not in FreeCan mode...")
        self.config_mode = config_mode
    def update_send_total(self, new_total):
        if new_total > 10 or new_total < 0:
            raise Exception("Specified total out of bounds...")
        if len(self.send_messages) < new_total:
            for i in range(new_total - len(self.send_messages)):
                self.send_messages.append(SendMessage())
        self.total_send = new_total

    def update_receive_total(self, new_total):
        if new_total > 10 or new_total < 0:
            raise Exception("Specified total out of bounds...")
        if len(self.receive_messages) < new_total:
            for i in range(new_total - len(self.receive_messages)):
                self.receive_messages.append(ReceiveMessage())
        self.total_receive = new_total
    
    def update_transmission_rate(self, new_transmission_rate):
        if new_transmission_rate > two_byte_size or new_transmission_rate < 0:
            raise Exception("Specified total out of bounds")
        self.transmission_rate = new_transmission_rate

    # Constructor
    def __init__(self, config_mode = 1, total_send = 0, total_receive = 0, transmission_rate = 500, send_messages = [], receive_messages = []):
        self.send_messages = send_messages
        self.receive_messages = receive_messages
        self.update_config_mode(config_mode)
        self.update_send_total(total_send)
        self.update_receive_total(total_receive)
        self.update_transmission_rate(transmission_rate)

        # fix attempt
        self.CANMessageDict = dict()
        self.CANMessageDict["message_config"] = self.config_mode
        self.CANMessageDict["total_send"] = self.total_send
        self.CANMessageDict["total_recv_msgs"] = self.total_receive
        self.CANMessageDict["send_msgs"] = self.send_messages[0:self.total_send]
        self.CANMessageDict["receive_messages"] = self.receive_messages[0:self.total_receive]
        for i in range(len(self.CANMessageDict["send_msgs"])):
            self.CANMessageDict["send_msgs"][i] = self.CANMessageDict["send_msgs"][i].getDict()
        for i in range(len(self.CANMessageDict["receive_messages"])):
            self.CANMessageDict["receive_messages"][i] = self.CANMessageDict["receive_messages"][i].getDict()
        self.CANMessageDict["transmission_rate"] = self.transmission_rate
        # doesnt make dict???

        self.mappings = {
            "message_config": {
                "function": self.update_config_mode,
                "description": "Message Mode Configuration. The 'Free CAN message configuration' is activated with the value 1."
            },

            "total_send": {
                "function": self.update_send_total,
                "description": "do later"
            },

            "total_recv_msgs": {
                "function": self.update_receive_total,
                "description": "sdf"
            },

            "transmission_rate": {
                "function": self.update_transmission_rate,
                "description": "tadf"
            }
        }
    
    # Dictionary getter
    def get_dict(self):
        ret = dict()
        ret["message_config"] = self.config_mode
        ret["total_send"] = self.total_send
        ret["total_recv_msgs"] = self.total_receive
        ret["send_msgs"] = self.send_messages[0:self.total_send]
        ret["receive_messages"] = self.receive_messages[0:self.total_receive]
        for i in range(len(ret["send_msgs"])):
            ret["send_msgs"][i] = ret["send_msgs"][i].getDict()
        for i in range(len(ret["receive_messages"])):
            ret["receive_messages"][i] = ret["receive_messages"][i].getDict()
        ret["transmission_rate"] = self.transmission_rate
        return ret

class SendMessage:
    def __init__(self, CAN_ID=0, cycle_time=0, data_length=8, attr=0, total_signals=0, signals=[]):
        self.signals = signals
        self.update_CAN_ID(CAN_ID)
        self.update_data_length(data_length)
        self.update_total_signals(total_signals)
        self.update_cycle_time(cycle_time)
        self.update_attr(attr)
        self.mappings = {
            "CAN_ID": {
                "function": self.update_CAN_ID,
                "description": "11-bit CAN identifier."
            },
            "data_length": {
                "function": self.update_data_length,
                "description": "Size of the CAN message (0-8 bytes)."
            },
            "total_signals": {
                "function": self.update_total_signals,
                "description": "Number of signals in this CAN message."
            },
            "cycle_time": {
                "function": self.update_cycle_time,
                "description": "Cycle time of the message in milliseconds."
            },
            "attr": {
                "function": self.update_attr,
                "description": "Attribute flag (0 or 1)."
            }
        }

    def update_CAN_ID(self, CAN_ID):
        if CAN_ID > 2047 or CAN_ID < 0:
            raise OverflowError("CAN_ID needs to fit within an 11-bit integer...")
        self.CAN_ID = CAN_ID
        
    def update_data_length(self, data_length):
        if data_length > 8 or data_length < 0:
            raise OverflowError("data_length needs to be within [0,8]...")
        self.data_length = data_length
        
    def update_total_signals(self, new_total):
        byte_size = 8  # Assuming byte size to be 8 for this context
        if new_total > byte_size:
            raise OverflowError("total_signals needs to fit within 1 byte...")
        if len(self.signals) < new_total:
            for i in range(new_total - len(self.signals)):
                self.signals.append(Signal())
        self.total_signals = new_total

    def getDict(self):
        ret = {
            "CAN_ID": self.CAN_ID,
            "data_length": self.data_length,
            "total_signals": self.total_signals,
            "signals": [signal.get_dict() for signal in self.signals[:self.total_signals]],
            "cycle_time": self.cycle_time,
            "attr": self.attr
        }
        return ret
    
    def update_cycle_time(self, cycle_time):
        if cycle_time > two_byte_size or cycle_time < 0:
            raise OverflowError("cycle_time needs to fit within two bytes...")
        self.cycle_time = cycle_time
    
    def update_attr(self, attr):
        if attr not in [0, 1]:
            raise Exception("attr can only be 1 or 0...")
        self.attr = attr

class ReceiveMessage:
    def __init__(self, CAN_ID=0, telegram_failure_monitoring=0, data_length=8, total_signals=0, signals=[]):
        # Core CAN attributes
        self.signals = signals
        self.update_CAN_ID(CAN_ID)
        self.update_data_length(data_length)
        self.update_total_signals(total_signals)
        
        # ReceiveMessage-specific attributes
        self.update_telegram_failure_monitoring(telegram_failure_monitoring)
        self.mappings = {
            "CAN_ID": {
                "function": self.update_CAN_ID,
                "description": "11-bit CAN identifier."
            },
            "data_length": {
                "function": self.update_data_length,
                "description": "Size of the CAN message (0-8 bytes)."
            },
            "total_signals": {
                "function": self.update_total_signals,
                "description": "Number of signals in this CAN message."
            },
            "telegram_failure_monitoring": {
                "function": self.update_telegram_failure_monitoring,
                "description": "Error-checking value (0-65535)."
            }
        }

    # ===== Core CAN Methods (from Packet) =====
    def update_CAN_ID(self, CAN_ID):
        if CAN_ID > 2047 or CAN_ID < 0:
            raise OverflowError("CAN_ID needs to fit within an 11-bit integer...")
        self.CAN_ID = CAN_ID
        
    def update_data_length(self, data_length):
        if data_length > 8 or data_length < 0:
            raise OverflowError("data_length needs to be within [0,8]...")
        self.data_length = data_length
        
    def update_total_signals(self, new_total):
        byte_size = 8  # Assuming byte size to be 8 for this context
        if new_total > byte_size:
            raise OverflowError("total_signals needs to fit within 1 byte...")
        if len(self.signals) < new_total:
            for i in range(new_total - len(self.signals)):
                self.signals.append(Signal())
        self.total_signals = new_total

    def getDict(self):
        ret = {
            "CAN_ID": self.CAN_ID,
            "data_length": self.data_length,
            "total_signals": self.total_signals,
            "signals": [signal.get_dict() for signal in self.signals[:self.total_signals]],
            "telegram_failure_monitoring": self.telegram_failure_monitoring
        }
        return ret
    
    # ===== ReceiveMessage Specific Method =====
    def update_telegram_failure_monitoring(self, telegram_failure_monitoring):
        two_byte_size = 65535  # 2-byte max value
        if telegram_failure_monitoring > two_byte_size or telegram_failure_monitoring < 0:
            raise OverflowError("telegram_failure_monitoring needs to fit within two bytes...")
        self.telegram_failure_monitoring = telegram_failure_monitoring


class Signal:

    # Update functions
    def update_signal_type(self, signal_type):
        if signal_type != 0 and signal_type != 2:
            raise Exception("Signal type must be 0 or 2...")
        self.signal_type = signal_type      # Specifies if message is a SERCOS Parameter or Special Signal
    def update_index(self, index):
        if index > two_byte_size:
            raise OverflowError("Ensure signal index is less than two bytes...")
        self.index = index                  # Index SERCOS or Special signal
    def update_bit_length(self, bit_length):
        if bit_length < 0:
            raise Exception("Data length cannot be negative...")
        if bit_length > byte_size:
            raise OverflowError("data_length must fit within a byte...")
        self.bit_length = bit_length      # Data length index in bit
    def update_message(self, message):
        if message >= pow(2, self.bit_length * 8):
            raise OverflowError("Ensure message fits within data length...")
        for checker in self.checkers:
            checker(message)
        self.message = message
    def update_start_bit(self, start_bit):
        self.start_bit = start_bit


    def __init__(self, signal_type = 0, index = 0, bit_length = 0, message = 0, start_bit = 0, checker_functions = []):
        self.checkers = checker_functions   # Custom validations for the message
        self.update_signal_type(signal_type)
        self.update_index(index)
        self.update_bit_length(bit_length)
        self.update_message(message)
        self.update_start_bit(start_bit)
        self.mappings = {
            "signal_type": {
                "function": self.update_signal_type,
                "description": "Signal type (0 = SERCOS Parameter, 2 = Special Signal)."
            },
            "index": {
                "function": self.update_index,
                "description": "Signal index (max 65535)."
            },
            "bit_length": {
                "function": self.update_bit_length,
                "description": "Length of the signal in bits."
            },
            "start_bit": {
                "function": self.update_start_bit,
                "description": "Start position of the signal in the CAN frame."
            },
            "sig_attr": {
                "function": self.update_message,
                "description": "Encoded message content."
            }
        }
    
    def get_dict(self):
        ret = dict()
        ret["signal_type"] = self.signal_type
        ret["index"] = self.index
        ret["bit_length"] = self.bit_length
        ret["start_bit"] = self.start_bit
        ret["sig_attr"] = self.message
        return ret




class Verification:
    def read_JSON(file_path):
        # Open and read the JSON file
        with open(file_path, 'r') as file:
            data = json.load(file)

        new_message = CANMessage(data["message_config"], data["total_send"], data["total_recv_msgs"], data["transmission_rate"])

        for i in range(data["total_send"]):
            packet_to_encode = data["send_msgs"][i]
            new_packet = SendMessage(packet_to_encode["CAN_ID"], packet_to_encode["cycle_time"], packet_to_encode["data_length"], packet_to_encode["attr"], packet_to_encode["total_signals"])
            for ii in range(new_packet.total_signals):
                signal_to_encode = packet_to_encode["signals"][ii]
                new_signal = Signal(signal_to_encode["signal_type"], signal_to_encode["index"], signal_to_encode["bit_length"], signal_to_encode["start_bit"])
                new_packet.signals[ii] = new_signal
            new_message.send_messages[i] = new_packet

        for i in range(data["total_recv_msgs"]):
            packet_to_encode = data["receive_messages"][i]
            new_packet = ReceiveMessage(packet_to_encode["CAN_ID"], packet_to_encode["telegram_failure_monitoring"], packet_to_encode["data_length"], packet_to_encode["total_signals"])

            for ii in range(new_packet.total_signals):
                signal_to_encode = packet_to_encode["signals"][ii]
                new_signal = Signal(signal_to_encode["signal_type"], signal_to_encode["index"], signal_to_encode["bit_length"], signal_to_encode["start_bit"])
                new_packet.signals[ii] = new_signal
            new_message.receive_messages[i] = new_packet
        
        return new_message

    def write_JSON(file_path, can_message):
        with open(file_path, 'w') as file:
            json.dump(can_message.get_dict(), file, indent=2)
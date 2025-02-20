## Project Plannning:

# Make a bunch of classes that represent the messages we can send
# Specify object/functions to run checks on the attributes of each class
# Message class structure:
# Attributes list: stores tuple/object? that contains a name, value, and a checker Object???

import json

byte_size = 255
two_byte_size = 65535

class CANMessage:

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
                self.send_messages.append(Packet())
        self.total_send = new_total

    def update_receive_total(self, new_total):
        if new_total > 10 or new_total < 0:
            raise Exception("Specified total out of bounds...")
        if len(self.receive_messages) < new_total:
            for i in range(new_total - len(self.receive_messages)):
                self.receive_messages.append(Packet())
        self.total_receive = new_total

    # Constructor
    def __init__(self, config_mode = 1, total_send = 0, total_receive = 0, send_messages = [], receive_messages = []):
        self.send_messages = send_messages
        self.receive_messages = receive_messages
        self.update_config_mode(config_mode)
        self.update_send_total(total_send)
        self.update_receive_total(total_send)
    
    # Dictionary getter
    def getDict(self):
        ret = dict()
        ret["config_mode"] = self.config_mode
        ret["total_send"] = self.total_send
        ret["total_receive"] = self.total_receive
        ret["send_messages"] = self.send_messages[0:self.total_send]
        ret["return_messages"] = self.receive_messages[0:self.total_receive]
        return ret

        

class Packet:

    # update methods
    def update_CAN_ID(self, CAN_ID):
        if CAN_ID > 2047 or CAN_ID < 0:
            raise OverflowError("CAN_ID needs to fit within a 11-bit integer...")
        self.CAN_ID = CAN_ID
    def update_cycle_time(self, cycle_time):
        if cycle_time > two_byte_size or cycle_time < 0:
            raise OverflowError("cycle_time needs to fit within two bytes...")
        self.cycle_time = cycle_time
    def update_data_length(self, data_length):
        if data_length > 8 or data_length < 0:
            raise OverflowError("data_length needs to be within [0,8]...")
        self.data_length = data_length
    def update_attr(self, attr):
        if attr != 0 and attr != 1:
            raise Exception("attr can only be 1 or 0...")
        self.attr = attr
    def update_total_signals(self, new_total):
        if new_total > byte_size:
            raise OverflowError("total_signals needs to fit within 1 byte...")
        if len(self.signals) < new_total:
            for i in range(len(self.signals) - new_total):
                self.signals.append(Signal())
        self.total_signals = new_total

    # Constructor
    def __init__(self, CAN_ID = 0, cycle_time = 0, data_length = 8, attr = 0, total_signals = 0, signals = []):
        self.signals = signals
        self.update_CAN_ID(CAN_ID)
        self.update_cycle_time(cycle_time)
        self.update_data_length(data_length)
        self.update_attr(attr)
        self.update_total_signals(total_signals)

    # Dictionary method
    def getDict(self):
        ret = dict()
        ret["CAN_ID"] = self.CAN_ID
        ret["cycle_time"] = self.cycle_time
        ret["data_length"] = self.data_length
        ret["attr"] = self.attr
        ret["total_signals"] = self.total_signals
        ret["signals"] = self.signals[0:self.total_signals]
        return ret

    


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
    def update_data_length(self, data_length):
        if data_length < 0:
            raise Exception("Data length cannot be negative...")
        if data_length > byte_size:
            raise OverflowError("data_length must fit within a byte...")
        self.data_length = data_length      # Data length index in bit
    def update_message(self, message):
        if message >= pow(2, self.data_length * 8):
            raise OverflowError("Ensure message fits within data length...")
        for checker in self.checkers:
            checker(message)
        self.message = message
    def update_start_bit(self, start_bit):
        self.start_bit = start_bit


    def __init__(self, signal_type = 0, index = 0, data_length = 0, message = 0, start_bit = 0, checker_functions = []):

        self.update_signal_type(signal_type)
        self.update_index(index)
        self.update_data_length(data_length)
        self.update_message(message)
        self.update_start_bit(start_bit)
        self.checkers = checker_functions   # Custom validations for the message

    
    def get_dict(self):
        ret = dict()
        ret["signal_type"] = self.signal_type
        ret["index"] = self.index
        ret["bit_length"] = self.data_length
        ret["start_bit"] = self.start_bit
        ret["sig_attr"] = self.message
        return ret




class Verification:
    def read_JSON(file_path):
        # Open and read the JSON file
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Print the data
        new_message = CANMessage(data["message_config"], data["total_send"], data["total_recv_msgs"])

        for i in range(data["total_send"]):
            packet_to_encode = data["send_msgs"][i]
            print(packet_to_encode)
            new_packet = Packet(packet_to_encode["CAN_ID"], packet_to_encode["cycle_time"], packet_to_encode["data_length"], packet_to_encode["attr"])

            for ii in range(new_packet.total_signals):
                signal_to_encode = packet_to_encode["signals"][ii]
                new_signal = Signal(signal_to_encode["signal_type"], signal_to_encode["index"], signal_to_encode["bit_length"], signal_to_encode["start_bit"])
                new_packet.signals.append(new_signal)
            new_message.send_messages.append(new_packet)

        for i in range(data["total_recv_msgs"]):
            packet_to_encode = data["receive_messages"][i]
            new_packet = Packet(packet_to_encode["CAN_ID"], packet_to_encode["cycle_time"], packet_to_encode["data_length"], packet_to_encode["attr"])

            for ii in range(new_packet.total_signals):
                signal_to_encode = packet_to_encode["signals"][ii]
                new_signal = Signal(signal_to_encode["signal_type"], signal_to_encode["index"], signal_to_encode["bit_length"], signal_to_encode["start_bit"])
                new_packet.signals.append(new_signal)
            new_message.send_messages.append(new_packet) 
        
        return new_message



    def verify_config(config_dictionary):
        # Helper function to verify send signals
        def verify_send_signal():
            pass

        # Helper function to verify send messages
        def verify_send_message(send_message):
            for signal in send_message["signals"]:
                Signal(signal["signal_type"], signal["index"], signal["bit_length"], signal["sig_attr"])

        # Ensure that configuration is set to FreeCAN
        if config_dictionary["message_config"] != 1:
            raise Exception("The config is not set up in FreeCAN mode...")

        # Preprocessing for send message verification
        maximum_messages = 10

        total_send = config_dictionary["total_send"]
        send_msgs = config_dictionary["send_msgs"]

        if total_send > maximum_messages:
            raise Exception("Specified too many messages to send...")
        if total_send < 0:
            raise Exception("Cannot send a negative amount of messages...")
        
        for i in range(total_send):
            verify_send_message(config_dictionary["send_msgs"][i])

print(Verification.read_JSON("test_data/data.json"))





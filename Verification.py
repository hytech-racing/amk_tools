## Project Plannning:

# Make a bunch of classes that represent the messages we can send
# Specify object/functions to run checks on the attributes of each class
# Message class structure:
# Attributes list: stores tuple/object? that contains a name, value, and a checker Object???

byte_size = 255
two_byte_size = 65535

class CANMessage:
    def __init__(self, config_mode, total_send, total_receive):
        if config_mode != 1:
            raise Exception("Not in FreeCan mode...")
        if total_send > 10 or total_receive > 10:
            raise Exception("Maximum of 10 send or receive messages...")
        if total_send < 0 or total_receive < 0:
            raise Exception("Specify non-negative send or receive messages...")
        
        self.config_mode = config_mode
        self.total_send = total_send
        self.send_messages = []

        for i in range(total_send):
            self.send_messages.append(Packet())

        self.total_receive = total_receive
        self.receive_messages = []

        for i in range(total_receive):
            self.receive_messages.append(Packet())

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
    
    def getDict(self):
        ret = dict()
        ret["config_mode"] = self.config_mode
        ret["total_send"] = self.total_send
        ret["total_receive"] = self.total_receive
        ret["send_messages"] = self.send_messages[0:self.total_send]
        ret["return_messages"] = self.receive_messages[0:self.total_receive]

        

class Packet:
    def __init__(self, CAN_ID = 0, cycle_time = 0, data_length = 8, attr = 0, total_signals = 0, signals = []):
        if CAN_ID > 2047 or CAN_ID < 0:
            raise OverflowError("CAN_ID needs to fit within a 11-bit integer...")
        if cycle_time > two_byte_size or cycle_time < 0:
            raise OverflowError("cycle_time needs to fit within two bytes...")
        if data_length > 8 or data_length < 0:
            raise OverflowError("data_length needs to be within [0,8]...")
        if attr != 0 and attr != 1:
            raise Exception("attr can only be 1 or 0...")
        if total_signals > byte_size:
            raise OverflowError("total_signals needs to fit within 1 byte...")
        if len(signals) < total_signals:
            raise Exception("Did not provide enough signals...")
        
        self.CAN_ID = CAN_ID
        self.cycle_time = cycle_time
        self.data_length = data_length
        self.attr = attr
        self.total_signals = total_signals
        self.signals = signals
    
    def add_signal(self, signal):
        self.signals[self.total_signals] = signal
        self.total_signals += 1

    def update_total_signals(self, new_total):
        if new_total > byte_size:
            raise OverflowError("total_signals needs to fit within 1 byte...")
        if len(self.signals) < new_total:
            for i in range(len(self.signals) - new_total):
                self.signals.append(Signal())
        self.total_signals = new_total


class Signal:

    def __init__(self, signal_type = 0, index = 0, data_length = 0, message = 0, start_bit = 0, checker_functions = []):
        if signal_type != 0 and signal_type != 2:
            raise Exception("Signal type must be 0 or 2...")
        if index > two_byte_size:
            raise OverflowError("Ensure signal index is less than two bytes...")
        # Do we need to write code to check if negative?
        if data_length < 0:
            raise Exception("Data length cannot be negative...")
        if message >= pow(2, data_length * 8):
            raise OverflowError("Ensure message fits within data length...")
        self.signal_type = signal_type      # Specifies if message is a SERCOS Parameter or Special Signal
        self.index = index                  # Index SERCOS or Special signal
        self.data_length = data_length      # Data length index in bit
        self.start_bit = start_bit          # The entered value is used to specify the start bit of the signal in the message. (0..63 bit)
        self.checkers = checker_functions   # Custom validations for the message

    def check_message_fit(self, message):
        if message >= pow(2, self.data_length * 8):
            raise OverflowError("Ensure message fits within data length...")

    def updateMessage(self, message):
        self.check_message_fit(message)
        for func in self.checkers:
            func(message)

        self.message = message

    def update_index(self, new_index):
        self.index = new_index
    
    def get_dict(self):
        ret = dict()
        ret["signal_type"] = self.signal_type
        ret["index"] = self.index
        ret["bit_length"] = self.data_length
        ret["start_bit"] = self.start_bit
        ret["sig_attr"] = self.message
        return ret










class Verification:



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





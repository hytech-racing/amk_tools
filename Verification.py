## Project Plannning:

# Make a bunch of classes that represent the messages we can send
# Specify object/functions to run checks on the attributes of each class
# Message class structure:
# Attributes list: stores tuple/object? that contains a name, value, and a checker Object???

byte_size = 255
two_byte_size = 65535

class CANMessage:
    pass

class Packet:
    pass

class Signal:

    def __init__(self, signal_type, index, data_length, message, start_bit = 0, checker_functions = []):
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





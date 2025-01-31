class Verification:

    def verify_config(config_dictionary):
        # Helper function to verify send signals
        def verify_send_signal():
            pass

        # Helper function to verify send messages
        def verify_send_message(send_message):
            pass

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





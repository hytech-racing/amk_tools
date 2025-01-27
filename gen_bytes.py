import json

def write_word_to_file(word, file_out):
    word_formatted_hex = f"{word:04x}"
    file_out.write(f"{word_formatted_hex}\n")

def write_msg_signal()

def write_send_CAN_msg(json_message_desc, file_out, leftover_byte_char = None):
    msg_leftover_byte = None
    if(leftover_byte_char is None):
        can_id = json_message_desc["CAN_ID"]
        cycle_time = json_message_desc["cycle_time"]
        write_word_to_file(can_id)
        write_word_to_file(cycle_time)
        
        data_length = json_message_desc["data_length"]
        attr = json_message_desc["attr"]

        data_length_and_attr_word = (attr << 8) | (data_length)
        write_word_to_file(data_length_and_attr_word)
        total_signals = json_message_desc["total_signals"]
        sig_count = 0
        while (sig_count < total_signals):

            sig_count = sig_count + 1


# Read JSON from a file
with open('test.json', 'r') as f:
    json_desc = json.load(f)
    with open('CAN_write.txt', 'w') as f_out:
        # Safely access values and combine them
        try:
            message_config = json_desc["message_config"]
            total_send = json_desc["total_send"]

            # Ensure the integers are within a byte range (0-255)
            if 0 <= message_config <= 255 and 0 <= total_send <= 255:
                # Combine the values into a 2-byte word
                combined_word =  (total_send << 8)| (message_config)

                # Format as a zero-padded 4-character hex string without '0x'
                formatted_hex = f"{combined_word:04x}"

                # Write the result to a file
                f_out.write(f"{formatted_hex}\n")

                msg_write_ind = 0
                while( msg_write_ind < total_send ):
                    write_send_CAN_msg(json_desc["send_msgs"][msg_write_ind], f_out)
                    msg_write_ind = msg_write_ind + 1
            else:
                print("Error: Both values must be within the range 0-255.")
        except KeyError as e:
            print(f"Error: Missing key in JSON data: {e}")
        except ValueError as e:
            print(f"Error: Invalid data in JSON: {e}")

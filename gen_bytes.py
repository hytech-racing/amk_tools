import json

def get_least_sig_val(val):
    return val & 0xFF

def get_most_sig_val(val):
    return (val >> 8) & 0xFF

def combine_bytes_and_write(lsb, msb, file_out):
    word = (msb << 8) | (lsb)
    write_word_to_file(word, file_out)

def write_word_to_file(word, file_out):
    word_formatted_hex = f"{word:04x}".upper()
    file_out.write(f"{word_formatted_hex}\n")


def write_msg_signal(file_out, msg_signal_dict, leftover_byte = None):
    if(leftover_byte is not None):
        reserved = 0
        signal_type = msg_signal_dict["signal_type"]
        combine_bytes_and_write(leftover_byte, signal_type, file_out) # word 1
        index = msg_signal_dict["index"] 
        combine_bytes_and_write(reserved, get_least_sig_val(index), file_out) # word 2
        bit_length = msg_signal_dict["bit_length"]
        combine_bytes_and_write(get_most_sig_val(index), bit_length, file_out) # word 3
        start_bit = msg_signal_dict["start_bit"]
        attribute = msg_signal_dict["sig_attr"] 
        combine_bytes_and_write(start_bit, attribute, file_out) # word 4
        return None
    else:
        signal_type = msg_signal_dict["signal_type"]
        reserved = 0
        combine_bytes_and_write(signal_type, reserved, file_out) # word 1
        index = msg_signal_dict["index"] 
        write_word_to_file(index, file_out) # word 2

        bit_length = msg_signal_dict["bit_length"]
        start_bit = msg_signal_dict["start_bit"]
        combine_bytes_and_write(bit_length, start_bit, file_out) # word 3
        return msg_signal_dict["sig_attr"] # word 4 lsb


def write_CAN_msg(json_message_desc, file_out, leftover_byte_char = None, writing_send_CAN_msgs = True):
    leftover_byte = leftover_byte_char
    if(leftover_byte is None):
        can_id = json_message_desc["CAN_ID"]
        write_word_to_file(can_id, file_out)
        if(writing_send_CAN_msgs):
            cycle_time = json_message_desc["cycle_time"]
            write_word_to_file(cycle_time, file_out)
            attr = json_message_desc["attr"]
        else:
            attr = 0 # reserved
            telegram_failure_monitoring = json_message_desc["telegram_failure_monitoring"] 
            write_word_to_file(telegram_failure_monitoring, file_out)
         
        data_length = json_message_desc["data_length"]

        data_length_and_attr_word = (attr << 8) | (data_length)
        write_word_to_file(data_length_and_attr_word, file_out)

        leftover_byte = json_message_desc["total_signals"]
        total_signals = leftover_byte
        
        sig_count = 0
        # file_out.write("starting_sigs\n")
        while (sig_count < total_signals):
            # print(json_message_desc["signals"][sig_count])
            leftover_byte = write_msg_signal(file_out, json_message_desc["signals"][sig_count], leftover_byte)
            sig_count = sig_count + 1
    else:
        can_id_lsb = get_least_sig_val(json_message_desc["CAN_ID"])
        combine_bytes_and_write(leftover_byte, can_id_lsb, file_out) # word 1
        leftover_byte = None # reset leftover_byte because it has been written
        
        can_id_msb = get_most_sig_val(json_message_desc["CAN_ID"])

        if(writing_send_CAN_msgs):
            cycle_time_lsb = get_least_sig_val(json_message_desc["cycle_time"])

            combine_bytes_and_write(can_id_msb, cycle_time_lsb, file_out) # word 2
            cycle_time_msb = get_most_sig_val(json_message_desc["cycle_time"])
            data_length = json_message_desc["data_length"]

            combine_bytes_and_write(cycle_time_msb, data_length, file_out) # word 3
        else:
            telegram_failure_monitoring_lsb = get_least_sig_val(json_message_desc["telegram_failure_monitoring"])

            combine_bytes_and_write(can_id_msb, telegram_failure_monitoring_lsb, file_out) # word 2
            telegram_failure_monitoring_msb = get_most_sig_val(json_message_desc["telegram_failure_monitoring"])
            data_length = json_message_desc["data_length"]

            combine_bytes_and_write(telegram_failure_monitoring_msb, data_length, file_out) # word 3

        attr = 0
        if(writing_send_CAN_msgs): 
            attr = json_message_desc["attr"]

        total_signals = json_message_desc["total_signals"]
        combine_bytes_and_write(attr, total_signals, file_out) # word 4
        
        sig_count = 0
        while (sig_count < total_signals):
            print(json_message_desc["signals"][sig_count])
            leftover_byte = write_msg_signal(file_out, json_message_desc["signals"][sig_count], leftover_byte)
            sig_count = sig_count + 1

    return leftover_byte
def jsonToRaw (inpath, outpath):
    # Read JSON from a file
    with open(inpath, 'r') as f:
        json_desc = json.load(f)
        with open(outpath, 'w') as f_out:
            # Safely access values and combine them
            try:
                message_config = json_desc["message_config"]
                total_send = json_desc["total_send"]


                ### writing send msgs
                # Ensure the integers are within a byte range (0-255)
                if 0 <= message_config <= 255 and 0 <= total_send <= 255:
                    # Combine the values into a 2-byte word
                    combined_word =  (total_send << 8)| (message_config)
                    write_word_to_file(combined_word, f_out)

                    msg_write_ind = 0
                    leftover_byte = None
                    while( msg_write_ind < total_send ):
                        leftover_byte = write_CAN_msg(json_desc["send_msgs"][msg_write_ind], f_out, leftover_byte)
                        msg_write_ind = msg_write_ind + 1
                    

                    ### writing recv msgs
                    if (leftover_byte is None):
                        total_recv_msgs = json_desc["total_recv_msgs"]

                        leftover_byte = total_recv_msgs 
                        recv_msg_ind = 0
                        while( recv_msg_ind < total_recv_msgs):
                            leftover_byte = write_CAN_msg(json_desc["receive_messages"][recv_msg_ind], f_out, leftover_byte, False)
                            recv_msg_ind = recv_msg_ind + 1
                    else:
                        total_recv_msgs = json_desc["total_recv_msgs"]
                        combine_bytes_and_write(leftover_byte, total_recv_msgs, f_out)
                        leftover_byte = None # reset leftover byte
                        recv_msg_ind = 0
                        while( recv_msg_ind < total_recv_msgs):
                            leftover_byte = write_CAN_msg(json_desc["receive_messages"][recv_msg_ind], f_out, leftover_byte, False)
                            recv_msg_ind = recv_msg_ind + 1
                    ### writing transmission rate and end byte / padding
                    if(leftover_byte is None):
                        transmission_rate_k_baud = json_desc["transmission_rate"]
                        write_word_to_file(transmission_rate_k_baud, f_out)
                        write_word_to_file(0, f_out)
                    else:
                        transmission_rate_k_baud_lsb = get_least_sig_val(json_desc["transmission_rate"])
                        combine_bytes_and_write(leftover_byte, transmission_rate_k_baud_lsb, f_out) # test
                        transmission_rate_k_baud_msb = get_most_sig_val(json_desc["transmission_rate"])
                        combine_bytes_and_write(transmission_rate_k_baud_msb, 0, f_out) # test
                else:
                    print("Error: Both values must be within the range 0-255.")
            except KeyError as e:
                print(f"Error: Missing key in JSON data: {e}")
            except ValueError as e:
                print(f"Error: Invalid data in JSON: {e}")

# ===================================
# remnant
# ===================================
# # Read JSON from a file
# with open('test_ser.json', 'r') as f:
#     json_desc = json.load(f)
#     with open('CAN_write.txt', 'w') as f_out:
#         # Safely access values and combine them
#         try:
#             message_config = json_desc["message_config"]
#             total_send = json_desc["total_send"]


#             ### writing send msgs
#             # Ensure the integers are within a byte range (0-255)
#             if 0 <= message_config <= 255 and 0 <= total_send <= 255:
#                 # Combine the values into a 2-byte word
#                 combined_word =  (total_send << 8)| (message_config)
#                 write_word_to_file(combined_word, f_out)

#                 msg_write_ind = 0
#                 leftover_byte = None
#                 while( msg_write_ind < total_send ):
#                     leftover_byte = write_CAN_msg(json_desc["send_msgs"][msg_write_ind], f_out, leftover_byte)
#                     msg_write_ind = msg_write_ind + 1
                

#                 ### writing recv msgs
#                 if (leftover_byte is None):
#                     total_recv_msgs = json_desc["total_recv_msgs"]

#                     leftover_byte = total_recv_msgs 
#                     recv_msg_ind = 0
#                     while( recv_msg_ind < total_recv_msgs):
#                         leftover_byte = write_CAN_msg(json_desc["receive_messages"][recv_msg_ind], f_out, leftover_byte, False)
#                         recv_msg_ind = recv_msg_ind + 1
#                 else:
#                     total_recv_msgs = json_desc["total_recv_msgs"]
#                     combine_bytes_and_write(leftover_byte, total_recv_msgs, f_out)
#                     leftover_byte = None # reset leftover byte
#                     recv_msg_ind = 0
#                     while( recv_msg_ind < total_recv_msgs):
#                         leftover_byte = write_CAN_msg(json_desc["receive_messages"][recv_msg_ind], f_out, leftover_byte, False)
#                         recv_msg_ind = recv_msg_ind + 1
#                 ### writing transmission rate and end byte / padding
#                 if(leftover_byte is None):
#                     transmission_rate_k_baud = json_desc["transmission_rate"]
#                     write_word_to_file(transmission_rate_k_baud, f_out)
#                     write_word_to_file(0, f_out)
#                 else:
#                     transmission_rate_k_baud_lsb = get_least_sig_val(json_desc["transmission_rate"])
#                     combine_bytes_and_write(leftover_byte, transmission_rate_k_baud_lsb)
#                     transmission_rate_k_baud_msb = get_most_sig_val(json_desc["transmission_rate"])
#                     combine_bytes_and_write(transmission_rate_k_baud_msb, 0)
#             else:
#                 print("Error: Both values must be within the range 0-255.")
#         except KeyError as e:
#             print(f"Error: Missing key in JSON data: {e}")
#         except ValueError as e:
#             print(f"Error: Invalid data in JSON: {e}")
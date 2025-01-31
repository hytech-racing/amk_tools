import json


def get_least_sig_val(val):
    return val & 0xFF
def get_most_sig_val(val):
    return (val >> 8) & 0xFF

def read_word(line):
    if(line == '0000'):
        return 0
    else:
        return int(line, 16)

def parse_message_signal(cur_can_desc_file, leftover_byte = None):
    sig_dict= {}
    if(leftover_byte is not None):
        sig_dict["signal_type"] = leftover_byte
        res_byte_and_index_word_lsb = int(cur_can_desc_file.readline(), 16)
        index_word_msb_and_length_byte = int(cur_can_desc_file.readline(), 16)
        
        sig_dict["index"] =   (get_least_sig_val(index_word_msb_and_length_byte) << 8) | get_most_sig_val(res_byte_and_index_word_lsb)
        sig_dict["bit_length"] = get_most_sig_val(index_word_msb_and_length_byte)
        
        test = cur_can_desc_file.readline()
        # print(test)
        start_bit_and_sig_attr_word = int(test, 16)
        sig_dict["start_bit"] = get_least_sig_val(start_bit_and_sig_attr_word)
        sig_dict["sig_attr"] = get_most_sig_val(start_bit_and_sig_attr_word)

        return None, sig_dict
    else:
        sig_type_and_reserved_word = int(cur_can_desc_file.readline(), 16)
        sig_dict["signal_type"] = get_least_sig_val(sig_type_and_reserved_word)
        sig_dict["index"] = int(cur_can_desc_file.readline(), 16)

        length_and_shift_word = int(cur_can_desc_file.readline(), 16)

        sig_dict["bit_length"] = get_least_sig_val(length_and_shift_word)
        sig_dict["start_bit"] = get_most_sig_val(length_and_shift_word)
        attr_and_next_signal_type_word = int(cur_can_desc_file.readline(), 16)
        sig_dict["sig_attr"] = get_least_sig_val(attr_and_next_signal_type_word)
        return get_most_sig_val(attr_and_next_signal_type_word), sig_dict
        

def parse_send_message(cur_can_desc_file, leftover_byte_arg = None):
    leftover_byte = leftover_byte_arg

    if(leftover_byte is None):
        send_msg = {}
        send_msg["CAN_ID"] = int(cur_can_desc_file.readline(), 16)
        send_msg["cycle_time"] = int(cur_can_desc_file.readline(), 16)

        data_length_and_attr_word = int(cur_can_desc_file.readline(), 16)

        send_msg["data_length"] = get_least_sig_val(data_length_and_attr_word)
        send_msg["attr"] = get_most_sig_val(data_length_and_attr_word)

        total_signals_and_first_sig_type_word = int(cur_can_desc_file.readline(), 16)
        send_msg["total_signals"] = get_least_sig_val(total_signals_and_first_sig_type_word)

        cur_sig_index = 0
        send_msg["signals"] = []
        leftover_byte = get_most_sig_val(total_signals_and_first_sig_type_word)
        while(cur_sig_index < send_msg["total_signals"]):
            
            leftover_byte, signal = parse_message_signal(cur_can_desc_file, leftover_byte)
            send_msg["signals"].append(signal)
            cur_sig_index = cur_sig_index +1
        
        return send_msg, leftover_byte
    else:
        send_msg = {}
        lsb_CAN_id = leftover_byte
        msb_CAN_id_and_lsb_cycle_time = int(cur_can_desc_file.readline(), 16)
        send_msg["CAN_ID"] = (get_least_sig_val(msb_CAN_id_and_lsb_cycle_time)) | (lsb_CAN_id)
        cycle_time_msb_and_data_length = int(cur_can_desc_file.readline(), 16)
        send_msg["cycle_time"] = (get_least_sig_val(cycle_time_msb_and_data_length)) | get_most_sig_val(msb_CAN_id_and_lsb_cycle_time)
        send_msg["data_length"] = get_most_sig_val(cycle_time_msb_and_data_length)

        attr_and_total_signals = int(cur_can_desc_file.readline(), 16)
        send_msg["attr"] = get_least_sig_val(attr_and_total_signals)
        send_msg["total_signals"] = get_most_sig_val(attr_and_total_signals)

        cur_sig_index = 0
        send_msg["signals"] = []
        leftover_byte = None
        while(cur_sig_index < send_msg["total_signals"]):
            leftover_byte, signal = parse_message_signal(cur_can_desc_file, leftover_byte)
            send_msg["signals"].append(signal)
            cur_sig_index = cur_sig_index + 1
        
        return send_msg, leftover_byte

def parse_recv_message(cur_can_desc_file, leftover_byte_arg = None):
    leftover_byte = leftover_byte_arg

    if(leftover_byte is None):
        send_msg = {}
        send_msg["CAN_ID"] = int(cur_can_desc_file.readline(), 16)
        send_msg["telegram_failure_monitoring"] = int(cur_can_desc_file.readline(), 16)

        data_length_and_resvd_word = int(cur_can_desc_file.readline(), 16)

        send_msg["data_length"] = get_least_sig_val(data_length_and_resvd_word)

        total_signals_and_first_sig_type_word = int(cur_can_desc_file.readline(), 16)
        send_msg["total_signals"] = get_least_sig_val(total_signals_and_first_sig_type_word)

        cur_sig_index = 0
        send_msg["signals"] = []
        leftover_byte = get_most_sig_val(total_signals_and_first_sig_type_word)
        while(cur_sig_index < send_msg["total_signals"]):
            
            leftover_byte, signal = parse_message_signal(cur_can_desc_file, leftover_byte)
            send_msg["signals"].append(signal)
            cur_sig_index = cur_sig_index +1
        
        return send_msg, leftover_byte
    else:
        send_msg = {}
        lsb_CAN_id = leftover_byte
        msb_CAN_id_and_lsb_telegram_failure_monitoring = int(cur_can_desc_file.readline(), 16)
        send_msg["CAN_ID"] = (get_least_sig_val(msb_CAN_id_and_lsb_telegram_failure_monitoring)) | (lsb_CAN_id)
        telegram_failure_monitoring_msb_and_data_length = int(cur_can_desc_file.readline(), 16)
        send_msg["telegram_failure_monitoring"] = (get_least_sig_val(telegram_failure_monitoring_msb_and_data_length)) | get_most_sig_val(msb_CAN_id_and_lsb_telegram_failure_monitoring)
        send_msg["data_length"] = get_most_sig_val(telegram_failure_monitoring_msb_and_data_length)

        resvd_and_total_signals = int(cur_can_desc_file.readline(), 16)
        send_msg["total_signals"] = get_most_sig_val(resvd_and_total_signals)

        cur_sig_index = 0
        send_msg["signals"] = []
        leftover_byte = None
        while(cur_sig_index < send_msg["total_signals"]):
            leftover_byte, signal = parse_message_signal(cur_can_desc_file, leftover_byte)
            send_msg["signals"].append(signal)
            cur_sig_index = cur_sig_index + 1
        
        return send_msg, leftover_byte

CAN_desc = open("CAN_write.txt", "r")
# CAN_desc = open("test_data/AMK_raw_CAN_userlist", "r")

total_send_and_message_config_word = int(CAN_desc.readline(), 16)

description_json = {}
description_json["message_config"] = total_send_and_message_config_word & 0xFF

description_json["total_send"] = (total_send_and_message_config_word >> 8) & 0xFF



current_send_msg_parse_ind = 0
description_json["send_msgs"] = []
leftover_byte = None
while(current_send_msg_parse_ind < description_json["total_send"]):
    send_msg, leftover_byte = parse_send_message(CAN_desc, leftover_byte)
    description_json["send_msgs"].append(send_msg)
    current_send_msg_parse_ind = current_send_msg_parse_ind + 1

if(leftover_byte is None):
    total_recv_msgs_and_lsb_first_can_recv_msg_word = int(CAN_desc.readline(), 16)
    description_json["total_recv_msgs"] = get_least_sig_val(total_recv_msgs_and_lsb_first_can_recv_msg_word)

    leftover_byte = get_most_sig_val(total_recv_msgs_and_lsb_first_can_recv_msg_word)
    current_recv_msg_ind = 0
    description_json["receive_messages"] = []
    while(current_recv_msg_ind < description_json["total_recv_msgs"]):
        recv_msg, leftover_byte = parse_recv_message(CAN_desc, leftover_byte)
        description_json["receive_messages"].append(recv_msg)
        current_recv_msg_ind = current_recv_msg_ind + 1

else:

    description_json["total_recv_msgs"] = leftover_byte
    current_recv_msg_ind = 0
    description_json["receive_messages"] = []
    while(current_recv_msg_ind < description_json["total_recv_msgs"]):
        recv_msg, leftover_byte = parse_recv_message(CAN_desc, leftover_byte)
        description_json["receive_messages"].append(recv_msg)
        current_recv_msg_ind = current_recv_msg_ind + 1

if(leftover_byte is not None):

    transmission_rate_msb_and_end_byte = int(CAN_desc.readline(), 16)
    description_json["transmission_rate"] =  (get_least_sig_val(transmission_rate_msb_and_end_byte) << 8) | (leftover_byte)
else:
    description_json["transmission_rate"] = int(CAN_desc.readline(), 16)

json_formatted_str = json.dumps(description_json, indent=2)

print(json_formatted_str)





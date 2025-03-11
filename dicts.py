signal = [{"Signal Type": 0},
          {"Index": 0},
          {"Bit Length": 0},
          {"Start Bit": 0},
          {"Signal Attribute": 0},
          ]

message = [{"CAN ID": 0},
           {"Cycle Time": 0},
           {"Data Length": 0},
           {"Attribute": 0},
           {"Total Signal Count": 0},
           ]

for i in range (16):
    message[f"Signal {i}"] = signal

main = [{"Message Config" : 1},
        {"Total Send Message Count" : 0},
        {"Total Receive Message Count" : 0},
        ]

for i in range(10):
    main[f"Receive Message {i}"] = message
    main[f"Send Message {i}"] = message

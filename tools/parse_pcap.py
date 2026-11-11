import struct

f = open( "capture.pcap", "rb")


pcap_metadata = f.read(24)

fields = struct.unpack("<IHHIIII", pcap_metadata)

print(fields)

count = 0
while True:

    record_header = f.read(16)

    if not record_header:
        break 

    ts_sec, ts_usec, incl_len, orig_len = struct.unpack("<IIII", record_header)

    frame = f.read(incl_len)

    print(ts_sec, ts_usec, incl_len, len(frame))

    count += 1 

print(count)

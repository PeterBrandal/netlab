# Decodes a .pcap capture file by hand - no parsing libraries.
#
# Three nested things live in this file, and only the third is network data:
#
#   1. file header  (24 bytes, once)  - tcpdump's metadata about the capture
#   2. record header (16 bytes, each) - tcpdump's bookkeeping per packet
#   3. frame        (incl_len bytes)  - the actual bytes off the wire
#
# Inside each frame the layers nest again:
#
#   SLL2 (20) -> IP (20) -> TCP (32) -> WebSocket (7)

import struct



def parse(path: str):

    with open( path, "rb") as f:

        pcap_metadata = f.read(24)

        # magic, version_major, version_minor, thiszone, sigfigs, snaplen, network
        fields = struct.unpack("<IHHIIII", pcap_metadata)


        while True:

            # --- record header: pcap's own per-packet wrapper, not a network layer ---
            record_header = f.read(16)

            if not record_header:
                break

            ts_sec, ts_usec, incl_len, orig_len = struct.unpack("<IIII", record_header)

            # incl_len says how many bytes of frame follow, so reading exactly that
            # many leaves the cursor on the next record header.
            frame = f.read(incl_len)

            # --- layer 2: skipped. frame[0:20] is SLL2, a fake link header Linux
            # fabricates for 'tcpdump -i any'. Nothing real to learn from it.

            # --- layer 3: IP. Starts right after SLL2. ---
            ip_header = frame[20:40]

            # byte 9 = protocol number of whatever is nested inside. 6 = TCP.
            protocol = ip_header[9]

            # bytes 12-16 and 16-20 are the addresses, one byte per octet.
            src_ip = '.'.join(str(b) for b in ip_header[12:16])
            dest_ip= '.'.join(str(b) for b in ip_header[16:20])

            # --- layer 4: TCP Layer ---
            tcp_header  = frame[40:72]

            src_port, dest_port = struct.unpack('>HH', tcp_header[0:4]) 

            # --- Data --- 
            payload = frame[72:]

            yield { "timestamp": ts_sec + ts_usec / 1_000_000, "protocol": protocol, "source_ip": src_ip, "source_port": src_port, "destination_ip": dest_ip, "destination_port": dest_port, "payload": payload }

    
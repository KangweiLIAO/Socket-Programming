import sys, getopt, binascii, random, time
import socket

HOST = socket.gethostbyname(socket.gethostname())
SERVER = ''
PORT = 6666
payload = ''

def calc_checksum(headerSum):
    """ 
    Calculate the checksum of given sum of header (hex_string) 
    and return checksum (int, base 16)
    """
    checksum = 0x0
    if(len(header) > 4):            # means carry exist
        checksum = int(header[0],16) + int(header[1:],16)
    else:                           # no carry
        checksum = int(header,16)
    checksum = 0xffff-checksum      # take one's complement
    return checksum

def encode(hexMsg):
    """ 
    Encode the msg (int, base 16) got from user and return an IP datagram (hex_string)
    """
    # Header's components:
    ip_ver = 0x4500     # Protocol, header length, TOS
    ip_len = int(       # total length of HOST header
        hex(
            20 + int(len(bin(hexMsg))/8)            # 20bytes + bin(payload_len)/8
        ),16
    )
    ip_id = int(hex(random.randint(0,65535)),16)    # identification
    ip_frag = 0x4000                                # fragment offset
    ip_ttl = 0x4006                                 # time to live
    ip_cs = 0x0                                     # initialize checksum = 0000
    ip_src1 = int(binascii.hexlify(socket.inet_aton(HOST))[:4],16)
    ip_src2 = int(binascii.hexlify(socket.inet_aton(HOST))[5:],16)
    ip_dst1 = int(binascii.hexlify(socket.inet_aton(SERVER))[:4],16)
    ip_dst2 = int(binascii.hexlify(socket.inet_aton(SERVER))[5:],16)
    # compute the header with checksum = 0000
    header = ip_ver + ip_len + ip_id + ip_frag + ip_ttl + ip_cs + ip_src1 + ip_src2 + ip_dst1 + ip_dst2
    ip_cs = calc_checksum(hex(header)[2:])   # getting checksum
    hexHeader = ("%04X" % ip_ver)+("%04X" % ip_len)+("%04X" % ip_id)+("%04X" % ip_frag)+("%04X" % ip_ttl)+("%04X" % ip_cs)+("%04X" % ip_src1)+("%04X" % ip_src2)+("%04X" % ip_dst1)+("%04X" % ip_dst2)
    return (hexHeader + hex(hexMsg)[2:])     # return datagram

def main(argv):
    """ 
    Main function that create a socket to connect the server with given 
    command line options
    """
    global HOST, SERVER, PORT, payload         # set these local vars match the global var
    try:
        # opts: list of returning key-value pairs, args: the options left after striped
        # 'hs:p:' means h is optional, s/p is required short option (followed by ":")
        # "['server=','payload=']" means server/payload is required long option (followed by "=")
        opts, args = getopt.getopt(argv,'hs:p:',['server=','payload='])
    except getopt.GetoptError:
        print('python3 packet_sender.py -server <server_ip> -payload <string>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('python3 packet_sender.py -s(server) <server_ip> [-p(payload) <string>]')
            sys.exit()
        elif opt in ('-s', '--server'):
            SERVER = arg
        elif opt in ('-p', '--payload'):
            payload = arg
    # connecting to server
    try:
        print("Connecting to {}:{}".format(SERVER, PORT))
        while True:
            s = socket.socket()
            s.connect((SERVER,PORT))
            if(payload == ''):
                print("Please enter your message (1-line) and press return:")
                payload = input()
            hexMsg = int(payload.encode('utf-8').hex(), 16)
            datagram = encode(hexMsg)       # encode msg
            s.send(datagram.encode())
            sentTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print("\"{}\" - {}\n".format(payload, sentTime))
            payload = ''
        s.close()
    except:
        print("Unexpected Error:", sys.exc_info()[0])
        raise

if __name__ == '__main__':
    main(sys.argv[1:])
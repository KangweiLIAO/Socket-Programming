import sys, binascii
import socket              

HOST = socket.gethostbyname(socket.gethostname())
PORT = 6666

def decode(hexMsg):
    """
    Decode the msg(hex_string) to verify the packet, return True if no error
    """
    msgArr = [int(hexMsg[i:i+4],16) for i in range(0, len(hexMsg), 4)]
    headerSum = hex(sum(msgArr[0:10]))[2:]
    if(len(headerSum) > 4):         # means carry exist
        headerSum = int(headerSum[0],16) + int(headerSum[1:],16)
    else:                           # no carry
        headerSum = int(headerSum,16)
    if (0xffff-headerSum == 0):     # check 1's complement if 0 then no error
        return True
    return False

def main():
    """ 
    Main function that create a socket and wait for client's connection
    """
    s = socket.socket()
    s.bind((HOST, PORT))    # bind IP address with given port
    s.listen(5)             # up to 5 connections
    print("Server started on: " + str(HOST) + ":" + str(PORT))
    try:
        while True:
            print("*" * 50)
            conn, addr = s.accept()
            rawMsg = conn.recv(2048)
            if (rawMsg == b''):
                print("{}:{} Offline \U0001f644\n".format(addr[0], addr[1]))
            else:
                msg = hex(int(rawMsg,16))
                totalLen = len(bin(int(msg,16)))
                dataLen = len(str(bin(int(msg[40:],16))))
                msgStr = binascii.unhexlify(msg[40:]).decode('ascii')
                print("The data received from {}:{} is \"{}\"".format(addr[0], addr[1], msgStr))
                print("The data has {} bits or {} bytes.".format(dataLen,dataLen/8))
                print("Total length of the packet is {} bytes.".format(int(totalLen/8)))
                if (decode(msg[2:]) == True):
                    print("The verification of the checksum demonstrates that the packet received is correct.\n")
                else:
                    print("The verification of the checksum demonstrates that the packet received is corrupted. Packet discarded!\n")
    except:
        print("Unexpected Error:", sys.exc_info()[0])
        raise
    s.close()
    return

if __name__ == '__main__':
    main()
import socket
import time
import pickle

UDP_IP = "0.0.0.0"
UDP_PORT = 8080

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    req_data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    rec_time = int(round(time.time() * 1000))
    req = pickle.loads(req_data)
    ret_addr = addr[0]
    ret_port = addr[1]

    print ("received request: ", req, " from ", ret_addr, " on port", ret_port)

    if(req == "request_time"):
        client_sock = socket.socket(socket.AF_INET, # Internet
                              socket.SOCK_DGRAM) # UDP

        client_sock.sendto(
            pickle.dumps((rec_time,int(round(time.time() * 1000)))),
            (UDP_IP, ret_port))
        client_sock.close()

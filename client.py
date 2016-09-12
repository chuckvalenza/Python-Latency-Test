import socket
import time
import select
import pickle

SRV_IP = "agate.cs.unh.edu"
SRV_PORT = 8080
MESSAGE = "request_time"
RETURN_TIMEOUT = 5

def recv_resp(sock, send_time):
    sock.setblocking(0)
    ready = select.select([sock], [], [], RETURN_TIMEOUT)
    if ready[0]:
        resp, addr = sock.recvfrom(1024)
        recv_time = int(round(time.time() * 1000))
        time_data = pickle.loads(resp)
        srv_recv  = time_data[0]
        srv_send = time_data[1]
        return (send_time,
                srv_recv,
                srv_send,
                recv_time)
    else:
        return ("failed")

def send_req(sock, ip, port, req):
    send_time = int(round(time.time() * 1000))
    sock.sendto(pickle.dumps(req), (ip, port))
    return send_time

def main():
    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP

    for f in range(0,3):
        send_time = send_req(sock, SRV_IP, SRV_PORT, MESSAGE)
        times = recv_resp(sock, send_time)

        if times == "failed":
                print("timed out, reattempting connection")
        else:
            print("Client send time:    " + str(times[0]))
            print("Server recieve time: " + str(times[1]))
            print("Server send time:    " + str(times[2]))
            print("Client recieve time: " + str(times[3]))
            print("Client delta:        " + str(times[3] - times[0]))
            print("Server delta:        " + str(times[2] - times[1]))
            rtt = (times[3] - times[0]) - (times[2] - times[1])
            print("RTT:                 " + str(rtt))
            print("Offset:              " + str((times[0] + rtt/2) - times[1]))
            return

main()

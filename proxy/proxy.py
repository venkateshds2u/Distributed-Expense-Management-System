import socket
import select
import time
import sys
import redis
import gbcb

# Changing the buffer_size and delay, you can improve the speed and bandwidth.
# But when buffer get to high or delay go too down, you can broke things
buffer_size = 4096
delay = 0.0001
forward_to = ('192.168.99.100', 6701)

class Forward:
    MY_EXCEPTION = 'Threw Dependency Exception'
    def __init__(self):
        self.forward = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    @gbcb.CircuitBreaker(name='My CB-3', max_failure_to_open=3, reset_timeout=3)
    def dependency_call3(self, host, port,portid):
        try:
            self.forward.connect((host, port))
            return self.forward
        except Exception as e:
            raise Exception(self.MY_EXCEPTION)

    @gbcb.CircuitBreaker(name='My CB-2', max_failure_to_open=3, reset_timeout=3)
    def dependency_call2(self, host, port,portid):
        try:
            self.forward.connect((host, port))
            return self.forward
        except Exception as e:
            raise Exception(self.MY_EXCEPTION)

    @gbcb.CircuitBreaker(name='My CB-1', max_failure_to_open=3, reset_timeout=3)
    def dependency_call1(self, host, port,portid):
        try:
            self.forward.connect((host, port))
            return self.forward
        except Exception as e:
            raise Exception(self.MY_EXCEPTION)


class TheServer:
    input_list = []
    channel = {}

    portID = 1
    port = 0
    r = redis.StrictRedis(host='redis', port=6379, db=0)
    MY_EXCEPTION = 'Threw Dependency Exception'




    def __init__(self, host, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        self.server.listen(200)

    def main_loop(self):
        self.input_list.append(self.server)
        while 1:
            time.sleep(delay)
            ss = select.select
            inputready, outputready, exceptready = ss(self.input_list, [], [])
            for self.s in inputready:
                if self.s == self.server:
                    self.on_accept()
                    break

                self.data = self.s.recv(buffer_size)
                if len(self.data) == 0:
                    self.on_close()
                    break
                else:
                    self.on_recv()




    def setPort(self, temp):
        if self.r.get(temp):
            self.port = self.r.get(temp)
        else:
            if self.portID == 3:
                self.portID = 1
            else:
                self.portID += 1
            self.setPort(self.portID)

        if self.portID == 3:
            self.portID = 1
        else:
            self.portID += 1

    def on_accept(self):
        self.setPort(self.portID)
        clientsock, clientaddr = self.server.accept()
        try:
            if self.port[-1:]=="1":
                forward = Forward().dependency_call1('flask'+self.port[-1:], int(self.port), int(self.port[-1:]))
            else:
                if self.port[-1:]=="2":
                    forward = Forward().dependency_call2('flask'+self.port[-1:], int(self.port), int(self.port[-1:]))
                else:
                    forward = Forward().dependency_call3('flask'+self.port[-1:], int(self.port), int(self.port[-1:]))
            #forward = Forward().dependency_call('flask'+self.port[-1:],  int(self.port),int(self.port[-1:]))

            print clientaddr, "has connected"
            self.input_list.append(clientsock)
            self.input_list.append(forward)
            self.channel[clientsock] = forward
            self.channel[forward] = clientsock
        except Exception as ex:
            print ex.message
            print "Can't establish connection with remote server.",
            print "Closing connection with client side", clientaddr
            clientsock.close()



    def on_close(self):
        print self.s.getpeername(), "has disconnected"
        #remove objects from input_list
        self.input_list.remove(self.s)
        self.input_list.remove(self.channel[self.s])
        out = self.channel[self.s]
        # close the connection with client
        self.channel[out].close()  # equivalent to do self.s.close()
        # close the connection with remote server
        self.channel[self.s].close()
        # delete both objects from channel dict
        del self.channel[out]
        del self.channel[self.s]

    def on_recv(self):
        data = self.data
        # here we can parse and/or modify the data before send forward
        print data
        self.channel[self.s].send(data)

if __name__ == '__main__':
        server = TheServer('0.0.0.0', 12345)
        try:
            server.main_loop()
        except KeyboardInterrupt:
            print "Ctrl C - Stopping server"
            sys.exit(1)

import TCPClient
import TCPServer


if __name__=="__main__": #se stiamo lanciando questo script come programma
    TCPServer.sub_server(("127.0.0.1",20000))
    TCPClient.conn_sub_server(("127.0.0.1",20000))

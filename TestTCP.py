import TCPClient

def testing(n_test):
    for i in range(n_test):
        TCPClient.conn_sub_server(("127.0.0.1",20000))



if __name__=="__main__": #se stiamo lanciando questo script come programma
    testing(2)


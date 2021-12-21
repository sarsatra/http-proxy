import socket, threading, sys, argparse

def main():
    parser = argparse.ArgumentParser(description='HTTP Proxy server.')
    parser.add_argument('-p', '--port', type=int, help='Port number', default=8080)
    parser.add_argument('-m', '--mconn', type=int, help='Max connection', default=5)
    parser.add_argument('-b', '--byte', type=int, help='Bytes of recieve buffers', default=8192)
    args = parser.parse_args()
    global port, buffers, maxconn
    port =  args.port
    maxconn = args.mconn
    buffers = args.byte
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', port))
        s.listen(maxconn)
        print("Starting server...")
        print(f"Server started at [{port}]")
    except Exception as e:
        print(e)
        sys.exit()
    
    while True:
        try:
            conn, addr = s.accept()
            data = conn.recv(buffers)
            t = threading.Thread(connstring(conn, data, addr))
            t.start()
        except KeyboardInterrupt:
            s.close()
            print("\nShutting down...")
            sys.exit()
def connstring(conn, data, addr):
    try:
        isIP = False
        fline = data.decode('utf-8').split('\n')[0]
        url = fline.split(' ')[1]
        requrl = url
        a = requrl.find(":")
        b = requrl[:a]
        pp = requrl[:a]
        wport = requrl[a+1:]
        if pp == 'http':
            wport = '80'
            b = requrl[a+3:len(requrl)]
            slash = b.find('/', 7, len(requrl)+1)
            b = b[:slash]
        if isIP:
            ip = b
        else:
            ip = socket.gethostbyname(b)
        print(f"New Request from {addr[0]} => {ip} ")
        proxyserver(ip, int(wport), conn, data, addr)
    except Exception as e:
        print(e)
def proxyserver(webserver, port, conn, data, addr):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((webserver, port))
        s.send(data)
        while True:
            reply = s.recv(buffers)
            if len(reply) > 0:
                try:
                    conn.send(reply)
                    dar = float(len(reply)) 
                    dar = float(dar/1024)
                    dar = f"{dar}"
                    print(f"Request done: {addr[0]} => {dar} <= {webserver}")
                except Exception as e:
                    print(e)
            else:
                break
        s.close()
        conn.close()
    except socket.error:
        s.close()
        conn.close()
        sys.exit()

if __name__ == "__main__":
    main()

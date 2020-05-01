#Copyright (c) 2020 Derek Frombach

import time
import socket
import subprocess

connectmyrio=True
oip='0.0.0.0' #Don't Change This
remhost='192.168.0.2'
remport=8082
port=8081 #Hosting Port, Don't Change This
buff=1400 #Also Don't Change This
tout=0.5
giveup=2.0
fps=1/30

#Function Call Speedups
tc=time.perf_counter
tt=time.time
ts=time.sleep
ste=socket.timeout
rdwr=socket.SHUT_RDWR
se=socket.error

def secure_connect(ip,port):
    #Initalisation of TCP Socket Server
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP/IP Socket
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Unbind when Done
    s.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1) #Zero-Latency TCP
    s.bind((ip,port)) #Starting Connect Back Server
    s.listen(1) #Listen for Connections
    ip=False
    running=False
    while True:
        if not running:
            print('Accepting Clients')
            running=True
        try:
            s.settimeout(0.1)
            conn,addr=s.accept()
        except KeyboardInterrupt:
            exit()
        except ste:
            try:
                ts(0.1)
                continue
            except KeyboardInterrupt:
                exit()
        running=False
        s.settimeout(None)
        ct=conn.settimeout
        ct(tout)
        #Header Communication with Client
        cs=conn.sendall #Connection Speedup
        ts(tout)
        #Client Timeout Handler
        try:
            data=conn.recv(buff)
        except ste:
            print("BOT!")
            conn.shutdown(rdwr)
            conn.close()
            continue
        except se:
            conn.shutdown(rdwr)
            conn.close()
            continue
        if len(data)>1:
            dstr=data.decode('utf-8')
            data=dstr.find('Passwd: ')
            if data>=0:
                try:
                    q=int(dstr[data+8:data+12])
                except:
                    print("BOT!")
                    conn.shutdown(rdwr)
                    conn.close()
                    continue
                try:
                    r=int(input('Enter the Key: '))
                except:
                    print('Invalid Input')
                    conn.shutdown(rdwr)
                    conn.close()
                    continue
                if q==r:
                    print('Keys Match!')
                    try:
                        cs(('Match: '+str(r)).encode('utf-8'))
                    except:
                        print('Early Disconnect!')
                        continue
                    ip=addr[0]
                    try:
                        conn.shutdown(rdwr)
                        conn.close()
                    except:
                        pass
                    break
                else:
                    print("KEYS DO NOT MATCH!")
                    conn.shutdown(rdwr)
                    conn.close()
                    continue
            else:
                print("BOT!")
                conn.shutdown(rdwr)
                conn.close()
                continue
        else:
            print("BOT!")
            conn.shutdown(rdwr)
            conn.close()
            continue
    #Recieving Pairing Request was successful, now off to pairing land
    ts(2.0)
    s.close()
    return ip

def start_video():
    proc=subprocess.Popen(['gst-launch-1.0 -v nvcompositor name=comp sink_0::alpha=1.0 sink_1::alpha=0.5 ! nvjpegenc idct-method=1 quality=50 ! queue max-size-bytes=5242880 max-size-buffers=3 min-threshold-buffers=1 leaky=2 ! multipartmux ! tcpserversink buffers-max=3 sync=false host=0.0.0.0 port=8082 recover-policy=1 timeout=5000000000 \\ v4l2src device=/dev/video1 ! \'video/x-raw,width=640,height=480,framerate=15/1,format=YUY2\' ! comp. v4l2src device=/dev/video2 ! \'video/x-raw,width=640,height=480,framerate=15/1,format=RGB\' ! comp.'],shell=True)
    return proc

def stop_video(proc):
    proc.terminate()
    proc.kill()
    proc.communicate()

#NOW THE ACTUAL CODE
while True:
    ip=secure_connect(oip,port)

    #Initalisation of Camera
    proc=start_video()

    #Initalisation of Address
    print("READY!")
    addr=(ip,port)

    first=True
    redo=False
    giveat=tc()
    #Continuity Loop
    while True:
        conn=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP/IP Socket
        conn.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1) #Zero-Latency TCP
        ct=conn.settimeout

        if not redo:
            #Do Not Change Anything Below, All of this is Security
            print("Disconnected")
            print(tt())
            print(addr)

        #Give Up Handler
        if not first:
            if tc()-giveat>=giveup:
                print('Giving Up')
                stop_video(proc)
                break
        ct(0.1)
        #Ctrl-C Handler
        try:
            conn.connect(addr)
        except KeyboardInterrupt:
            if not redo:
                stop_video(proc)
            break
        except ste:
            conn.close()
            ts(0.1)
            redo=True
            continue
        except se:
            conn.close()
            ts(0.1)
            continue
        ct(tout)
        first=False
        redo=False
        
        print("Connected")
        print(tt())
        print(addr)
        ct(tout)
        #Do Not Change Anything Above
        
        #Header Communication with Client
        cs=conn.sendall #Connection Speedup
        cv=conn.recv #Connection Speed
        #Client Timeout Handler
        try:
            data=cv(buff)
        except ste:
            print("BOT!")
            conn.shutdown(rdwr)
            conn.close()
            giveat=tc()
            continue
        except se:
            conn.shutdown(rdwr)
            conn.close()
            giveat=tc()
            continue
        
        #Server Connection Failure Handler
        try:
            cs(b'Hello!') #Sending Hello
        except ste:
            print("BOT!")
            conn.shutdown(rdwr)
            conn.close()
            giveat=tc()
            continue
        except se:
            conn.shutdown(rdwr)
            conn.close()
            giveat=tc()
            continue

        if connectmyrio:
            #Connecting to Serial Here
            #Initalisation of TCP Socket Server
            rs=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP/IP Socket
            rs.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1) #Zero-Latency TCP
            #connect with robot
            rs.settimeout(tout)
            rs.connect((remhost,remport))
            rss=rs.sendall
        
        #Capture Loop
        while True:
            
            a=tc()#Start Time for Frame Limiting

            #Client Timeout Handler
            try:
                data=cv(buff)
            except ste:
                print("LATENCY!")
                conn.shutdown(rdwr)
                conn.close()
                giveat=tc()
                break
            except se:
                print("SOCKET ERROR!")
                conn.shutdown(rdwr)
                conn.close()
                giveat=tc()
                break
            except KeyboardInterrupt:
                conn.shutdown(rdwr)
                conn.close()
                giveat=tc()
                break

            #Data Interpreter
            if len(data)>=12:
                if connectmyrio:
                    try:
                        rss(data)
                    except KeyboardInterrupt:
                        conn.shutdown(rdwr)
                        conn.close()
                        giveat=tc()
                        break
                    except ste: #Handles Robot Comms Timeout
                        print("ROBOT LATENCY!")
                        conn.shutdown(rdwr)
                        conn.close()
                        stop_video(proc)
                        exit()
                    except se: #Handles Robot Comms Error
                        print("ROBOT SOCKET ERROR!")
                        conn.shutdown(rdwr)
                        conn.close()
                        stop_video(proc)
                        exit()
                pass
            
            #Sending Contents to Client
            try:
                cs(b'Ping!')
            except ste:
                print("LATENCY!")
                conn.shutdown(rdwr)
                conn.close()
                giveat=tc()
                break
            except se:
                print("SOCKET ERROR!")
                conn.shutdown(rdwr)
                conn.close()
                giveat=tc()
                break
            except KeyboardInterrupt:
                conn.shutdown(rdwr)
                conn.close()
                giveat=tc()
                break
                
            #frame rate limiter
            b=tc() #End Time for Frame Limiting
            c=b-a
            t=fps #seconds per frame
            if t-c>0.0:
                try:
                    ts(t-c) #delay remaining seconds
                except KeyboardInterrupt:
                    conn.shutdown(rdwr)
                    conn.close()
                    giveat=tc()
                    break
            elif c>t:
                #pass
                print(c)
                
    #End of Program (when Ctrl-C)
    conn.close()
    stop_video(proc)

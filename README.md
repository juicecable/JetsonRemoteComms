# JetsonRemoteComms
Reliable Long Distance, Low Latency Communication for the Jetson Nano, suitable for Remote Control

### Requirements:
- You need a Jetson Nano that connects to the internet, running linux
- You need Python 3.6 or higher
- You need to have a camera plugged into the Jetson Nano
- You need to have gstreamer installed

### Optional:
- A MyRio that is connected through wired internet link
- A remote control computer

### Usage First Run:
1. Make sure you comply with the liscence before modifying the code
2. If you do not have a MyRio connected via wired internet link
    1. Set connectmyrio=False
3. If you do have a MyRio connected via wired internet link
    1. Set connectmyrio=True
    2. Get the Static or Static DHCP IP Address of the MyRio's Wired Interface
    3. Get the Hosting Port of the running MyRio program
    4. Set remhost to the IP Address of the MyRio
    5. Set the remport to the port of the MyRio
4. If you have a camera that doesn't work with the current video configuration
    1. In the start_video function, modify the string to match the camera settings of your camera
    2. This can be found through v4l-ctl
5. You should start with the remaining values as supplied
6. Use ifconfig to get your current IP address
7. Use UFW to open the hosting port to TCP, which by default is TCP port 8081
    1. > sudo ufw allow 8081
8. Use UFW to open the video hosting port to TCP, which by default is TCP port 8082
    1. > sudo ufw allow 8082
9. Run robo.py using Python3
10. If you are going to connect with a client
    1. Enter your IP Address into the client's configuration
    2. Enter your hosting port into the client's configuraiton
    3. Enter your video hosting port into the respective client configuration file
    4. Configure the rest of the client as specified in the client documentation
    5. Run the client
    6. Copy the 4 digit random pairing code from the client to the terminal created by robo.py, and hit enter
    7. The program should be connected and running now if you entered the number correctly
    8. If you didn't then the server will say so, and you will have to go back to step 10. v.
    
### Usage:
1. Make sure you comply with the liscence before modifying the code
2. Use ifconfig to get your current IP address
3. Run robo.py using Python3
4. If you are going to connect with a client
    1. Enter your IP Address into the client's configuration, if it has changed
    2. Enter your video hosting port into the respective client configuration file
    3. Configure the rest of the client as specified in the client documentation
    4. Run the client
    5. Copy the 4 digit random pairing code from the client to the terminal created by robo.py, and hit enter
    6. The program should be connected and running now if you entered the number correctly
    7. If you didn't then the server will say so, and you will have to go back to step 4. iv.

# Socket Programming
This is a socket programming which can encode message on client side, send the encoded packet to server side and decode it.

## Steps to start client & server
1. Start 2 new terminal/cmd window and cd to the current directory

2. Start server in one window and obtain the server's IP address

3. Start client in another window and enter the server's IP address with -s/--server option

4. Start server socket:  
   ```
   python3 packet_receiver.py
   ```

5. Start client socket:  
    * Required command line argument:
      * -s/--server <server_ip>  
      ```
      python3 packet_sender.py -s 192.168.0.1
      ```
    * Optional command line arguments:  
      * -h: shows help  
      ```
      python3 packet_sender.py -h
      ```
      * -p <message>: start socket with sending a message  
      ```
      python3 packet_sender.py -s 192.168.0.1 -p “​COLOMBIA 2 - MESSI 0​”
      ```  
      
### Tested on MacOs Catalina - v10.15.5 with python 3.7.6

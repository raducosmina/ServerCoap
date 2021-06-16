import socket
from Message_Header import Message_Header
from Parse_Message_Service import Parse_Message_Service
import Defines as d
import Options as o
import logging
import time
import Inputs as input_city


UDP_IP = "127.0.0.1"
UDP_PORT = 5005
logging.basicConfig(filename='CLIENT.log',level=logging.DEBUG)

addr = (UDP_IP, UDP_PORT)
print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)

city_list = []
method_list = []
for i in range(1):
    city,method = input_city.inputs()
    city_list.append(city)
    method_list.append(method)
print("city_list:",city_list)
print("methood_list:",method_list)
index_method_list = 0


a = 0
for i in method_list:
    if i == 1:
        a = int(d.TYPE_CON)
    elif i == 2:
        a = int(d.TYPE_NON)
    elif i == 6:
        a = int(d.TYPE_CON)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
for oras in city_list:
# construim pachetul pe care il trimitem la server
    buildMsg = Message_Header()
    msg = buildMsg.BuildMessage(d.COAP_VERSION, a, d.COAP_CLASS_METHODS,method_list[index_method_list],d.newMessageId(), d.newToken())
    index_method_list +=1
    #buildMsg.Print()
    msg_string = "" # msg to string pt encode
    for x in msg:
        msg_string += str(x)+'/' # fiecare element din lista il facem string si este concatenat la msg_string
    m_package = buildMsg.package(msg_string,oras)
    
    #trimit pachet de la client la server

    sock.sendto(m_package.encode("utf-8"), addr)
    
    
    #aici e pachetul primit de la server

    data, addr = sock.recvfrom(1024)
    data_decode = data.decode("utf-8")
    
    logging.info("data_decode from server TYPE/CON/CLASS/CODE/MID/TOKEN/ ")
    logging.info(data_decode)
    
    
    message_list = list(data_decode.split("/"))
    
    parsed_message = Parse_Message_Service()
    msg_parsed = parsed_message.Parse(data_decode)
    
    logging.info("Mesaj parsat de la server:")
    logging.info(msg_parsed.Print())
    date_api = list(msg_parsed.payload.split("-"))
    #aici primim date legate de vreme
    
    print("Data primita este", msg_parsed.payload)
    time.sleep(2)
# Inchide conexiune
sock.close()



print("PRESS CTRL-C TO EXIT THE PROG...")
try:
    while True:
        pass
except KeyboardInterrupt:
    print ("Exiting")
    exit(0)







import socket
from Get_Weather_Data import Get_Weather_Data
from Parse_Message_Service import Parse_Message_Service
import Package as Pack
import Defines as d
import  threading
import logging



logging.basicConfig(filename='SERVER.log',level=logging.DEBUG)


UDP_IP = "127.0.0.1"
UDP_PORT = 5005

class Broker():
    def __init__(self):
        logging.info('Initializing class Broker')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        self.sock.bind((UDP_IP, UDP_PORT))
        self.clients_list = []
        request = 0
        OK = 200
        ERROR = 404

    def listen_clients(self):
        while True:
        
            #primesc locatia de la client(pachet)
            
            data, addr = self.sock.recvfrom(1024) # buffer size is 1024 bytes
            print("received ", len(data), "bytes from ", addr)
            
            if data:
                data_decode = data.decode("utf-8")
                logging.info("data_decode from client VERSION/TYPE/CON/CLASS/CODE/MID/TOKEN/PAYLOAD ")
                logging.info(data_decode)
                #aici e pachetul de la client pe care il parsez
                parsed_message_locatie = Parse_Message_Service()
                
                
                # parsez pachetul cu payload-ul locatie
                msg_parsed_locatie = parsed_message_locatie.Parse(data_decode)
               
               
                msg_parsed_locatie.Print()
                logging.info(" ")
                
                
               
                t = threading.Thread(target=self.talkToClient, args=(addr, msg_parsed_locatie))
                
                #start threading
                
                t.start()
                logging.info("")

    def talkToClient(self,addr, msg_parsed_locatie):
        # testez versiunea
        
        #tratare metoda 0.0
        
        #print(msg_parsed_locatie)
        
        if msg_parsed_locatie.payload == "":
        
            m = Pack.Pack(msg_parsed_locatie,"", d.TYPE_ACK, d.COAP_CLASS_METHODS, d.METHOD_EMPTY)
            logging.info("0.0 Empty Method // 200 OK")
            request = 200 
            message_sent = ""
            self.sock.sendto(m.encode("utf-8"), addr)
            print(m)
        else:
            if int(msg_parsed_locatie.VERSION) != d.COAP_VERSION:
                logging.info("Client has wrong version. It must be 1!")

            # testez type
            msg_type = 0
            if int(msg_parsed_locatie.TYPE) == d.TYPE_CON:
                msg_type = d.TYPE_ACK
                
            elif int(msg_parsed_locatie.TYPE) == d.TYPE_NON:
                msg_type = d.TYPE_NON
                
            else:
                logging.info("TYPE error:must be CON/NON")
                
                
               
            #0.1

            if int(msg_parsed_locatie.CLASS) == d.COAP_CLASS_METHODS and int(msg_parsed_locatie.CODE) == d.METHOD_GET:
                #if class.code=0.1 --> facem GET
                
                #2.05 content
                msg_class = d.COAP_CLASS_SUCCESS 
                msg_code = d.CODE_CONTENT

                # obtinem data despre vreme
                App = Get_Weather_Data()
                code, info_weather = App.get_data(msg_parsed_locatie.payload, msg_parsed_locatie.CODE)
                
                list_info_w =  list(info_weather.split("-"))
                print("aici trimit!:", list_info_w)
                
                if code == 200:
                    m = Pack.Pack(msg_parsed_locatie, info_weather, msg_type, msg_class, msg_code)
                    self.sock.sendto(m.encode("utf-8"), addr)
                    logging.info("GET // 200 OK")
                    
                else:
                    logging.info("ERROR: Can not make request from API!")
                    request = 404
                    m = Pack.Pack(msg_parsed_locatie,"4.04:city NOT FOUND", msg_type, d.COAP_CLASS_ERROR, d.CODE_CHANGED)
                    logging.info("GET ERROR 404 NOT FOUND")
                    self.sock.sendto(m.encode("utf-8"), addr)
                    
                    

            elif int(msg_parsed_locatie.CODE) == d.METHOD_POST:
            #metoda este post
            
                App = Get_Weather_Data()
                # print("msg_parsed:",msg_parsed_locatie.payload)
                
                if msg_parsed_locatie.payload == 0:
                    print("payload null")
                    
                    
                code, info_weather = App.get_data(msg_parsed_locatie.payload, msg_parsed_locatie.CODE)
                
                print("aici trimit!:", info_weather)
                
                list_info_w =  list(info_weather.split("-"))
                temp_update = str( round(float(list_info_w[0]) - 273.15, 2))
                
                #stocam datele cu orasul: temperatura
                #cand se face post, se cauta in lista orasul
                #exista? faci update
                #nu exista? faci create

                f = open("city_list_POST.txt", "r")
                contents = f.read()
                contents_list= list(contents.split("  "))
                print(contents_list)
                
                

                index = 0
                if msg_parsed_locatie.payload in contents:
                    for item in contents_list:
                        if msg_parsed_locatie.payload in item:
                        
                            item_list = list(item.split(":"))
                            item_list[1] =':'+ temp_update
                            print("item_list[1]:",item_list[1])
                            item = ''.join(item_list)
                            print("item:",item)
                            contents_list[index] = item
                        index += 1
                    
                        
                    print("content_list:",contents_list)
                    f = open("city_list_POST.txt", "w")
                    update_list = ""
                    
                    for i in contents_list:
                        update_list+= str(i)+"  "
                    f.write(update_list)
                    
                    logging.info("POST // 2.04 CHANGED")
                    
                else:
                
                    f = open("city_list_POST.txt","a")
                    city_temp = ""
                    city_temp += msg_parsed_locatie.payload  + ":" + temp_update+"  "
                    print("info_weather:",list_info_w)
                    f.write(city_temp)
                    
                    logging.info("POST // 2.01 CREATED")
               
            #metoda aleasa de noi o sa fie CONVERT

            elif  int(msg_parsed_locatie.CODE) == d.METHOD_CONVERT:
            
                msg_class = d.COAP_CLASS_SUCCESS
                msg_code = d.CODE_CHANGED
                App = Get_Weather_Data()

                if msg_parsed_locatie.payload == 0:
                    print("payload null")
                    
                    
                code, info_weather = App.get_data(msg_parsed_locatie.payload, msg_parsed_locatie.CODE)
                print("aici trimit!:", info_weather)
                
                if code == 200:
                    m = Pack.Pack(msg_parsed_locatie,info_weather,msg_type,msg_class,msg_code)
                    self.sock.sendto(m.encode("utf-8"), addr)
                else:
                    msg_type = d.TYPE_ACK
                    msg_class = d.COAP_CLASS_ERROR
                    msg_code = d.CODE_CHANGED
                    m = Pack.Pack(msg_parsed_locatie,"",msg_type,msg_class,msg_code)
                    self.sock.sendto(m.encode("utf-8"), addr)
                    logging.info("ERROR: Can not make request from API!")
                logging.info("CONVERT // 200 OK")
                    
        request = 200                   
            



b = Broker()
b.listen_clients()





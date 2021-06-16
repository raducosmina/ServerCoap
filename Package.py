from Message_Header import Message_Header
import Defines as d



def Pack(msg_parsed_locatie,info_to_client,msg_type,msg_class,msg_code):
    buildMsg = Message_Header() 
    # construim pachetul 
    msg = buildMsg.BuildMessage(d.COAP_VERSION,msg_type,msg_class,msg_code,int(msg_parsed_locatie.MESSAGE_ID), int(msg_parsed_locatie.token))
    msg_string = ""  # msg to string pt encode
    for x in msg:
        msg_string += str(x) + '/'
    m = buildMsg.package(msg_string,info_to_client)
    return m

from Message_Header import Message_Header

class Parse_Message_Service():
    def __init__(self):
        pass

    def Parse(self,BinaryString):
        message_list = list(BinaryString.split("/"))
        message_header = Message_Header()
        message_header.VERSION = message_list[0]
        message_header.TYPE = message_list[1]
        message_header.TOKEN_LENGTH = message_list[2]
        message_header.CLASS = message_list[3]
        message_header.CODE = message_list[4]
        message_header.MESSAGE_ID = message_list[5]

        if message_header.TOKEN_LENGTH:
            message_header.token = message_list[6]
        else:
            message_header.token = None
        payload_code = message_list[7]
        message_header.payload = payload_code[3:]
        return message_header



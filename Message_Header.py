'''
        0                   1                   2                   3
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |Ver| T |  TKL  |      Code     |          Message ID           |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |   Token (if any, TKL bytes) ...
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |   Options (if any) ...
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |1 1 1 1 1 1 1 1|    Payload (if any) ...
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

   Request/Response Code (8 bits)
0	1	2	3	4	5	6	7
 Class  |	      Code

 COAP_MESSAGE_FORMAT

HEADERUL FORMAT DIN :
1. VERSIUNEA: 2 BITI
2. MESSAGE-TYPE : 2 BITI
3. TOKENLENGTH:4 bit
4. CODE: -code class -3 biti
        -code response -5 biti
        CODE RESPONSE (8 bit)
5. MESSAGE_Id : 16 bit!

EMPTY = <Code 0 “EMPTY”>
GET = <Request Code 1 “GET”>
POST = <Request Code 2 “POST”>
PUT = <Request Code 3 “PUT”>
DELETE = <Request Code 4 “DELETE”>

    Version (VER) (2 bits)
Indicates the CoAP version number.

    Type (2 bits)
This describes the datagram's message type for the two message type context of Request and Response.
Request
0 : Confirmable : This message expects a corresponding Acknowledgement message.
1 : Non-confirmable : This message does not expect a confirmation message.
Response
2 : Acknowledgement : This message is a response that acknowledge a confirmable message
3 : Reset : This message indicates that it had received a message but could not process it.
'''
import Defines as d


class Message_Header():
    def __init__(self):
        self.VERSION = 0
        self.TYPE = 0
        self.token=0
        self.CLASS=0

        self.CODE=0
        self.MESSAGE_ID=0
        self.options = []
        self.payload = ''
        message = ""

    def BuildMessage(self, VERSION, TYPE, CLASS, CODE, MESSAGE_ID,token,options=[]):
        # formatam elementele din header setandu-le dimensiunea
       
        self.VERSION = format(VERSION, '02b')
        self.TYPE = format(TYPE,'02b')
        self.CLASS = format(CLASS, '03b')
        self.CODE = format(CODE, '05b')
        self.MESSAGE_ID = format(MESSAGE_ID, '016b')
        self.TYPE = TYPE
        self.CODE = CODE
        self.token = token
        self.options = options
       # self.payload = payload

        TKL = 0 #bytes
        if token:
            # determine token length
            for tokenLen in range(1, 8 + 1):
                if token < (1 << (8 * tokenLen)):
                    TKL = tokenLen
                    break
            if not TKL:
                raise ('token too long')

        message  = []
        #header
        
        message += [VERSION]
        message += [TYPE]
        message += [TKL]
        message += [CLASS]
        message +=[CODE]
        message += [MESSAGE_ID]
        message += d.int2buf(token,TKL)

       
        message += d.encodeOptions(options)
       
        return message



    def package(self,header,oras):
        pack = ""
        pack += header+ str(d.COAP_PAYLOAD_MARKER) + oras
        return pack

    def getVERSION(self):
        return int(str(self.VERSION),2)
    def getType(self):
        return  self.TYPE#int(str(self.TYPE))
    def getCLass(self):
        return int(str(self.CLASS))
    def getCode(self):
        return self.CODE

    def getMessageId(self):
        return int(str(self.MESSAGE_ID))
    def getToken(self):
        return int(str(self.token))
    def getOptions(self):
        return d.buf2int(self.options)
    def getPayload(self):
        return self.payload

    def Print(self):
        print("\n We are printing the message format....")
        print("\n VERSION: "+ str(self.getVERSION()))
        print("\n TYPE: "+str(self.getType()))
        print("\n CLASS.CODE: "+ (str(self.getCLass())+"."+str(self.getCode())))
        #FOLOSIM MESSAGE ID PENTRU A GASI DUPLICATELE
        #MATCH MESSAGES OF TYPE ACK/RST
        #RESPONSE MESSAGES WILL HAVE THE SAME MESSAGE ID
        print("\n MESSAGE ID: " +str(self.getMessageId()))
        print("\n token: " + str(self.getToken()))
        print("\n options: " + str(self.getOptions()))


'''
The entire code is typically communicated in the form class.code .
Method: 0.XX EMPTY , GET ,POST
Success: 2.XX Created,Deleted,Valid,Changed,Content,Continue
Client Error: 4.XX
Bad Request, Unauthorized, Bad Option, Forbidden ,Not Found, Method Not Allowed, Not Acceptable

Server Error: 5.XX
Internal Server Error,Not Implemented,Bad Gateway,Service Unavailable,Gateway Timeout,Proxying Not Supported
Signaling Codes: 7.XX Unassigned,CSM,Ping,Pong,Release,Abort


EMPTY = <Code 0 “EMPTY”>
GET = <Request Code 1 “GET”>
POST = <Request Code 2 “POST”>
PUT = <Request Code 3 “PUT”>
DELETE = <Request Code 4 “DELETE”>
FETCH = <Request Code 5 “FETCH”>
PATCH = <Request Code 6 “PATCH”>
iPATCH = <Request Code 7 “iPATCH”>
CREATED = <Successful Response Code 65 “2.01 Created”>
DELETED = <Successful Response Code 66 “2.02 Deleted”>
VALID = <Successful Response Code 67 “2.03 Valid”>
CHANGED = <Successful Response Code 68 “2.04 Changed”>

"""
    
"""


'''








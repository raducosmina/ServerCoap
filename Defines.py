COAP_PAYLOAD_MARKER                    = 0xff


COAP_VERSION =                           1
# CoAP Message Types
TYPE_CON                               = 0
TYPE_NON                               = 1
TYPE_ACK                               = 2
TYPE_RST                               = 3

# CoAP Method Codes
METHOD_EMPTY                           = 0
METHOD_GET                             = 1
METHOD_POST                            = 2
METHOD_PUT                             = 3
METHOD_DELETE                          = 4
METHOD_CONVERT                         = 6

CODE_CONTENT                           = 5
CODE_CHANGED                           = 4

COAP_CLASS_METHODS  = 0
COAP_CLASS_SUCCESS  = 2
COAP_CLASS_ERROR    = 4


# CoAP Option Number Registry
OPTION_NUM_IFMATCH                     = 1
OPTION_NUM_URIHOST                     = 6
OPTION_NUM_ETAG                        = 4

# CoAP Response Codes

COAP_RC_ALL =       0

import Options as o


def int2buf(val,length):
    returnVal  = []
    for i in range(length,0,-1):
        returnVal += [val>>(8*(i-1))&0xff]
    return returnVal

def buf2int(buf):
    returnVal  = 0
    for i in range(len(buf)):
        returnVal += buf[i]<<(8*(len(buf)-1-i))
    return returnVal

def encodeOptions(options, lastOptionNum = 0):
    encoded = []
    for option in options:
        assert option.optionNumber >= lastOptionNum
        encoded += option.toBytes(lastOptionNum)
        lastOptionNum = option.optionNumber
    return encoded


def encodePayload(payload):
    encoded = []
    if payload:
        encoded += [COAP_PAYLOAD_MARKER]
        encoded += payload
    return encoded


def decodeOptionsAndPayload(rawbytes, currentOptionNumber = 0):
    options = []
    while True:
        (option,rawbytes) = o.parseOption(rawbytes, currentOptionNumber)
        if not option:
            break
        options += [option]
        currentOptionNumber  = option.optionNumber
    return (options, rawbytes)

import random
def newMessageId ():
    return random.randint(0x0000,0xffff)
def newToken():
    return random.randint(0x00,0xff)

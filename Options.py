import Defines as d

"""""
Option Format
Bit Positions
0	1	2	3	4	5	6	7
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
Option Delta	Option Length
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
Option Delta Extended (None, 8bit, 16bits)
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
Option Length Extended (None, 8bit, 16bits)
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
Option Value
"""

class coapOption(object):
    def __init__(self, optionNumber, oscoapClass=None):
        # store params
        self.optionNumber = optionNumber
        self.oscoapClass = oscoapClass
        self.length = 0

    def getPayloadBytes(self):
        raise NotImplementedError()

    def toBytes(self, lastOptionNum):
        payload = self.getPayloadBytes()
        delta = self.optionNumber - lastOptionNum

        # optionDelta and optionDeltaExt fields
        if delta <= 12: #  between 0 to 12
            optionDelta = delta
            print('optionDelta ',optionDelta)
            optionDeltaExt = d.int2buf(delta, 0)
        elif delta <= (0xff + 13): #  from 13 to 268
            optionDelta = 13
            optionDeltaExt = d.int2buf(delta - 13, 1) # Option Delta Extended is 8bit that is the Option Delta value minus 13
        elif delta <= (0xffff + 269): # from 269 to 65,804
            optionDelta = 14
            optionDeltaExt = d.int2buf(delta - 269, 2) # Option Delta Extended is 16bit that is the Option Delta value minus 269
        else:
            raise ('delta is too large: {0}'.format(delta))

        # optionLength and optionLengthExt fields
        if len(payload) <= 12:
            optionLength = len(payload)
            optionLengthExt = d.int2buf(len(payload), 0)
        elif len(payload) <= (0xff + 13):
            optionLength = 13
            optionLengthExt = d.int2buf(len(payload) - 13, 1)
        elif len(payload) <= (0xffff + 269):
            optionLength = 14
            optionLengthExt = d.int2buf(len(payload) - 269, 2)
        else:
            raise ('payload is too long')

        returnVal = []
        returnVal += [optionDelta << 4 | optionLength]
        returnVal += optionDeltaExt
        returnVal += optionLengthExt
        returnVal += payload

        return returnVal


#=== OPTION_NUM_URIHOST

class UriHost(coapOption):
    def __init__(self, host):
        # initialize parent
        coapOption.__init__(self, d.OPTION_NUM_URIHOST)

        # store params
        self.host = host

    def __repr__(self):
        return 'UriHost(host={0})'.format(self.host)

    def getPayloadBytes(self):
        return [ord(b) for b in self.host]


def parseOption(message, prevOpNr):
    if len(message)==0:
        message = message[1:]
        return (None,message)

    if message[0]==d.COAP_PAYLOAD_MARKER:
        message = message[1:]
        return (None,message)

    #header
    optionDelta = (message[0] >> 4)&0x0f
    optionLength = (message[0] >> 0)&0x0f
    message = message[1:]

    #optionDelta
    if optionDelta <= 12:
        pass
    elif optionDelta == 13:
        optionDelta = d.buf2int(message[0:1])+13
        message = message[1:]
    elif optionDelta == 14:
        optionDelta = d.buf2int(message[0:2])+269
        message = message[2:]
    else:
        raise ('Invalid')

        # optionLength
    if optionLength <= 12:
        pass
    elif optionLength == 13:
        optionLength = d.buf2int(message[0:1]) + 13
        message = message[1:]
    elif optionLength == 14:
        optionLength = d.buf2int(message[0:2]) + 269
        message = message[2:]
    else:
        raise ('invalid optionLength')

    # optionValue
    if len(message) < optionLength:
        raise ('message too short')
    optionValue = message[:optionLength]
    message = message[optionLength:]

    # ===== create option
    optionNumber = prevOpNr + optionDelta
    print('optionNumber ',optionDelta)
    if optionNumber not in d.OPTION_NUM_ALL:
        raise ('invalid option number')

    if optionNumber == d.OPTION_NUM_URIHOST:
        option = UriHost(host=''.join([chr(b) for b in optionValue]))
    print('aici')
    return (option, message)




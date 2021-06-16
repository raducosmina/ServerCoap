import Defines as d

def inputs():
    oras = input("\nintrodu numele orasului: ")
    oras = oras.replace(" ", "+")  # pentru orase formate din mai multe cuvinte

    method = input(" Alege o metoda: GET-1  POST-2  CONVERT-3:")
    met_request = 0
    if int(method) == 1:
        met_request = d.METHOD_GET
    elif int(method) == 2:
        met_request = d.METHOD_POST
    elif int(method) == 3:
        met_request = d.METHOD_CONVERT
    return oras,met_request

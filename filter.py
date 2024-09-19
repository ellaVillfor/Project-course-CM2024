#A EWMA filter funqtion syntax name_name()

def ewma_filter(values):
    alfa = 0.5
    ewmaOutOld = 0 
    ewmaOut = [None]
    for i in values:
        ewmaOut.append(ewmaOutOld * alfa + values[i] * (1-alfa)) 
        ewmaOutOld = ewmaOut[i]


    
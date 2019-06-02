a = {'God genius spot': 'fuckoff12345', 'Telekom_FON': None, '#HIAQatar Complimentary Wi-Fi': None, 'Burrawang Free Wi-Fi': None, "JKookStudios' Hotspot": 'unodapassword', 'Orana Wireless': None, 'Eloise phone': 'EloiseAnne88', 'Dumb_Telstra0806': '9353095401', 'Telstra0806_2GEXT': '9353095401', 'Oaks Public Wireless': None, 'TelstraAD0429': 'txg3jpsgzk', 'FRITZ!Box 7490': '03183182820227776237'}



max_len = max(max(len(str(x)),len(str(a[x]))) for x in a)+1
b = [(i+(" "*(max_len-len(i))), str(a[i]).replace("None", "")+(" "*(max_len-len(str(a[i]))))) for i in a]
out = "\n".join(i[0]+i[1] for i in b)

print(out)

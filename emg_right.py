import pandas as pd                  #import pandas-libary to prosess data in tabells
import matplotlib.pyplot as plt      #import matplotlib to create graphs

# Read the data (via path)
#file_path = "C:\\Användare\\Saffie\\Dokument\\emg_right.py"

file_path = "C:\\Users\\DittNamn\\Documents\\filnamn.txt"

# Öppna filen i läsläge ('r')
with open(file_path, 'r') as file:
    content = file.read()  # Läs innehållet i filen
    print(content)  # Skriv ut filens innehåll till terminalen

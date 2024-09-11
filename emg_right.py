import pandas as pd                  #import pandas-libary to prosess data in tabells
import matplotlib.pyplot as plt      #import matplotlib to create graphs

# Read the data (via path)
#file_path = "C:\\Användare\\Saffie\\Dokument\\emg_right.py"

#file_path = "C:\\Användare\\Saffie\\Dokument\\OpenSignals (r)evolution\\files\\punches\\opensignals_0007804b3c23_2024-09-09_15-04-53.txt"
file_path = "C:\\Skrivbord\\opensignals_0007804b3c23_2024-09-09_15-04-53.txt"
# Öppna filen i läsläge ('r')
with open(file_path, 'r') as file:
    content = file.read()  # Läs innehållet i filen
    print(content)  # Skriv ut filens innehåll till terminalen

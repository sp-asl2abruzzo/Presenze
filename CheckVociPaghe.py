import csv
import json
from datetime import datetime
import tkinter as tk
from tkinter import filedialog

# Function to convert a CSV to JSON
# Takes the file paths as arguments

def make_json(fileTimbrature, fileDestinazioneOutput):

    # create a dictionary
    data = []
    output = {}
    alphabet = {
    'A-C': ('A', 'B', 'C'),
    'D-D': ('D',),
    'E-L': ('E', 'F', 'G', 'H', 'I', 'J', 'K', 'L'),
    'M-R': ('M', 'N', 'O', 'P', 'Q', 'R'),
    'S-Z': ('S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z')
}
    
    # Open a csv reader called DictReader
    with open(fileTimbrature, encoding='latin-1') as file:  
        csvReader = csv.DictReader(file, delimiter=',')    
        for row in csvReader:
            data.append(row)
        
    # print(giustificativi)
    for index,row in enumerate(data):
        firstLetter = row["Nominativo"][0].upper()        
        if firstLetter in output:
            if "totali" in output[firstLetter]:
                output[firstLetter]["totali"]+=1
            else:
                output[firstLetter]["totali"]=1

            if row["Voce Variabile"] in output[firstLetter]:
                output[firstLetter][row["Voce Variabile"]]+=1
            else:
                output[firstLetter][row["Voce Variabile"]]=0
        else:
            output[firstLetter] = {"totali": 1, row["Voce Variabile"]: 1}
        
    
    print(output)

    # Dizionario per la somma degli intervalli
    output_intervalli = {}

    # Itera sugli intervalli di iniziali
    for intervallo, iniziali in alphabet.items():
        output_intervalli[intervallo] = {"totali": 0}
        
        # Itera sul dizionario aggregato e somma i valori per le iniziali nell'intervallo corrente
        for chiave_aggregata, valori_aggregati in output.items():
            if any(iniziale in iniziali for iniziale in chiave_aggregata.split('-')):
                for chiave, valore in valori_aggregati.items():
                        output_intervalli[intervallo].setdefault(chiave, 0)
                        output_intervalli[intervallo][chiave] += valore

    with open(fileDestinazioneOutput+'.json', 'w') as json_file:
        json.dump(output, json_file, indent=2)

    with open(fileDestinazioneOutput+'_intervallo.json', 'w') as json_file:
        json.dump(output_intervalli, json_file, indent=2)

    
    
    # for row in outputSenzaGiustificativi:
    #     export.append({"MATRICOLA":row["MATRICOLA"],"CAUSALE":"TFL","DATA_INIZIO (gg/mm/aaaa)":row["GIORNO"],"DATA_FINE (gg/mm/aaaa)":row["GIORNO"],"TIPO_INSERIMENTO":"I","ORA_INIZIO (hh:mm)":"","ORA_FINE (hh:mm)":"","DURATA (hh:mm)":"","FAMILIARE":"","NOTA_INFORMATIVA":"TFLAUTO","FORZATURA_INSERIMENTO":"S"})
    
    # with open(fileDestinazioneOutput+'.csv', 'w',newline='') as f:
    #     writer = csv.DictWriter(f, fieldnames=outputSenzaGiustificativi[0].keys())
    #     writer.writeheader()
    #     writer.writerows(outputSenzaGiustificativi)

    print("COMPLETATO!")

# Function to handle the button click and call make_json
def process_files():
    file_timbrature = file_timbrature_entry.get()
    file_destinazione_output = file_destinazione_output_entry.get()

    make_json(file_timbrature, file_destinazione_output)

# Funzione per sfogliare un file e aggiornare il widget di inserimento corrispondente
def browse_file(entry_widget):
    file_path = filedialog.askopenfilename()
    entry_widget.delete(0, tk.END)
    entry_widget.insert(0, file_path)

# Creare la finestra principale della GUI
root = tk.Tk()
root.title("Check Voci Paghe")

# Creare e posizionare i widget di inserimento per i percorsi dei file
file_timbrature_entry = tk.Entry(root, width=50)
file_destinazione_output_entry = tk.Entry(root, width=50)

file_timbrature_entry.grid(row=0, column=1, padx=10, pady=5)
file_destinazione_output_entry.grid(row=2, column=1, padx=10, pady=5)

# Creare e posizionare le etichette per i widget di inserimento
tk.Label(root, text="File Timbrature:").grid(row=0, column=0, padx=10, pady=5)
tk.Label(root, text="Nome del File di Destinazione:").grid(row=2, column=0, padx=10, pady=5)

# Creare e posizionare i pulsanti di navigazione
tk.Button(root, text="Sfoglia", command=lambda: browse_file(file_timbrature_entry)).grid(row=0, column=2, pady=5)

# Creare e posizionare il pulsante Converti
tk.Button(root, text="Check", command=process_files).grid(row=20, column=0, columnspan=3, pady=10)

# Esegui la GUI
root.mainloop()
import csv
import json
from datetime import datetime
import tkinter as tk
from tkinter import filedialog

# Function to convert a CSV to JSON
# Takes the file paths as arguments

def make_json(fileTimbrature, fileGiustificativi, fileDestinazioneOutput, giorni_festivi):

    # create a dictionary
    data = []
    output = []
    giustificativi = []
    export = []

    # Open a csv reader called DictReader
    with open(fileTimbrature, encoding='latin-1') as file:  
        csvReader = csv.DictReader(file, delimiter=',')    
        for row in csvReader:
            data.append(row)


    with open(fileGiustificativi, encoding='latin-1') as file2:   
        csvReader = csv.DictReader(file2, delimiter=',')    
        for row in csvReader:
            giustificativi.append(row)
        
    # print(giustificativi)
    for index,row in enumerate(data):
        if (row["RUO"] == "ORTONA1" or row["RUO"] == "CHIETI2") and (row["QUALIFICA"]=="Dirigente Medico" or row["QUALIFICA"]=="Biologo Dirigente" or row["QUALIFICA"]=="Psicologo Dirigente" or row["QUALIFICA"]=="Farmacista Dirigente" or row["QUALIFICA"]=="Dirigente Fisico") and (any(row["GIORNO"]==x for x in giorni_festivi)) and (row["CAUSALE"]=="" or row["CAUSALE"]=="09"):
            print(index)
            if row["VERSO"]=="U":
                row["Turno"]="Monto"
                output.append(row)
            if row["VERSO"]=="E":
                t1 = datetime.strptime(row["ORA"],"%H:%M")
                res = [x for x in data if (x["MATRICOLA"]==row["MATRICOLA"] and x["VERSO"]=="U" and row["GIORNO"]==x["GIORNO"])]
                if len(res)>0:
                    t2 = datetime.strptime(res[0]["ORA"],"%H:%M")
                    delta=(t2-t1).total_seconds()/60
                    data.remove(res[0])
                    # print(row["MATRICOLA"]+str(t2)+'-'+str(t1)+'='+str(delta))
                    if delta<190:
                        print(row)
                        print(str(t2)+"-"+str(t1)+"="+str(delta))

                    else:
                        row["Turno"]=delta/60
                        output.append(row)
                    res.clear()
                    
                else: 
                    # print("SMONTO")
                    row["Turno"]="Smonto"
                    output.append(row)
                    res.clear()

    
    outputSenzaGiustificativi = [el for el in output if (not any((el["MATRICOLA"] == x["Matricola"] and el["GIORNO"]==x["Data Inizio"]) for x in giustificativi))]
    # with open(fileDestinazioneOutput+".json", 'w') as f:
    #     json.dump(o, f)

    for row in outputSenzaGiustificativi:
        export.append({"MATRICOLA":row["MATRICOLA"],"CAUSALE":"TFL","DATA_INIZIO (gg/mm/aaaa)":row["GIORNO"],"DATA_FINE (gg/mm/aaaa)":row["GIORNO"],"TIPO_INSERIMENTO":"I","ORA_INIZIO (hh:mm)":"","ORA_FINE (hh:mm)":"","DURATA (hh:mm)":"","FAMILIARE":"","NOTA_INFORMATIVA":"TFLAUTO","FORZATURA_INSERIMENTO":"S"})
    
    with open(fileDestinazioneOutput+'.csv', 'w',newline='') as f:
        writer = csv.DictWriter(f, fieldnames=outputSenzaGiustificativi[0].keys())
        writer.writeheader()
        writer.writerows(outputSenzaGiustificativi)

    with open('export_'+fileDestinazioneOutput+'.csv', 'w',newline='') as f:
        writer = csv.DictWriter(f, fieldnames=export[0].keys())
        writer.writeheader()
        writer.writerows(export)
    print("COMPLETATO!")

# Function to handle the button click and call make_json
def process_files():
    file_timbrature = file_timbrature_entry.get()
    file_giustificativi = file_giustificativi_entry.get()
    file_destinazione_output = file_destinazione_output_entry.get()
    giorni_festivi = [
       date_entries['g1'].get(),
        date_entries['g2'].get(),
        date_entries['g3'].get(),
        date_entries['g4'].get(),
        date_entries['g5'].get(),
        date_entries['g6'].get(),
        date_entries['g7'].get(),
        date_entries['g8'].get(),
        date_entries['g9'].get(),
        date_entries['g10'].get(),
        date_entries['g11'].get(),
        date_entries['g12'].get(),
        date_entries['g13'].get(),
        date_entries['g14'].get(),
        date_entries['g15'].get()
    ]

    make_json(file_timbrature, file_giustificativi, file_destinazione_output, giorni_festivi)

# Funzione per sfogliare un file e aggiornare il widget di inserimento corrispondente
def browse_file(entry_widget):
    file_path = filedialog.askopenfilename()
    entry_widget.delete(0, tk.END)
    entry_widget.insert(0, file_path)

# Creare la finestra principale della GUI
root = tk.Tk()
root.title("TFLAUTO")

# Creare e posizionare i widget di inserimento per i percorsi dei file
file_timbrature_entry = tk.Entry(root, width=50)
file_giustificativi_entry = tk.Entry(root, width=50)
file_destinazione_output_entry = tk.Entry(root, width=50)

file_timbrature_entry.grid(row=0, column=1, padx=10, pady=5)
file_giustificativi_entry.grid(row=1, column=1, padx=10, pady=5)
file_destinazione_output_entry.grid(row=2, column=1, padx=10, pady=5)

# Creare e posizionare le etichette per i widget di inserimento
tk.Label(root, text="File Timbrature:").grid(row=0, column=0, padx=10, pady=5)
tk.Label(root, text="File Giustificativi:").grid(row=1, column=0, padx=10, pady=5)
tk.Label(root, text="Nome del File di Destinazione:").grid(row=2, column=0, padx=10, pady=5)

# Creare campi di input per le date
date_entries = {}
for i, giorno in enumerate(['g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'g7', 'g8', 'g9', 'g10', 'g11', 'g12', 'g13', 'g14', 'g15']):
    tk.Label(root, text=f"{giorno}:").grid(row=i+3, column=0, padx=10, pady=5)
    date_entries[giorno] = tk.Entry(root, width=10)
    date_entries[giorno].grid(row=i+3, column=1, padx=10, pady=5)

# Creare e posizionare i pulsanti di navigazione
tk.Button(root, text="Sfoglia", command=lambda: browse_file(file_timbrature_entry)).grid(row=0, column=2, pady=5)
tk.Button(root, text="Sfoglia", command=lambda: browse_file(file_giustificativi_entry)).grid(row=1, column=2, pady=5)

# Creare e posizionare il pulsante Converti
tk.Button(root, text="Converti", command=process_files).grid(row=20, column=0, columnspan=3, pady=10)

# Esegui la GUI
root.mainloop()
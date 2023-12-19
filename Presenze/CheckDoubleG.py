import csv
import tkinter as tk
from tkinter import filedialog

# Function to convert a CSV to JSON
# Takes the file paths as arguments

def make_json(fileAssenze, fileDestinazioneOutput):

    # create a dictionary
    data = []
    output = []
  
    # Open a csv reader called DictReader
    with open(fileAssenze, encoding='latin-1') as file:  
        csvReader = csv.DictReader(file, delimiter=',')    
        for row in csvReader:
            data.append(row)

    for row in data:
        for el in data:
            if el["Matricola"]==row["Matricola"] and el["Data Inizio"]==row["Data Inizio"] and el["Causale"]!=row["Causale"]:
                output.append(row); 

    with open(fileDestinazioneOutput+'.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=output[0].keys())
        writer.writeheader()
        writer.writerows(output)

    print("COMPLETATO!")

# Function to handle the button click and call make_json
def process_files():
    file_giustificativi = file_giustificativi_entry.get()
    file_destinazione_output = file_destinazione_output_entry.get() 
    make_json(file_giustificativi, file_destinazione_output)

# Funzione per sfogliare un file e aggiornare il widget di inserimento corrispondente
def browse_file(entry_widget):
    file_path = filedialog.askopenfilename()
    entry_widget.delete(0, tk.END)
    entry_widget.insert(0, file_path)

# Creare la finestra principale della GUI
root = tk.Tk()
root.title("CheckDoubleG")

# Creare e posizionare i widget di inserimento per i percorsi dei file
file_giustificativi_entry = tk.Entry(root, width=50)
file_destinazione_output_entry = tk.Entry(root, width=50)

file_giustificativi_entry.grid(row=1, column=1, padx=10, pady=5)
file_destinazione_output_entry.grid(row=2, column=1, padx=10, pady=5)

# Creare e posizionare le etichette per i widget di inserimento
tk.Label(root, text="File Giustificativi:").grid(row=1, column=0, padx=10, pady=5)
tk.Label(root, text="Nome del File di Destinazione:").grid(row=2, column=0, padx=10, pady=5)

# Creare campi di input per le date

# Creare e posizionare i pulsanti di navigazione
tk.Button(root, text="Sfoglia", command=lambda: browse_file(file_giustificativi_entry)).grid(row=1, column=2, pady=5)

# Creare e posizionare il pulsante Converti
tk.Button(root, text="Converti", command=process_files).grid(row=12, column=0, columnspan=3, pady=10)

# Esegui la GUI
root.mainloop()
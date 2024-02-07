import pandas as pd

df = pd.read_excel("./Anomalie.xlsx", sheet_name="Dicembre")

output={}

for index,row in df.iterrows():
    matr=row["Matricola"]
    if matr not in output.keys():
        mese=str(row["Giorno"]).split("-")[1]
        giorno=str(row["Giorno"]).split("-")[2].split(" ")[0]
        output[matr]="Gentilissimo/a Dott./ssa "+row["Cognome"]+" "+row["Nome"]+",\n\nse non ha già provveduto, si prega giustificare o correggere le timbrature dei seguenti giorni: "+giorno+"/"+mese
    else:
        mese=str(row["Giorno"]).split("-")[1]
        giorno=str(row["Giorno"]).split("-")[2].split(" ")[0]
        output[matr]=output[matr]+", "+giorno+"/"+mese
        

for item in output.keys():
    output[item]=output[item]+".\n\nCordiali saluti."
    print(output[item],"\n\n\n\n\n")


# print(output)

# print(df)
import pandas as pd
from datetime import datetime, timedelta
import math


def toTimedelta(time):
    if ":" in str(time):
      (h,m) = time.split(':')
      d=timedelta(hours=int(h), minutes=int(m))
      return d
    else:
      return timedelta(hours=0, minutes=0)
def tohhmm (minutes):
  hh=math.trunc(minutes/60)
  mm=int(minutes%60)
  return str(hh).zfill(2)+":"+str(mm).zfill(2)


data = pd.read_excel('StraordinariLiquidabiliComparto18-23.xlsx', sheet_name="Saldi Complessivi", nrows=2696)
df = pd.DataFrame(data, columns=["Matricola","Nominativo","Saldo 2018","Saldo 2019","Saldo 2020","Saldo 2021","Saldo 2022","Saldo 2023"])
output=[]

saldi=["Saldo 2018","Saldo 2019","Saldo 2020","Saldo 2021","Saldo 2022","Saldo 2023"]
liquidazioni=["Liquidazioni 2018","Liquidazioni 2019","Liquidazioni 2020","Liquidazioni 2021","Liquidazioni 2022","Liquidazioni 2023"]

for l in liquidazioni:
  df[l]="00:00"

for index,row in df.iterrows():
  print(index)
  hoursArray=[]
  for i in saldi:
    hoursArray.append(row[i])
  
  verifiedHoursIndexes = [idx for idx, s in enumerate(hoursArray) if ':' in str(s)]
  startIndex = verifiedHoursIndexes[0]
  endIndex = verifiedHoursIndexes[len(verifiedHoursIndexes)-1]
  
  for vindex in verifiedHoursIndexes:
    # print("i",vindex)
    # print(toTimedelta(row[saldi[vindex]])<=toTimedelta(row[saldi[endIndex]]),(toTimedelta(row[saldi[vindex]])>timedelta(hours=0,minutes=0)),(toTimedelta(row[saldi[endIndex]])>timedelta(hours=0,minutes=0)))
    if (toTimedelta(df.at[index,saldi[vindex]])<toTimedelta(df.at[index,saldi[endIndex]])) and (toTimedelta(df.at[index,saldi[vindex]])>timedelta(hours=0,minutes=0)) and (toTimedelta(df.at[index,saldi[endIndex]])>timedelta(hours=0,minutes=0)):
      j=vindex
      subtract=toTimedelta(df.at[index,saldi[vindex]])
      df.at[index,liquidazioni[j]] = tohhmm(subtract/timedelta(minutes=1))
      while j<=endIndex:
        # print("j",j)
        df.at[index,saldi[j]]=tohhmm((toTimedelta(df.at[index,saldi[j]]) - subtract)/timedelta(minutes=1))
        j=j+1
    if (toTimedelta(df.at[index,saldi[vindex]])>=toTimedelta(df.at[index,saldi[endIndex]])) and (toTimedelta(df.at[index,saldi[vindex]])>timedelta(hours=0,minutes=0)) and (toTimedelta(df.at[index,saldi[endIndex]])>timedelta(hours=0,minutes=0)):
      j=vindex
      subtract=toTimedelta(df.at[index,saldi[endIndex]])
      df.at[index,liquidazioni[j]] = tohhmm(subtract/timedelta(minutes=1))
      while j<=endIndex:
        df.at[index,saldi[j]]=tohhmm((toTimedelta(df.at[index,saldi[j]]) - subtract)/timedelta(minutes=1))
        j=j+1


print(df)
df.to_excel("LIQ.xlsx", index=False)
  # print(row,startIndex,endIndex)
  
  # for s in saldi:


  
  # somma = timedelta()
  #   for s in saldi:
  #     somma= somma + toTimedelta(row[s])
    
  # output.append(somma/timedelta(hours=1))


# print(df)
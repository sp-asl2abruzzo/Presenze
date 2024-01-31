import pandas as pd
from datetime import datetime, timedelta
import math


def toTimedelta(time):
    if ":" in str(time):
      print(time)
      (h,m) = time.split(':')
      d=timedelta(hours=int(h), minutes=int(m))
      return d
    else:
      return timedelta(hours=0, minutes=0)
def tohhmm (minutes):
  hh=math.trunc(minutes/60)
  mm=int(minutes%60)
  return str(hh)+":"+str(mm)


data = pd.read_excel('StraordinariLiquidabiliComparto18-23.xlsx', sheet_name="Saldi Complessivi")
df = pd.DataFrame(data, columns=["Matricola","Nominativo","Saldo 2018","Saldo 2019","Saldo 2020","Saldo 2021","Saldo 2022","Saldo 2023"])

output=[]
saldi=["Saldo 2018","Saldo 2019","Saldo 2020","Saldo 2021","Saldo 2022","Saldo 2023"]

for index,row in df.iterrows():
  hoursArray=[]
  for i in saldi:
    hoursArray.append(row[i])
  
  verifiedHoursIndexes = [idx for idx, s in enumerate(hoursArray) if ':' in str(s)]
  startIndex = verifiedHoursIndexes[0]
  endIndex = verifiedHoursIndexes[len(verifiedHoursIndexes)-1]
  
  for index in verifiedHoursIndexes:
    print("i",index)
    print(toTimedelta(row[saldi[index]])<=toTimedelta(row[saldi[endIndex]]),(toTimedelta(row[saldi[index]])>timedelta(hours=0,minutes=0)),(toTimedelta(row[saldi[endIndex]])>timedelta(hours=0,minutes=0)))
    if (toTimedelta(row[saldi[index]])<=toTimedelta(row[saldi[endIndex]])) and (toTimedelta(row[saldi[index]])>timedelta(hours=0,minutes=0)) and (toTimedelta(row[saldi[endIndex]])>timedelta(hours=0,minutes=0)):
      j=index
      subtract=toTimedelta(row[saldi[index]])
      while j<=endIndex:
        print("j",j)
        row[saldi[j]]=tohhmm((toTimedelta(row[saldi[j]]) - subtract)/timedelta(minutes=1))
        j=j+1
    if (toTimedelta(row[saldi[index]])>toTimedelta(row[saldi[endIndex]])) and (toTimedelta(row[saldi[index]])>timedelta(hours=0,minutes=0)) and (toTimedelta(row[saldi[endIndex]])>timedelta(hours=0,minutes=0)):
      j=index
      subtract=toTimedelta(row[saldi[endIndex]])
      while j<=endIndex:
        row[saldi[j]]=tohhmm((toTimedelta(row[saldi[j]]) - subtract)/timedelta(minutes=1))
        j=j+1
  print(row,startIndex,endIndex)
  
  # for s in saldi:



  
  # somma = timedelta()
  #   for s in saldi:
  #     somma= somma + toTimedelta(row[s])
    
  # output.append(somma/timedelta(hours=1))


print(df)
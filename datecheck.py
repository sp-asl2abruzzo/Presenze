import datetime

def checkIfInDate(dateString,startString,endString):
    date = datetime.datetime.strptime(dateString, "%d/%m/%Y")
    start = datetime.datetime.strptime(startString, "%d/%m/%Y")
    end = datetime.datetime.strptime(endString, "%d/%m/%Y")
    return start <= date <= end


print(checkIfInDate("33/10/2023","23/10/2023","24/10/2023"))
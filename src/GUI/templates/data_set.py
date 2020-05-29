import csv
data_close=[]
data_date=[]
#for Shell
with open(r"C:\Users\Flori\Downloads\RDS-A (3).csv") as f:
            reader = csv.DictReader(x.replace('\0', '') for x in f)
            for row in reader:
                for k, v in row.items():
                    if k=="Date":
                        m=row["Date"]
                        m=m.split("-")
                        n=[]
                        n.append(int(m[0]))
                        n.append(int(m[1]))
                        n.append(int(m[2]))

                        data_date.append(n)

                    if k=="Close":
                        data_close.append(float(row["Close"]))

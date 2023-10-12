
def storeClients(clientList):
    with open('clients.txt','w') as c:
        for i in clientList:
            c.write(str(i))
            c.write("\n")

def storeBid(clientId,bid):
    import csv
    row=[str(clientId),str(bid)]
    with open('bids.csv','a') as b:
        csvwriter=csv.writer(b)
        csvwriter.writerow(row)
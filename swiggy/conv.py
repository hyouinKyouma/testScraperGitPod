import csv 

r = csv.reader(open('./final_data.csv')) # Here your csv file
lines = list(r)

for i in range(3351):
    if lines[i][1] != 'Closed':
        lines[i][1] = 'available'
    
        
writer = csv.writer(open('./output.csv', 'w'))
writer.writerows(lines)

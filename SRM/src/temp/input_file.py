file=open('../resources/InputSites.csv','r')

temp_file=open('../resources/InputSites_temp.csv','w')

for row in file:
    str=row.split(',')[0] + ',' + '1' + '\n'
    temp_file.write(str)


import csv
import struct

es1 = open('4ES_1.epx','rb')
es2 = open('4ES_2.epx','rb')
es3 = open('4ES_3.epx','rb')
es4 = open('4ES_4.epx','rb')

pf1 = open('4PF_1.epx','rb')
pf2 = open('4PF_2.epx','rb')
pf3 = open('4PF_3.epx','rb')
pf4 = open('4PF_4.epx','rb')

data = [es1,es2,es3,es4,pf1,pf2,pf3,pf4]

for file in data:
	line = ''
	for line in file:
		if line.find(b'//Binary') != -1:
			#print('found')
			break;
	print(line)

# reached the point
csvfile = open('C27.csv','w')
wr = csv.writer(csvfile, delimiter=',')
wr.writerow([ 'Index','Time' , '4ES_1' , 'Time' , '4ES_2' ,'Time' ,  '4ES_3' ,'Time' ,  '4ES_4' , 'Time' , '4PF_1' , 'Time' , '4PF_2' ,'Time' ,  '4PF_3' , 'Time' , '4PF_4' ])

# write all time
ind = 1

while True:
	row = []
	end = 0	
	for file in data:
		t = file.read(4)
		if(t==b''):
			end = 1
			break
		pt = file.read(4)
		if(pt==b''):
			end = 1
			break
		# ok point
		t = round(struct.unpack('f',t)[0],3)
		pt = round(struct.unpack('f', pt)[0],3)
		if file==data[0]:
			row.append(ind)
			ind = ind + 1
			row.append(t)
			row.append(pt)
		else:
			row.append(t)
			row.append(pt)

	if(end==1):
		break

	else:
		# write to csv
		wr.writerow( row )


csvfile.close()

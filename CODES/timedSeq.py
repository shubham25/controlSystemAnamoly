import csv
import struct

es1 = open('4ES_1.epx','rb')
#es2 = open('4ES_2.epx','rb')
#es3 = open('4ES_3.epx','rb')
#es4 = open('4ES_4.epx','rb')

pf1 = open('4PF_1.epx','rb')
#pf2 = open('4PF_2.epx','rb')
#pf3 = open('4PF_3.epx','rb')
#pf4 = open('4PF_4.epx','rb')

data = [es1,pf1]#'es2,es3,es4,pf1,pf2,pf3,pf4]

for file in data:
	line = ''
	for line in file:
		if line.find(b'//Binary') != -1:
			#print('found')
			break;
	print(line)

# reached the point
csvfile = open('C29_seq.csv','w')
wr = csv.writer(csvfile, delimiter=',')
wr.writerow([ 'Index','Time' , '4ES_1' , '4PF_1' ] )

# write all time

es1_pos = es1.tell()
pf1_pos = pf1.tell()

start_t = min( round(struct.unpack('f',es1.read(4))[0],3) , round(struct.unpack('f',pf1.read(4))[0],3) )
cur_t = 0
prev_es1 = round(struct.unpack('f',es1.read(4))[0],3)
prev_pf1 = round(struct.unpack('f',pf1.read(4))[0],3)
cur_es1 = prev_es1
cur_pf1 = prev_pf1
es1_pos = es1.seek(es1_pos)
pf1_pos = pf1.seek(pf1_pos)

ind = 1
ind_es = 0
ind_pf = 0

while True:
	t1 = es1.read(4)
	t2 = pf1.read(4)
	print(t1,t2)
	if(t1==b'' or t2==b''):
		if(t1==b'' and t2==b''):
			break
		elif(t1==b''):
		  t2 = round(struct.unpack('f',t2)[0],3) - start_t
		  cur_t = t2
		  cur_es1 = prev_es1
		  cur_pf1 = round(struct.unpack('f',pf1.read(4))[0],3)
		  ind_pf = ind_pf + 1		  
		else:
			t1 = round(struct.unpack('f',t1)[0],3) - start_t
			cur_t = t1
			cur_es1 = round(struct.unpack('f',es1.read(4))[0],3)
			ind_es = ind_es + 1
			cur_pf1 = prev_pf1			
	else:		
		t1 = round(struct.unpack('f',t1)[0],3) - start_t
		t2 = round(struct.unpack('f',t2)[0],3) - start_t
	
		if(t1==t2):
			cur_t = t1
			cur_es1 = round(struct.unpack('f',es1.read(4))[0],3)
			cur_pf1 = round(struct.unpack('f',pf1.read(4))[0],3)
			ind_pf + ind_pf + 1
			ind_es = ind_es + 1
		elif(t1 < t2):
			cur_t = t1
			cur_es1 = round(struct.unpack('f',es1.read(4))[0],3)
			ind_es = ind_es + 1
			pf1.seek(pf1_pos)
			cur_pf1 = prev_pf1
		elif(t2<t1):
			cur_t = t2
			cur_pf1 = round(struct.unpack('f',pf1.read(4))[0],3)
			ind_pf = ind_pf + 1
			pf1.seek(es1_pos)
			cur_es1 = prev_es1
	# write current point
	row = [ind,cur_t,cur_es1,cur_pf1]
	ind = ind  + 1
	prev_pf1 = cur_pf1
	prev_es1 = cur_es1
	es1_pos = es1.tell()
	pf1_pos = pf1.tell()
	print(row)

csvfile.close()
print(ind)

import csv
import sys
import struct
mission = '../' + sys.argv[1]

es1 = open(mission + '/4ES_1.epx','rb')
#es2 = open('4ES_2.epx','rb')
#es3 = open('4ES_3.epx','rb')
#es4 = open('4ES_4.epx','rb')

pf1 = open(mission +'/4PF_1.epx','rb')
#pf2 = open('4PF_2.epx','rb')
#pf3 = open('4PF_3.epx','rb')
#pf4 = open('4PF_4.epx','rb')

data = [es1,pf1]#'es2,es3,es4,pf1,pf2,pf3,pf4]

for file in data:
	line = ''
	for line in file:
		if line.find(b'//Binary') != -1:
			#print('found')
			break
	#print(line)

# reached the point
csvfile = open(mission + '/' + sys.argv[1] + '_seq.csv','w')
wr = csv.writer(csvfile, delimiter=',')
wr.writerow([ 'Index','Time' , '4ES_1' , '4PF_1' ] )

# write all time

es1_pos = es1.tell()
pf1_pos = pf1.tell()

#print('start ' , es1_pos, pf1_pos) 

start_t = min( struct.unpack('f',es1.read(4))[0] , struct.unpack('f',pf1.read(4))[0] )
print(start_t)
cur_t = -1
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
	#print(t1,t2)
	if(t1==b'' or t2==b''):
		##a = input()
		if(t1==b'' and t2==b''):
			break
		elif(t1==b''):
		  t2 = round(struct.unpack('f',t2)[0]  - start_t , 3 )
		  cur_pf1 = round(struct.unpack('f',pf1.read(4))[0],3)
		  
		  cur_es1 = prev_es1
		  ##es1.seek(es1.tell() - 4 )
		  ind_pf = ind_pf + 1
		  if(t2==cur_t):
		    continue
		  cur_t = t2		  
		elif(t2 == b''):
			t1 = round(struct.unpack('f',t1)[0] - start_t , 3 )
			cur_es1 = round(struct.unpack('f',es1.read(4))[0],3)
					
			##pf1.seek(pf1.tell() -4 )
			ind_es = ind_es + 1
			cur_pf1 = prev_pf1
			if(cur_t == t1):
			  continue
			cur_t = t1	
		else:
		  print('NTC1:', t1,t2)			
	else:		
		t1 = round(struct.unpack('f',t1)[0] - start_t , 3)
		t2 = round(struct.unpack('f',t2)[0] - start_t , 3) 
		#print(t1,t2)
		if(t1==t2):
			cur_es1 = round(struct.unpack('f',es1.read(4))[0],3)
			cur_pf1 = round(struct.unpack('f',pf1.read(4))[0],3)
				
			ind_pf + ind_pf + 1
			ind_es = ind_es + 1
			if(cur_t == t1):
			  continue
			cur_t = t1
		elif(t1 < t2):
			cur_es1 = round(struct.unpack('f',es1.read(4))[0],3)
			ind_es = ind_es + 1
			pf1.seek(pf1.tell() - 4)
			cur_pf1 = prev_pf1
			if(cur_t == t1):
			  continue
			cur_t = t1	
		elif(t2 < t1):
			cur_pf1 = round(struct.unpack('f',pf1.read(4))[0],3)
			ind_pf = ind_pf + 1
			es1.seek(es1.tell() - 4)
			cur_es1 = prev_es1
			if(cur_t == t2):
			  continue
			cur_t = t2	
		else:
		  print('NTC:', t1,t2)
	# write current point
	row = [ind,cur_t,cur_es1,cur_pf1]
	ind = ind  + 1
	prev_pf1 = cur_pf1
	prev_es1 = cur_es1
	#es1_pos = es1.tell()
	#pf1_pos = pf1.tell()
	#print(row)
	wr.writerow(row)

csvfile.close()
print(ind,ind_es,ind_pf)

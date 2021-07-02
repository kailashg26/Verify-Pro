# Python3 code to demonstrate 
# generating random strings 
# using random.choices() 
import string 
import random 
import csv
import pandas as pd
input_col = ['num of packets','Fields in pkt 1','Fields in pkt 2','Fields in pkt 3','Fields in pkt 4','Fields in pkt 5','Fields in pkt 6','Type of 1st Field in 1st pkt','Type of 2nd Field in 1st pkt','Type of 3rd Field in 1st pkt','Type of 4th Field in 1st pkt','Type of 1st Field in 2nd pkt','Type of 2nd Field in 2nd pkt','Type of 3rd Field in 2nd pkt','Type of 4th Field in 2nd pkt','Type of 1st Field in 3rd pkt','Type of 2nd Field in 3rd pkt','Type of 3rd Field in 3rd pkt','Type of 4th Field in 3rd pkt','Type of 1st Field in 4th pkt','Type of 2nd Field in 4th pkt','Type of 3rd Field in 4th pkt','Type of 4th Field in 4th pkt','Type of 1st Field in 5th pkt','Type of 2nd Field in 5th pkt','Type of 3rd Field in 5th pkt','Type of 4th Field in 5th pkt','Type of 1st Field in 6th pkt','Type of 2nd Field in 6th pkt','Type of 3rd Field in 6th pkt','Type of 4th Field in 6th pkt']
def ranstring():
	N = random.randint(5,15)
	res = ''.join(random.choices(string.ascii_uppercase +
							string.digits, k = N)) 

	return str(res)

def stringtofield(input):

	List = input.split('/')
	num = len(List)
	packets = []
	for e in List:
		e= e[3:]
		packets.append(e.split(','))
	sizes = [0]*6
	types = []
	for i in range(len(packets)):
		sizes[i]=len(packets[i])
		packet_type = [0]*4
		j = 0
		for each in packets[i]:
			if each.isdigit():
				packet_type[j]=1
			else:
				packet_type[j]=-1
			j+=1
		
		types = types + packet_type
	if(len(types)!=24):
		types= types + [0]*(24-len(types))

	return [num]+sizes+types


L1 = []

for i in range(10000):
	data = "P1:"+ranstring()+','+str(random.randint(100,1000))
	inputlist = [data,'Dialect 1'] + stringtofield(data)
	L1.append(inputlist)
	





for i in range(10000):
	data =("P1:"+str(random.randint(100,1500))+'/P2:'+ranstring())
	inputlist = [data,'Dialect 2'] + stringtofield(data)
	L1.append(inputlist)







for i in range(10000):
	data = ("P1:"+ranstring()+','+str(random.randint(100,1000))+'/P2:'+ranstring())
	inputlist = [data,'Dialect 3'] + stringtofield(data)
	L1.append(inputlist)






for i in range(10000):
	x=str(random.randint(100,1000))
	data = ("P1:"+x+'/P2:'+x)
	inputlist = [data,'Dialect 4'] + stringtofield(data)
	L1.append(inputlist)


for i in range(10000):
	
	data = ('P1:'+str(random.randint(100,1000))+','+str(random.randint(100,1000))+','+str(random.randint(100,1000))+'/P2:'+str(random.randint(100,1000)))
	inputlist = [data,'Dialect 5'] + stringtofield(data)
	L1.append(inputlist)





for i in range(10000):
	
	data = ('P1:'+ranstring()+"/P2:"+str(random.randint(100,1000))+','+str(random.randint(100,1000))+'/P3:'+str(random.randint(100,1000)))
	inputlist = [data,'Dialect 6'] + stringtofield(data)
	L1.append(inputlist)





for i in range(10000):
	
	data = ('P1:'+ranstring()+"/P2:"+str(random.randint(100,1000))+'/P3:'+str(random.randint(100,1000)))
	inputlist = [data,'Dialect 7'] + stringtofield(data)
	L1.append(inputlist)





for i in range(10000):
	
	data = ('P1:'+ranstring()+','+str(random.randint(100,1000))+','+ranstring()+','+ranstring())
	inputlist = [data,'Dialect 8'] + stringtofield(data)
	L1.append(inputlist)





for i in range(10000):
	
	data = ('P1:'+ranstring()+','+str(random.randint(100,1000))+'/P2:'+ranstring()+','+ranstring())
	inputlist = [data,'Dialect 9'] + stringtofield(data)
	L1.append(inputlist)





for i in range(10000):
	
	data = ('P1:'+ranstring()+'/P2:'+str(random.randint(100,1000))+','+ranstring()+','+ranstring())
	inputlist = [data,'Dialect 10'] + stringtofield(data)
	L1.append(inputlist)






for i in range(10000):
	
	data = ('P1:'+ranstring()+'/P2:'+str(random.randint(100,1000))+'/p3:'+ranstring()+','+str(random.randint(100,1000))+'/p4:'+ranstring()+','+str(random.randint(100,1000)))
	inputlist = [data,'Dialect 11'] + stringtofield(data)
	L1.append(inputlist)




for i in range(10000):
	
	data = ('P1:'+str(random.randint(100,1000)))
	inputlist = [data,'Dialect 12'] + stringtofield(data)
	L1.append(inputlist)




for i in range(10000):
	
	data = ('P1:'+ranstring()+'/P2:'+str(random.randint(100,1000)))
	inputlist = [data,'Dialect 13'] + stringtofield(data)
	L1.append(inputlist)



for i in range(10000):
	
	data = ('P1:'+ranstring()+','+ranstring()+','+ranstring()+'/P2:'+str(random.randint(100,1000)))
	inputlist = [data,'Dialect 14'] + stringtofield(data)
	L1.append(inputlist)


for i in range(10000):
	
	data = ('P1:'+ranstring()+'/P2:'+str(random.randint(100,1000))+'/P3:'+ranstring()+'/P4:'+ranstring()+'/P5:'+str(random.randint(100,1000))+'/P6:'+ranstring())
	inputlist = [data,'Dialect 15'] + stringtofield(data)
	L1.append(inputlist)



random.shuffle(L1)




with open('dataset.csv',mode = 'w' , newline = '') as csv_file:
	WT = csv.writer(csv_file , delimiter = ',',lineterminator='\n')
	WT.writerow(['input','Dialect']+input_col)
	WT.writerows(L1)


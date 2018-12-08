import numpy as np
import random
import copy
from math import *

class TSP_GA:
	'''
	要求输入：
	population_size:种群大小
	generation_size:迭代次数
	cross_rate:交叉概率
	mutate_rate:变异概率
	fitness=1/sum(sqrt((x1-x2)**2+(y1-y2)**2))
	n:城市个数
	x,y:城市坐标
	编码原则：字符串排序"abcdefghij"和"abcdedfghijklmnopqrst",其中"a":1,"b":2...
	'''
	
	def __init__(self):
		self.population_size=None
		self.generation_size=None
		self.cross_rate=None
		self.mutate_rate=None
		self.n=None
		self.dict_char_number={'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,
							'g':6,'h':7,'i':8,'j':9,'k':10,'l':11,
							'm':12,'n':13,'o':14,'p':15,'q':16,'r':17,'s':18,'t':19}
		self.distance_mat=None
		self.population=[]
		self.dict_fitness={}
		self.parents=[]
	
	def input_info(self,population_size,generation_size,cross_rate,mutate_rate,n,x,y):
		self.population_size=population_size
		self.generation_size=generation_size
		self.cross_rate=cross_rate
		self.mutate_rate=mutate_rate
		self.n=n
		self.distance_mat=np.zeros([n,n])
		for i in range(n):
			for j in range(n):
				self.distance_mat[i][j]=sqrt((x[i]-x[j])**2+(y[i]-y[j])**2)
	
	def __inite(self):
		if self.n==10:
			original_x="bcdefghij"
		else:
			original_x="bcdefghijklmnopqrst"
		num=0
		while True:
			if num==self.population_size:
				break
			x=list(original_x)
			random.shuffle(x)
			x.append('a')
			x.insert(0,'a')
			if x in self.population:
				continue
			else:
				self.population.append(x)
				num+=1
	
	def __cal_fitness(self):
		for x in self.population:
			temp_distance=0
			for i in range(len(x)-1):
				m=self.dict_char_number[x[i]]
				n=self.dict_char_number[x[i+1]]
				temp_distance+=self.distance_mat[m][n]
			str_x=''.join(x)
			self.dict_fitness[str_x]=1/temp_distance

	def __choose_parents(self):
		fitness_sum=sum(self.dict_fitness.values())
		sort_fitness=sorted(self.dict_fitness.items(),key=lambda x:x[1],reverse=True)
		dict_possibility={}
		for x in self.dict_fitness.keys():
			dict_possibility[x]=self.dict_fitness[x]/fitness_sum
		dict_roulette={}
		temp=0
		for x in sort_fitness:
			dict_roulette[x[0]]=dict_possibility[x[0]]+temp
			temp=dict_roulette[x[0]]
		values=list(dict_roulette.values())
		values.insert(0,0)
		values.pop(-1)
		values.append(1)
		keys=list(dict_roulette.keys())
		for k in range(int(self.population_size/2)):
			temp=[]
			for i in range(2):
				r=random.uniform(0,1)
				for j in range(self.population_size):
					if values[j]<=r<values[j+1]:
						temp.append(keys[j])
						break
			self.parents.append(tuple(temp))
		
	def __cross_parents(self):
		new_population=[]
		for k in range(int(self.population_size/2)):
			determine_cross=random.uniform(0,1)
			if determine_cross<self.cross_rate:
				par1=list(self.parents[k][0]);par2=list(self.parents[k][1])
				par1.pop(0);par2.pop(0)
				par1.pop(-1);par2.pop(-1)
				if self.n==10:
					while True:
						r1=random.randint(0,8);r2=random.randint(0,8)
						if r1==r2:
							continue
						elif r1==0 and r2==8:
							continue
						elif r1==8 and r2==0:
							continue
						else:
							break
				else:
					while True:
						r1=random.randint(0,18);r2=random.randint(0,18)
						if r1==r2:
							continue
						elif r1==0 and r2==18:
							continue
						elif r1==18 and r2==0:
							continue
						else:
							break
				h=max(r1,r2);l=min(r1,r2)
				temp=copy.copy(par1)
				#temp_2=copy.copy(par2)
				new_par1=copy.copy(par1)
				new_par2=copy.copy(par2)
				match_dict1={}
				match_dict2={}
				for i in range(l,h+1):
					new_par1[i]=par2[i]
					new_par2[i]=temp[i]
					match_dict1[par2[i]]=temp[i]
					match_dict2[temp[i]]=par2[i]
				keys1=list(match_dict1.keys())
				keys2=list(match_dict2.keys())
				while True:
					if self.n==10:
						if len(set(new_par1))==9:
							break
					else:
						if len(set(new_par1))==19:
							break
					for i in range(l):
						if new_par1[i] in keys1:
							new_par1[i]=match_dict1[new_par1[i]]
					for i in range(h+1,self.n-1):
						if new_par1[i] in keys1:
							new_par1[i]=match_dict1[new_par1[i]]
				while True:
					if self.n==10:
						if len(set(new_par2))==9:
							break
					else:
						if len(set(new_par2))==19:
							break
					for i in range(l):
						if new_par2[i] in keys2:
							new_par2[i]=match_dict2[new_par2[i]]
					for i in range(h+1,self.n-1):
						if new_par2[i] in keys2:
							new_par2[i]=match_dict2[new_par2[i]]						
				#print(par1,par2)
				#print(new_par1,new_par2)
				new_par1.insert(self.n,'a');new_par1.insert(0,'a')
				new_par2.insert(self.n,'a');new_par2.insert(0,'a')
				new_population.append(new_par1);new_population.append(new_par2)
			else:
				new_population.append(list(self.parents[k][0]))
				new_population.append(list(self.parents[k][1]))
		self.population=new_population
	
	def __mutate(self):
		for k in range(self.population_size):
			r=random.uniform(0,1)
			if r<self.mutate_rate:
				if self.n==10:
					while True:
						r1=random.randint(1,9);r2=random.randint(1,9)
						if r1==r2:
							continue
						else:
							break
				else:
					while True:
						r1=random.randint(1,19);r2=random.randint(1,19)
						if r1==r2:
							continue
						else:
							break
				temp=copy.copy(self.population[k][r1])
				self.population[k][r1]=self.population[k][r2]
				self.population[k][r2]=temp
	
	def __select_best(self):
		values=self.dict_fitness.values()
		best_fitness=max(list(values))
		road=list(self.dict_fitness.keys())[list(values).index(best_fitness)]
		return(best_fitness,road)
	
	def main(self):
		best_fitness=0
		self.__inite()
		for k in range(self.generation_size):
			self.__cal_fitness()
			temp=self.__select_best()
			#print(temp[0])
			if temp[0]>best_fitness:
				best_fitness=temp[0]
				best_road=temp[1]
			self.__choose_parents()
			self.__cross_parents()
			self.__mutate()
		final_temp=self.__select_best()
		final_best_fitness=final_temp[0]
		final_best_road=final_temp[1]
		print(final_best_fitness,best_fitness,final_best_road)
		return (best_fitness,best_road)
		
		
	
x1=[0.4000,0.2439,0.1707,0.2293,0.5171,0.8732,0.6878,0.8488,0.6683,0.6195]
y1=[0.4439,0.1463,0.2293,0.7610,0.9414,0.6536,0.5219,0.3609,0.2536,0.2634]
x2=[5.294,4.286,4.719,4.185,0.915,4.771,1.524,3.447,3.718,2.649,4.399,4.660,
	1.232,5.036,2.710,1.072,5.855,0.194,1.762,2.682]
y2=[1.558,3.662,2.774,2.230,3.821,6.041,2.871,2.111,3.665,2.556,1.194,2.949,
	6.440,0.244,3.140,3.454,6.203,1.862,2.693,6.097]		
road_number={}
for i in range(500):
	test=TSP_GA()
	test.input_info(200,400,0.7,0.05,10,x1,y1) #600,600,0.7,0.1,10,x1,x2
	road=test.main()
	if road[1] in road_number:
		road_number[road[1]]+=1
	else:
		road_number[road[1]]=0
		road_number[road[1]]+=1
sort=sorted(road_number.items(),key=lambda x:x[1],reverse=True)
print(road_number)
merge={}
for i in sort:
	merge[i[0]]=i[1]
temp=copy.copy(merge)
temp_keys=list(temp.keys())
i=0
while True:
	if temp_keys==[]:
		break
	item=sort[i][0]
	i+=1
	print(item)
	if item[::-1] in temp_keys:
		merge[item]+=merge[item[::-1]]
		temp_keys.remove(item)
		temp_keys.remove(item[::-1])
	else :
		if item in temp_keys:
			temp_keys.remove(item)
print(merge)
'''
[('abcjihgfeda', 16), ('adegfhijbca', 15), ('adefhgijbca', 15), ('acbjihfgeda', 14), ('adefghijbca', 12), ('acbjighfeda', 10), 
('acbijhfgeda', 10), ('abcdefghija', 10), ('adefghjicba', 10), ('ajihgfedcba', 9), ('abcjihfgeda', 9), ('adefghijcba', 9), 
('ajighfedcba', 9), ('acbjihgfeda', 9), ('acbijhgfeda', 9), ('acbdefghija', 8), ('aedcbjihfga', 8), ('abcijhgfeda', 8), 
('abcdefghjia', 8), ('agfhijbcdea', 8), ('ajihgfedbca', 7), ('adegfhjibca', 7), ('adefhgjibca', 6), ('aijghfedbca', 6), 
('adegfhijcba', 6), ('abcdegfhjia', 6), ('abcdefhijga', 6), ('acbjihfedga', 6), ('aijhgfedcba', 6), ('agjihfedcba', 6), 
('acbdegfhjia', 6), ('aijghfedcba', 5), ('abcjighfeda', 5), ('ajihfgedcba', 5), ('acbhijgfeda', 5), ('abcdegfhija', 5), 
('aijhfgedbca', 5), ('agijhfedcba', 4), ('agdefhijcba', 4), ('adefhgijcba', 4), ('agjihfedbca', 4), ('aijhgfedbca', 4), 
('adefgjhibca', 4), ('acbihjgfeda', 4), ('ajihfgedbca', 4), ('abcijghfeda', 4), ('adefghjibca', 4), ('adefgihjbca', 3), 
('aijhfgedcba', 3), ('acbjgihfeda', 3), ('acbijghfeda', 3), ('agdefhijbca', 3), ('acbjhigfeda', 3), ('ajighfedbca', 3), 
('aghijfedcba', 3), ('abcgijhfeda', 3), ('adefhijgbca', 3), ('adefhigjbca', 3), ('acbjifhgeda', 3), ('ajibcdefhga', 3), 
('agfhijedcba', 3), ('adefgijhbca', 3), ('abcdefhgjia', 2), ('aedgfhijcba', 2), ('adefgjhicba', 2), ('acbdegfhija', 2), 
('ajifhgedcba', 2), ('adefgjihcba', 2), ('abcjifhgeda', 2), ('abcdefgjiha', 2), ('ajbcdefghia', 2), ('adegfhjicba', 2), 
('aedfghijbca', 2), ('acbdefhijga', 2), ('abcijhfgeda', 2), ('ahijgfedbca', 2), ('abchijgfeda', 2), ('acbgjihfeda', 2), 
('adefgjihbca', 2), ('agfedcbjiha', 2), ('agdefhjibca', 2), ('acbdefhjiga', 2), ('ahijbcdefga', 2), ('abcdefhjiga', 2), 
('acbdefgjiha', 2), ('adefghicbja', 2), ('ajihbcdefga', 1), ('abcgjihfeda', 1), ('adehfgijcba', 1), ('aihjgfedcba', 1), 
('aedfghijcba', 1), ('acbjihdefga', 1), ('acbijhgdefa', 1), ('abcjigfheda', 1), ('abcdejihfga', 1), ('abcdeijhfga', 1), 
('acbdefghjia', 1), ('ajhigfedcba', 1), ('acbdefgihja', 1), ('adefhijcbga', 1), ('aedgfhijbca', 1), ('ajgihfedcba', 1), 
('adefhjigbca', 1), ('adcbjihfega', 1), ('ajhibcdefga', 1), ('acbhjigfeda', 1), ('aihgfedcbja', 1), ('abcdefhgija', 1), 
('adehfgjibca', 1), ('abcdefgijha', 1), ('acbjighfdea', 1), ('adeghfijbca', 1), ('agcbjihfeda', 1), ('acbghjifeda', 1), 
('acbdejihfga', 1), ('agfhjibceda', 1), ('adefhigjcba', 1), ('adecbjihfga', 1), ('acbjigfheda', 1), ('adehfgijbca', 1), 
('acbgijhfeda', 1), ('abcjgihfeda', 1), ('acbjhgifeda', 1), ('adefhgjicba', 1), ('agfhijcbdea', 1), ('adehgfijcba', 1), 
('acbijgfheda', 1), ('agijhfedbca', 1), ('aghijbcdefa', 1), ('aijbcdefhga', 1), ('agfhijbceda', 1), ('ajigfhedcba', 1), 
('acbjihgfdea', 1), ('adefhgcbija', 1), ('adegfihjbca', 1), ('adefighjbca', 1), ('acbjihfgdea', 1), ('aghfedcbjia', 1), 
('aedcbgfhija', 1), ('abcijgfheda', 1), ('aedcbijhfga', 1), ('ajcbihgfeda', 1), ('ahjigfedcba', 1), ('adefgijhcba', 1), 
('abcihjgfeda', 1), ('aghjifedcba', 1), ('aedbcijhfga', 1), ('abcdefhigja', 1), ('afhijgedcba', 1)]
'''

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	

from math import log
import numpy as np

class prox_choice:

	def makedict(self,listv):

		return dict(zip(listv,range(len(listv))))


	def __init__(self,factors,values=range(-100,101)):

		#self.itemdefs 	= itemdefs
		self.factors 	= factors
		self.values 	= values
		self.maxval 	= len(values) - 1

		self.valtrans 	= self.makedict(values)
		self.factrans 	= self.makedict(factors)

		self.nobs 		= 0

		self.store 		= [[0 for _ in self.values] for _ in self.factors]

		print ('Transform of ordinal observations:',values, '=>', self.valtrans)
		print ('Factor names transladed to index :',factors,"=>", self.factrans)


	#-------------------------------------------------------------------------------------------------------
	# an observation looks like strings (MUST BE STRINGS)
	# 1. Losing factor
	# 2. Winning factor
	# 3. Rating for winning factor
	#
	# EXAMPLE: 
	# ["A","C",'a'] = compare A and C, C is last and thus won with rating 'a' (with complement "x", say)
	#   	ABCD
	#       x_a_   <<< Winsteps format 
	#
	#-------------------------------------------------------------------------------------------------------

	def addobs(self,facleft,facright,obs): 

		if obs < 0: facleft,facright = facright,facleft # left was the winner and goes in the rightside position

		leftid 	= self.factrans[facleft]		# transform a name into index
		rightid	= self.factrans[facright]
		ratid   = self.valtrans[obs]

		self.store[rightid][ratid] 				+= 1
		self.store[leftid][self.maxval-ratid]  	+= 1

		self.nobs += 1

		#print self.store
		return True

	# Divide sum by max total, take log 
	# Return as dictionary
	# maxiter = maximum number of iterations that will be done
	# eps: convergence due to change in variance allowed
	# delta: value to be used when 0 frequenciew are encountered

	def estimate(self,maxiter=25,eps=0.01,delta=0.1):

		totrat  = np.log(np.array([(float(sum(i*v for i,v in enumerate(f)))+delta)/(sum(f)*self.maxval + delta) for f in self.store])) # different method

		totrat  = totrat - np.mean(totrat)

		#totsum = [sum([i*v for i,v in enumerate(f)]) for f in self.store]
		
		t = dict(zip(self.factors,totrat)) #zip(totrat,totsum)))
		t['*sd'] = np.std(totrat)

		return t


if __name__ == '__main__':

	prox = prox_choice('ABCDE','01') #['a','b','c'])

	for p in spairs: prox.addobs(p)

	t = prox.estimate() 

	with open('test.txt','w') as fout:

		for k in prox.factors:
			v = t[k]
			s = '%s,%7.3f,%7.3f,%7.3f,%7.3f,%7.3f,%7.3f,%10s,%s'%(k,v[0],v[1],v[2],v[3],v[4],v[5],v[6],v[7])
			print (s)
			fout.write(s+'\n')

	print (t)






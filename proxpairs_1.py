
from math import log
import numpy as np

class prox_choice:


	def __init__(self,ndatacats,pop_rescore_vals={}):

		self.store  = {} 			# dict entries are the factor names, reserve array with ndatacats values for each
		self.ncats 	= ndatacats + 1

		self.pop_rescore_vals    = pop_rescore_vals # dictionary to make populaton M+SD based scores

		#orint ndatacats


	#-------------------------------------------------------------------------------------------------------
	# provide names of left and right factors
	# and add left and right observation values <<<< these have been fully preprocessed, no changes needed
	# allocate new storage arrays as needed in dictionary
	#-------------------------------------------------------------------------------------------------------

	def addobs(self,facleft,facright,obsleft,obsright): 

		if not facleft  in self.store: self.store[facleft]  = [1 for _ in range(self.ncats)]
		if not facright in self.store: self.store[facright] = [1 for _ in range(self.ncats)]

		self.store[facleft][obsleft] 	+= 1
		self.store[facright][obsright] 	+= 1

		return self.store

	# Divide sum by max total, take log 
	# Return as dictionary
	# maxiter = maximum number of iterations that will be done
	# eps: convergence due to change in variance allowed
	# delta: value to be used when 0 frequenciew are encountered

	def estimatez(self): #,maxiter=25,eps=0.01,delta=0.1):

		#rawest,zpers,persz,pscaled = {},{},{},{}
		zest,rawest,pilotscore,popscore = {},{},{},{}

		n,sx,sxx = 0,0.0,0.0

		#print "STORE",self.store

		for fac in self.store:

			freqs = self.store[fac]
			#print freqs

			sum135etc 	= sum([freqs[odd] for odd in range(1,2,self.ncats)])
			sum024etc 	= sum([freqs[evn] for evn in range(0,2,self.ncats)])

			#print "FACTOR:",fac,sum135etc,sum024etc,float(sum135etc)/sum024etc,

			rat		  	= log(float(sum135etc) / sum024etc)

			#print rat

			sx 			+= rat
			sxx			+= rat * rat
			n 			+= 1
		
			rawest[fac] = rat #(freqs,sum024etc,sum135etc,rat)

		m = float(sx) / n

		sd = (float(sxx) - float(sx) * sx / n) / n

		sd = 1.0 if sd<=0.0 else sd**0.5

	# RESCORE rawest in varioius ways

		for fac in self.store: 

			zest[fac] 		= (rawest[fac] - m) / sd
			pilotscore[fac] = int(min(max(zest[fac] * 10.0 + 70,40.0),100.0)+0.5)

			if fac in self.pop_rescore_vals:
				mult_pop,add_pop,min_pop,max_pop	= self.pop_rescore_vals[fac]
				popscore[fac] = int(min(max(rawest[fac] * mult_pop + add_pop,min_pop),max_pop)+0.5)
			else:
				popscore[fac] = pilotscore[fac]

		return {'zest':zest, 'rawest':rawest,'pilotscore':pilotscore,'popscore':popscore}


if __name__ == '__main__':

	prox = prox_choice('ABCDE','01') #['a','b','c'])

	for p in spairs: prox.addobs(p)

	t = prox.estimate() 

	'''with open('test.txt','w') as fout:

		for k in prox.factors:
			v = t[k]
			s = '%s,%7.3f,%7.3f,%7.3f,%7.3f,%7.3f,%7.3f,%10s,%s'%(k,v[0],v[1],v[2],v[3],v[4],v[5],v[6],v[7])
			print s
			fout.write(s+'\n')

	print t'''






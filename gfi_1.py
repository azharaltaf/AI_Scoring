from flask import Flask
from flask import jsonify
from flask import request
app = Flask(__name__)


from random import randrange
from proxpairs_1 import prox_choice


#
# read a dictionary of items and raw values (and other stuff): {"1":44,"99":2,"not an item":"whatever"}
# this example yields:
# {'*item':"1","*recoded":2,'*leftright':[A,B]} ......
#


def read_gfi_factors(answers,cuts=[0]):


	# compare value to a set of ordered "cuts"
	# 0 compared to [1,5] => 0
	# 1 compared to [1,5] => 0   (comparison is: <=)
	# 2                   => 1
	# 5                   => 1
	# 6                   => 2
	# for integer cut values, this works "as if" the cutvalues c were: c+0.5
	# NOTE: to make symmetric cuts (some for neg as for pos) do
	# [-3,-2,-1,0,1,2,3] 

	def rescore(rawvalue): # default: LTE 0 => 0, GT 0 => 1

		for cat,cut in enumerate(cuts):
			if rawvalue <= cut: return cat
	# we passed the last value
		return len(cuts)

	#------------------------
	# the answer comes as a pair: 77/1 == 77 on the left, 1 on the right
	# so: 77/1 => -77
	# and: the -77 is then recoded via "rescore"
	# 1/77 would become: 77

	def unsplit(response):

		if "/" in str(response): 
	
			l,r = [int(v) for v in response.split('/')]

			if l > r: 
				return rescore(-l)
			elif l < r:
				return rescore(r)
			else:
				return rescore(0)
		else:
			return rescore(0) 

	# process series of answer records
	#print 'aap'
	#print answers

	for a in answers:

		item 	= answers[a]

		leftfac = item['LItemTopic']
		rightfac= item['RITemTopic']

		leftsub = item['LItemSubtopic']
		rightsub= item['RItemSubtopic']

		answer 	= unsplit(item['Answer'])
		inverse = len(cuts) - answer
		#yield answer,inverse, answer+inverse

		yield {'*itid':a,'*rightanswer':answer,'*leftanswer':inverse,#'*oldanswer':item['Answer'],
				'*leftfac':leftfac,'*rightfac':rightfac,'*leftsub':leftsub,'*rightsub':rightsub}



'''def testanswer(n):

	d = {}

	for i in range(n):
		itid 	= 'obs_%d'%i 
		atnum 	= i % 4
		atnum1 	= (i+1) % 4

		d[itid] = {
			'LItemTopic' : 'Factor_%d'%atnum,
			'RITemTopic' : 'Factor_%d'%atnum1,

			'LItemSubtopic' : 'Sub_%d'%atnum,
			'RItemSubtopic' : 'Sub_%d'%atnum1,

			'Answer' : '%d/%d' % (atnum,atnum1)
			}

	return d'''


xxx = 33

@app.route('/test/0/',methods=['POST'])

def TEST_0():

	request_input 	= request.json
	name = request_input["name"]
	message = 'Hello, how are you %s'%name

	return jsonify({"message":message})


@app.route('/gfi/1/',methods=['POST'])

def GFI_1():

	common_cuts 	= [0] 					# only distinguish left and right for now
	ncats			= len(common_cuts) 		# n cutvalues give n+1 categories 0, 1, 2, .....

	prox_factor 	= prox_choice(ncats) 	# we need ncats "bins" for observations
	prox_subfactor 	= prox_choice(ncats)

	request_input 	= request.json

	#print request_input

	for v in read_gfi_factors(request_input,common_cuts):

		prox_factor.addobs(v['*leftfac'],v['*rightfac'],v['*leftanswer'],v['*rightanswer'])
		prox_subfactor.addobs(v['*leftsub'],v['*rightsub'],v['*leftanswer'],v['*rightanswer'])

	results = {"*factors": prox_factor.estimatez(),"*subfactors":prox_subfactor.estimatez()}

	return jsonify(results)

if __name__ == '__main__':

	#app.run(debug=True,port=6041)
	app.run(debug=True,host="0.0.0.0")

'''
	test = testanswer(9)

	for k in sorted(test.keys()):
		print k,test[k]
	print '***'

	#for s in score_gfi_factors(test,cuts=[-3,-2,-1,0,1,2]): print s

#--------------------------------

	common_cuts 	= [0]
	ncats			= len(common_cuts) 		# n cutvalues give n+1 categories 0, 1, 2, .....

	prox_factor 	= prox_choice(ncats) 	# we need ncats "bins" for observations
	prox_subfactor 	= prox_choice(ncats)

	for v in read_gfi_factors(test,common_cuts):

		print '\n\n',v['*itid'],v

		print('Factor    :'), 
		prox_factor.addobs(v['*leftfac'],v['*rightfac'],v['*leftanswer'],v['*rightanswer'])
		print prox_factor.store

		print('Sub Factor:'),
		prox_subfactor.addobs(v['*leftsub'],v['*rightsub'],v['*leftanswer'],v['*rightanswer'])
		print prox_subfactor.store

	print 'factor   ',prox_factor.estimatez()
	print 'subfactor',prox_subfactor.estimatez()'''






	





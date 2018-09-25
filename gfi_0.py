from flask import Flask
from flask import jsonify
from flask import request
app = Flask(__name__)


from random import randrange
from proxpairs import prox_choice

GFI_factors = ['Character', 'Commitment', 'Compliance', 'Decision M', 'Enterprisi', 'Influentia', 'Intellect']

GFI_pairs = {
		"A-goes-here___24": {"*fac": ["Commitment","Intellect"],"*subfac": ["Achievemen","Creativity"]}, 	#1
		"42___39": {"*fac": ["Compliance","Character"],"*subfac": ["Morality","Locus of C"]}, 	#2
		"36___91": {"*fac": ["Intellect","Compliance"],"*subfac": ["Innovation","Systematic"]}, 	#3
		"22___27": {"*fac": ["Intellect","Decision M"],"*subfac": ["Creativity","Deliberati"]}, 	#4
		"43___10": {"*fac": ["Compliance","Commitment"],"*subfac": ["Morality","Achievemen"]}, 	#5
		"20___34": {"*fac": ["Character","Intellect"],"*subfac": ["Composure","Innovation"]}, 	#6
		"73___3": {"*fac": ["Compliance","Commitment"],"*subfac": ["Rule-Follo","Achievemen"]}, 	#7
		"78___54": {"*fac": ["Influentia","Enterprisi"],"*subfac": ["Self-Confi","Proactivit"]}, 	#8
		"13___94": {"*fac": ["Enterprisi","Influentia"],"*subfac": ["Competitiv","Vision"]}, 	#9
		"77___51": {"*fac": ["Influentia","Enterprisi"],"*subfac": ["Self-Confi","Proactivit"]}, 	#10
		"89___66": {"*fac": ["Compliance","Commitment"],"*subfac": ["Systematic","Responsibl"]}, 	#11
		"41___31": {"*fac": ["Compliance","Intellect"],"*subfac": ["Morality","Flexibilit"]}, 	#12
		"52___4": {"*fac": ["Enterprisi","Commitment"],"*subfac": ["Proactivit","Achievemen"]}, 	#13
		"25___63": {"*fac": ["Decision M","Character"],"*subfac": ["Deliberati","Resilience"]}, 	#14
		"58___23": {"*fac": ["Decision M","Intellect"],"*subfac": ["Problem-So","Creativity"]}, 	#15
		"75___82": {"*fac": ["Compliance","Decision M"],"*subfac": ["Rule-Follo","Self-Contr"]}, 	#16
		"68___15": {"*fac": ["Commitment","Enterprisi"],"*subfac": ["Responsibl","Competitiv"]}, 	#17
		"29___72": {"*fac": ["Intellect","Enterprisi"],"*subfac": ["Flexibilit","Risk-Takin"]}, 	#18
		"56___48": {"*fac": ["Enterprisi","Commitment"],"*subfac": ["Proactivit","Perseveran"]}, 	#19
		"74___33": {"*fac": ["Compliance","Intellect"],"*subfac": ["Rule-Follo","Innovation"]}, 	#20
		"18___71": {"*fac": ["Character","Enterprisi"],"*subfac": ["Composure","Risk-Takin"]}, 	#21
		"96___28": {"*fac": ["Influentia","Decision M"],"*subfac": ["Vision","Deliberati"]}, 	#22
		"35___92": {"*fac": ["Intellect","Compliance"],"*subfac": ["Innovation","Systematic"]}, 	#23
		"17___32": {"*fac": ["Character","Intellect"],"*subfac": ["Composure","Flexibilit"]}, 	#24
		"57___19": {"*fac": ["Decision M","Character"],"*subfac": ["Problem-So","Composure"]}, 	#25
		"88___40": {"*fac": ["Influentia","Character"],"*subfac": ["Social Rel","Locus of C"]}, 	#26
		"64___83": {"*fac": ["Character","Decision M"],"*subfac": ["Resilience","Self-Contr"]}, 	#27
		"21___76": {"*fac": ["Intellect","Compliance"],"*subfac": ["Creativity","Rule-Follo"]}, 	#28
		"86___38": {"*fac": ["Influentia","Character"],"*subfac": ["Social Rel","Locus of C"]}, 	#29
		"84___67": {"*fac": ["Decision M","Commitment"],"*subfac": ["Self-Contr","Responsibl"]}, 	#30
		"80___30": {"*fac": ["Influentia","Intellect"],"*subfac": ["Self-Confi","Flexibilit"]}, 	#31
		"65___85": {"*fac": ["Commitment","Influentia"],"*subfac": ["Responsibl","Social Rel"]}, 	#32
		"37___44": {"*fac": ["Character","Compliance"],"*subfac": ["Locus of C","Morality"]}, 	#33
		"87___14": {"*fac": ["Influentia","Enterprisi"],"*subfac": ["Social Rel","Competitiv"]}, 	#34
		"70___59": {"*fac": ["Enterprisi","Decision M"],"*subfac": ["Risk-Takin","Problem-So"]}, 	#35
		"45___16": {"*fac": ["Commitment","Enterprisi"],"*subfac": ["Perseveran","Competitiv"]}, 	#36
		"81___93": {"*fac": ["Decision M","Influentia"],"*subfac": ["Self-Contr","Vision"]}, 	#37
		"26___62": {"*fac": ["Decision M","Character"],"*subfac": ["Deliberati","Resilience"]}, 	#38
		"46___79": {"*fac": ["Commitment","Influentia"],"*subfac": ["Perseveran","Self-Confi"]}, 	#39
		"47___95": {"*fac": ["Commitment","Influentia"],"*subfac": ["Perseveran","Vision"]}, 	#40
		"60___69": {"*fac": ["Decision M","Enterprisi"],"*subfac": ["Problem-So","Risk-Takin"]}, 	#41
		"90___61": {"*fac": ["Compliance","Character"],"*subfac": ["Systematic","Resilience"]}, 	#42
	}

GFI_subfactors = sorted(['Achievemen', 'Rule-Follo', 'Systematic', 'Composure', 'Locus of C', 'Competitiv', 'Deliberati', 'Creativity', 'Proactivit', 'Risk-Takin', 'Problem-So', 'Perseveran', 'Self-Confi', 'Social Rel', 'Flexibilit', 'Innovation', 'Self-Contr', 'Resilience', 'Responsibl', 'Vision', 'Morality'])


'''for k in GFI_pairs: 
	v = randrange(-100,100)
	s = "%d/1"%(-v) if v < 0 else "1/%d"%v
	#print '"%s": {"Answer": "%s"},'%(k,s)'''

#
# read a dictionary of items and raw values (and other stuff): {"1":44,"99":2,"not an item":"whatever"}
# this example yields:
# {'*item':"1","*recoded":2,'*leftright':[A,B]} ......
#

def score_gfi_factors(itemdefs,inputs):

	#------------------------
	# the answer comes as a pair: 77/1 <-- 77 on the left, 1 on the right
	#

	def unsplit(response): # needs work <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

		if "/" in str(response): 
	# crashes for non-integers
			l,r = [int(v) for v in response.split('/')]

			if l > r: 
				return -l
			elif l < r:
				return r
			else:
				return 0
		else:
			return 0 # for now ...

	# process inputs
	for k in inputs:
		if k in itemdefs: 							# make sure this is an item, not some stray stuff
			answer = unsplit(inputs[k]['Answer']) 			# what to do with the / ?
			yield k,{'*raw':answer,'*fac':itemdefs[k]['*fac'],'*sub':itemdefs[k]['*subfac']} #,'*raw':inputs[r]['Answer'],'cuts':cuts} 



@app.route('/gfi/0/',methods=['POST'])

def GFI_0():

	prox_factor 	= prox_choice(GFI_factors,range(-100,101))
	prox_subfactor 	= prox_choice(GFI_subfactors,range(-100,100))

	request_input 	= request.json

	for k,v in score_gfi_factors(GFI_pairs,request_input):

		fac1,fac2 = v['*fac']
		prox_factor.addobs(fac1,fac2,v['*raw'])

		sub1,sub2 = v['*sub']
		prox_subfactor.addobs(sub1,sub2,v['*raw'])

	results = {"*fac": prox_factor.estimate(),"*sub":prox_subfactor.estimate()}

	return jsonify(results)

if __name__ == '__main__':

 app.run(debug=True,host="0.0.0.0")

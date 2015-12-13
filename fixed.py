def pfun(L=["nope"]):
	print "\n\n\n\n\n\n\n\n\n\n current POP\n"
	print L[0]
	#for t in L:
	#	print t
	raw_input()
import genetic
	


def fixed_evolve(opp_strat, ticks):
	POP = genetic.make_pop(50,ticks,5)
	counter = 0
	while True:	
		POP = genetic.newGen(POP, opp_strat, ticks, genetic.breed_discrete_select)
		print POP[0]
		counter = counter +1
		print "itter: {}".format(counter)
		raw_input()

	return 0



def strat1(time):
	return time%500 == 20 or time == 250

def aahlad(time):
	return time%210 == 1

fixed_evolve(strat1, 1500)

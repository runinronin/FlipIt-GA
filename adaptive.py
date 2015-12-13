import genetic

	
def group_density(POP, time):
	n = 0
	for S in POP:
		n = n + indv_density(genetic.expand(S,time), time)
	return n

def indv_density(L, time):
	n = 0
	for l in L:
		if l < time:
			d = 1.0/float((l-time)*(l-time))
			n = n+d
			print "d= {}".format(d)
	return n
#what matters?
#ratio of move penalty over value of one tick control


def democracy(POP, time, LED, strat):
	votes = 0
	dense_factor = 1/25
	board = indv_density(map(lambda x: x[1], filter(lambda x: x[0],LED)),time)
	tot = 0
	for S in POP:
		f = genetic.fitness(S, strat, time)
		tot = tot+f
		k = "no"
		n = indv_density(genetic.expand(S,time),time)
		if n - board> dense_factor:
			k = "yes"
			votes = votes+f
		#print "{} \nround {}.\nvoted:  {}  score:{}\n\n".format(S,time,k,n)
	print "votes: {}".format(votes)#,  board density: {}\nLedger: {}".format(votes, board, LED)
	return float(votes) / tot
	
def opstrat(time):
	return time%250 == 50



def xmove(Led, time):
	Led.append((True, time))
	return list(Led)

def ymove(Led, time):
	Led.append((False, time))

def Adapt(pop, badLed, Led, time):
	k = 0

	if badLed != []:
		k = Led_strat(badLed)

	z = democracy(pop, time, Led, k) 
	if z > .5:
		Led.append((True, time))
		badLed = filter(lambda x: not x[1], Led)
		Kids = genetic.TrainChildren(pop, Led, 10, time)
		print "LED: {}, badLed: {}, time: {}".format(Led, badLed, time)
		for k in Kids:
			print k
		print "umm"
		raw_input()
	elif opstrat(y):
		Led.append((False, time))
	
	return list(pop), list(badLed)

pop = genetic.make_pop(40, 500, 6)
bled, Led = [], []
y = 1
while True:
	pop, bled = Adapt(pop, bled, Led, y)
	y = y+1

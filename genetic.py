import random


def expand(S, cap):
	I,L = S
	ARR = []
	for l in L:
		x = 0
		while x*I + l < cap:
			ARR.append(x*I+l)
			x = x+1
	return ARR


def score(ledger, start, ticks, CTRL=True):
	xPen = 100
	yPen = 100
	xVal = 1
	yVal = 1
	gamelength = 1000

	xscore, yscore = 0,0
	xcon = CTRL
	last = 0	

	for (con, tick) in ledger:
		if con:
			xscore = xscore-xPen
		else:
			yscore = yscore-yPen
		if xcon:
			xscore = xscore + (tick - last)*xVal
		else:
			yscore = yscore + (tick - last)*yVal
		xcon = con
		last = tick
	if xcon:
		xscore = xscore + (ticks - last)*xVal
	else:
		yscore = yscore + (ticks - last)*yVal
	return xscore-yscore
	

def make_pop(n,max,movs):
	L = []
	while len(L) < n:
		x = make_seller(max,movs)
		L.append(x)
	return L

def make_seller(imax, lmax):
	interval = imax#*random.random()
	L = []
	leng = int(random.random()*lmax)
	while len(L) < leng:
		L.append(random.random()*interval)
	L.sort()
	return (interval, L)


def breed_discrete_select(s1,s2):
	selrate = .5
	int_choice_rate = .5
	smooth_rate = .05

	if random.random() < smooth_rate:
		return breed_scale(s1,s2)
	
	int1, L1 = s1
	int2, L2 = s2
	INT = 0
	
	r = random.random()
	if r < int_choice_rate:
		INT = int1
	else:
		INT = int2
		

	L = []
	for l1 in L1:
		if random.random() < selrate:
			if l1 > INT:
				L.append(l1%INT)
			else:
				x = 0
				while x*int1 + l1 < INT:
					L.append(x*int1 + l1)
					x = x+1
	for l2 in L2:
		if random.random() < selrate:
			if l2 > INT:
				L.append(l2%INT)
			else:
				x = 0
				while x*int2 + l2 < INT:
					L.append(x*int2 + l2)
					x = x+1
	L.sort()
	return INT,L

def breed_scale(s1,s2):
	sel_rate = .1

	int1, L1 = s1
	int2, L2 = s2
	x = random.random()
	x = x/2 + .25
	INT = x*int1 + (1-x)*int2

	scale1,scale2 = INT/int1,INT/int2
	L = []

	i,j = 0,0
	for l1 in L1:
		if random.random() < sel_rate:
			L.append(l1*scale1)
	for l2 in L2:
		if random.random() < sel_rate:
			L.append(L2[j]*scale2)
			j = j+1
	L.sort()
	return (INT,L)

def mutate(S):
	del_rate = .05
	chg_rate = .1
	add_rate = 1/40
	
	INT,L1 = S
	L = []

	for l in L1:
		if random.random() <= (1-del_rate):
			if random.random() < chg_rate:
				L.append(l*(1 - random.random()/20))
			else:
				L.append(l)
	if random.random() < add_rate:
		L.append(random.random*INT)

	L.sort()
	return INT,L
		
def fitness(s1, strat, time):
	if strat == 0:
		return 1

	INT, L = s1
	INT2 = int(INT)
	L2 = []
	for l in L:
		L2.append(int(l))
	Led = []
	ticks = 1
	while ticks <= time:
		if ticks % INT2 in L2:
			Led.append((True, ticks))
		elif strat(ticks):
			Led.append((False, ticks))
		ticks = ticks+1
	ch = 0
	if len(L) > 6:
		ch = len(L)-6
	return score(Led, 0, time)-  20*ch# - 5*len(L)

def select(L):
	cap = 100000
	tot = 0
	i = -1
	while tot<cap:
		i = int(random.random()*len(L))
		tot = tot+L[i][1] + 10
	return L[i][0]

def prune(S):
	i,l = S
	if len(l) == 0:
		return i,l
	L = [l[0]]
	idx = 0
	for x in l:
		if int(l[idx]) !=  int(x):
			L.append(x)
			idx = idx+1
	return i,L
	

def Led_strat(Led):
	return lambda x: x in map(lambda y: int(y[1]), Led)


def newGen(POP, opp_strat, ticks, breed):
	brate = .5
	mrate = .25
	S = len(POP)
	NPOP = []
	L = []
	

	for s in POP:
		i,l = s
		L.append((s,fitness(s, opp_strat, ticks)))
	L = sorted(L,key = lambda x: -x[1])
	

	min = L[len(L)-1][1]
	k = lambda x: (x[0], x[1]-min)
	L2 = map(k,L)

	
	NPOP.append(prune(L2[0][0]))


	i = 1
	while i < S:
		i = i+1
		j = 0
		if random.random() < brate:
			j = breed(select(L2),select(L2))
		else:
			j = select(L2)
		if random.random() < mrate:
			j = mutate(j)
		j = prune(j)
		NPOP.append(j)

	return NPOP


def Score(Led):
	if len(Led) == 0:
		return 0
	x = Led[len(Led)-1][1]
	return score(Led,0,x,True)

def sCore(LED, S, time):
	print S
	k = LED+map(lambda x: (True,x),expand(S, time))
	k.append((True, time))
	k.sort(key=lambda x: x[1])
	for K in k:
		print K
	print "\n"
	return Score(k)

def AdaptGen(pop):
	k = len(pop)
	POP = []
	
	

def TrainChildren(pop, Led, itter, time):
	print Led
	print "score is: {}".format(Score(Led))
	raw_input()
	LED = filter(lambda x: not x[0],Led)

	kids = []
	POP = pop
	for i in range(0,itter):
		POP = newGen(POP, Led_strat(LED), time, breed_discrete_select)
		print POP[0]
		print i
	return POP

		

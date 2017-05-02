class TAC :
	def __init__(self,Sym_tab) :
		self.Sym_tab = Sym_tab 
		self.code = {'head' : []}
		self.quad = {'head' : -1}
		self.nq = {'head':0}

	def inc_q(self) :
		cur_scope = self.Sym_tab.scope[-1]['__scope__']
		self.quad[cur_scope] = self.nq[cur_scope]
		self.nq[cur_scope]  += 1

	def emit(self,operator='',out='',in1='',in2='',var1='',var2='') :
		cur_scope = self.Sym_tab.scope[-1]['__scope__']
		self.inc_q()
		strs = ''
		strs = ','+str(operator)
		if not out == '' :
			strs = strs + ','+str(out)
		if not in1 == '':
			strs = strs + ','+str(in1)
		if not in2 == '':
			strs = strs + ','+str(in2)
		if not var1 == '':
			strs = strs + ','+str(var1)
		if not var2 == '':
			strs = strs + ','+str(var2)

		self.code[cur_scope].append(strs)

	def backP(self, lists, loc):
		currentFunction = self.Sym_tab.getCurrentScope()
		
		for position in lists:
			print (self.code[currentFunction][position]), "JEL"
			if self.code[currentFunction][position][1] == 'I' or self.code[currentFunction][position][1] == 'g' :
				
				self.code[currentFunction][position] = self.code[currentFunction][position]+','+str(loc[0]+1)+', '
			

	def noop(self, locationList):
		currentFunction = self.Sym_tab.getCurrentScope()
		for position in locationList:
			self.code[currentFunction][position][3] = 'NOOP'

	def merge(self,list1,list2) :
		list_new = list1
		list_new = list_new+(list2)
		
		return list_new

	def getNQ(self):
		func = self.Sym_tab.getCurrentScope()
		return self.nq[func]
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
		strs = ','+str(operator)+','+str(out)
		if not in1 == '':
			strs = strs + ','+str(in1)
		if not in2 == '':
			strs = strs + ','+str(in2)
		if not var1 == '':
			strs = strs + ','+str(var1)
		if not var2 == '':
			strs = strs + ','+str(var2)

		self.code[cur_scope].append(strs)

	def backP(self, list, loc):
		currentFunction = self.Sym_tab.getCurrentScope()
		for position in list:
			self.code[currentFunction][position][2] = loc

	def merge(self,list1,list2) :
		list_new = list1
		list_new.append(list2)
		return list_new

	def getNQ(self):
		func = self.Sym_tab.getCurrentScope()
		return self.nq[func]
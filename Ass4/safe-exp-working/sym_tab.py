class Sym_tab :
		 def __init__(self):	
			self.sym_tab = {'head' : {'__scope__':'head','__parentscope':'-1','__returns__':'', '__stringList__':'', '__level__':0} }


			self.count = 0
			self.string_cnt = 0
			#We will be adding new scopes when required
			self.scope = [self.sym_tab['head']]
			self.offset = []
			self.addressDescriptor = {}
			self.offset.append(0)


		 def new_temp(self,memlo = '',variable='', load_memory=False):
			self.count = self.count + 1
			name = 't'+str(self.count)		 	
			self.addressDescriptor[name] = { 'memory': None , 
													'register': None, 
													'store': load_memory, 
													'dirty': False,
													'scope': self.scope[len(self.scope)-1]['__scope__'],
													'variable': variable}
			if memlo != '':
				self.addressDescriptor[name]['memory'] = memlo

			return name

		 def getCurrentScope():
			return self.scope[len(scope)-1]['__scope__']

		 def getAttri(self,variable,attribute) :
			entry = self.look_for(variable)
			if ('__'+attribute+'__') in entry :
				return entry['__'+attribute+'__']
			else :
				return None



		 def label_string(self) :
			self.string_cnt += 1
			return '__string' + str(self.string_cnt) + '__'

		 def lookupScope(self, identifier, scopeLocation):
			if scopeLocation == -1:
				return None
			
			currentScope = self.scope[scopeLocation]
			
			if currentScope.has_key(identifier):
				return currentScope[identifier]
			else:
				return self.lookupScope(identifier, scopeLocation - 1)

		 def add_S_list(self,label,string) :
			len_scope = len(self.scope) 
			currentScope = self.scope[len_scope - 1]
			currentScope['__stringList__'].append([label,string])

		 def look_for(self, variable) :
			scope_loc = len(self.scope) -1
			return self.lookupScope(variable, scope_loc)

		 def add_attri(self,identifier,name,value) :
			entry = self.look_for(identifier) 
			entry['__'+name+'__'] = value
			return 	


		 def addID(self,identifier, type,width=0) :
		 	if type == 'NUMBER' :
		 		width = 4
		 	if type == 'STRING' :
		 		width = 4

		 	offset = self.offset.pop()
		 	scopes = self.scope[len(self.scope)-1]
		 	if not identifier in self.scope[len(self.scope)-1] :
		 		scopes[identifier] = {}
		 	
		 	scopes[identifier]['__width__'] = width
		 	scopes[identifier]['__type__'] = type
		 	scopes[identifier]['__offset__'] = offset
		 	scopes[identifier]['__scopelevel__'] = scopes['__level__']

		 	self.offset.append(offset + width)





		 def exists(self,variable) :
			entry = self.look_for(variable)
			if entry == None :
				return False
			else :
				return True





		

h  = Sym_tab()
print h.new_temp()
# Yacc example
import sym_tab
from ply import *
import logging
import TAC
import sys

# Get the token map from the lexer.  This is required.
from lexer import lexer,tokens

line_no = 1


#Denotes the start expression 
def p_start(p):
  '''start :  compstmt    '''
  i=1
  
  
  for x in TAC.code :
	for z in TAC.code[x] :
	  if z[-1] == ',':
		z = z[:-1]
	  print str(i)+z

	  i += 1
  print str(i)+',exit'

  sys.stdout = open('./test/kane.txt', 'w')
  i = 1
  for x in TAC.code :
	for z in TAC.code[x] :
	  if z[-1] == ',':
		z = z[:-1]
	  print str(i)+z

	  i += 1
  print str(i)+',exit'

  #print TAC.code 

#For reducing to expression 
def p_compstmt(p):
  '''compstmt : STMT compstmt 
			| STMT  M_state'''
  # p[0] = p[1]
  # print p[1]
  # TAC.backP(p[1]['nextList'],p[2]['instr'] )
  # p[0]['nextList'] = p[3]['nextList']
  p[0] = {}

  # break statements and continue statements need to pushed up
  p[0]['loopEndList'] = TAC.merge(p[1].get('loopEndList', []), p[2].get('loopEndList', []))
  p[0]['loopBeginList'] = TAC.merge(p[1].get('loopBeginList', []), p[2].get('loopBeginList', []))

def p_M_state(p) :
  ''' M_state : empty '''
  p[0] = {}





precedence = (
		('left', 'OP_OR'),
		('left', 'OP_AND'),
		('left', 'EQUALS', 'double_equals'),
		('left', 'less_than', 'greater_than', 'lessthan_equals', 'greater_than_equals'),
		('left', 'Add', 'MINUS'),
		('left', 'Multiply', 'DIVIDE', 'Percentage'),
		('right', 'UMINUS', 'Exclaimation'),
		)



def p_ARG_operations(p) :
  ''' EXPR :  EXPR Add EXPR 
		  | EXPR MINUS EXPR 
		  | EXPR Multiply EXPR
		  | EXPR DIVIDE EXPR 
		  | EXPR Percentage EXPR'''

  p[0] = {}
  p[0]['place'] = sym_tab.new_temp()
  
  types = ''
  if p[2] == '*' :
	p[2] = 'X'
  if p[1]['type'] == 'NUMBER' and p[3]['type'] == 'NUMBER' : 
	types = 'NUMBER'
	TAC.emit(p[2],p[0]['place'], p[1]['place'], p[3]['place'])    
	p[0]['code'] = []
	p[0]['code']= [(p[2]+','+str(p[0]['place'])+','+str(p[1]['place'])+','+str(p[3]['place'])) ]

	

  else:
	debug.printError('Type Mismatch')

  p[0]['type'] = types

  
def p_statement_conditionals(p) :
  ''' STMT : ifThen M_quad 
		   | ifThenElse M_quad
		   | whiles M_quad'''

  p[0] = {}

  nextList = p[1].get('nextList', [])
  print p[1], "HELL"

  TAC.backP(nextList, p[2]['quad'])

  # break statements and continue statements need to pushed up
  p[0]['loopEndList'] = p[1].get('loopEndList', [])
  p[0]['loopBeginList'] = p[1].get('loopBeginList', [])






def p_ARG_relational(p) :
  ''' STMT : ASGN M_quad SemiColon  
		   | PRINTS M_quad SemiColon
		   | func M_quad SemiColon'''

  p[0] = {}

  nextList = p[1].get('nextList', [])
  TAC.backP(nextList, p[2]['quad'])
  p[0]['loopEndList'] = p[1].get('loopEndList', [])
  p[0]['loopBeginList'] = p[1].get('loopBeginList', [])

def p_ASGN_basic(p) :
  '''ASGN : Identifier EQUALS EXPR '''
  p[0] = {}
  place = None
  if sym_tab.exists(p[1]):
	
	sym_tab.add_attri(p[1], 'type', p[3]['type'])

	if p[1] in sym_tab.scope[len(sym_tab.scope)-1] :
	  place = sym_tab.getAttri(p[1],sym_tab.scope[len(sym_tab.scope)-1]['__scope__'])
	else :
	  disp_val = sym_tab.getAttri(p[1],'level')
	  offset = sym_tab.getAttri(p[1],'offset')
	  place = sym_tab.new_temp((disp_val, offset), variable=p[1])
	  sym_tab.add_attri(p[1],sym_tab.scope[len(self.scope) - 1]['__scope__'],p[1])
	TAC.emit('=',place,str(p[3]['place']),'')
	  # if p[1] == 'a' and p[3]['place'] == '3' :
	  #   print "HOLLO"
	print p[3], "OKY" , p[1]
	p[0]['code']=p[3]['code']+['='+','+str(place)+','+str(p[3]['place']) +','+'' ]
  else :
	sym_tab.addID(p[1], p[3]['type'])
	

	# Create a temporary for the current scope
	displayValue, offset = sym_tab.getAttri(p[1], 'scopeLevel'), sym_tab.getAttri(p[1], 'offset')
	place = sym_tab.new_temp((displayValue, offset), variable=p[1])
	sym_tab.add_attri(p[1], sym_tab.scope[len(sym_tab.scope)-1]['__scope__'], p[1])
	TAC.emit('=',p[1],str(p[3]['place']),'')

	#p[0]['code']=p[3]['code']+['='+','+str(p[1])+','+str(p[3]['place']) +','+'' ]



  
	




  
  
  
  




def p_ARG_others(p):
  ''' EXPR :   PRIMARY '''

  # p[0]['place'] = p[1]['place']
  # p[0]['code'] = p[1]['code']
  p[0] = p[1]
 

  

def p_variable(p):
  '''VARIABLE : VARNAME '''
  p[0] = {}
  p[0] = p[1]







def p_LHS(p):
  ''' LHS : VARIABLE '''
  p[0] = {}
  p[0] = p[1]
  

def p_varname(p) :
  ''' VARNAME : Identifier '''

  p[0] = {}
  
  if sym_tab.exists(p[1]):

		p[0]['type'] = sym_tab.getAttri(p[1], 'type')

		# Here we have to load in the value of the variable
		if not p[1] in sym_tab.scope[len(sym_tab.scope)-1]:


			# If an identifier is used, we assume that it is present in memory
			displayValue, offset = sym_tab.getAttri(p[1], 'scopeLevel'), sym_tab.getAttri(p[1], 'offset')
			p[0]['place'] = sym_tab.newTemp((displayValue, offset), variable=p[1], loadFromMemory=True)
			sym_tab.addAttribute(p[1], sym_tab.getCurrentScope(), p[0]['place'])
		else:
			p[0]['code'] = []
			p[0]['place'] = sym_tab.getAttri(p[1],sym_tab.scope[len(sym_tab.scope)-1]['__scope__'] )
  else :
	 print "FUCK OFF"
  
  


def p_PRIMARY_variable(p) :
  ''' PRIMARY : VARIABLE'''
  p[0] = {}
  p[0] = p[1]

def p_relation_operations(p) :
  ''' EXPR  : EXPR less_than EXPR
			| EXPR greater_than EXPR
			| EXPR lessthan_equals EXPR
			| EXPR greater_than_equals EXPR
			| EXPR double_equals EXPR
			| EXPR Exclaim1 EXPR '''

  oper = ''
  if p[2] == '<' :
	oper = 'jl'
  if p[2] == '>' :
	oper = 'jg'
  if p[2] == '<=' :
	oper = 'jle'
  if p[2] == '>=' :
	oper = 'jge'
  if p[2] == '==' :
	oper = 'je'
  if p[2] == '!=' :
	oper = 'jne'




  # str1 = 'IFgoto,'+oper+','+p[1]+','+p[3]+ ','+p[0]['true']
  # str2 = 'goto,'+ p[0]['false']
  # p[0]['code'] = p[1]['code'] + p[3]['code']+[str1]+ []

  ##Old code starts ***************
  # types = 'UNDEFINED'

  # if p[1]['type'] == p[3]['type'] == 'NUMBER':
  #       types = 'BOOLEAN'
 
  # p[0] = { 'type' : types }
  # p[0]['place'] = sym_tab.new_temp()

  p[0] = {}
  p[0]['truelist'] = [TAC.getNQ()]
  p[0]['falseList'] = [TAC.getNQ()+1]
  print p[0]['truelist'], p[0]['falseList']
  
  TAC.emit('IFgoto',oper,p[1]['place'],p[3]['place'])
  TAC.emit('goto')

  #   # Emit code
  # TAC.emit(p[2],p[0]['place'], p[1]['place'], p[3]['place'])
  # p[0]['code'] = p[2]+","+str(p[0]['place'])+","+str(p[1]['place'])+","+ str(p[3]['place'])
  #END ***********************


def p_PRIMARY_conditionals(p) :
  ''' whiles : WHILE M_quad EXPR DO M_quad compstmt END'''

  p[0] = {}
  p[0]['nextList'] = []
  print p[3], "KANE"
  list1 = p[6].get('nextList',[])
  TAC.backP(list1, p[2]['quad'])
  print (p[3])
  TAC.backP(p[3]['truelist'],p[5]['quad'])
  p[0]['nextList'] = p[3]['falseList']
	

	# Loop around
  TAC.emit( 'goto',p[2]['quad'][0]+1,",")


  


def p_m_while(p):
	'M_while : empty'

	p[0] = {}
	p[0]['falseList'] = [TAC.getNQ()]
	

def p_mark(p):
	'M_quad : empty'
	p[0] = {}
	p[0] = { 'quad' : [TAC.getNQ()]}



def p_primary_IF(p) :
  ''' ifThen : IF EXPR THEN M_ifB compstmt END '''
  p[0] = {}
  
  TAC.backP(p[2]['truelist'], p[4]['instr'])
  list1 = p[2].get('falseList',[])
  list2 = p[5].get('nextList', [])
  
  p[0]['nextList'] = TAC.merge(list1 , list2)
  print p[0]['nextList'], "COW"

  print p[2], "LEGAL"
  p[0]['loopEndList'] = p[5].get('loopEndList', [])
  p[0]['loopBeginList'] = p[5].get('loopBeginList',[])


def p_primary_ifthen(p) :
  ''' ifThenElse : IF EXPR THEN M_ifB compstmt ELSE N_rare M_ifB compstmt END '''
  p[0] = {}
  TAC.backP(p[2]['truelist'],p[4]['instr'])
  TAC.backp(p[2]['falseList'],p[8]['instr'] )
  temp = TAC.merge(p[5]['nextList'], p[7]['nextList'])
  p[0]['nextList'] = TAC.merge(temp,p[9]['nextList'] )

def p_N_rare(p) :
  '''N_rare : empty '''
  p[0]['nextList'] = [TAC.getNQ()]
  TAC.emit('goto')

def p_M_ifB(p) :
  ''' M_ifB : empty '''
  p[0] = {}
  p[0]['instr'] = [TAC.getNQ()]


def p_PRIMARY_function(p):
  '''func : DEF Identifier complex22 LPAREN ARGLIST RPAREN complex33 DO compstmt END  '''
  TAC.noop(p[9]['loopEndList'])
  TAC.noop(p[9]['loopBeginList'])

  
  TAC.emit('return')

  
  functionName = p[3]['name_fun']
  sym_tab.scope.pop()
  sym_tab.offset.pop()

  
  p[0] = { 'type' : 'FUNCTION', 'name_fun': functionName }

def p_complex22(p) :
  ''' complex22 : empty '''
  p[0] = {}
  p[0]['name_fun'] = sym_tab.get_name()
  
  sym_tab.addID(p[-1], "function")
  displayValue, offset = sym_tab.getAttri(p[-1], 'level'), sym_tab.getAttri(p[-1], 'offset')
  place = sym_tab.new_temp((displayValue, offset), variable=p[-1])
  sym_tab.add_attri(p[-1], sym_tab.getCurrentScope(), place)
  sym_tab.add_attri(p[-1], 'name_fun', p[0]['name_fun'])
  TAC.emit('label',p[0]['name_fun'])
  sym_tab.add_Sc(p[0]['name_fun'])
  TAC.code[p[0]['name_fun']] = []
  TAC.quad[p[0]['name_fun']] = 0
  qTAC.nq[p[0]['name_fun']] = -1

def p_complex33(p) :
  '''complex33 : empty '''
  for args in p[-2] :
	print args
	sym_tab.addID(args['name'],args['type'])
	displayValue, offset = sym_tab.getAttri(args['name'], 'level'), sym_tab.getAttri(argument['name'], 'offset')
	place = sym_tab.new_temp((displayValue, offset), variable=argument['name'], loadFromMemory=True)
	sym_tab.addAttri(args['name'],  sym_tab.getCurrentScope(), place)
  ST.addAttributeToCurrentScope('numParam', len(p[-2]))

def p_arglist(p) :
  ''' ARGLIST :  Identifier '''
  p[0] = {name : p[1]}
  p[0]['type'] = ''

  p[0] = [p[1]]

def p_arglist(p) :
  ''' ARGLIST : empty '''
  p[0] = []


def complex0(p) :
  ''' complex0 : ELSIF EXPR THEN compstmt 
			   | empty'''

def p_complex2(p):
  '''complex2 : ELSE compstmt 
			  | empty'''


def p_PRIMARY_LITERAL(p):
  ''' PRIMARY : LITERAL '''
  p[0] = {}
  var = ''
  if 'reference' in p[1].keys():
	var = p[1]['reference']
  else :
	var = p[1]['value']
  p[0] = { 'type' : p[1]['type']}
  p[0]['place'] = sym_tab.new_temp()
  #sym_tab.count = sym_tab.count + 1
  


  

  if p[1]['type'] == 'STRING' :
	p[0]['reference'] = p[1]['reference']
	TAC.emit('=',p[0]['place'],p[1]['reference'],'')
	
	p[0]['code'] = p[1]['code']+[('='+','+str(p[0]['place'])+','+str(p[1]['reference'])+','+'') ]
  else : 
	TAC.emit('=',p[0]['place'],p[1]['value'],'')
	print "MON" , TAC.getNQ(), p[1]['value'], (TAC.code)
	p[0]['code'] = p[1]['code']+ [('='+','+str(p[0]['place'])+','+str(p[1]['value'])+','+'') ]  
	print TAC.getNQ(), "JOKE"
  
  
def p_express_or(p) :
  ''' EXPR : EXPR OP_OR M_quad EXPR'''
  p[0] = {}
  TAC.backP(p[1]['falseList'],p[3]['quad'])
  p[0]['truelist'] = TAC.merge(p[1]['truelist'], p[4]['truelist'])
  p[0]['falseList'] = p[4]['falseList']

def p_expression_bracket(p) :
  ''' EXPR : LPAREN EXPR RPAREN '''
  p[0]= {}

  p[0] = p[2]

def p_express_not(p) :
  '''EXPR : Exclaimation EXPR '''
  p[0] = {}
  p[0]['truelist'] = p[1]['falseList']
  p[0]['falseList'] = p[0]['truelist']

def p_express_and(p) :
  ''' EXPR : EXPR OP_AND M_quad EXPR'''
  TAC.backP(p[1]['truelist'],p[3]['quad'])
  p[0] = {}
  p[0]['truelist'] =  p[4]['truelist']
  p[0]['falseList'] = TAC.merge(p[1]['falseList'], p[4]['falseList'])

def p_literal_string(p):
  '''LITERAL    : STRING '''
  p[0] = {'type' : 'STRING' , 'value' : p[1], 'reference': Sym_tab.nameString() }

  Sym_tab.add_S_list(p[0]['reference'], p[1])
  p[0]['code'] = []
  
def p_literal_number(p):
  '''LITERAL    :  NUMBER '''
  p[0] = { 'type' : 'NUMBER', 'value' : p[1]}
  p[0]['code'] = []


def p_print_list(p) :
  '''PRINTS : PUTS LISTS '''
  p[0] = {}
  for vals in p[2] :
	TAC.emit('call','print',vals['place'],vals['type'])

def p_List(p) :
  ''' LISTS : EXPR Seperator LISTS 
		   | EXPR 
		   | empty'''     
  if len(p) > 2 :
	  p[0] = [ { 'place': p[1]['place'], 'type' : p[1]['type'] } ] + p[3]
  else :
	 p[0] = [ { 'place': p[1]['place'], 'type' : p[1]['type'] } ]




#The epsilon or empty one
def p_empty(p):
	'empty :'
	p[0] = 1
	pass


# Error rule for syntax errors
def p_error(p):
	print("Syntax error in input!")




# Build the parser
logging.basicConfig(
	level = logging.DEBUG,
	filename = "parselog.txt",
	filemode = "w",
	format = "%(filename)10s:%(lineno)4d:%(message)s"
)
log = logging.getLogger()
sym_tab = sym_tab.Sym_tab()
TAC = TAC.TAC(sym_tab)
parser = yacc.yacc(debug=True, debuglog=log)




# for function in TAC.code.keys :
#   print function,":"
#   for i in range(len(TAC.code[function])):
#     codePoint = TAC.code[function][i]
#     print "%5d: \t%s" %(i, codePoint)

#print lines
s = ''' a = 5;

c = 10;
if a != 6 then
  while ( a < 10 || c > 8 ) do
    puts a;
    a = a + 1;
  end
puts c;
end




'''
					
					 

result = parser.parse(s, lexer = lexer, debug = log)

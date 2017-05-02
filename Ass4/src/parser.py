# Yacc example
import sym_tab
from ply import *
import logging
import TAC


# Get the token map from the lexer.  This is required.
from lexer import lexer,tokens

line_no = 1


#Denotes the start expression 
def p_start(p):
  '''start :  compstmt    '''
  i = 1
  for lines in TAC.code['head'] :
    print str(i)+lines
    i += 1
  print str(i)+',exit'

  
  #print TAC.code 

#For reducing to expression 
def p_compstmt_1(p):
  '''compstmt :  compstmt M_quad STMT '''
  p[0] = {}
  TAC.backP(p[1]['nextlist'],p[2]['instr'])
  p[0]['nextlist'] = p[3]['nextlist']
  

def p_compstmt_2(p):
  '''compstmt : STMT complex1 '''
  p[0] = {}
  p[0]['nextlist'] = p[1]['nextlist']



def p_STMT(p) :
  ''' STMT : EXPR  '''
  p[0] = p[1]


def p_expre_return(p):
  ''' EXPR : RETURN ARG SemiColon '''

  TAC.emit('return',p[2])

# def p_returns(p) :
#   ''' RETURNS : RETURN ARG '''


def p_EXPR_new(p) :
  ''' EXPR : ARG '''

  p[0] = p[1]

def p_EXPR(p) :
  '''EXPR : ARG M_quad SemiColon '''
  p[0] = {}

  if 'nextlist' in p[1].keys():
    p[0]['nextlist'] = p[1]['nextlist']
    TAC.backP(p[1]['nextlist'],p[2]['instr'])
  else:
    p[0]['nextlist'] = []
    TAC.backP([],p[2]['instr'])

  
    

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
  ''' ARG :  ARG Add ARG 
          | ARG MINUS ARG 
          | ARG Multiply ARG 
          | ARG DIVIDE ARG '''

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

  






def p_ARG_relational(p) :
  ''' ARG : Identifier EQUALS ARG '''

  p[0] = {}
  
  place = None
  
  
  if sym_tab.exists(p[1]):
    
    sym_tab.add_attri(p[1])

    if p[1] in sym_tab.scope[len(sym_tab.scope)-1] :
      place = sym_tab.getAttri(p[1],sym_tab.scope[len(sym_tab.scope)-1]['__scope__'])
    else :
      disp_val = sym_tab.getAttri(p[1],'scopelevel')
      offset = sym_tab.getAttri(p[1],'offset')
      place = sym_tab.new_temp((disp_val, offset), variable=p[1])
      sym_tab.add_attri(p[1],sym_tab.scope[len(self.scope) - 1]['__scope__'],p[1])
      TAC.emit('=',p[1],str(p[3]['place']),'')
      p[0]['code']=p[3]['code']+['='+','+str(p[1])+','+str(p[3]['place']) +','+'' ]
  else :
    
    sym_tab.addID(p[1], p[3]['type'])
    

    # Create a temporary for the current scope
    displayValue, offset = sym_tab.getAttri(p[1], 'scopeLevel'), sym_tab.getAttri(p[1], 'offset')
    place = sym_tab.new_temp((displayValue, offset), variable=p[1])
    sym_tab.add_attri(p[1], sym_tab.scope[len(sym_tab.scope)-1]['__scope__'], p[1])
    TAC.emit('=',p[1],str(p[3]['place']),'')

    p[0]['code']=p[3]['code']+['='+','+str(p[1])+','+str(p[3]['place']) +','+'' ]



  


def p_PRIMARY_function(p):
  '''PRIMARY : DEF Identifier  ARGDECL DO compstmt END  '''

  TAC.emit('label',p[2])
  sym_tab.scope.pop()
  sym_tab.offset.pop()

  p[0] = {'type' : 'FUNCTION' }



def p_complex145(p):
  '''complex145 : empty'''
  p[0] = {}
  p[0]['name_fun'] = sym_tab.get_name()
  print p[0]
  sym_tab.addID(p[-1], "function")
  displayValue, offset = sym_tab.getAttri(p[-1], 'level'), sym_tab.getAttri(p[-1], 'offset')
  place = sym_tab.new_temp((displayValue, offset), variable=p[-1])
  sym_tab.add_attri(p[-1], sym_tab.getCurrentScope(), place)
  sym_tab.add_attri(p[-1], 'name_fun', p[0]['name_fun'])
  sym_tab.add_Sc(p[0]['name_fun'])
  TAC.code[p[0]['name_fun']] = []
  TAC.quad[p[0]['name_fun']] = 0
  TAC.nq[p[0]['name_fun']] = -1



def p_ARGDECL(p):
  ''' ARGDECL : LPAREN ARGLIST RPAREN '''
  p[0] = []
  p[0] = p[2]


def p_ARGLIST(p):
  ''' ARGLIST : Identifier complex2000 
              | empty'''
  
  if len(p) > 2:
    p[0] = [p[1]]+ p[2]
  else :
    p[0] = []
  

def p_complex2000(p):
  '''complex2000 : Seperator Identifier complex2000 
                 | empty'''
  
  if len(p) > 2 :
    p[0] = [p[1]] + p[3]
  else :
    p[0] = []

def p_complex169(p):
  '''complex169 : empty '''
  for args in p[-2] :
    print args
    sym_tab.addID(args['name'],args['type'])
    displayValue, offset = sym_tab.getAttri(args['name'], 'level'), sym_tab.getAttri(argument['name'], 'offset')
    place = sym_tab.new_temp((displayValue, offset), variable=argument['name'], loadFromMemory=True)
    sym_tab.addAttri(args['name'],  sym_tab.getCurrentScope(), place)





def p_ARG_others(p):
  ''' ARG :   PRIMARY '''

  # p[0]['place'] = p[1]['place']
  # p[0]['code'] = p[1]['code']
  p[0] = p[1]
 

  

def p_variable(p):
  '''VARIABLE : VARNAME '''
  p[0] = {}
  p[0] = p[1]




def p_literal_fpnumber(p):
  '''LITERAL    : FPNUMBER'''





def p_LHS(p):
  ''' LHS : VARIABLE '''

  p[0] = {}
  p[0] = p[1]
  

def p_varname(p) :
  ''' VARNAME : Identifier '''

  p[0] = {}
  
  if sym_tab.exists(p[1]):      
        p[0]['type'] = sym_tab.getAttri(p[1], 'type')      
        p[0]['code'] = ['']  
        if not p[1] in sym_tab.scope[len(sym_tab.scope)-1]:            
            displayValue = sym_tab.getAttri(p[1], 'scopeLevel')
            offset = sym_tab.getAttri(p[1], 'offset')
            p[0]['place'] = sym_tab.newTemp((displayValue, offset), variable=p[1], loadFromMemory=True)
            sym_tab.addAttribute(p[1], sym_tab.getCurrentScope(), p[0]['place'])
        else:
            p[0]['place'] = sym_tab.getAttri(p[1],sym_tab.scope[len(sym_tab.scope)-1]['__scope__'] )
 
  



def p_PRIMARY_variable(p) :
  ''' PRIMARY : VARIABLE'''
  p[0] = {}
  p[0] = p[1]



def p_relation_operations(p) :
  ''' ARG : ARG less_than ARG
          | ARG greater_than ARG
          | ARG lessthan_equals ARG
          | ARG greater_than_equals ARG
          | ARG double_equals ARG
          | ARG Exclaim1 ARG '''
  types = 'UNDEFINED'
  
  if p[1]['type'] == 'NUMBER' and p[3]['type'] == 'NUMBER':
        types = 'BOOLEAN'
  else:
        expType = 'error'
        debug.printError('Operands to relational expressions must be numbers')
        raise SyntaxError

  p[0] = { 'type' : types }
  p[0]['place'] = sym_tab.new_temp()

    # Emit code
  var = ''
  if var == '<' :
    var = 'jl'
  if var == '>' :
    var = 'jg'
  if var == '>=':
    var = 'jge'
  if var == '<=' :
    var = 'jle' 
  if var == '==' :
    var = 'je'

  p[0]['truelist'] = []
  p[0]['truelist'].append(TAC.getNQ())
  p[0]['falseList'] = []
  p[0]['truelist'].append(TAC.getNQ()+1)
  TAC.emit('IFgoto',var,p[1]['place'],p[3]['place'],'__')
  TAC.emit('goto','__')
  # p[0]['code'] =  p[1]['code'] + p[3]['code'];
  # p[0]['code'] = p[0]['code'] + ['IFgoto,'+var+','+p[1]['code']+','+p[2]['code']+',__']
  # p[0]['code'] = [p[2]+","+str(p[0]['place'])+","+str(p[1]['place'])+","+ str(p[3]['place']) ]

def p_PRIMARY_conditionals(p) :
  ''' PRIMARY : WHILE M_quad EXPR DO M_while compstmt END '''

  p[0] = {}
  p[0]['nextlist'] = []

  if p[3]['type'] == 'BOOLEAN' :
    TAC.backP(p[6]['nextlist'] , p[2]['instr'])
    TAC.backP(p[3]['truelist'] , p[5]['instr'])
    p[0]['nextlist'] = p[3]['falseList']



    # Loop around
    TAC.emit('goto',p[2]['instr'])
    
  else:
        debug.printError('The condition should be a proper BOOLEAN')
        raise SyntaxError

  p[0]['type'] = 'VOID'


def p_m_while(p):
    'M_while : empty'

    p[0] = {}
    p[0]['instr'] = [TAC.getNQ()]
    
    #TAC.emit(p[-2]['place'], '', -1, 'COND_GOTO_Z')
    #Something Missing

def p_mark(p):
    'M_quad : empty'
   
    p[0] = {}
    p[0]['instr'] = [TAC.getNQ()]





def p_PRIMARY_LITERAL(p):
  ''' PRIMARY : LITERAL '''
  p[0] = {}
  p[0] = { 'type' : p[1]['type']}
  p[0]['place'] = sym_tab.new_temp()
  #sym_tab.count = sym_tab.count + 1
 
  


  

  if p[1]['type'] == 'STRING' :
    p[0]['reference'] = p[1]['reference']
    TAC.emit('=',p[0]['place'],p[1]['reference'],'')
    p[0]['code'] = p[1]['code']+[('='+','+str(p[0]['place'])+','+str(p[1]['reference'])+','+'') ]
  else : 
    TAC.emit('=',p[0]['place'],p[1]['value'],'')
    p[0]['code'] = p[1]['code']+ [('='+','+str(p[0]['place'])+','+str(p[1]['value'])+','+'') ]  
  
  
  


def p_literal_string(p):
  '''LITERAL    : STRING '''
  p[0] = {'type' : 'STRING' , 'value' : p[1], 'reference': Sym_tab.nameString() }

  Sym_tab.add_S_list(p[0]['reference'], p[1])
  p[0]['code'] = []
  
def p_literal_number(p):
  '''LITERAL    :  NUMBER '''
  p[0] = { 'type' : 'NUMBER', 'value' : p[1]}
  p[0]['code'] = []

def p_complex1(p) :
  ''' complex1 : empty '''
  
     



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
s = ''' def akhil() do
  i = 2;
  end
  
'''
                    
result = parser.parse(s, lexer = lexer, debug = log)
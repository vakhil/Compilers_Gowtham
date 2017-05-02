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
  i=1

  for x in TAC.code :
    for z in TAC.code[x] :
      if z[-1] == ',':
        z = z[:-1]
      print str(i)+z

      i += 1
  #print TAC.code 

#For reducing to expression 
def p_compstmt(p):
  '''compstmt :  STMT  compstmt  
            | STMT complex1 '''
  


def p_STMT(p) :
  ''' STMT : EXPR  '''

def p_EXPR(p) :
  ''' EXPR : ARG '''


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
  ''' ARG : Identifier EQUALS ARG SemiColon       '''

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
    print p[3], "FOOO"

    # Create a temporary for the current scope
    displayValue, offset = sym_tab.getAttri(p[1], 'scopeLevel'), sym_tab.getAttri(p[1], 'offset')
    place = sym_tab.new_temp((displayValue, offset), variable=p[1])
    sym_tab.add_attri(p[1], sym_tab.scope[len(sym_tab.scope)-1]['__scope__'], p[1])
    TAC.emit('=',p[1],str(p[3]['place']),'')
    p[0]['code']=p[3]['code']+['='+','+str(p[1])+','+str(p[3]['place']) +','+'' ]



  print p[3], "RANDi"


  




  
  
  
  




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

        # Here we have to load in the value of the variable
        if not p[1] in sym_tab.scope[len(sym_tab.scope)-1]:


            # If an identifier is used, we assume that it is present in memory
            displayValue, offset = sym_tab.getAttri(p[1], 'scopeLevel'), sym_tab.getAttri(p[1], 'offset')
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

  if p[1]['type'] == p[3]['type'] == 'NUMBER':
        types = 'BOOLEAN'
  else:
        expType = 'error'
        debug.printError('Operands to relational expressions must be numbers')
        raise SyntaxError

  p[0] = { 'type' : type }
  p[0]['place'] = sym_tab.new_temp()

    # Emit code
  TAC.emit(p[2],p[0]['place'], p[1]['place'], p[3]['place'])
  p[0]['code'] = p[2]+","+str(p[0]['place'])+","+str(p[1]['place'])+","+ str(p[3]['place'])

def p_PRIMARY_conditionals(p) :
  ''' PRIMARY : WHILE M_quad EXPR DO M_while compstmt END '''

  p[0] = {}
  p[0]['nextl'] = []

  if p[2]['type'] == 'BOOLEAN' :
    TAC.backP(p[6]['loopBeginList'], p[2]['quad'])
    p[0]['nextList'] = TAC.merge(p[6].get('loopEndList', []), p[6].get('nextList', []))
    p[0]['nextList'] = TAC.merge(p[5].get('falseList', []), p[5].get('nextList', []))

    # Loop around
    TAC.emit( 'GOTO',p[2]['quad'],'','')
  else:
        debug.printError('The condition should be a proper BOOLEAN')
        raise SyntaxError

  p[0]['type'] = 'VOID'


def p_m_while(p):
    'M_while : empty'

    p[0] = {}
    p[0]['falseList'] = [TAC.getNQ()]
    TAC.emit(p[-2]['place'], '', -1, 'COND_GOTO_Z')

def p_mark(p):
    'M_quad : empty'

    p[0] = { 'quad' : TAC.getNQ()}





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
s = ''' require("good")

#Lats code in the modules

masch = Addition.parse('+')
    assert(masch)
    assert(masch.matches)
    assert_equal(2, masch.matcheslength)
'''
                    
                     
import sys

file_name = sys.argv[1]
#file_name = raw_input()
open_file = "../"+file_name

print open_file
with open(open_file) as f:
   liness = f.read()  
print liness

result = parser.parse(liness, lexer = lexer, debug = log)
#print( result )

finale = file_name.split("/")
finals = finale[1].split(".")

kane = finals[0]+ ".html"
sys.stdout = open(kane, 'w')

lines = [line.rstrip('\n') for line in open('parselog.txt')]
lines.reverse()
start = "start"

print "<html> \n <body> "
finals = ""
for line in lines :
  print "<p> ",
  brake = line.split("yacc.py: ")
  shake = []
  hell = []
  if brake[1][0] == '4' and brake[1][1] == '6' and brake[1][2] == '9':
    #print "<p>"
    shake =  brake[1].split("[")
    hell = shake[1].split("]")
    #hell0 contains the derivation
    kane = hell[0].split(" -> ")
    #print kane
    
    goats = start.split()
    fox = start.split()
    fox.reverse()
    i = 0
    

    for home in fox :
      if not home == kane[0] :

        i = i -1
        continue
      else :

       i = i -1
       break

    j = 0 

    for items in goats :
      if j == len(goats)+i:
        print "<b> "+ items + " </b> ",
      else :
        print items + " ",
      j = j + 1

    print ""

    goats[i] = ""

    required = kane[1].split()


    
    
    #print (start) + "JEL"
    
    #print (required)
    
    for strs in required:
      goats[i] =  goats[i] + " " + strs 

    


    


    final = ""
    for holm in goats:
      final = final + " " + holm

    start = final
    finals = final
    print "</p> "
print "<p>", finals ,"</p>"
#print "</body> \n </html>"
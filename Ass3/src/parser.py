# Yacc example

from ply import *
import logging


# Get the token map from the lexer.  This is required.
from lexer import lexer,tokens



#Denotes the start expression 
def p_start(p):
  'start :  compstmt'
  
  

#For reducing to expression 
def p_compstmt(p):
  '''compstmt : STMT complex1  
            | empty '''
  

def p_complex1(p): 
  '''complex1 :  EXPR complex1
              | empty '''
  
def p_complex2(p) :
  ''' complex2 : TERM 
               | empty'''

  
def p_term(p):
  ''' TERM : newline  TERMS
           | SemiColon TERMS '''

def p_TERMS(p):
  '''TERMS : newline TERMS
           | SemiColon TERMS
           | empty '''

def p_term1(p):
  ''' term1 : newline
            |  empty '''


def p_stmt(p) :
  ''' STMT    : EXPR   '''


def p_expr(p) :
  ''' EXPR    : ARG'''



def p_arg(p) :
  ''' ARG   : target EQUALS ARG TERMS       
            | ARG operation ARG
            | Exclaimation ARG TERMS
            | PRIMARY '''

def p_operation(p):
   ''' operation : DOT DOT 
                  | DOT DOT DOT
                  |  Add 
                  |  MINUS 
                  |  Multiply 
                  |  DIVIDE 
                  |  Percentage 
                  |  Exponent 
                  |  OR 
                  |  CARROT 
                  |  AND 
                  |  less_equal_more 
                  |  greater_than 
                  |  greater_than_equals  
                  |  less_than 
                  |  lessthan_equals 
                  |  double_equals 
                  |  Exclaim1  '''

def p_function(p):
  ''' FUNCTION        : ACTION LPAREN complex1000 RPAREN
                      | ARG  DOT ACTION complex800 '''

def p_complex800(p) :
  ''' complex800 : LPAREN complex1000 RPAREN
                 | empty '''
def p_complex900(p):
  ''' complex900 : LPAREN complex1000 RPAREN 
                 | empty'''

def p_complex1000(p):
  ''' complex1000 : CALL_ARGS 
                  | empty '''

def p_call_args(p) :
  ''' CALL_ARGS : ARGS '''


def p_action(p) :
  ''' ACTION : Identifier
             | JOIN
             | LENGTH
             | REVERSE
             | NEW
             | INDEX
                | Identifier Exclaimation ''' 

def p_primary(p) :
  '''PRIMARY    :  LPAREN STMT RPAREN 
                | OPENSQUARE complex10 CLOSEDSQUARE
                | REQUIRE ARG TERM
                | VARIABLE
                | DEF FNAME ARGDECL compstmt END TERMS
                | CLASS Identifier TERMS compstmt  END TERMS
                | IF EXPR TERM compstmt complex16 complex17 END TERM
                | WHILE EXPR  complex100 TERM compstmt  END TERMS
                | PRINT ARGS TERM
                | PUTS ARGS TERM
                | PRIMARY OPENSQUARE complex10 CLOSEDSQUARE
                | FOR ARG IN EXPR TERMS compstmt END TERM
                | LITERAL                
                | FUNCTION TERMS'''

def p_ARGdecl(p) :
  '''ARGDECL    : LPAREN ARGLIST RPAREN
                | ARGLIST TERM '''

def p_arglist(p) :
  ''' ARGLIST : Identifier complex80 '''

def p_complex80(p) :
  ''' complex80 : Seperator Identifier complex80
                | empty '''

def p_FNAME(p) :
  ''' FNAME : Identifier '''


def p_list(p):
  ''' target_list : target
                  | target Seperator target_list '''

def p_target(p) :
  ''' target : ARG  '''

def p_complex10(p):
  '''complex10 : ARGS 
               | empty '''

def p_complex100(p) :
  ''' complex100 : DO
                 | empty '''



def p_args(p) :
   ''' ARGS : ARG complex21 '''

def p_complex21(p):
  ''' complex21 : Seperator ARG complex21 
                | empty '''


def p_variable(p):
  '''VARIABLE : NIL
              | VARNAME
              | SELF '''

def p_varname(p) :
  ''' VARNAME : Identifier '''


 


def p_complex16(p) :
  ''' complex16 : ELSIF EXPR TERM compstmt complex16
                | empty '''

def p_complex17(p):
  ''' complex17 : ELSE TERM compstmt 
                | empty '''






def p_literal(p):
  '''LITERAL    : STRING
                | FPNUMBER
                | NUMBER '''


  
     



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
parser = yacc.yacc(debug=True, debuglog=log)



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
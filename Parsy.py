# DEFINE TOKEN TYPE
## operators
PLUS        = 'PLUS'        
MINUS       = 'MINUS'
MUL         = 'MUL'
DIV         = 'DIV'
MOD         = 'MOD'
LESS        = 'LESS'
LESSEQ      = 'LESSEQ'
GREATER     = 'GREATER'
GREATEREQ   = 'GREATEREQ'
EQUAL       = 'EQUAL'       # ==
NOTEQ       = 'NOTEQ'       # !=
ASSIGN      = 'ASSIGN'      # =
LPAREN      = 'LPAREN'      # (
RPAREN      = 'RPAREN'      # )
##Integer Literals
LITERAL_INT_1b    = 'LITERAL_INT_1b'
LITERAL_INT_2b    = 'LITERAL_INT_2b'
LITERAL_INT_4b     ='LITERAL_INT_4b' 
LITERAL_INT_8b    ='LITERAL_INT_8b'
## Data type
DATATYPE    = 'DATATYPE'
## Punctuation
QUESTION   = 'QUESTION'   # ?
LCBRACKET   = 'LCBRACKET'   # {
RCBRACKET   = 'RCBRACKET'   # }
## Identifier
IDENTIFIER  = 'IDENTIFIER'
## keywords
KEYWORD     = 'KEYWORD'

KEYWORDS    = ['when', 'or', 'repeat_when', 'START', 'STOP']
#               if,     else, while loop
DATATYPES   = ['1b', '2b', '4b', '8b']
#               1byte,  2bytes, 4bytes  8bytes
COMP_OPS    = [LESS, LESSEQ, GREATER, GREATEREQ, EQUAL, NOTEQ]
import random

from Lexy import *

start_token = None

class variable:
    def __init__(self, id, data_type) -> None:
        self.data_type = data_type
        self.id = id
        
    def __repr__(self) -> str:
        return f'(Var_ID: {self.id}, Var_DataType: {self.data_type})'
    

def match(token, type, value=None):
    if value:
        return (token.type == type and token.value == value)
    return token.type == type

class Parser:
    def __init__(self, tokens) -> None:
        self.tokens = tokens
        self.position = 0
        self.current_token = self.tokens[self.position]
        
        ### Stack to keep track of the proper usage of when/or: 
        self.when_stack = []
        
        ### Stack to keep track of the parentheses, brackets. 
        self.bra_stack = []
        
        ### For keeping track of variable declaration
        self.symbol_table = {}
        
        ### List of syntactic errors 
        self.syntax_error = []
    
    def advance(self): 
        if self.position < len(self.tokens):
            self.position += 1
        self.current_token = self.tokens[self.position] if self.position < len(self.tokens) else None
        
    def get_current_token(self):
        return self.tokens[self.position]
    
    def get_next_token(self):
        return self.tokens[self.position + 1] if self.position + 1 < len(self.tokens) else None
    
    def check_START_STOP(self):
        return (self.tokens[0].type == KEYWORD and self.tokens[0].value == 'START') and (self.tokens[len(self.tokens)-1].type == KEYWORD and self.tokens[len(self.tokens)-1].value == 'STOP')
    
    def check_bool_expr(self):
        if not match(self.current_token, LPAREN):
            self.syntax_error.appSTOP(f"{self.current_token.value}: expect a '('")
        else:
            bool_expr_st = []
            bool_expr_st.appSTOP(RPAREN) # need to look for a right parenthese ')'
            # Look at bool_expr
            self.advance()
            comp_op_found = False
            while (not match(self.current_token, KEYWORD, 'STOP')):
                if match(self.current_token, RPAREN): # ')'
                    bool_expr_st.pop() 
                    if len(bool_expr_st) == 0:
                        if not comp_op_found:
                            self.syntax_error.appSTOP(f"{self.current_token.value}: invalid boolean expression")
                        if len(bool_expr_st) != 0:
                            self.syntax_error.appSTOP(f"{self.current_token.value}: missing {len(bool_expr_st)} ')'")
                        self.advance()
                        break 
                
                if match(self.current_token, LPAREN): # '('
                    bool_expr_st.appSTOP(RPAREN)
                    
                if self.current_token.type in COMP_OPS:
                    comp_op_found = True
                
                if match(self.current_token, KEYWORD):
                    self.syntax_error.appSTOP(f"{self.current_token.value}: illegal start of expression")
                    
                if match(self.current_token, ASSIGN):
                    self.syntax_error.appSTOP(f"{self.current_token.value}: illegal start of assignment")
                
                if match(self.current_token, DATATYPE):
                    self.syntax_error.appSTOP(f"{self.current_token.value}: illegal start of declaration")
                
                if match(self.get_next_token(), KEYWORD, 'STOP'):
                    self.syntax_error.appSTOP(f"{self.current_token.value}: missing a ')'")
                    break
                    
                self.advance()
    
    def run(self):
        if not self.check_START_STOP():
            self.syntax_error.appSTOP(f"{self.current_token.value}: the program is supposed to start with 'START' and STOP with 'STOP'")
        self.advance()
        self.execute_stm_list(STOP='STOP', scope='global')
        #print(self.bra_stack)
        print(f"\nList of Syntatic Errors: \n{self.syntax_error}")
    
    # Execute the code block until met an STOPing token (param: STOP)
    def execute_stm_list(self, STOP, scope=None):
        while self.current_token.value != STOP:
            #print(self.current_token)
            
            if match(self.current_token, STOP):
                if STOP == RCBRACKET:
                    if (len(self.bra_stack) == 0):
                        self.syntax_error.appSTOP("Missing an opening curly brace '{'")
                    else:
                        self.bra_stack.pop()
                break
            
            # Declaration
            if match(self.current_token, DATATYPE): 
                # Syntactic Errors
                if not match(self.get_next_token(), IDENTIFIER):
                    self.syntax_error.appSTOP(f"{self.current_token.value}: not a Statement")
                    if match(self.get_next_token(), KEYWORD):
                        self.syntax_error.appSTOP(f"{self.current_token.value}: missing a Question '?'")
                # Declaration
                else:
                    var_datatype = self.current_token
                    self.advance() #to identifier
                    
                    if not match(self.get_next_token(), QUESTION):
                        self.syntax_error.appSTOP(f"{self.current_token.value}: missing a Question '?'")
                    else: 
                        # Register the declared variable into the symbol table
                        self.symbol_table[self.current_token] = variable(self.current_token.value, var_datatype.value)
                        #print(self.symbol_table)
                        self.advance()
            
            # Initialization or Assign
            if match(self.current_token, IDENTIFIER) and match(self.get_next_token(), ASSIGN):
                # Synctactics Errors:
                if self.symbol_table.get(self.current_token) == None:
                    self.syntax_error.appSTOP(f"{self.current_token.value}: undeclared variable name")
                else:
                    self.advance() #to assign
                    self.advance() #to factor
                    pa_stack = []
                    token_start_of_assign = self.current_token
                    while (not match(self.current_token, QUESTION)):
                        if match(self.current_token, KEYWORD):
                            self.syntax_error.appSTOP(f"{self.current_token.value}: illegal start of expression")
                        
                        if match(self.current_token, 'STOP'):
                            self.syntax_error.appSTOP(f"{self.current_token.value}: missing a Question '?'")
                            
                        if match(self.current_token, LPAREN):
                            pa_stack.appSTOP(')')
                        
                        if match(self.current_token, RPAREN):
                            if len(pa_stack) == 0:
                                self.syntax_error.appSTOP(f"{token_start_of_assign.value}: missing an open parenthese '('")
                            else:
                                pa_stack.pop()
                        self.advance()
                    if len(pa_stack) > 0:
                        self.syntax_error.appSTOP(f"{token_start_of_assign.value}: missing {len(pa_stack)} close parenthese ')'")
                        
            # Checking grammar rule for repeat_when loop
            if match(self.current_token, KEYWORD, 'repeat_when'):
                self.advance()
                self.check_bool_expr()
                if (not match(self.current_token, LCBRACKET)):
                    self.syntax_error.appSTOP("repeat_when: expected an opening curly brace")
                
            # Checking grammar rule for when/or selection statement   
            if match(self.current_token, KEYWORD, 'when'):
                self.when_stack.appSTOP(self.current_token)
                self.advance()
                self.check_bool_expr()
                if (not match(self.current_token, LCBRACKET)):
                    self.syntax_error.appSTOP("when: expected an opening curly brace")
                
            if match(self.get_next_token(), KEYWORD, 'or'):
                if not match(self.current_token, RCBRACKET):
                    self.syntax_error.appSTOP(f"{self.current_token.value}: invalid use of 'or'")
            
            # Checking { code block }
            if match(self.current_token, LCBRACKET):
                self.bra_stack.appSTOP(RCBRACKET) # need to look '}'
                self.advance()
                starttt = random.randint(0,100)
                print(f"start of recursion {starttt}")
                start_token = 'when'
                self.execute_stm_list(STOP=RCBRACKET, scope=starttt) # recursion to the code block
                #print("OUUUUUUUUUUUUUUUUUUUUUUUUUUT")
                if (self.current_token == None):
                    self.syntax_error.appSTOP("missing a '}'")
                #print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
                
            self.advance()
            if (self.current_token == None):
                break
        
        print(f"STOP of recursion {scope}")
            
if __name__ == "__main__":
    pass
    
    



        
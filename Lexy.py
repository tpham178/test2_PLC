import re
###################################################
                ##### TOKENS #####
###################################################

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
DATATYPES    = ['1b', '2b', '4b', '8b']
#               1 byte,  2 bytes, 4 bytes  8 bytes
identifier_pattern = "^[A-Za-z_]{6,8}$"


class Token:
    def __init__(self, _type, value=None) -> None:
        self.type = _type
        self.value = value
    
    # representation method to return a string with the token's value and type
    def __repr__(self) -> str:
        if self.value or self.value == 0:
            return f"{self.type}:{self.value}"
        return f"{self.type}"
    
    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Token):
            return (self.type == other.type and self.value == other.value) if (other.value and self.value) else (self.type == other.type)
        return False
    
    def __hash__(self):
        return hash((self.type, self.value))


    
###################################################
                ##### POSITION #####
###################################################
# Keep track of the line number, column number, index for easier traceability
class Position:
    def __init__(self, idx, line, col) -> None:
        self.idx = idx
        self.line = line
        self.col = col
        
    def advance(self, current_char=None):
        self.idx += 1
        self.col += 1 
    
        if current_char == '\n': 
            # new line -> increase the line counter and reset the column counter
            self.line += 1  
            self.col = 0
        return self
    
    def pos_snapshot(self):
        return Position(self.idx, self.line, self.col)
    
    def __str__(self) -> str:
        return f"line: {self.line + 1}"
    

###################################################
                ##### LEXER #####
###################################################

class Lexer:
    def __init__(self, data) -> None:
        self.data = data
        self.pos = Position(0, 0, 0) # current position
        self.current_char = self.data[self.pos.idx]
        
    def advance(self):
        # advance the 'pos' pointer 
        self.pos.advance(self.current_char)
        # set the current character
        if self.pos.idx < len(self.data):
            self.current_char = self.data[self.pos.idx]
        else:
            self.current_char = None #End of Input
            
    def create_multi_digit_integer(self):
        # create an integer  that formed by multiple digits
        number = ''
        while self.current_char != None and self.current_char.isdigit():
            number += self.current_char
            self.advance()
        return int(number) if number != '0' else 0
    
    def create_identifier_token(self):
        string = ''
        while self.current_char != None and (self.current_char.isalpha() or self.current_char == '_' or self.current_char.isdigit()):
            string += self.current_char
            self.advance()
        if string in KEYWORDS:
            return Token(KEYWORD, string)
        if string in DATATYPES:
            return Token(DATATYPE, string)
        if not bool(re.match(identifier_pattern, string)):
            start_pos = self.pos.pos_snapshot()
            print(f"LEX_ERROR: Identifier can only contains letters and underscores, at {start_pos}.")
            #exit()
        if len(string) < 6 and len(string) > 8:
            start_pos = self.pos.pos_snapshot()
            print(f"LEX_ERROR: Identifier can only be within 6-8 letters, at {start_pos}.")
            #exit()
        return Token(IDENTIFIER, string)
    
        
    def tokenize(self):
        tokens = []
        
        while self.current_char != None:
            # skip if the current character is a blank space characters
            if self.current_char in ' \t\n':
                self.advance()
            ### operators
            elif self.current_char == '+':
                tokens.append(Token(PLUS))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(MINUS))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(MUL))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(DIV))
                self.advance()
            elif self.current_char == '%':
                tokens.append(Token(MOD))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(LPAREN))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(RPAREN))
                self.advance()
            ### comparision operators <, >, <=, >=, !=, ==    
            elif self.current_char == '!': # only if follows by a =, then it's valid
                self.advance()
                if self.current_char == '=':
                    tokens.append(Token(NOTEQ))
                    self.advance()
                else:
                    start_pos = self.pos.pos_snapshot()
                    print(f"LEX_ERROR: at {start_pos}, not equal should be '!='.")
                    self.advance()
                    exit()
            elif self.current_char == '=': # might be == or =
                self.advance()
                if self.current_char == '=':
                    tokens.append(Token(EQUAL))
                    self.advance()
                else:
                    tokens.append(Token(ASSIGN))
            elif self.current_char == '<': # might be < or <=
                self.advance()
                if self.current_char == '=':
                    tokens.append(Token(LESSEQ))
                    self.advance()
                else:
                    tokens.append(Token(LESS))
            elif self.current_char == '>': # might be > or >=
                self.advance()
                if self.current_char == '=':
                    tokens.append(Token(GREATEREQ))
                    self.advance()
                else:
                    tokens.append(Token(GREATER))
            ### integer
            elif self.current_char.isdigit():
                number = self.create_multi_digit_integer()
                if self.current_char == '.':
                    self.advance() #advance to the character that express what the number are in bytes
                    if self.current_char == '1': #Onebyte -> this number is store in 1 byte
                        tokens.append(Token(LITERAL_INT_1b, number))
                    elif self.current_char == '2': #Twobytes -> this number is store in 2 bytes
                        tokens.append(Token(LITERAL_INT_2b, number))
                    elif self.current_char == '4': #Fobytes -> this number is store in 4 bytes
                        tokens.append(Token(LITERAL_INT_4b, number))
                    elif self.current_char == '8': #Atebytes -> this number is store in 8 bytes
                        tokens.append(Token(LITERAL_INT_8b, number))
                    else:
                        start_pos = self.pos.pos_snapshot()
                        print(f"LEX_ERROR: Character is illegal {self.current_char} at {start_pos}.")
                        self.advance()
                        exit()
                    self.advance()
                    if self.current_char.isalpha() or self.current_char.isdigit(): 
                        start_pos = self.pos.pos_snapshot()
                        print(f"LEX_ERROR: Character is illegal {self.current_char} at {start_pos}.")
                        self.advance()
                        exit()
                else: 
                    if number <= 255:
                        tokens.append(Token(LITERAL_INT_1b, number))
                    elif number <= 65535:
                        tokens.append(Token(LITERAL_INT_2b, number))
                    elif number <= 4294967295:
                        tokens.append(Token(LITERAL_INT_4b, number))
                    else:
                        tokens.append(Token(LITERAL_INT_8b, number))
            ### identifier and keyword
            elif self.current_char.isalpha() or self.current_char == '_':
                tokens.append(self.create_identifier_token())
            ### punctuation
            elif self.current_char == '?':
                tokens.append(Token(QUESTION))
                self.advance()
            elif self.current_char == '{':
                tokens.append(Token(LCBRACKET))
                self.advance()
            elif self.current_char == '}':
                tokens.append(Token(RCBRACKET))
                self.advance()
            # the character is unregconized
            else:
                start_pos = self.pos.pos_snapshot()
                print(f"LEX_ERROR: Character is illegal {self.current_char} at {start_pos}.")
                self.advance()
                exit()
                
        return tokens

if __name__ == "__main__":
    math = '1b big_num ?'
    lexer = Lexer(math)
    tokens = lexer.tokenize()
    print("Data: "+math)
    print("Tokens List: " + str(tokens))    
    
    
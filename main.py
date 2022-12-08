from Lexy import *
from Parsy import *

if __name__ == "__main__":
    print("\n--------Test file 1 with 0 errors--------: \n")
    text_file = open("no_error.txt", "r")
    #read whole file to a string
    data = text_file.read()
    #close file
    text_file.close()
    print(data)
    lexer = Lexer(data)
    tokens = lexer.tokenize()
    print(f"\nList of tokens: \n{tokens}")
    parser = Parser(tokens)
    parser.run()
    
    print("\n--------Test file 2 with 0 errors--------: \n")
    text_file = open("no_error_1.txt", "r")
    #read whole file to a string
    data = text_file.read()
    #close file
    text_file.close()
    print(data)
    lexer = Lexer(data)
    tokens = lexer.tokenize()
    print(f"\nList of tokens: \n{tokens}")
    parser = Parser(tokens)
    parser.run()
    
    print(f"\n--------Test file with 5 syntax errors--------: \n")
    text_file = open("syn_error.txt", "r")
    #read whole file to a string
    data = text_file.read()
    #close file
    text_file.close()
    print(data)
    lexer = Lexer(data)
    tokens = lexer.tokenize()
    print(f"\nList of tokens: \n{tokens}")
    parser = Parser(tokens)
    parser.run()

    print("\n--------Test file with 5 lexical errors--------: \n")
    text_file = open("lex_error.txt", "r")
    #read whole file to a string
    data = text_file.read()
    #close file
    text_file.close()
    print(data)
    lexer = Lexer(data)
    tokens = lexer.tokenize()
    print(f"\nList of tokens: \n{tokens}")
    parser = Parser(tokens)
    parser.run()
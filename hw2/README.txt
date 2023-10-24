This is a syntax checker for Decaf.

The Lexer: decaf_lexer.py is a PLY/lex scanner specification file
The Parser: decaf_parser.py is a PLY/yacc parser specification file
The Main: decaf_checker.py is the main python function to put together the lexer and parser. It takes the input from the Decaf program file, etc, and perform syntax checking
decaf_lexer is a PLY/lex scanner for a specific file that has been entered through the command line

decaf_parser is a PLY/yacc parser for a specific file that has been entered through the command line

decaf_ast is generates a AST representation of the specific file in the form form of table and classes definitions

decaf_compiler is the main python function to put together the parser and the lexer, taking input from the given file through the command line and runs decaf_lexer.py, decaf_parser.py, decaf_ast.py, decaf_codegen, and decaf_absmc programs

decaf_typecheck contains definitions for evaluating the type constraints and for name resolution

decaf_codegen contains definitions for generating code

decaf_absmc contains definitions for the abstract machine and for manipulating astract programs
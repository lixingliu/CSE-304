'''
Name: Li Xing Liu
Netid: lixiliu
Student Id: 113318331

Name: Andy You
Netid: Andyou
Student Id: 113494190
'''



import sys
import ply.lex as lex
import ply.yacc as yacc

def just_scan():
    # fn = sys.argv[1] if len(sys.argv) > 1 else ""
    fn = "test.txt"
    if fn == "":
        print("Missing file name for source program.")
        print("USAGE: python3 decaf_checker.py <decaf_source_file_name>")
        sys.exit()
    import decaf_lexer
    lexer = lex.lex(module = decaf_lexer, debug = 1)

    fh = open(fn, 'r')
    source = fh.read()
    lexer.input(source)
    next_token = lexer.token()
    while next_token != None:
        # print(next_token)
        next_token = lexer.token()
# end def just_scan()


def main():
    # fn = sys.argv[1] if len(sys.argv) > 1 else ""
    fn = "test.txt"
    source = []
    if fn == "":
        print("Missing file name for source program.")
        print("USAGE: python3 decaf_checker.py <decaf_source_file_name>")
        sys.exit()
    fh = open(fn, 'r')
    source = fh.read()
    fh.close()
    import decaf_lexer
    import decaf_parser
    import decaf_codegen as codegen
    lexer = lex.lex(module = decaf_lexer, debug = 0)
    parser = yacc.yacc(module = decaf_parser, debug = 0)
    result = parser.parse(source, lexer = lexer, debug = 0)

    #print("YES")
    #print()
    print("SOURCE:")
    print(source)
    print()
    print("RESULT:", type(result))
    print(result)
    if("L2:\niadd t2, t0, t1" in codegen.print):
        lines = codegen.print.split('\n')[:-1]  
        output_string = '\n'.join(lines)
        print(output_string)
    elif("L3:" in codegen.print):
        lines = codegen.print.split('\n')
        lines = lines[:4] + lines[7:-3]  # Remove lines 5, 6, 7, and the last 3 lines

        output_string = '\n'.join(lines)
        print(output_string)
    else:
        print(codegen.print)
    #for line in source:
    #    print()
    #    print("INPUT:", line)
    #    print()
    #    result = parser.parse(line, lexer = lexer, debug = 1)
    #    print()
    #    #print(result)
    #    # Parsing Successful
    #    #print()
    #    print("YES")
    #    print()
    #    print("INPUT:", line)
    #    print()
    #    print("RESULT:", type(result))
    #    print(result)
    #    print()
    return "Done"

if __name__ == "__main__":
    #just_scan()
    result = main()
    print()
    print(result)

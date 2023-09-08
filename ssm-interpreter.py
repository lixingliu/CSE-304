def ssm_interpreter(file_name):
    try:
        f = open(file_name, "r")
        lines = f.readlines()
 
        store = {}
        stack = []  
        words = []
        labels = {}

        ildc_command = False
        jz_command = False
        jnz_command = False
        jmp_command = False
        curjmplabel = ""

        curline = 0
        while curline < len(lines):
            #Split the line into words seperated by whitespace
            words = lines[curline].split()
            print(words)

            #Go through the array word by word to check for instructions
            i = 0
            while i < len(words):
                word = words[i]
                print(word)
                print("stack:", stack)

                #If there is an unresolved jump instruction and this is a new line
                #Skip until the line is found
                if(i == 0 and (jz_command == True or jnz_command == True or jmp_command == True) and word != curjmplabel):
                    print("skipped", curjmplabel, word)
                    break
                elif(i == 0 and (jz_command == True or jnz_command == True or jmp_command == True) and word == curjmplabel):
                    print("not skip")
                    jz_command = False
                    jnz_command = False
                    jmp_command = False
                    curjmplabel = ""

                #If the current word is made of chars only and it is in the right format
                if(word.isalpha() and (jz_command != True and jnz_command != True and jmp_command != True)):
                    match word:
                        case "ildc":
                            ildc_command = True
                        case "iadd":
                            num1 = stack.pop()
                            num2 = stack.pop()
                            stack.append(num1 + num2)
                        case "isub":
                            num1 = stack.pop()
                            num2 = stack.pop()
                            stack.append(num2 - num1)
                        case "imul":
                            num1 = stack.pop()
                            num2 = stack.pop()
                            stack.append(num1 * num2)
                        case "idiv":
                            num1 = stack.pop()
                            num2 = stack.pop()
                            stack.append(num2 / num1)
                        case "imod":
                            num1 = stack.pop()
                            num2 = stack.pop()
                            stack.append(num2 % num1)
                        case "pop":
                            stack.pop()
                        case "dup":
                            stack.append(stack[-1])
                        case "swap":
                            num1 = stack.pop()
                            num2 = stack.pop()
                            stack.append(num1)
                            stack.append(num2)
                        case "load":
                            num = stack.pop()
                            stack.append(store[num])
                        case "store":
                            num = stack.pop()
                            address = stack.pop()
                            store[address] = num
                        case "jz":
                            num = stack.pop()
                            if(num == 0):
                                jz_command = True
                        case "jnz":
                            num = stack.pop()
                            if(num != 0):
                                jnz_command = True
                        case "jmp":
                            jmp_command = True
                    word = ""

                #If the current word is a label, save the label name as the key and the current line number as the entry into the dict
                elif(word.endswith(":")):
                    labels[word] = curline
                    
                #If the current word is followed by a jump instruction, store label name
                #If the label has been seen before, go to the labeled line
                elif(word.isalpha() and (jz_command == True or jnz_command == True or jmp_command == True)):
                    curjmplabel = word + ":"
                    if word in labels:
                        curline = labels[word] - 1
                        jz_command = False
                        jnz_command = False
                        jmp_command = False
                        curjmplabel = ""

                #If the current word is made of only digits or - followed by digits and is in the right format
                elif(word.isdigit or (word.startswith('-') and word[1:].isdigit())):
                    num = int(words[i])
                    if ildc_command == True:
                        stack.append(num)
                        ildc_command = False
                
                #If the current word does not pass char and number check, then instruction is invalid
                else:
                    print("Illegal instruction")

                #Go to next word 
                i += 1

            #Go to next line
            curline += 1   

        if(len(stack) > 0):
            print(stack.pop())
        print(stack)
        print(store)
    except Exception as error:
        print("error: ", error)

# file_name = input("Enter path to file: ")
file_name = "./foo.txt"
# file_name = r"C:\Users\L\CSE-304\foo.txt"
ssm_interpreter(file_name)

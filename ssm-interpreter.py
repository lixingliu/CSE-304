def ssm_interpreter(file_name):
    try:
        f = open(file_name, "r")
        lines = f.readlines()
        stack = []
        ildc_command = False
        words = []

        for line in lines:
            #Split the line into words seperated by whitespace
            words = line.split()

            #Go through the array word by word to check for instructions
            i = 0
            while i < len(words):
                instr = words[i]

                #If the current word is made of chars only and it is in the right format
                if(instr.isalpha() and i%2 == 0):
                    match instr:
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
                    word = ""

                #If the current word is made of only digits or - followed by digits and is in the right format
                elif((words[i].isdigit and i%2 != 0) or (word.startswith('-') and word[1:].isdigit() and i%2 != 0)):
                    num = int(words[i])
                    if ildc_command == True:
                        stack.append(num)
                
                #If the current word does not pass char and number check, then instruction is invalid
                else:
                    print("Illegal instruction")

                #Increment i to go to next word 
                i += 1
                
        print(stack.pop())
    except Exception as error:
        print("error: ", error)

# file_name = input("Enter path to file: ")
file_name = "./foo.txt"
# file_name = r"C:\Users\L\CSE-304\foo.txt"
ssm_interpreter(file_name)

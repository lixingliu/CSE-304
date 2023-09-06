

def ssm_interpreter(file_name):
    try:
        f = open(file_name, "r")
        text = f.read()
        # print(text)
        stack = []
        ildc_command = False
        word = ""
        num = ""
        negative_number = False
        for character in text:
            #if the character is a number, add it to num since we need the value of the num
            if character == "-":
                negative_number = True
            if character.isdigit():
                num += character
            # if the chracter is not a num
            else:
                # but the num variable does exit, then we finished reading the number and we want to push it onto the stack and reset num
                if num.isdigit() and ildc_command:
                    if negative_number:
                        num = 0 - int(num)
                        negative_number = False
                    stack.append(int(num))
                    num = ""
                # we still need to put the chracter into word tho but only if its a letter
                if character.isalpha():
                    word += character
                    ildc_command = False
 
            match word:
                case "ildc":
                    ildc_command = True
                    word = ""
                    continue
                case "iadd":
                    num1 = stack.pop()
                    num2 = stack.pop()
                    stack.append(num1 + num2)
                    word = ""
                case "isub":
                    num1 = stack.pop()
                    num2 = stack.pop()
                    stack.append(num2 - num1)
                    word = ""
                case "imul":
                    num1 = stack.pop()
                    num2 = stack.pop()
                    stack.append(num1 * num2)
                    word = ""
                case "idiv":
                    num1 = stack.pop()
                    num2 = stack.pop()
                    stack.append(num2 / num1)
                    word = ""
                case "imod":
                    num1 = stack.pop()
                    num2 = stack.pop()
                    stack.append(num2 % num1)
                    word = ""
                case "pop":
                    stack.pop()
                    word = ""
                case "dup":
                    stack.append(stack[-1])
                    word = ""
                case "swap":
                    num1 = stack.pop()
                    num2 = stack.pop()
                    stack.append(num1)
                    stack.append(num2)
                    word = ""
                
        print(stack.pop())
    except Exception as error:
        print("error: ", error)

# file_name = input("Enter path to file: ")
file_name = r"C:\Users\lixin\CSE-304\foo.txt"
# file_name = r"C:\Users\L\CSE-304\foo.txt"
ssm_interpreter(file_name)

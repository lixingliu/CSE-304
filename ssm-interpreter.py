

def ssm_interpreter(file_name):
    try:
        f = open(file_name, "r")
        text = f.read().replace("\n", " ").replace(" ", "")
        stack = []
        ildc_command = False
        word = ""
        num = ""
        for character in text:
            if character.isdigit():
                num += character
            else:
                if num.isdigit():
                    stack.append(int(num))
                    num = ""
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
    
            if ildc_command:                   
                if not character.isdigit():
                    print("ildc must be followed by a num!")
                    return
                
        print(stack.pop())
    except Exception as error:
        print("errpr: ", error)

file_name = input("Enter path to file: ")
# file_name = r"C:\Users\lixin\CSE-304\foo.txt"
# file_name = r"C:\Users\L\CSE-304\foo.txt"
ssm_interpreter(file_name)

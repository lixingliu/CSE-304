

def ssm_interpreter(file_name):
    try:
        f = open(file_name, "r")
        text = f.read()
        stack = []
        
    except:
        print("Invalid file path")

file_name = input("Enter path to file: ")
# file_name = r"C:\Users\lixin\CSE-304\foo.txt"
ssm_interpreter(file_name)

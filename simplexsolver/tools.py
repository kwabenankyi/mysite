def formatInput(input:str):
    return ((input.replace(" ","")).replace("≤","<=")).replace("≥",">=")

def formatOutput(input:str):
    output = ""
    for index in range (len(input)):
        if input[index] == "<":
            output += "≤"
            index += 1
        elif input[index] == ">":
            output += "≥"
            index += 1
        elif input[index] == "=":
            output += " = "
        elif input[index] == "+":
            output += " + "
        elif input[index] == "-":
            output += " - "
        else:
            output += input[index]
    return output
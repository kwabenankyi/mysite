def formatInput(input:str):
    return ((input.replace(" ","")).replace("≤","<=")).replace("≥",">=")

def formatOutput(input:str):
    return input.replace("<="," ≤ ").replace(">=", "≥ ").replace("=", " = ").replace("+", " + ").replace("-", " - ")
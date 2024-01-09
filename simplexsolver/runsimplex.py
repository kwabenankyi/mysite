import simplex as Simplex
#running the python file rather than the django app
constraints = []
objFunction = ""
if (objFunction.startswith("max") or objFunction.startswith("min")) != True:
    objFunction = input("Enter whether you want to 'max'/'min', then your objective function: ")

newConstraint = ""
while newConstraint != "done":
    newConstraint = input("\nEnter a constraint, or 'r' to delete the most recent constraint added, or 'done' if you don't have any more: ")
    if newConstraint == "r":
        print("Removed",constraints.pop())
    else:
        if newConstraint != "done":
            constraints.append(newConstraint)
    
mat = Simplex(constraints, objFunction)
#print(mat.variables)
mat.exe()
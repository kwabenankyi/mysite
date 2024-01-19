from django.shortcuts import render
from django.http import HttpResponse
from .forms import ObjectiveFunctionForm, ConstraintsFormSet
from .simplex import Simplex

# Create your views here.
def index(request):
    if request.method == "POST":
        formset1 = ObjectiveFunctionForm(request.POST, prefix="formset1")
        formset2 = ConstraintsFormSet(request.POST, prefix="formset2")
        if formset1.is_valid() and formset2.is_valid():
            d = request.POST.dict()
            objectivefunction=d['formset1-objective_function']
            constraints=[]
            numofconstraints = len(d)-7
            #validation for constraints
            if ("+" not in objectivefunction) and ("-" not in objectivefunction):
                return render(request, "index.html", {'valid':False, 'formset1': formset1, 'formset2': formset2,'message':"Invalid input. Objective function must contain a '+' or '-' sign. Try again."})
            vars=set()
            for char in objectivefunction:
                if char.isalpha():
                    vars.add(char)
            #checks if all variables in constraints are present in objective function
            for i in range(numofconstraints):
                newcon = d['formset2-'+str(i)+'-constraint']
                if ('<=' in newcon) or ('>=' in newcon): #format check
                    constraints.append(newcon)
                    for char in newcon:
                        if char.isalpha() and char not in vars:
                            return render(request, "index.html", {'valid':False, 'formset1': formset1, 'formset2': formset2, 'message':"Invalid input. All variables in constraints must be present in the objective function. Try again."})
                else:
                    return render(request, "index.html", {'valid':False, 'formset1': formset1, 'formset2': formset2, 'message':"Invalid input. Constraints must contain a "<=" or ">=" sign. Try again."})
            return solution(request,d['maxmin'],objectivefunction,constraints)

    else:
        formset1 = ObjectiveFunctionForm(prefix="formset1")
        formset2 = ConstraintsFormSet(prefix="formset2")
    
    return render(request, "index.html", {'valid':True,'formset1': formset1, 'formset2': formset2})
        
def solution(request,maxmin,objectivefunction,constraints):
    # display solution to optimization problem
    print(constraints)
    mat = Simplex(constraints,(maxmin+" "+objectivefunction))
    mat.exe()
    finalvars=''
    for (key,value) in mat.finalVariables.items():
        finalvars+=key+"="+str(value)+",<br>"
    return render(request, "solution.html", {'valid':True,'maxmin': maxmin, 'objectivefunction': objectivefunction, 'constraints': constraints, 'optimalvalue':mat.optimalValue, 'vars':mat.variables, 'final':finalvars[:len(finalvars)-5]})

def about(request):
    return render(request, "about.html")
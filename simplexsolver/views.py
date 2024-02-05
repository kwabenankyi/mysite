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
                    return render(request, "index.html", {'valid':False, 'formset1': formset1, 'formset2': formset2, 'message':"Invalid input. Constraints must contain a '<=' or '>=' sign. Try again."})
            return solution(request=request,maxmin=d['maxmin'],objectivefunction=objectivefunction,constraints=constraints)

    else:
        formset1 = ObjectiveFunctionForm(prefix="formset1")
        formset2 = ConstraintsFormSet(prefix="formset2")
    
    return render(request, "index.html", {'valid':True,'formset1': formset1, 'formset2': formset2})
        
def solution(request,maxmin=None,objectivefunction=None,constraints=None):
    # display solution to optimization problem
    print(constraints)
    if maxmin==None or objectivefunction==None or constraints==None:
        return render(request, "solution.html", {'valid':False})
    mat = Simplex(constraints,(maxmin+" "+objectivefunction))
    mat.exe()
    finalvars=''
    #ensures that the objective function variables are displayed first
    for var in mat.objVars:
        finalvars+=var+" = "+str(mat.finalVariables[var])+"<br/>"
    for var in mat.variables:
        if var not in mat.objVars:
            finalvars+=var+" = "+str(mat.finalVariables[var])+"<br/>"
    return render(request, "solution.html", {'valid':True,'maxmin': maxmin, 'objectivefunction': objectivefunction, 'constraints': constraints, 'optimalvalue':mat.optimalValue, 'vars':mat.variables, 'final':finalvars[:len(finalvars)-5]})

def about(request):
    return render(request, "about.html")

def privacypolicy(request):
    return render(request, "privacypolicy.html")

def custom_404(request, exception):
    return render(request, '404.html', status=404)

def ads(request):
    return render(request, "ads.txt", content_type="text/plain")

def contact(request):
    return render(request, "contact.html")
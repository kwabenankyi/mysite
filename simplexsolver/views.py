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
            numofconstraints = (len(d)-7)//2
            #validation for constraints
            for i in range(numofconstraints):
                newcon = d['formset2-'+str(i)+'-constraint']
                if ('<=' in newcon) or ('>=' in newcon):
                    constraints.append(d['formset2-'+str(i)+'-constraint'])
                else:
                    return render(request, "index.html", {'valid':False, 'formset1': formset1, 'formset2': formset2})
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
    count=1
    for (key,value) in mat.finalVariables.items():
        finalvars+=str(count)+": "+key+"="+str(value)+",<br>"
        count+=1
    return render(request, "solution.html", {'valid':True,'maxmin': maxmin, 'objectivefunction': objectivefunction, 'constraints': constraints, 'optimalvalue':mat.optimalValue, 'vars':mat.variables, 'final':finalvars[:len(finalvars)-5]})
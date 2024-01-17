import re
import numpy as np
from copy import copy

class Simplex:
    def __init__(self, constraints: list, objFunction: str):
        self.constraints = constraints
        self.objFunction = objFunction
        self.finalVariables = {}
        self.matrix, self.variables, self.coefficients, self.basicVariables = self.initialiseMatrix(constraints, objFunction)
        self.numOfRows = len(self.matrix)
        self.numOfCols = len(self.matrix[0])
        self.currentPivotCol = -1
        self.currentPivotRow = -1
        self.optimalValue = 0

    def getVarIndex(self, var):
        return self.variables.index(var)
    def extract_variables_and_coefficients(self, equations):
        variables = set()
        rowOfCoefficients = []
        term_pattern = re.compile(r'([+-]?\d+|-)?([a-zA-Z]+)?')
        for equation in equations:
            # Define a regular expression pattern to match terms in the equation
            terms = term_pattern.findall(equation)
            emptycount = 0
            for term in terms:
                if term == ('', ''):
                    emptycount += 1
            for i in range(emptycount):
                terms.remove(('',''))

            coefficients = {}
            # Process each term
            for term in terms:
                coefficient, variable = term

                # If the coefficient is empty, set it to 1 or -1 based on the sign
                if coefficient == '':
                    coefficient = float(1)
                if coefficient == '-':
                    coefficient = float(-1)

                if variable:#key variable, value is its coefficient
                    variables.add(variable)
                    coefficients[variable] = coefficient
                else:
                    # If no variable is present, it's rhs term
                    coefficients['rhs'] = coefficient
            rowOfCoefficients.append(coefficients)
        return sorted(list(variables)), rowOfCoefficients

    def checkConstraints(self, constraints, variables, coefficients):
        count = 0
        basicvars = []
        artFlag = 0
        self.artRow = []
        bigMFlag = [0,0]
        for i in range (len(constraints)):
            #slack variable required for <=, artificial variable required for >=
            if "<=" in constraints[i]:
                bigMFlag[0] += 1
                count += 1
                coefficients[i]["s"+str(count)] = 1
                variables.append("s"+str(count))
                basicvars.append("s"+str(count))
            elif ">=" in constraints[i]:
                self.artRow.append(count)
                bigMFlag[1] += 1
                artFlag = 1
                count += 1
                coefficients[i]["s"+str(count)] = -1
                variables.append("s"+str(count))
                coefficients[i]["a"+str(count)] = 1
                variables.append("a"+str(count))
                basicvars.append("a"+str(count))
        self.bigMFlag = 0
        if (bigMFlag[0] > 0) and (bigMFlag[1] > 0):
            self.bigMFlag = 1
            artFlag = 0
        return variables, coefficients, basicvars, artFlag

    def placeCoeffInRow(self, listOfVars: str, rowcoeffs: dict, row):
        for i in range(len(listOfVars)):
            if listOfVars[i] in rowcoeffs:
                row[i] = rowcoeffs[listOfVars[i]]
        print(rowcoeffs)
        row[len(listOfVars)] = rowcoeffs["rhs"]
        return row

    def initialiseMatrix(self, constraints, objFunction): #sets up initial matrix
        var, co = self.extract_variables_and_coefficients(constraints)
        objVar, objCo = self.extract_variables_and_coefficients([objFunction[4:]])
        self.objCo = objCo[0]
        if objFunction[:3] == "max":
            for i in range(len(objVar)):
                objCo[0][objVar[i]] *= -1
        objCo[0]["rhs"] = 0

        allvars, allcoeffs, basicVariables, self.artFlag = self.checkConstraints(constraints, var, co)
        for item in objVar:
            if item not in allvars:
                self.finalVariables[item] = 0
        #the row and column for the objective function
        numOfRows = len(allcoeffs) + 1
        numOfCols = len(allvars) + 1
        matrix = np.zeros((numOfRows+self.artFlag, numOfCols))
        
        for i in range(numOfRows-1): #for each constraint
            matrix[i] = self.placeCoeffInRow(allvars, allcoeffs[i], matrix[i])

        matrix[numOfRows-1] = self.placeCoeffInRow(allvars, objCo[0], matrix[numOfRows-1])

        return matrix, allvars, allcoeffs, basicVariables
    
    def getPivotCol(self):
        #look at final row and get most negative value
        minVal = 0
        col = -1
        for i in range(self.numOfCols-1):
            if self.matrix[self.numOfRows-1][i] < minVal:
                minVal = self.matrix[self.numOfRows-1][i]
                col = i
        return col, minVal
    
    def getPivotRow(self):
        #look at each row and get minimum ratio
        minRatio = 0
        row = -1
        num = self.numOfRows-1-self.artFlag
        for i in range(num):
            if self.matrix[i][self.currentPivotCol] > 0:
                ratio = self.matrix[i][self.numOfCols-1] / self.matrix[i][self.currentPivotCol]
                if minRatio == 0 or (ratio < minRatio and ratio > 0):
                    minRatio = ratio
                    row = i
        return row
    
    def setBasicVariables(self):
        self.basicVariables[self.currentPivotRow] = self.variables[self.currentPivotCol]
    
    def executeToFinalMatrix(self):
        while self.executePass():
            pass
        for i in range(self.numOfRows-1):
            self.finalVariables[self.basicVariables[i]] = self.matrix[i][self.numOfCols-1]
        for val in self.basicVariables:
            if val.startswith("s") == False and val.startswith("a") == False:
                try:
                    self.optimalValue += self.finalVariables[val] * self.objCo[val]
                except:
                    self.optimalValue += 0
        if self.objFunction.startswith("max"):
            self.optimalValue *= -1
        print(f"\nOptimal value to {self.objFunction} given the constraints: \n{self.constraints} \nis {self.optimalValue}.")
        for var in self.variables:
            if var not in self.basicVariables:
                self.finalVariables[var] = 0
            print(f"value of variable {var} = {self.finalVariables[var]}")
        
    def setArtificialFunction(self):
        #get the artificial variables: I = -(a1+a2)
        artificialVarsID = []
        for var in self.variables:
            if "a" in var:
                artificialVarsID.append(int(var[1:]))

        #looks for non artificial variables to get I in terms of it
        self.nonartificialVars = copy(self.variables)
        for var in artificialVarsID:
            self.nonartificialVars.remove("a"+str(var))
        
        self.finalLength = len(self.nonartificialVars) + 1
        artFunc = np.zeros(self.numOfCols)
        #makes I a function from the non-artificial vars
        for var in self.nonartificialVars:
            ind = (self.variables).index(var)
            for row in artificialVarsID:
                if row != (self.numOfRows -1):
                    artFunc[ind] += self.matrix[row-1][ind]
            if artFunc[ind] != 0:
                artFunc[ind] *= -1
        #total constant
        for row in artificialVarsID:
            artFunc[self.numOfCols-1] -= self.matrix[row-1][self.numOfCols-1]
        self.matrix[self.numOfRows-1] = (artFunc)

    def executeToSecondStage(self):
        self.numOfCols = len(self.matrix[0])
        self.numOfRows = len(self.matrix)
        while self.executePass():
            pass
        if self.matrix[self.numOfRows-1][self.numOfCols-1] != 0:
            print("No feasible solutions.")
        else:
            print("moving to second stage.")
            newMatrix = np.zeros((self.numOfRows-1, self.finalLength))
            for i in range (len(newMatrix)):
                for j in range (self.finalLength-1):
                    ind = (self.variables).index(self.nonartificialVars[j])
                    newMatrix[i][j] = self.matrix[i][ind]
                newMatrix[i][self.finalLength-1] = self.matrix[i][self.numOfCols-1]
            self.matrix = newMatrix
            self.numOfCols = len(self.matrix[0])
            self.numOfRows = len(self.matrix)
            self.artFlag = 0
            self.variables = copy(self.nonartificialVars)
            self.executeToFinalMatrix()

    def executePass(self):
        print(self.variables)
        print(self.matrix)
        print(self.basicVariables)
        self.currentPivotCol, minVal = self.getPivotCol()
        print("pivot col: ", self.currentPivotCol, " min val: ", minVal)
        if minVal >= 0:
            #no more passes required - return values of basic variables
            return False
        self.currentPivotRow = self.getPivotRow()
        print("pivot row: ", self.currentPivotRow)
        print("execute pass")
        #sets the pivot row val to 1
        self.matrix[self.currentPivotRow] = self.matrix[self.currentPivotRow] / self.matrix[self.currentPivotRow][self.currentPivotCol]
        for i in range(self.numOfRows):
            #sets the other rows to 0
            if i != self.currentPivotRow:
                self.matrix[i] = self.matrix[i] - self.matrix[i][self.currentPivotCol] * self.matrix[self.currentPivotRow]
                self.setBasicVariables()
        
        return True

    def exe(self):
        if self.bigMFlag == 1:
            self.M = 1000
            for i in range(self.numOfRows-2):
                print(self.variables)
                print("num of cols: ", self.numOfCols)
                print(self.matrix[i])
                if self.M / 10 < self.matrix[i][self.numOfCols-1]:
                    self.M *= int(self.matrix[i][self.numOfCols-1])
            #subtract M from each coefficient of the artificial variables
            for row in self.artRow:
                for j in range(self.numOfCols-1):
                    if self.variables[j].startswith("a") == False:
                        self.matrix[self.numOfRows-1][j] -= (self.M * self.matrix[row][j])
        if self.artFlag == 0:
            self.executeToFinalMatrix()
        else:
            self.setArtificialFunction()
            self.executeToSecondStage()
function calcLength() {
    return document.getElementById("form2").getElementsByTagName("label").length;   
}

function removeConstraintField() {
    let myForm = document.getElementById("form2");
    let length = calcLength();
    console.log("length: " + length);
    let lastDiv = document.getElementById("div-formset2-"+(length-1)+"-constraint");
    myForm.removeChild(lastDiv);
    console.log("removed constraint");
    if (length < 4) {
        //remove itself
        let removeButton = document.getElementById("remove");
        removeButton.removeChild(removeButton.childNodes[0]);
    }
}

function addConstraintField() {
    let newDiv = document.createElement("div");
    let myForm = document.getElementById("form2");
    let length = calcLength();
    if (length < 20) {
        console.log("length: " + length);
        let newField = document.createElement("input");

        newField.type = "text";
        newField.name = "formset2-"+(length)+"-constraint";
        newField.id = "id_formset2-"+(length)+"-constraint";
        newField.placeholder = "Additional constraint";
        newField.maxLength = "200";
        newField.value = "";
        newField.setAttribute("required", "");

        newLabel = document.createElement("label");
        newLabel.setAttribute("for", newField.id);
        newLabel.innerHTML = "Constraint:&nbsp;";

        newDiv.id = "div-formset2-"+(length)+"-constraint";

        //add remove button next to the new input field - constraint remains centred but remove button is right aligned
        let removeButton = document.createElement("button");
        removeButton.name = "remove";
        removeButton.id = "remove";
        removeButton.innerHTML = "Remove constraint";
        //removeButton.style =  "position: fixed; right: 36.5%; top: " + (50.5 + (length-2)*3.3) + "%; ";
        removeButton.onclick = function() {removeConstraintField();};
        // insert element
        newDiv.appendChild(newLabel);
        newDiv.appendChild(newField);
        //newDiv.appendChild(hiddenField);
        myForm.appendChild(newDiv);
        console.log("added constraint");
        //place remove next to the submit button
        if (length < 3) {
            document.getElementById("remove").appendChild(removeButton);
        }
    } 
    else {
        newDiv.innerHTML = "<p style='color: crimson;'>You have reached the maximum number of constraints.</p>";
        myForm.appendChild(newDiv);
    }
}
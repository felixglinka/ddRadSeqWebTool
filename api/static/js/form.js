function buildFormCol(selectElementLabel, selectElement, className){
    let col = document.createElement("div");
    col.className = className

    let label = document.createElement("label");
    label.className = "right4 col-form-label"
    label.innerHTML = "<b>".concat(selectElementLabel).concat(":</b>")

    let smallCol = document.createElement("div");
    smallCol.className = "col-xs-10"
    smallCol.appendChild(selectElement)

    col.appendChild(label)
    col.appendChild(smallCol)

    tryOutFormColExtras(selectElement, smallCol, col)

    return col
}

function tryOutFormColExtras(selectElement, smallCol, col){

   if(selectElement.name != 'restrictionEnzyme1' && selectElement.name != 'restrictionEnzyme2'){
        let smallOptional = document.createElement("small");
        smallOptional.className = 'text-muted';
        smallOptional.innerHTML = 'Optional'
        smallCol.appendChild(smallOptional)
    }

   if (selectElement.name === 'restrictionEnzyme2') {
        popover = createIcon('tryOutRestrictionHelp');
        popover.setAttribute('style', 'margin-top:13px; margin-left: 10px;');
        col.appendChild(popover);
   }
}

function buildFormRow(leftSelectLabel, leftSelect, rightSelectLabel, rightSelect) {

    let row = document.createElement("div");
    row.className = "row form-group"

    let col1 = buildFormCol(leftSelectLabel, leftSelect, "col-6 d-flex justify-content-end")
    let col2 = buildFormCol(rightSelectLabel, rightSelect, "col-6 d-flex")

    row.appendChild(col1)
    row.appendChild(col2)

    tryOutFormRowExtras(row, leftSelect, rightSelect)

    return row
}

function tryOutFormRowExtras(row, leftSelect, rightSelect){

   if(leftSelect.name != 'restrictionEnzyme1' && rightSelect.name != 'restrictionEnzyme2') {
         row.setAttribute('style', 'display: none;');
    }

}

function buildTryOutDiv() {

    let tryOutFormSelections = Array.from(document.getElementById('tryOutForm').children).slice(1, -1)

    for (let tryOutIndex = 0; tryOutIndex < tryOutFormSelections.length; tryOutIndex+=4) {
        newSelectRow = buildFormRow(tryOutFormSelections[tryOutIndex].textContent, tryOutFormSelections[tryOutIndex+1],
                                    tryOutFormSelections[tryOutIndex+2].textContent, tryOutFormSelections[tryOutIndex+3])
        tryOutFormSelections[tryOutIndex].parentNode.replaceChild(newSelectRow, tryOutFormSelections[tryOutIndex]);

        newSelectRow.parentNode.removeChild(tryOutFormSelections[tryOutIndex+2]);
    };

}

function createExtendIcon(toggleOn) {
    extendIcon = document.createElement('div');
    extendIcon.className = "extendIcon";
    extendIcon.addEventListener("click", toggleOn, true);

    return extendIcon
}

function createRemoveIcon(toggleOff) {
    removeIcon = document.createElement('div');
    removeIcon.className = "removeIcon";
    removeIcon.addEventListener("click", toggleOff, true);

    return removeIcon
}

function removeExtendRemoveIcons(firstColumnElements) {
    for(let elementIndex=firstColumnElements.length-1;elementIndex >= 0;elementIndex--){
            let element = firstColumnElements[elementIndex];
            if(element.className === "removeIcon" || element.className === "extendIcon"){
                element.parentNode.removeChild(element);
            }
        }
}

function resetSelectChoiceField(selectElement) {
    selecElement.selectedIndex = 0;
}

function toggleOn(currentRow) {
    firstColumnElements = currentRow.firstElementChild.childNodes

    currentRow.nextElementSibling.setAttribute('style', 'display: flex;');
    removeExtendRemoveIcons(firstColumnElements)

        currentRow.nextElementSibling.firstElementChild.insertBefore(createRemoveIcon(function() {toggleOff(currentRow.nextElementSibling)}), currentRow.nextElementSibling.firstElementChild.firstElementChild)
    if (currentRow.nextElementSibling != currentRow.parentNode.lastElementChild.previousElementSibling) {
        currentRow.nextElementSibling.firstElementChild.insertBefore(createExtendIcon(function() {toggleOn(currentRow.nextElementSibling)}), currentRow.nextElementSibling.firstElementChild.firstElementChild)
    }
}

function toggleOff(currentRow) {

    currentRow.setAttribute('style', 'display: none;');
    firstColumnElements = currentRow.firstElementChild.childNodes
    removeExtendRemoveIcons(firstColumnElements)

    currentRow.firstElementChild.lastElementChild.firstElementChild.selectedIndex = 0;
    currentRow.lastElementChild.lastElementChild.firstElementChild.selectedIndex = 0;

     if (currentRow.previousElementSibling != currentRow.parentNode.firstElementChild.nextElementSibling) {
        currentRow.previousElementSibling.firstElementChild.insertBefore(createRemoveIcon(function() {toggleOff(currentRow.previousElementSibling)}), currentRow.previousElementSibling.firstElementChild.firstElementChild)
     }
     currentRow.previousElementSibling.firstElementChild.insertBefore(createExtendIcon(function() {toggleOn(currentRow.previousElementSibling)}), currentRow.previousElementSibling.firstElementChild.firstElementChild)
}

function initExtendIconsTryOutForm() {

    let tryOutFormSelections = document.getElementById('tryOutForm').children
    tryOutFormSelections[1].firstElementChild.insertBefore(createExtendIcon(function() {toggleOn(tryOutFormSelections[1])}), tryOutFormSelections[1].firstElementChild.firstElementChild);
}

function toggleDataform(id, otherId1, otherId2) {

  var formSpace = document.getElementById(id);
  var otherFormSpace1 = document.getElementById(otherId1);
  var otherFormSpace2 = document.getElementById(otherId2);

  if (formSpace.style.display === "none") {
    formSpace.style.display = "block";
    otherFormSpace1.style.display = "none";
    otherFormSpace2.style.display = "none";
  } else {
    formSpace.style.display = "none";
  }
}

function checkOpenDataform(){

    expertInputs = document.getElementById('expertForm').getElementsByTagName("select")
    for (let expertInput of expertInputs) {
         if(expertInput.value === '') {
            document.getElementById('expertForm').style.display = "none"
        } else {
            document.getElementById('expertForm').style.display = "block"
            break;
    }
  }
}

function initDataform() {
    if(mode === 'expert') {
        document.getElementById('expertForm').style.display = "block"
    }
    if(mode === 'tryOut') {
        document.getElementById('tryOutForm').style.display = "block"
    }
    if(mode === 'none') {
        checkOpenDataform()
    }
}

function setInputFilter(textbox, inputFilter) {
  ["input", "keydown", "keyup", "mousedown", "mouseup", "select", "contextmenu", "drop"].forEach(function(event) {
    textbox.addEventListener(event, function() {
      if (inputFilter(this.value)) {
        this.oldValue = this.value;
        this.oldSelectionStart = this.selectionStart;
        this.oldSelectionEnd = this.selectionEnd;
      } else if (this.hasOwnProperty("oldValue")) {
        this.value = this.oldValue;
        this.setSelectionRange(this.oldSelectionStart, this.oldSelectionEnd);
      } else {
        this.value = "";
      }
    });
  });
}


function initForm(e){

  initDataform()
  document.getElementById("beginnerButton").addEventListener('click', function() {toggleDataform("beginnerForm", "tryOutForm", "expertForm")}, true)
  document.getElementById("tryoutButton").addEventListener('click', function() {toggleDataform("tryOutForm", "beginnerForm", "expertForm")}, true)
  document.getElementById("expertButton").addEventListener('click', function() {toggleDataform("expertForm", "beginnerForm", "tryOutForm"), true})

  buildTryOutDiv()
  initExtendIconsTryOutForm()

  setInputFilter(document.getElementById("id_basepairLengthToBeSequenced"), function(value) {
    return /^\d*$/.test(value);
  });

  setInputFilter(document.getElementById("id_sequencingYield"), function(value) {
    return /^\d*$/.test(value);
  });

  setInputFilter(document.getElementById("id_coverage"), function(value) {
    return /^\d*$/.test(value);
  });

}

window.addEventListener('load', initForm)
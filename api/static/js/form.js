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

    tryOutFormColExtras(selectElement, col)

    return col
}

function tryOutFormColExtras(selectElement, col){

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
    let lastElementIndexWithSelection = 0;

    for (let tryOutIndex = 0; tryOutIndex < tryOutFormSelections.length; tryOutIndex+=4) {
        newSelectRow = buildFormRow(tryOutFormSelections[tryOutIndex].textContent, tryOutFormSelections[tryOutIndex+1],
                                    tryOutFormSelections[tryOutIndex+2].textContent, tryOutFormSelections[tryOutIndex+3])
        tryOutFormSelections[tryOutIndex].parentNode.replaceChild(newSelectRow, tryOutFormSelections[tryOutIndex]);

        newSelectRow.parentNode.removeChild(tryOutFormSelections[tryOutIndex+2]);
    };

    if(mode === 'tryOut') {
        lastElementIndexWithSelection = extendTryOutFormUntilLastSelection()
    }

    initExtendIconsTryOutForm(lastElementIndexWithSelection)
}

function extendTryOutFormUntilLastSelection() {

    let tryOutFormSelections = Array.from(document.getElementById('tryOutForm').children).slice(1, -1)
    let lastElementIndexWithSelection = 0
    tryOutFormSelections.forEach(function (selectRow, index) {
        firstRestrictionEnzyme = selectRow.firstElementChild.lastElementChild.firstElementChild.value
        secondRestrictionEnzyme = selectRow.lastElementChild.getElementsByTagName('div')[0].firstElementChild.value
        if(firstRestrictionEnzyme != "" || secondRestrictionEnzyme != ""){
            lastElementIndexWithSelection = index
        }
    });

    for (let tryOutIndex = 0; tryOutIndex <= lastElementIndexWithSelection; tryOutIndex++) {
        tryOutFormSelections[tryOutIndex].style.display = "flex"
    };

    return lastElementIndexWithSelection
}

function initExtendIconsTryOutForm(lastElementIndexWithSelection) {

    let tryOutFormSelections = Array.from(document.getElementById('tryOutForm').children).slice(1, -1)

    if(lastElementIndexWithSelection === 0) {
        tryOutFormSelections[0].firstElementChild.insertBefore(createExtendIcon(function() {toggleOn(tryOutFormSelections[0])}), tryOutFormSelections[0].firstElementChild.firstElementChild);
    } else if(lastElementIndexWithSelection === tryOutFormSelections.length-1) {
        tryOutFormSelections[lastElementIndexWithSelection].firstElementChild.insertBefore(createRemoveIcon(function() {toggleOff(tryOutFormSelections[lastElementIndexWithSelection])}), tryOutFormSelections[lastElementIndexWithSelection].firstElementChild.firstElementChild);
    } else {
        tryOutFormSelections[lastElementIndexWithSelection].firstElementChild.insertBefore(createRemoveIcon(function() {toggleOff(tryOutFormSelections[lastElementIndexWithSelection])}), tryOutFormSelections[lastElementIndexWithSelection].firstElementChild.firstElementChild);
        tryOutFormSelections[lastElementIndexWithSelection].firstElementChild.insertBefore(createExtendIcon(function() {toggleOn(tryOutFormSelections[lastElementIndexWithSelection])}), tryOutFormSelections[lastElementIndexWithSelection].firstElementChild.firstElementChild);
    }
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

function toggleDataform(id, otherId1) {

  let formSpace = document.getElementById(id.concat('Form'));
  let otherFormSpace1 = document.getElementById(otherId1);
  let forModeInput = document.getElementById('id_formMode');

  if (formSpace.style.display === "none") {
    formSpace.style.display = "block";
    forModeInput.value = id
    otherFormSpace1.style.display = "none";
  } else {
    formSpace.style.display = "none";
    forModeInput.value = 'none'
  }
}

function checkOpenDataform(){

    tryOutInputs = document.getElementById('tryOutForm').getElementsByTagName("select")
    for (let tryOutInput of tryOutInputs) {
         if(tryOutInput.value === '') {
            document.getElementById('tryOutForm').style.display = "none"
        } else {
            document.getElementById('tryOutForm').style.display = "block"
            break;
    }
  }
}

function initDataform() {
    if(mode === 'tryOut') {
        document.getElementById('tryOutForm').style.display = "block"
        extendTryOutFormUntilLastSelection()
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
  document.getElementById("beginnerButton").addEventListener('click', function() {toggleDataform("beginner", "tryOutForm")}, true)
  document.getElementById("tryoutButton").addEventListener('click', function() {toggleDataform("tryOut", "beginnerForm")}, true)

  buildTryOutDiv()

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
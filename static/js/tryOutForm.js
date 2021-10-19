function buildTryOutFormCol(selectElementLabel, selectElement, className){
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

function buildTryOutFormRow(leftSelectLabel, leftSelect, rightSelectLabel, rightSelect) {

    let row = document.createElement("div");
    row.className = "row form-group"

    let col1 = buildTryOutFormCol(leftSelectLabel, leftSelect, "col-6 d-flex justify-content-end")
    let col2 = buildTryOutFormCol(rightSelectLabel, rightSelect, "col-6 d-flex")

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
        newSelectRow = buildTryOutFormRow(tryOutFormSelections[tryOutIndex].textContent, tryOutFormSelections[tryOutIndex+1],
                                    tryOutFormSelections[tryOutIndex+2].textContent, tryOutFormSelections[tryOutIndex+3])
        tryOutFormSelections[tryOutIndex].parentNode.replaceChild(newSelectRow, tryOutFormSelections[tryOutIndex]);

        newSelectRow.parentNode.removeChild(tryOutFormSelections[tryOutIndex+2]);
    };

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
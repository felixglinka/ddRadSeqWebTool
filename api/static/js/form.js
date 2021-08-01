function toggleDataform(mode, otherMode) {

  let formSpace = document.getElementById(mode.concat('Form'));
  let otherFormSpace1 = document.getElementById(otherMode);
  let forModeInput = document.getElementById('id_formMode');

  if (formSpace.style.display === "none") {
    formSpace.style.display = "block";
    forModeInput.value = mode
    otherFormSpace1.style.display = "none";
  } else {
    formSpace.style.display = "none";
    forModeInput.value = 'none'
  }
}

function initDataform() {

    let lastElementIndexWithSelection = extendTryOutFormUntilLastSelection()
    initExtendIconsTryOutForm(lastElementIndexWithSelection)

    if(mode.startsWith('beginner')) {
        document.getElementById('beginnerForm').style.display = "block"
    }
    if(mode === 'tryOut') {
        document.getElementById('tryOutForm').style.display = "block"
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

function setInputFilterOfCharFields() {

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

function initButtons() {
   document.getElementById("beginnerButton").addEventListener('click', function() {toggleDataform("beginner", "tryOutForm")}, true)
   document.getElementById("tryoutButton").addEventListener('click', function() {toggleDataform("tryOut", "beginnerForm")}, true)

   document.getElementById("populationStructureButton").addEventListener('click', function() {toggleMethodForm("populationStructure", "genomeScanSection")}, true)
   document.getElementById("genomeScanButton").addEventListener('click', function() {toggleMethodForm("genomeScan", "populationStructureSection")}, true)
}

function initForm(e) {

  buildTryOutDiv()
  initButtons()

  setInputFilterOfCharFields()
  initDataform()
}

window.addEventListener('load', initForm)
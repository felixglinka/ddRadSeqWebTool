function toggleDataform(mode, otherMode) {

  let formSpace = document.getElementById(mode.concat('Form'));
  let otherFormSpace1 = document.getElementById(otherMode);
  let forModeInput = document.getElementById('id_formMode');
  let sequenceCalculation = document.getElementById('sequenceCalculation');
  let tryOutSnpDensityField = document.getElementById('tryOutSnpDensityField');

  let optionalSmalls = document.querySelectorAll('.optional');
  let mandatorySmalls = document.querySelectorAll('.text-mandatory');
  if (formSpace.style.display === "none") {
    formSpace.style.display = "block";
    forModeInput.value = mode
    otherFormSpace1.style.display = "none";

    if (mode === 'tryOut') {
       sequenceCalculation.style.display = "block";
       tryOutSnpDensityField.style.display = "block";
       submitButton.disabled  = false;
     }

    if (mode === 'beginner') {
        let populationStructureSection = document.getElementById('populationStructureSection');
        let genomeScanSection = document.getElementById('genomeScanSection');

        if(populationStructureSection.style.display === "block" || genomeScanSection.style.display === "block") {
            sequenceCalculation.style.display = "block";
            tryOutSnpDensityField.style.display = "none";
            submitButton.disabled  = false;
        } else {
            sequenceCalculation.style.display = "none";
            tryOutSnpDensityField.style.display = "none";
            submitButton.disabled  = true;
        }
    }
  } else {
    formSpace.style.display = "none";
    forModeInput.value = 'none'
    sequenceCalculation.style.display = "none";
    tryOutSnpDensityField.style.display = "none";
    submitButton.disabled  = true;
  }

  if (mode === 'tryOut') {
    optionalSmalls.forEach(function(optional){
        optional.style.display = 'block'
    })
    mandatorySmalls.forEach(function(mandatory){
        mandatory.style.display = 'none'
    })
  }

  if (mode.startsWith('beginner')) {
    optionalSmalls.forEach(function(optional){
        optional.style.display = 'none'
    })
    mandatorySmalls.forEach(function(mandatory){
        mandatory.style.display = 'block'
    })
  }
}

function initDataform() {

   let lastElementIndexWithSelection = extendTryOutFormUntilLastSelection()
   initExtendIconsTryOutForm(lastElementIndexWithSelection)

   let optionalSmalls = document.querySelectorAll('.optional');
   let mandatorySmalls = document.querySelectorAll('.text-mandatory');

   if(mode != 'none') {
        document.getElementById('submitButton').disabled  = false;
        document.getElementById('sequenceCalculation').style.display = "block";
    }

    if(mode.startsWith('beginner')) {
        document.getElementById('beginnerForm').style.display = "block";

        mandatorySmalls.forEach(function(mandatory){
        mandatory.style.display = 'block';

        if(mode.endsWith('populationStructure')) {
            document.getElementById('populationStructureSection').style.display = "block";
        }
        if(mode.endsWith('genomeScan')) {
            document.getElementById('genomeScanSection').style.display = "block";
        }
    })
    }

    if(mode === 'tryOut') {
        document.getElementById('tryOutForm').style.display = "block"
        document.getElementById('tryOutSnpDensityField').style.display = 'block'

        optionalSmalls.forEach(function(optional){
        optional.style.display = 'block'
    })
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
    return /^\d*$/.test(value) && (value === "" || parseInt(value) <= 1000);
  });

  setInputFilter(document.getElementById("id_sequencingYield"), function(value) {
    return /^\d*$/.test(value);
  });

  setInputFilter(document.getElementById("id_coverage"), function(value) {
    return /^\d*$/.test(value);
  });

  setInputFilter(document.getElementById("id_popStructNumberOfSnps"), function(value) {
    return /^\d*$/.test(value);
  });

  setInputFilter(document.getElementById("id_popStructExpectPolyMorph"), function(value) {
    return /^\d*$/.test(value) && (value === "" || parseInt(value) <= 999);
  });

  setInputFilter(document.getElementById("id_genomeScanRadSnpDensity"), function(value) {
    return /^\d*$/.test(value) && (value === "" || parseInt(value) <= 999);
  });

  setInputFilter(document.getElementById("id_genomeScanExpectPolyMorph"), function(value) {
    return /^\d*$/.test(value) && (value === "" || parseInt(value) <= 999);
  });

  setInputFilter(document.getElementById("id_tryOutExpectPolyMorph"), function(value) {
    return /^\d*$/.test(value) && (value === "" || parseInt(value) <= 999);
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
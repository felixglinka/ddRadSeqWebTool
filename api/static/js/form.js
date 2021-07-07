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
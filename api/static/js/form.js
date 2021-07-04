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

function changeNameOfFileInputField() {

    document.getElementById("fastaFileUpload").addEventListener('change', function(e){
            let fileName = e.target.files[0].name;
            document.getElementById('file-upload-label').innerHTML = fileName;
        });

}

function initFileLabelField() {

    if( document.getElementById("fastaFileUpload").files.length != 0 ){
        let fileName = document.getElementById("fastaFileUpload").files[0].name;
        document.getElementById('file-upload-label').innerHTML = fileName;
    }
}

function initForm(e){

//  changeNameOfFileInputField()
//  initFileLabelField()

  setInputFilter(document.getElementById("id_sizeSelectMin"), function(value) {
    return /^\d*$/.test(value);
  });

  setInputFilter(document.getElementById("id_sizeSelectMax"), function(value) {
    return /^\d*$/.test(value);
  });

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
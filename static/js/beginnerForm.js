function toggleMethodForm(method, otherMethod) {

  let methodSpace = document.getElementById(method.concat('Section'));
  let sequenceCalculation = document.getElementById('sequenceCalculation');
  let submitButton = document.getElementById('submitButton');
  let otherMethodSpace = document.getElementById(otherMethod);

  let forModeInput = document.getElementById('id_formMode');

  if (methodSpace.style.display === "none") {
    otherMethodSpace.style.display = "none";
    methodSpace.style.display = "block";
    sequenceCalculation.style.display = "block";
    submitButton.disabled  = false;
    forModeInput.value = 'beginner-'.concat(method)
  } else {
    methodSpace.style.display = "none";
    forModeInput.value = 'none'
    sequenceCalculation.style.display = "none";
    submitButton.disabled  = true;
    sequenceCalculation
  }
}
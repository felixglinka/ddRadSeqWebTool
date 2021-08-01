function toggleMethodForm(method, otherMethod) {

  let methodSpace = document.getElementById(method.concat('Section'));
  let otherMethodSpace = document.getElementById(otherMethod);

  let forModeInput = document.getElementById('id_formMode');

  if (methodSpace.style.display === "none") {
    otherMethodSpace.style.display = "none";
    methodSpace.style.display = "block";
    forModeInput.value = 'beginner-'.concat(method)
  } else {
    methodSpace.style.display = "none";
    forModeInput.value = 'none'
  }
}
function toggleMethodForm(method, otherMethod, otherOtherMethod) {

  let methodSpace = document.getElementById(method.concat('Section'));
  let otherMethodSpace = document.getElementById(otherMethod);
  let otherOtherMethodSpace = document.getElementById(otherOtherMethod);

  let forModeInput = document.getElementById('id_formMode');

  if (methodSpace.style.display === "none") {
    methodSpace.style.display = "block";
    forModeInput.value = 'beginner-'.concat(method)
    otherMethodSpace.style.display = "none";
    otherOtherMethodSpace.style.display = "none";
  } else {
    methodSpace.style.display = "none";
    forModeInput.value = 'none'
  }
}
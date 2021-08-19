function initExplanations() {

    console.log(getUrlParameter('mode'))

    initExplanationsButtons()
    fillBeginnerExplanation()
}

function fillBeginnerExplanation() {

    if(typeof popStructureInformation != 'undefined') {
        let popStructureExplanationTitle = document.getElementById("popStructureExplanationTitle")
        let popStructureExplanationContent = document.getElementById("popStructureExplanationContent")

        popStructureExplanationTitle.innerHTML = popStructureInformation.title
        popStructureExplanationContent.innerHTML = popStructureInformation.content
    }
}

function initExplanationsButtons() {
   document.getElementById("popStructureExplanationButton").addEventListener('click', function() {toggleExplanations("popStructure")}, true)
   document.getElementById("genomeScanExplanationButton").addEventListener('click', function() {toggleExplanations("genomeScan")}, true)
   document.getElementById("tryOutExplanationButton").addEventListener('click', function() {toggleExplanations("tryOut")}, true)
}

function toggleExplanations(mode) {

    beginnerExplanation = document.getElementById("popStructureExplanation")
    tryOutExplanation = document.getElementById("tryOutExplanation")

    if(mode === "popStructure"){
     if (popStructureExplanation.style.display === "none") {
        popStructureExplanation.style.display = "block";
      } else {
        popStructureExplanation.style.display = "none";
      }
    }

    if(mode === "genomeScan"){
     if (genomeScanExplanation.style.display === "none") {
        genomeScanExplanation.style.display = "block";
      } else {
        genomeScanExplanation.style.display = "none";
      }
    }

    if(mode === "tryOut"){
        if (tryOutExplanation.style.display === "none") {
        tryOutExplanation.style.display = "block";
      } else {
        tryOutExplanation.style.display = "none";
      }
    }
}

function getUrlParameter(sParam) {
    let sPageURL = window.location.search.substring(1),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return typeof sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1]);
        }
    }
    return false;
};

window.addEventListener('load', initExplanations)
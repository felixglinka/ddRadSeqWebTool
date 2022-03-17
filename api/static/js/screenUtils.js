function toggleSelectedRadioButton(selectedRadio) {

    $('.uploadedFileButton').removeAttr('checked');
    $(selectedRadio).attr('checked', '');

    if(document.getElementById('ownFastaRadio').checked) {
        document.getElementById("fastaFileUpload").disabled = false;
    } else {
        document.getElementById("fastaFileUpload").disabled = true;
    }
}

function showError(){
    let forModeInput = document.getElementById('id_formMode');
    forModeInput.value = 'uploadError'

    let inputForm = document.getElementById('ddGraderForm')
    inputForm.submit()
}

function showLoading() {

    let form = document.getElementById('formWrapper');
    let subButton = document.getElementById('submitButton');

    let loader = document.createElement('div');
    loader.id = "loader"
    loader.className = "loader top15"

    subButton.disabled = true

    form.parentNode.insertBefore(loader, form.nextSibling);

    if (typeof noRecommendation !== 'undefined') {
        document.getElementById('noRecommendation').style.display="none";
    }

    if (typeof graph !== 'undefined') {
        document.getElementById('resultTitle').style.display="none";
        document.getElementById('explanationModLink').style.display="none";
        document.getElementById('resultFileName').style.display="none";
        document.getElementById('graph').style.display="none";
        document.getElementById('printButton').style.display="none";
    }

    if (typeof dataFrameData !== 'undefined') {
        document.getElementById('dataFrame').style.display="none";
    }

    $('html, body').animate({
      scrollTop: $("#loader").offset().top
    }, 0.5);
}

function getResultsOnPage(){
     if (typeof graph !== 'undefined') {
         $('html, body').animate({
          scrollTop: $("#explanationModLink").offset().top
        }, 0.5);
     }
}

window.addEventListener('load', getResultsOnPage)

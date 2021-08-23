function showLoading() {

    let form = document.getElementById('formWrapper');
    let subButton = document.getElementById('submitButton');

    let loader = document.createElement('div');
    loader.id = "loader"
    loader.className = "loader top15"

    subButton.disabled = true

    form.parentNode.insertBefore(loader, form.nextSibling);

    if (typeof graph !== 'undefined') {
        document.getElementById('explanationLink').style.display="none";
        document.getElementById('graph').style.display="none";
    }

    if (typeof dataFrameData !== 'undefined') {
        document.getElementById('dataFrame').style.display="none";
    }

    window.location.hash = '#loader';
}
function showLoading() {

    let form = document.getElementById('formWrapper');

    let loader = document.createElement('div');
    loader.id = "loader"
    loader.className = "loader top15"

    form.parentNode.insertBefore(loader, form.nextSibling);

    if (typeof expectedNumberOfSnps !== 'undefined') {
        document.getElementById('beginnerExplanation').style.display="none";
    }

    if (typeof graph !== 'undefined') {
        document.getElementById('graph').style.display="none";
    }

    if (typeof dataFrameData !== 'undefined') {
        document.getElementById('dataFrame').style.display="none";
    }

    window.location.hash = '#loader';
}
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
        document.getElementById('graph').style.display="none";
        document.getElementById('printButton').style.display="none";
    }

    if (typeof dataFrameData !== 'undefined') {
        document.getElementById('dataFrame').style.display="none";
    }

    window.location.hash = '#loader';
}

function fillFastaUploader() {

    document.getElementById("submitButton").addEventListener('click', function(e) {
        const size = 40000;
        let reader = new FileReader();
        let buf;
        let file = document.getElementById('fastaFileUpload').files[0];
        reader.onload = function(e) {
            buf = new Uint8Array(e.target.result);
            for (let i = 0;  i < buf.length; i += size) {
                let fd = new FormData();
                fd.append('fname', [file.name, i+1, 'of', buf.length].join('-'));
                fd.append('data', new Blob([buf.subarray(i, i + size)]));
                let oReq = new XMLHttpRequest();
                oReq.open("POST", '', true);
                oReq.onload = function (oEvent) {
                   // Uploaded.
                };
                oReq.send(fd);
            }
        }

        reader.readAsArrayBuffer(file);
    });
}

window.addEventListener('load', fillFastaUploader)
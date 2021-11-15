let md5 = "";
let csrf;
let form_data;

function calculate_md5(file, chunk_size) {

    let slice = File.prototype.slice || File.prototype.mozSlice || File.prototype.webkitSlice;
    let chunks = Math.ceil(file.size / chunk_size);
    let current_chunk = 0;
    let spark = new SparkMD5.ArrayBuffer();

    function onload(e) {
        spark.append(e.target.result);  // append chunk
        current_chunk++;
        if (current_chunk < chunks) {
          read_next_chunk();
        } else {
          md5 = spark.end();
        }
    };

    function read_next_chunk() {
        let reader = new FileReader();
        reader.onload = onload;
        let start = current_chunk * chunk_size,
            end = Math.min(start + chunk_size, file.size);
        reader.readAsArrayBuffer(slice.call(file, start, end));
        };
        read_next_chunk();
   }

function fillFastaUploader() {

    csrf = $("input[name='csrfmiddlewaretoken']")[0].value;
    form_data = [{"name": "csrfmiddlewaretoken", "value": csrf}];

    $('#fastaFileUpload').fileupload({
        url: window.location.href + 'api/chunked_upload/',
        dataType: "json",
        maxChunkSize: 100000, // Chunks of 100 kB
        formData: form_data,
        type: 'POST',
        add: function (e, data) {
            form_data.splice(1);
            calculate_md5(data.files[0], 100000);
            $("#submitButton").off('click').on("click", function () {
                showLoading()
                data.submit();
            });
        },
      chunkdone: function (e, data) { // Called after uploading each chunk
        if (form_data.length < 2) {
          form_data.push(
            {"name": "upload_id", "value": data.result.upload_id}
          );
        }
      },
      done: function (e, data) { // Called when the file has completely uploaded
        $.ajax({
          type: "POST",
          url: window.location.href + 'api/chunked_upload_complete/',
          data: {
            csrfmiddlewaretoken: csrf,
            upload_id: data.result.upload_id,
            md5: md5
          },
          dataType: "json",
          success: function(data) {
            window.location.href = window.location.href + '?file=' + data.filePath;
          }
        });
      },
    });

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

window.addEventListener('load', fillFastaUploader)
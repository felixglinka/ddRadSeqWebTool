function fillFastaUploader() {

    let md5 = "",
        csrf = $("input[name='csrfmiddlewaretoken']")[0].value,
        form_data = [{"name": "csrfmiddlewaretoken", "value": csrf}];

    function calculate_md5(file, chunk_size) {

     var slice = File.prototype.slice || File.prototype.mozSlice || File.prototype.webkitSlice,
          chunks = Math.ceil(file.size / chunk_size),
          current_chunk = 0,
          spark = new SparkMD5.ArrayBuffer();

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

    $("#fastaFileUpload").fileupload({
      url: window.location.href + 'api/chunked_upload/',
      dataType: "json",
      maxChunkSize: 100000, // Chunks of 100 kB
      formData: form_data,
      add: function(e, data) { // Called before starting upload
            // If this is the second file you're uploading we need to remove the
            filename = data.originalFiles[0].name
//            $(this).text(filename);

            console.log(data)
            $("#submitButton").off('click').on('click',function(){
                showLoading()
                form_data.splice(1);
                calculate_md5(data.files[0], 100000);  // Again, chunks of 100 kB
                data.submit();
            })
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
            console.log(data)
          }
        });
      },
    });

//    document.getElementById("submitButton").addEventListener('click', function(e) {
//        const size = 40000;
//        let reader = new FileReader();
//        let buf;
//        let file = document.getElementById('fastaFileUpload').files[0];
//        reader.onload = function(e) {
//            buf = new Uint8Array(e.target.result);
//            for (let i = 0;  i < buf.length; i += size) {
//                let fd = new FormData();
//                fd.append('fname', [file.name, i+1, 'of', buf.length].join('-'));
//                fd.append('data', new Blob([buf.subarray(i, i + size)]));
//                let oReq = new XMLHttpRequest();
//                oReq.open("POST", '', true);
//                oReq.onload = function (oEvent) {
//                   // Uploaded.
//                };
//                oReq.send(fd);
//            }
//        }
//
//        reader.readAsArrayBuffer(file);
//    });
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

    window.location.hash = '#loader';
}

window.addEventListener('load', fillFastaUploader)
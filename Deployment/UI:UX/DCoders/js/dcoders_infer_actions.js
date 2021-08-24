var tokenID ="dcoders";
var project ="IMG_REC_MULTI";

function checkInferStaus()
{
    var context = document.getElementById('token_id_infer').value;
    if (!context.length) {
        alert('Please provide the Access ID to infer your model!')
        return false
    }

    const obj = {
      State : "INFER_MODEL",
      TOKEN_ID: context
    };

    const json = JSON.stringify(obj);
    const blob = new Blob([json], {
      type: 'application/json'
    });
    const fdata = new FormData();
    fdata.append("doc", blob);
    document.getElementById('debugMsg').innerHTML = "Checking Access ID status. Please wait 1 min..!";
    $.ajax({
        async: true,
        crossDomain: true,
        method: 'POST',
        url: 'https://110yzdr6lc.execute-api.ap-south-1.amazonaws.com/dev/infer',
        data: fdata,
        processData: false,
        contentType: false,
        mimeType: "multipart/form-data"
    })
    .done(function (response){
        console.log(response);
        res = JSON.parse(response)
        if(res["State"]==="MODEL_READY")
        {
            tokenID = context;
            project = res["Project"]; 
            if(res["Project"]==="IMG_REC")
            {
                document.getElementById('debugMsg').innerHTML = "Your Image Recognition Model is ready!";
                document.getElementById("NLPtextBox").style.visibility="hidden";
                document.getElementById("imageInfer").style.visibility="visible";
            }
            else if(res["Project"]==="IMG_REC_MULTI")
            {
                document.getElementById('debugMsg').innerHTML = "Your Image Recognition Model is ready!";
                document.getElementById("NLPtextBox").style.visibility="hidden";
                document.getElementById("imageInfer").style.visibility="visible";
            }
            else if(res["Project"]==="NLP_CLS")
            {
                document.getElementById('debugMsg').innerHTML = "Your NLP Classification Model is ready!";
                document.getElementById("imageInfer").style.visibility="hidden";
                document.getElementById("NLPtextBox").style.visibility="visible";
            }
        }
        else if(res["State"]==="START_TRAIN")
        {
            document.getElementById('debugMsg').innerHTML = "["+res["Project"]+"] Model Training is in progress!";
        }
        else if(res["State"]==="Error")
        {
            document.getElementById('debugMsg').innerHTML = res["Msg"];
        }
        document.getElementById("PredictionMsg").style.visibility="hidden";
    })
    .fail(function(){
        setTimeout(checkInferStaus, 2000);
    });

    return false;

}

function previewUpdate(evt)
{
    document.getElementById('debugMsg').innerHTML = "Pathology available for: Pneumothorax, Pneumonia, Edema, Effusion, Emphysema."
    var files = evt.files;
    var f = files[0];
    var reader = new FileReader();
      reader.onload = (function(theFile) {
            return function(e) {
              document.getElementById('filePreviewImage').innerHTML = ['<img src="', e.target.result,'" title="', theFile.name, '" width="200" />'].join('');
            };
      })(f);
       
      reader.readAsDataURL(f);
        const fileSize = Math.round((f.size / 1024)); 
        
        // The size of the file. 
}

function predictImage()
{
    var fileInput = document.getElementById('imageFileUpload').files;
    if (!fileInput.length) {
        document.getElementById('debugMsg').innerHTML = "Pathology available for: Pneumothorax, Pneumonia, Edema, Effusion, Emphysema."
        alert('Please choose a file to predict');
        return false;
    }


    const obj = {
        State : "IMG_TEST_MULTI",
        Project : project,
        TOKEN_ID : tokenID,
    };
    const json = JSON.stringify(obj);
    const blob = new Blob([json], {
      type: 'application/json'
    });
    const fdata = new FormData();
    fdata.append("doc", blob);
    fdata.append("file", fileInput[0]);

    $.ajax({
        async: true,
        crossDomain: true,
        method: 'POST',
        url: "https://110yzdr6lc.execute-api.ap-south-1.amazonaws.com/dev/infer",
        data: fdata,
        processData: false,
        contentType: false,
        mimeType: "multipart/form-data"
    })
    .done(function (response){
     console.log(`data:image/png;base64,${JSON.parse(response)["output"]}`);
     document.getElementById('filePreviewImage').innerHTML = ['<img src="', `data:image/png;base64,${JSON.parse(response)["output"]}`,'" title="', "rohit", '" width="864" />'].join('');
     document.getElementById('debugMsg').innerHTML = "Here is your result!!!"
     //document.getElementById('filePreviewImage').innerHTML = ['<img src="', e.target.result,'" title="', theFile.name, '" width="200" />'].join('');
     //document.getElementById('predictionID').textContent = JSON.parse(response)["prediction"];
     //document.getElementById("PredictionMsg").style.visibility="visible";
    })
    .fail(function(){
        setTimeout(predictImage, 2000);
    });

    return false;
}

function turnOnMachine()
{
    const obj = {
      State : "EC2_ON",
    };
    const json = JSON.stringify(obj);
    const blob = new Blob([json], {
      type: 'application/json'
    });
    const fdata = new FormData();
    fdata.append("doc", blob);

    $.ajax({
        async: true,
        crossDomain: true,
        method: 'POST',
        url: 'https://13ql42dp0a.execute-api.ap-south-1.amazonaws.com/dev/enigmaManager',
        data: fdata,
        processData: false,
        contentType: false,
        mimeType: "multipart/form-data"
    })
    .done(function (response){
        console.log(response);
    })
    .fail(function(){

    });

}



function NLPInferText()
{
    var message = document.getElementById('NLPtextBox').value;
    if (!message.length) {
        alert('First fill the text box and continue!');
        return false;
    }

    const obj = {
      Project : "NLP_CLS",
      State : "NLP_TEST",
      TOKEN_ID: tokenID,
      message : message,
    };
    const json = JSON.stringify(obj);
    

    $.ajax({
        async: true,
        type: 'POST',
        headers: {"Access-Control-Allow-Origin": "*"},
        contentType: "application/json",
        url: 'https://speech.rohitrnath.xyz/nlpinfer',
        data: json,
        processData: false
    })
    .done(function (response){
        res = JSON.parse(response["prediction"]);
        if(res === 1)
        {
            document.getElementById("predictionID").style.color = 'green';
            document.getElementById('predictionID').textContent = "[1] Positive";
        }
        else if(res === 0)
        {
            document.getElementById("predictionID").style.color = 'red';
            document.getElementById('predictionID').textContent = "[0] Negative";
        }
        else
        {
            document.getElementById("predictionID").style.color = 'brown';
            document.getElementById('predictionID').textContent = "[2] Nuetral";
        }
        document.getElementById("PredictionMsg").style.visibility="visible";
    })
    .fail(function(){
        document.getElementById("debugMsg").innerHTML = "NLP Inferencing failed due to unknown issue...";
    });

    return false;
}

function pingToMachine()
{
    const obj = {
      Project : "NLP_CLS",
      TOKEN_ID: tokenID,
    };

    const json = JSON.stringify(obj);
    

    $.ajax({
        async: true,
        type: 'POST',
        headers: {"Access-Control-Allow-Origin": "*"},
        contentType: "application/json",
        url: 'https://speech.rohitrnath.xyz/hello',
        data: json,
        processData: false
    })
    .done(function (response){
        console.log(response);
        if(JSON.parse(response["status"]) == true)
        {

            NLPInferText();

        }
    })
    .fail(function(){
        document.getElementById("debugMsg").innerHTML = "Reconnecting to training server...";
        setTimeout(pingToMachine, 10000);
    });
}


(function($) {



    var form = $("#signup-form");
    form.validate({
        errorPlacement: function errorPlacement(error, element) {
            element.before(error);
        },
        rules: {
            email: {
                email: true
            }
        },
        onfocusout: function(element) {
            $(element).valid();
        },
    });
    form.children("div").steps({
        headerTag: "h3",
        bodyTag: "fieldset",
        transitionEffect: "fade",
        stepsOrientation: "vertical",
        startIndex: 1,
        titleTemplate: '<div class="title"><span class="step-number">#index#</span><span class="step-text">#title#</span></div>',
        labels: {
            previous: 'Previous',
            next: 'Next',
            finish: 'Predict',
            current: ''
        },
        onStepChanging: function(event, currentIndex, newIndex) {

            if (currentIndex === 0) {
        
                form.parent().parent().parent().append('<div class="footer footer-' + currentIndex + '"></div>');
            }
            if (currentIndex === 1) {
                if(newIndex===0)
                {
                    window.location.href = 'index.html';
                }
                
                form.parent().parent().parent().find('.footer').removeClass('footer-0').addClass('footer-' + currentIndex + '');
            }

            form.validate().settings.ignore = ":disabled,:hidden";
            return form.valid();
        },
        onFinishing: function(event, currentIndex) {
            form.validate().settings.ignore = ":disabled,:hidden";
            return form.valid();
        },
        onFinished: function(event, currentIndex) {
            if(tokenID ==="")
            {
                alert("First submit a valid AccessID and continue");
            }
            else
            {
                if(project === "IMG_REC_MULTI")
                {
                    document.getElementById('debugMsg').innerHTML = "Checking with D-Coders AI!"
                    turnOnMachine();
                    
                    predictImage();
                    document.getElementById('debugMsg').innerHTML = "Analysing your Chest X-Ray image!!"
                    
                }
                else if(project === "NLP_CLS")
                {
                    var message = document.getElementById('NLPtextBox').value;
                    if (!message.length) {
                        alert('First fill the text box and continue!');
                        return false;
                    }

                    turnOnMachine();
                    setTimeout(pingToMachine, 1000);
                }
                
            }
        },
        onStepChanged: function(event, currentIndex, priorIndex) {
            
            return true;
        }
    });

    
})(jQuery);
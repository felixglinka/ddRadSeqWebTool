
function updateInput(value) {
   sumAllBasesOfEveryBin = dataFrameData['sumAllBasesOfEveryBin'][Object.keys(dataFrameData['sumAllBasesOfEveryBin'])[parseInt(value)]];
   sumAllFragmentsLengthsOfEveryBin = dataFrameData['sumAllFragmentsLengthsOfEveryBin'][Object.keys(dataFrameData['sumAllFragmentsLengthsOfEveryBin'])[parseInt(value)]];
   maxNumberOfPossibleSamples = dataFrameData['maxNumberOfSamplesToSequence'][Object.keys(dataFrameData['maxNumberOfSamplesToSequence'])[parseInt(value)]];
   numberBasesToBeSequenced = dataFrameData['numberBasesToBeSequenced'][Object.keys(dataFrameData['numberBasesToBeSequenced'])[parseInt(value)]];
   document.getElementById('output').innerHTML=Object.keys(dataFrameData['maxNumberOfSamplesToSequence'])[parseInt(value)] + " " + sumAllBasesOfEveryBin +
   " " + sumAllFragmentsLengthsOfEveryBin + " " + maxNumberOfPossibleSamples + " " + numberBasesToBeSequenced;
}

window.onload = function(e){

    if(document.body.contains(document.getElementById("output")))  {
        document.getElementById('output').innerHTML=Object.keys(dataFrameData['maxNumberOfSamplesToSequence'])[30].concat(" ",
        dataFrameData['sumAllBasesOfEveryBin'][Object.keys(dataFrameData['sumAllFragmentsLengthsOfEveryBin'])[30]], " ",
        dataFrameData['sumAllFragmentsLengthsOfEveryBin'][Object.keys(dataFrameData['sumAllFragmentsLengthsOfEveryBin'])[30]], " ",
        dataFrameData['maxNumberOfSamplesToSequence'][Object.keys(dataFrameData['maxNumberOfSamplesToSequence'])[30]], " ",
        dataFrameData['numberBasesToBeSequenced'][Object.keys(dataFrameData['numberBasesToBeSequenced'])[30]]
        )
    }
}


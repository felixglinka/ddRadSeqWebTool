function sumUpFragmentLengths(inputArray){

    totalFragmentLengths = []

    inputArray.forEach( function(firstElement, index) {
        totalFragmentLengths.push(inputArray.slice(index).reduce((a, b) => a + b, 0));
    })

    return totalFragmentLengths;
}

function calculateSamplesToBeMultiplexed(totalFragmentLength, sequencingYield, coverage){

    sequencingDepth = totalFragmentLength == 0 ? 0 : sequencingYield/totalFragmentLength;
    return Math.round(sequencingDepth/coverage);
}

function experimentalEstimation(selectedFragmentLength, slope, sliderOneValue, sequenceLength, contaminationValue) {

    numberOfAdaptorContamination = Math.round(selectedFragmentLength*slope)
    console.log(numberOfAdaptorContamination)

    if( sliderOneValue <= sequenceLength/10) {
        return contaminationValue + numberOfAdaptorContamination;
    } else {
        return numberOfAdaptorContamination;
    }
}
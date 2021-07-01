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

function experimentalEstimation(fragmentLengths, slope, sliderOneValue, sequenceLength, contaminationValue) {

    selectedFragmentLength = parseInt(sliderOneValue) == 0 ? Object.values(fragmentLengths)[0] :
                             parseInt(sliderOneValue) <= sequenceLength/10 ? sumUpFragmentLengths(Object.values(fragmentLengths).slice(0, parseInt(sliderOneValue)))[0] :
                             sumUpFragmentLengths(Object.values(fragmentLengths).slice(0, sequenceLength/10))[0]

    numberOfAdaptorContamination = Math.round(selectedFragmentLength*slope)

    if( sliderOneValue <= sequenceLength/10) {
        return contaminationValue + numberOfAdaptorContamination;
    } else {
        return numberOfAdaptorContamination;
    }
}
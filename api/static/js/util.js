function calculateDataFrameValues(sliderOneValue, sliderTwoValue, dataFrame, restrictionEnzymes, currentSelectedFragmentSize, experimentalAdaptorContamination, experimentalOverlaps){

   sumAllBasesOfEveryBin = sumUpFragmentLengths(Object.values(dataFrame['numberSequencedBasesOfBin']).slice(0, parseInt(sliderTwoValue)))[parseInt(sliderOneValue)];
   sumAllBasesOfEveryBin = Math.round(sumAllBasesOfEveryBin + experimentalAdaptorContamination*(2/3)*parseInt(basepairLengthToBeSequenced) + experimentalOverlaps*(0.5*2)*parseInt(basepairLengthToBeSequenced))
   maxNumberOfPossibleSamples = calculateSamplesToBeMultiplexed(currentSelectedFragmentSize, sequencingYield, coverage);
   numberBasesToBeSequenced = maxNumberOfPossibleSamples*sumAllBasesOfEveryBin;

   adaptorContaminationSliderOne = dataFrame['adaptorContamination'][Object.keys(dataFrame['adaptorContamination'])[parseInt(sliderOneValue)]];
   adaptorContaminationSliderTwo = dataFrame['adaptorContamination'][Object.keys(dataFrame['adaptorContamination'])[parseInt(sliderTwoValue)]];
   adaptorContamination = adaptorContaminationSliderOne - adaptorContaminationSliderTwo
   adaptorContaminationPercentage = currentSelectedFragmentSize === 0 ? 0 : String(Math.round((adaptorContaminationSliderOne - adaptorContaminationSliderTwo)/currentSelectedFragmentSize*100));

   return {
        'currentSelectedFragmentSize': currentSelectedFragmentSize,
        'sumAllBasesOfEveryBin': sumAllBasesOfEveryBin,
        'maxNumberOfPossibleSamples': maxNumberOfPossibleSamples,
        'numberBasesToBeSequenced': numberBasesToBeSequenced
   }
}

function calculateAdaptorContamination(sliderOneValue, sliderTwoValue, dataFrame, currentSelectedFragmentSize) {

   adaptorContaminationSliderOne = dataFrame['adaptorContamination'][Object.keys(dataFrame['adaptorContamination'])[parseInt(sliderOneValue)]];
   adaptorContaminationSliderTwo = dataFrame['adaptorContamination'][Object.keys(dataFrame['adaptorContamination'])[parseInt(sliderTwoValue)]];
   adaptorContamination = adaptorContaminationSliderOne - adaptorContaminationSliderTwo
   adaptorContaminationPercentage = currentSelectedFragmentSize === 0 ? 0 : String(Math.round((adaptorContaminationSliderOne - adaptorContaminationSliderTwo)/currentSelectedFragmentSize*100));

   return {
        'adaptorContamination': adaptorContamination,
        'adaptorContaminationPercentage': adaptorContaminationPercentage
   }
}

function calculateOverlaps(sliderOneValue, sliderTwoValue, dataFrame, currentSelectedFragmentSize) {

       overlapsSliderOne = dataFrame['overlaps'][Object.keys(dataFrame['overlaps'])[parseInt(sliderOneValue)]];
       overlapsSliderTwo = dataFrame['overlaps'][Object.keys(dataFrame['overlaps'])[parseInt(sliderTwoValue)]];
       overlaps = overlapsSliderOne - overlapsSliderTwo
       overlapPercentage = currentSelectedFragmentSize === 0 ? 0 : String(Math.round((overlapsSliderOne - overlapsSliderTwo)/currentSelectedFragmentSize*100));

   return {
        'overlaps': overlaps,
        'overlapPercentage': overlapPercentage
   }
}

function calculateExperimentalAdapterContamination(fragmentLengths, slope, sliderOneValue, sequenceLength, contaminationValue) {

    selectedFragmentLength = parseInt(sliderOneValue) == 0 ? Object.values(fragmentLengths)[0] :
                             parseInt(sliderOneValue) <= parseInt(sequenceLength)/10 ? sumUpFragmentLengths(Object.values(fragmentLengths).slice(0, parseInt(sliderOneValue)))[0] :
                             sumUpFragmentLengths(Object.values(fragmentLengths).slice(0, parseInt(sequenceLength)/10))[0]

    numberOfAdaptorContamination = Math.round(selectedFragmentLength*slope)

    if( sliderOneValue <= parseInt(sequenceLength)/10) {
        return contaminationValue + numberOfAdaptorContamination;
    } else {
        return numberOfAdaptorContamination;
    }
}

function calculateExperimentalOverlaps(fragmentLengths, slope, sliderOneValue, sequenceLength, overlapValue) {

    console.log(Object.values(fragmentLengths).slice(parseInt(sequenceLength/10), parseInt(sequenceLength)*2/10))

    selectedFragmentLength = parseInt(sliderOneValue) < parseInt(sequenceLength)/10 || parseInt(sliderOneValue) >= parseInt(sequenceLength*2)/10 ?
                              sumUpFragmentLengths(Object.values(fragmentLengths).slice(parseInt(sequenceLength/10), parseInt(sequenceLength)*2/10))[0] :
                              sumUpFragmentLengths(Object.values(fragmentLengths).slice(parseInt(sequenceLength/10), parseInt(sliderOneValue)))[0]

    numberOfOverlaps = Math.round(selectedFragmentLength*slope)

    if(sliderOneValue <= parseInt(sequenceLength)/10 || sliderOneValue > parseInt(sequenceLength*2)/10) {
        return numberOfOverlaps;
    } else {
        return overlapValue + numberOfOverlaps;
    }
}

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
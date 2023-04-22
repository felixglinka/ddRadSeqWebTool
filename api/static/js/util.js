const sliderMaxValue = "100";

function createIcon(id){
    questionIcon = document.createElement('div');
    questionIcon.id = id;
    questionIcon.className = "questionIcon";
    questionIcon.setAttribute('data-bs-toggle', 'popover');
    questionIcon.title = "Popover title";

    return questionIcon
}

function calculateMaxBasePairsToBeSequencedInLane(){

    sequenceLength = parseInt(basepairLengthToBeSequenced)
    pairedEndModifier = 2

    if(pairedEndChoice === 'single end') {
        pairedEndModifier = 1
    }

    return parseInt(sequencingYield) * sequenceLength * pairedEndModifier/ coverage
}

function calculateDataFrameValues(sliderOneValue, sliderTwoValue, enzymeData, restrictionEnzymes, currentSelectedFragmentSize, experimentalAdaptorContamination, experimentalOverlaps){

   sumAllBasesOfEveryBin = sumUpFragmentLengths(Object.values(enzymeData['numberSequencedBasesOfBin']).slice(0, parseInt(sliderTwoValue)))[parseInt(sliderOneValue)];
   sumAllBasesOfEveryBin = Math.round( sliderOneValue >= basepairLengthToBeSequenced/10 ? sumAllBasesOfEveryBin + experimentalOverlaps*parseInt(basepairLengthToBeSequenced) + experimentalAdaptorContamination*(2/3)*parseInt(basepairLengthToBeSequenced) : sumAllBasesOfEveryBin + experimentalAdaptorContamination*(2/3)*parseInt(basepairLengthToBeSequenced))
   maxNumberOfPossibleSamples = calculateSamplesToBeMultiplexed(currentSelectedFragmentSize, sequencingYield, coverage);
   numberBasesToBeSequenced = maxNumberOfPossibleSamples*sumAllBasesOfEveryBin;

   return {
        'currentSelectedFragmentSize': currentSelectedFragmentSize,
        'sumAllBasesOfEveryBin': sumAllBasesOfEveryBin,
        'maxNumberOfPossibleSamples': Math.round(maxNumberOfPossibleSamples),
        'numberBasesToBeSequenced': numberBasesToBeSequenced
   }
}

function calculateAdaptorContamination(sliderOneValue, sliderTwoValue, enzymeData, currentSelectedFragmentSize) {

   adaptorContaminationSliderOne = enzymeData['adaptorContamination'][Object.keys(enzymeData['adaptorContamination'])[parseInt(sliderOneValue)]];
   adaptorContaminationSliderTwo = enzymeData['adaptorContamination'][Object.keys(enzymeData['adaptorContamination'])[parseInt(sliderTwoValue)]];
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
   overlaps = overlapsSliderOne - overlapsSliderTwo
   overlapPercentage = currentSelectedFragmentSize === 0 ? 0 : String(Math.round((overlapsSliderOne - overlapsSliderTwo)/currentSelectedFragmentSize*100));

   return {
        'overlaps': overlaps,
        'overlapPercentage': overlapPercentage
   }
}

function calculatepreExperimentalAdapterContamination(fragmentLengths, sliderOneValue, sequenceLength, contaminationValue) {

    selectedFragmentLength = parseInt(sliderOneValue) <= parseInt(sequenceLength)/10 ? sumUpFragmentLengths(Object.values(fragmentLengths).slice(0, parseInt(sliderOneValue)))[0] :
                             sumUpFragmentLengths(Object.values(fragmentLengths).slice(0, parseInt(sequenceLength)/10))[0]

    numberOfAdaptorContamination = selectedFragmentLength

    if(sliderOneValue == 0) {
         return contaminationValue
    } else if(sliderOneValue <= parseInt(sequenceLength)/10) {
        return contaminationValue + numberOfAdaptorContamination;
    } else {
        return numberOfAdaptorContamination;
    }
}

function calculateExperimentalAdapterContamination(experimentalSelectedFragmentSize, preExperimentalAdaptorContaminationPercentage) {
    return Math.round(experimentalSelectedFragmentSize * preExperimentalAdaptorContaminationPercentage)
}

function calculatepreExperimentalOverlaps(fragmentLengths, sliderOneValue, sequenceLength, overlapValue) {

    selectedFragmentLength =  parseInt(sliderOneValue) <= parseInt(sequenceLength)/10 || parseInt(sliderOneValue) >= parseInt(sequenceLength*2)/10 ?
                              sumUpFragmentLengths(Object.values(fragmentLengths).slice(parseInt(sequenceLength/10), parseInt(sequenceLength)*2/10))[0] :
                              sumUpFragmentLengths(Object.values(fragmentLengths).slice(parseInt(sequenceLength/10), parseInt(sliderOneValue)))[0]

    numberOfOverlaps = sliderOneValue >= basepairLengthToBeSequenced/10 ? Math.round(selectedFragmentLength) : 0

    if(sliderOneValue > parseInt(sequenceLength*2)/10) {
        return numberOfOverlaps;
    } else if(sliderOneValue <= parseInt(sequenceLength)/10) {
        return overlapValue;
    } else {
        return overlapValue + numberOfOverlaps;
    }
}

function calculateExperimentalOverlaps(experimentalSelectedFragmentSize, preExperimentalOverlapPercentage) {
    return Math.round(experimentalSelectedFragmentSize * preExperimentalOverlapPercentage)
}

function calculateExperimentalFragments(fragmentLengths, sliderOneValue, preExperimentalAdaptorContaminationPercentage, preExperimentalOverlapPercentage) {

    experimentalFragments = sumUpFragmentLengths(Object.values(fragmentLengths).slice(parseInt(sliderOneValue), sliderMaxValue))[0] / (1 - preExperimentalOverlapPercentage - preExperimentalAdaptorContaminationPercentage)

    return Math.round(experimentalFragments)
}

function sumUpFragmentLengths(inputArray){

    totalFragmentLengths = []

    inputArray.forEach( function(firstElement, index) {
        totalFragmentLengths.push(inputArray.slice(index).reduce((a, b) => a + b, 0));
    })

    return totalFragmentLengths;
}

function calculateSamplesToBeMultiplexed(totalFragmentLength, sequencingYield, coverage){

    sequencingDepth = totalFragmentLength === 0 ? 0 : sequencingYield/totalFragmentLength;
    return sequencingDepth/coverage;
}
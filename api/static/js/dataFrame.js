const minGap = 1;
const sliderMaxValue = "100";
const adaptorContaminationSlope = 0.4424;
const overlapSlope = 0.5797;

let columnNumber = 3
const dataFrameTitles = ['No. fragments', 'No. basepairs in insilico digested sample', 'No. samples multiplexable', 'No. basepairs sequenced in the lane', 'Fragments under '.concat(basepairLengthToBeSequenced)]
const overlapTitle = "Fragments between ".concat(basepairLengthToBeSequenced).concat(" and ").concat(parseInt(basepairLengthToBeSequenced)*2)

function slideOne(sliderOne, sliderTwo, resultTable, dataFrame, restrictionEnzymes) {

    if(parseInt(sliderTwo.value) - parseInt(sliderOne.value) <= minGap){
        sliderOne.value = parseInt(sliderTwo.value) - minGap;
    }
    updateSliderResult(sliderOne.value, sliderTwo.value, resultTable, dataFrame, restrictionEnzymes)
}

function slideTwo(sliderTwo, sliderOne, resultTable, dataFrame, restrictionEnzymes) {

    if(parseInt(sliderTwo.value) - parseInt(sliderOne.value) <= minGap){
        sliderTwo.value = parseInt(sliderOne.value) + minGap;
    }

    if(pairedEndChoice === 'paired end') {
        sliderTwo.value = parseInt(sliderTwo.value) <= basepairLengthToBeSequenced/10*2 ? basepairLengthToBeSequenced/10*2 : parseInt(sliderTwo.value)
    } else {
        sliderTwo.value = parseInt(sliderTwo.value) <= basepairLengthToBeSequenced/10 ? basepairLengthToBeSequenced/10 : parseInt(sliderTwo.value)
    }

    updateSliderResult(sliderOne.value, sliderTwo.value, resultTable, dataFrame, restrictionEnzymes)
}

function updateSliderResult(sliderOneValue, sliderTwoValue, resultTable, dataFrame, restrictionEnzymes) {

   currentSelectedFragmentSize = sumUpFragmentLengths(Object.values(dataFrame[restrictionEnzymes]).slice(0, parseInt(sliderTwoValue)))[parseInt(sliderOneValue)];
   adaptorContaminationValues = calculateAdaptorContamination(sliderOneValue, sliderTwoValue, dataFrame, currentSelectedFragmentSize)
   theoreticalDataFrameValues = calculateDataFrameValues(sliderOneValue, sliderTwoValue, dataFrame, restrictionEnzymes, currentSelectedFragmentSize,0,0)

   experimentalAdaptorContamination = currentSelectedFragmentSize != 0 ? calculateExperimentalAdapterContamination(dataFrame[restrictionEnzymes], adaptorContaminationSlope, sliderOneValue, basepairLengthToBeSequenced, adaptorContamination) : 0
   experimentalSelectedFragmentSize = sliderOneValue > basepairLengthToBeSequenced/10 ?  currentSelectedFragmentSize != 0 ? currentSelectedFragmentSize + experimentalAdaptorContamination : 0 : currentSelectedFragmentSize

   experimentalOverlaps = 0
   if(pairedEndChoice === 'paired end') {
    overlapValues = calculateOverlaps(sliderOneValue, sliderTwoValue, dataFrame, currentSelectedFragmentSize)
    experimentalOverlaps = currentSelectedFragmentSize != 0 ? calculateExperimentalOverlaps(dataFrame[restrictionEnzymes], overlapSlope, sliderOneValue, parseInt(basepairLengthToBeSequenced), overlaps) : 0
    experimentalSelectedFragmentSize = sliderOneValue > basepairLengthToBeSequenced/10 ?  currentSelectedFragmentSize != 0 ? experimentalSelectedFragmentSize + experimentalOverlaps : 0 : experimentalSelectedFragmentSize
    experimentalOverlapPercentage = currentSelectedFragmentSize === 0 ? 0 : String(Math.round((experimentalOverlaps)/experimentalSelectedFragmentSize*100));

    resultTable.tBodies[0].rows[5].cells[1].innerText = String(overlapValues.overlaps).concat().concat(' [')
                                                            .concat(overlapValues.overlapPercentage).concat('%]')
    resultTable.tBodies[0].rows[5].cells[2].innerText = String(experimentalOverlaps)
                                                            .concat(' [').concat(experimentalOverlapPercentage).concat('%]');
   }

   experimentalAdaptorContaminationPercentage = currentSelectedFragmentSize === 0 ? 0 : String(Math.round((experimentalAdaptorContamination/experimentalSelectedFragmentSize)*100));
   experimentalDataFrameValues = calculateDataFrameValues(sliderOneValue, sliderTwoValue, dataFrame, restrictionEnzymes, experimentalSelectedFragmentSize, experimentalAdaptorContamination, experimentalOverlaps)


   resultTable.tHead.rows[0].cells[1].innerText = "Sequencing calculation from ".concat(Object.keys(dataFrame[restrictionEnzymes])[parseInt(sliderOneValue)].split(",")[0].substring(1))
                                                                                .concat(" to ")
                                                                                .concat(Object.keys(dataFrame[restrictionEnzymes])[parseInt(sliderTwoValue)].split(",")[1].slice(0, -1))
                                                                                .concat(" bp");
                                                                                
   resultTable.tBodies[0].rows[0].cells[1].innerText = currentSelectedFragmentSize;
   resultTable.tBodies[0].rows[1].cells[1].innerText = theoreticalDataFrameValues.sumAllBasesOfEveryBin;
   resultTable.tBodies[0].rows[2].cells[1].innerText = theoreticalDataFrameValues.maxNumberOfPossibleSamples;
   resultTable.tBodies[0].rows[3].cells[1].innerText = (theoreticalDataFrameValues.numberBasesToBeSequenced).toLocaleString(undefined, { minimumFractionDigits: 0 });
   resultTable.tBodies[0].rows[4].cells[1].innerText = String(adaptorContaminationValues.adaptorContamination).concat(' [')
                                                            .concat(adaptorContaminationValues.adaptorContaminationPercentage).concat('%]');

   resultTable.tBodies[0].rows[0].cells[2].innerText = experimentalSelectedFragmentSize;
   resultTable.tBodies[0].rows[1].cells[2].innerText = experimentalDataFrameValues.sumAllBasesOfEveryBin;
   resultTable.tBodies[0].rows[2].cells[2].innerText = experimentalDataFrameValues.maxNumberOfPossibleSamples;
   resultTable.tBodies[0].rows[3].cells[2].innerText = (experimentalDataFrameValues.numberBasesToBeSequenced).toLocaleString(undefined, { minimumFractionDigits: 0 });
   resultTable.tBodies[0].rows[4].cells[2].innerText = String(experimentalAdaptorContamination)
                                                            .concat(' [').concat(experimentalAdaptorContaminationPercentage).concat('%]');

}

function generateDataFrameTableHead(table, restrictionEnzymes) {
  tableCaption = table.createCaption()
  tableCaption.innerHTML = restrictionEnzymes.concat("<br>").concat(basepairLengthToBeSequenced).concat(" bp")
  .concat("&nbsp;").concat(pairedEndChoice).concat("<br>Sequencing Yield: ").concat(sequencingYield)
  .concat(" bp - Coverage: ").concat(coverage)
  let thead = table.createTHead();
  let firstHeaderRow = thead.insertRow();
  let secondHeaderRow = thead.insertRow();

  for (let i = 0; i < columnNumber-1; i++) {
    let th = document.createElement("th");
    if(i == 0) {
      th.style.width = '45%';
    }
    if(i == 1) {
      th.style.width = '55%';
      th.colSpan ='2';
      th.scope='colgroup';
    }
    firstHeaderRow.appendChild(th);
  }

  for (let i = 0; i < columnNumber; i++) {
    let th = document.createElement("th");
    if(i == 0) {
      th.style.width = '46%';
    }if(i == 1) {
      th.style.width = '27%';
    }if(i == 1) {
      th.style.width = '27%';
    }
    secondHeaderRow.appendChild(th);
  }
  secondHeaderRow.cells[1].innerText = "theoretical"
  secondHeaderRow.cells[2].innerText = "experimental"
}

function generateDataframeTableRows(table) {

    let tbody = table.createTBody();

    dataFrameTitles.forEach( function(title) {
        let row = tbody.insertRow();
        for (let i = 0; i < columnNumber; i++) {
          if (i == 0) {

            th = document.createElement('th');
            th.style = 'display: flex;'
            titleElement = document.createElement('span');
            titleElement.className = 'right4'
            titleElement.appendChild(document.createTextNode(title));
            th.appendChild(titleElement);
            th.scope='row';

            if( title === 'No. samples multiplexed') {
                th.appendChild(createIcon("samplesMultiplexedHelp"));
            }

            if(title === "No. basepairs sequenced in the lane") {
                th.appendChild(createIcon("basepairsSequencedHelp"));
            }

            if( title === 'Fragments under '.concat(basepairLengthToBeSequenced) ) {
                th.style="color:red; display: flex;"
                th.appendChild(createIcon("adapterContaminationHelp"));
            }

            if( title === overlapTitle ) {
                th.style="color:red; display: flex;"
                th.appendChild(createIcon("overlapHelp"));
            }

            row.appendChild(th);
          } else {
            row.insertCell();
          }
       }
    })
}

function generateDataframeTable(dataFrameElement, tableId, restrictionEnzymes){
    let table = document.createElement("table");
    table.id = tableId
    table.className = "table table-striped"
    dataFrameElement.appendChild(table);
    generateDataFrameTableHead(table, restrictionEnzymes);
    generateDataframeTableRows(table);
}

function generateSlider(inputElement, tableId, idSliderOne, idSliderTwo, dataFrame, restrictionEnzymes) {

    let sliderTrack = document.createElement("div");
    sliderTrack.className = "form-group slider-track";
    let firstSlider = document.createElement("input");
    let secondSlider = document.createElement("input");
    let resultTable = document.getElementById(tableId)

    if(pairedEndChoice === 'paired end') {
        sliderTrack.style = 'background: linear-gradient(to right, #ff0000 0%, #ffff00 25%, #00ff00 35%, #00ff00 45%, #ffff00 100%);'
    } else {
        sliderTrack.style = 'background: linear-gradient(to right, #ff0000 0%, #ffff00 25%, #00ff00 35%, #00ff00 45%, #ffff00 100%);'
    }

    fillSlider(firstSlider, secondSlider, '30', idSliderOne, slideOne, resultTable, dataFrame, restrictionEnzymes)
    fillSlider(secondSlider, firstSlider, '100', idSliderTwo, slideTwo, resultTable, dataFrame, restrictionEnzymes)

    sliderTrack.appendChild(firstSlider);
    sliderTrack.appendChild(secondSlider);
    inputElement.appendChild(sliderTrack);
}

function fillSlider(selfSlider, otherSlider, startingValue, id, inputFunction, resultTable, dataFrame, restrictionEnzymes){
    selfSlider.type = "range";
    selfSlider.className = "form-range";
    selfSlider.min = "0";
    selfSlider.max = "100";
    selfSlider.value = startingValue;
    selfSlider.id = id;
    selfSlider.addEventListener('input', function() {inputFunction(selfSlider, otherSlider, resultTable, dataFrame, restrictionEnzymes)}, true);
    selfSlider.addEventListener('change', function() {inputFunction(selfSlider, otherSlider, resultTable, dataFrame, restrictionEnzymes)}, true);
}

function addSliderMarkers(firstSliderId, basepairLengthToBeSequenced){

    if(basepairLengthToBeSequenced > 1000){
        return;
    }

    let markerPosition = basepairLengthToBeSequenced/10;

    let line = document.createElement('div');
    line.className = "line";
    line.style = 'left:'.concat(String(markerPosition > 18 ? markerPosition : markerPosition + 1)).concat("%;")

    let lineTick = document.createElement('label');
    lineTick.className = "lineTick";
    let lineTickText = document.createTextNode(String(basepairLengthToBeSequenced).concat(" bp"));
    lineTick.appendChild(lineTickText);

    sliderTrackDiv = document.getElementById(firstSliderId).parentElement;
    line.append(lineTick)
    sliderTrackDiv.append(line)
}

function alignMarkerText(markerPosition) {

    if(markerPosition < 100) {
        return String(markerPosition - 3);
    } else if(markerPosition > 100) {
        return String(markerPosition - 5);
    } else {
        return String(markerPosition - 4);
    }

}

function buildUpDataFrame(inputElement, tableId, restrictionEnzymes, idSliderOne, idSliderTwo, dataFrame) {
    generateDataframeTable(inputElement, tableId, restrictionEnzymes)
    generateSlider(inputElement, tableId, idSliderOne, idSliderTwo, dataFrame, restrictionEnzymes)
}

function initDataframe() {

    if(document.body.contains(document.getElementById("dataFrame")))  {

        if(pairedEndChoice === 'paired end') {
            dataFrameTitles.push(overlapTitle);
        }

        sliderOneId = "slider-1"
        sliderTwoId = "slider-2"
        dataFrameTableId = "dataFrameTable"

        buildUpDataFrame(document.getElementById("dataFrame"), dataFrameTableId, firstChosenRestrictionEnzymes, sliderOneId, sliderTwoId, dataFrameData)

        let sliderOne = document.getElementById(sliderOneId);
        let sliderTwo = document.getElementById(sliderTwoId);
        let dataFrameTable = document.getElementById(dataFrameTableId)
        slideOne(sliderOne, sliderTwo, dataFrameTable, dataFrameData, firstChosenRestrictionEnzymes)
        slideTwo(sliderTwo, sliderOne, dataFrameTable, dataFrameData, firstChosenRestrictionEnzymes)

        addSliderMarkers(sliderOneId, parseInt(basepairLengthToBeSequenced))
        if(pairedEndChoice === 'paired end') {
            addSliderMarkers(sliderOneId, parseInt(basepairLengthToBeSequenced)*2)
        }
    }

    if(document.body.contains(document.getElementById("dataFrame1")) &&
       document.body.contains(document.getElementById("dataFrame2")))  {

               if(pairedEndChoice === 'paired end') {
                    dataFrameTitles.push(overlapTitle);
                }

               firstSliderOneId = "firstSlider-1"
               firstSliderTwoId = "firstSlider-2"
               firstDataFrameTableId = "firstDataFrameTable"

               buildUpDataFrame(document.getElementById("dataFrame1"), firstDataFrameTableId, firstChosenRestrictionEnzymes, firstSliderOneId, firstSliderTwoId, dataFrame1Data)

               let firstSliderOne = document.getElementById(firstSliderOneId);
               let firstSliderTwo = document.getElementById(firstSliderTwoId);
               let firstDataFrameTable = document.getElementById(firstDataFrameTableId);
               slideOne(firstSliderOne, firstSliderTwo, firstDataFrameTable, dataFrame1Data, firstChosenRestrictionEnzymes)
               slideTwo(firstSliderTwo, firstSliderOne, firstDataFrameTable, dataFrame1Data, firstChosenRestrictionEnzymes)

               addSliderMarkers(firstSliderOneId, parseInt(basepairLengthToBeSequenced))
               if(pairedEndChoice === 'paired end') {
                addSliderMarkers(firstSliderOneId, parseInt(basepairLengthToBeSequenced)*2)
               }

               secondSliderOneId = "secondSlider-1"
               secondSliderTwoId = "secondSlider-2"
               secondDataFrameTableId = "secondDataFrameTable"

               buildUpDataFrame(document.getElementById("dataFrame2"), secondDataFrameTableId, secondChosenRestrictionEnzymes, secondSliderOneId, secondSliderTwoId, dataFrame2Data)

               let secondSliderOne = document.getElementById(secondSliderOneId);
               let secondSliderTwo = document.getElementById(secondSliderTwoId);
               let secondDataFrameTable = document.getElementById(secondDataFrameTableId);
               slideOne(secondSliderOne, secondSliderTwo, secondDataFrameTable, dataFrame2Data, secondChosenRestrictionEnzymes)
               slideTwo(secondSliderTwo, secondSliderOne, secondDataFrameTable, dataFrame2Data, secondChosenRestrictionEnzymes)

               addSliderMarkers(secondSliderOneId, parseInt(basepairLengthToBeSequenced))
               if(pairedEndChoice === 'paired end') {
                addSliderMarkers(secondSliderOneId, parseInt(basepairLengthToBeSequenced)*2)
               }
    }
}


window.addEventListener('load', initDataframe)
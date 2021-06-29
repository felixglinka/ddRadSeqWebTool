const minGap = 1;
const sliderMaxValue = "100";

let columnNumber = 2
const dataFrameTitles = ['No. fragments', 'No. basepairs in insilico digested sample', 'No. samples multiplexed', 'No. basepairs sequenced in the lane', 'Adapter Contamination']

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
    updateSliderResult(sliderOne.value, sliderTwo.value, resultTable, dataFrame, restrictionEnzymes)
}

function updateSliderResult(sliderOneValue, sliderTwoValue, resultTable, dataFrame, restrictionEnzymes) {
   sumAllFragmentsLengths = sumUpFragmentLengths(Object.values(dataFrame[restrictionEnzymes]).slice(0, parseInt(sliderTwoValue)))[parseInt(sliderOneValue)];
   sumAllBasesOfEveryBin = sumUpFragmentLengths(Object.values(dataFrame['numberSequencedBasesOfBin']).slice(0, parseInt(sliderTwoValue)))[parseInt(sliderOneValue)];
   maxNumberOfPossibleSamples = calculateSamplesToBeMultiplexed(sumAllFragmentsLengths, sequencingYield, coverage);
   numberBasesToBeSequenced = maxNumberOfPossibleSamples*sumAllBasesOfEveryBin;

   adaptorContaminationSliderOne = dataFrame['adaptorContamination'][Object.keys(dataFrame['adaptorContamination'])[parseInt(sliderOneValue)]];
   adaptorContaminationSliderTwo = dataFrame['adaptorContamination'][Object.keys(dataFrame['adaptorContamination'])[parseInt(sliderTwoValue)]];

   resultTable.tHead.rows[0].cells[1].innerText = "Sequencing calculation from ".concat(Object.keys(dataFrame[restrictionEnzymes])[parseInt(sliderOneValue)].split(",")[0].substring(1))
                                                                                .concat(" to ")
                                                                                .concat(Object.keys(dataFrame[restrictionEnzymes])[parseInt(sliderTwoValue)].split(",")[1].slice(0, -1))
                                                                                .concat(" bp");
   resultTable.tBodies[0].rows[0].cells[1].innerText = sumAllFragmentsLengths;
   resultTable.tBodies[0].rows[1].cells[1].innerText = sumAllBasesOfEveryBin;
   resultTable.tBodies[0].rows[2].cells[1].innerText = maxNumberOfPossibleSamples;
   resultTable.tBodies[0].rows[3].cells[1].innerText = numberBasesToBeSequenced;
   adaptorContaminationPercentage = sumAllFragmentsLengths === 0 ? 0 : String(Math.round((adaptorContaminationSliderOne - adaptorContaminationSliderTwo)/sumAllFragmentsLengths*100));
   resultTable.tBodies[0].rows[4].cells[1].innerText = String(adaptorContaminationSliderOne - adaptorContaminationSliderTwo).concat(' [')
                                                            .concat(adaptorContaminationPercentage).concat('%]');

   if(pairedEndChoice === 'paired end') {
       overlapsSliderOne = dataFrame['overlaps'][Object.keys(dataFrame['overlaps'])[parseInt(sliderOneValue)]];
       overlapsSliderTwo = dataFrame['overlaps'][Object.keys(dataFrame['overlaps'])[parseInt(sliderTwoValue)]];
       overlapPercentage = sumAllFragmentsLengths === 0 ? 0 : String(Math.round((overlapsSliderOne - overlapsSliderTwo)/sumAllFragmentsLengths*100));
       resultTable.tBodies[0].rows[5].cells[1].innerText = String(overlapsSliderOne - overlapsSliderTwo).concat().concat(' [')
                                                            .concat(overlapPercentage).concat('%]');
    }
}

function generateDataFrameTableHead(table, restrictionEnzymes) {
  tableCaption = table.createCaption()
  tableCaption.innerHTML = restrictionEnzymes.concat("<br>").concat(basepairLengthToBeSequenced).concat(" bp")
  .concat("&nbsp;").concat(pairedEndChoice).concat("<br>Sequencing Yield: ").concat(sequencingYield)
  .concat("&emsp;Coverage: ").concat(coverage)
  let thead = table.createTHead();
  let row = thead.insertRow();

  for (let i = 0; i < columnNumber; i++) {
    let th = document.createElement("th");
    if(i == 0) {
      th.style.width = '45%';
    }
    if(i == 1) {
      th.style.width = '55%';
    }
    row.appendChild(th);
  }

}

function generateDataframeTableRows(table) {

    let tbody = table.createTBody();

    dataFrameTitles.forEach( function(title) {
        let row = tbody.insertRow();
        for (let i = 0; i < columnNumber; i++) {
          if (i == 0) {

            th = document.createElement('th');
            th.appendChild(document.createTextNode(title));
            th.scope='row';

            if( title === 'Adapter Contamination' || title === "Overlapping Fragments") {
                th.style="color:red;"
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
    fillSlider(secondSlider, firstSlider, '80', idSliderTwo, slideTwo, resultTable, dataFrame, restrictionEnzymes)

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
            dataFrameTitles.push("Overlapping Fragments");
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
                    dataFrameTitles.push("Overlapping Fragments");
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
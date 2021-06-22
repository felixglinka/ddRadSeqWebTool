const minGap = 1;
const sliderMaxValue = "100";

//let sliderOne = null;
//let sliderTwo = null;


let dataFrameTitles = ['# bases of fragments', '# fragments', '# samples multiplexed', '# bases to be sequenced']

function slideOne(sliderOne, sliderTwo, resultTable, dataFrame) {

    if(parseInt(sliderTwo.value) - parseInt(sliderOne.value) <= minGap){
        sliderOne.value = parseInt(sliderTwo.value) - minGap;
    }
    updateSliderOneResult(sliderOne.value, resultTable, dataFrame)
    updateSliderTwoResult(sliderOne.value, sliderTwo.value, resultTable, dataFrame)
}

function slideTwo(sliderTwo, sliderOne, resultTable, dataFrame) {

    if(parseInt(sliderTwo.value) - parseInt(sliderOne.value) <= minGap){
        sliderTwo.value = parseInt(sliderOne.value) + minGap;
    }
    updateSliderTwoResult(sliderOne.value, sliderTwo.value, resultTable, dataFrame)
}

function updateSliderOneResult(sliderOneValue, resultTable, dataFrame) {
   sumAllBasesOfEveryBin = dataFrame['sumAllBasesOfEveryBin'][Object.keys(dataFrame['sumAllBasesOfEveryBin'])[parseInt(sliderOneValue)]];
   sumAllFragmentsLengthsOfEveryBin = dataFrame['sumAllFragmentsLengthsOfEveryBin'][Object.keys(dataFrame['sumAllFragmentsLengthsOfEveryBin'])[parseInt(sliderOneValue)]];
   maxNumberOfPossibleSamples = dataFrame['maxNumberOfSamplesToSequence'][Object.keys(dataFrame['maxNumberOfSamplesToSequence'])[parseInt(sliderOneValue)]];
   numberBasesToBeSequenced = dataFrame['numberBasesToBeSequenced'][Object.keys(dataFrame['numberBasesToBeSequenced'])[parseInt(sliderOneValue)]];

   resultTable.tHead.rows[0].cells[1].innerText = Object.keys(dataFrame['maxNumberOfSamplesToSequence'])[parseInt(sliderOneValue)];
   resultTable.tBodies[0].rows[0].cells[1].innerText = sumAllBasesOfEveryBin;
   resultTable.tBodies[0].rows[1].cells[1].innerText = sumAllFragmentsLengthsOfEveryBin;
   resultTable.tBodies[0].rows[2].cells[1].innerText = maxNumberOfPossibleSamples;
   resultTable.tBodies[0].rows[3].cells[1].innerText = numberBasesToBeSequenced;
}

function updateSliderTwoResult(sliderOneValue, sliderTwoValue, resultTable, dataFrame) {
   sumAllBasesOfEveryBinSliderOne = dataFrame['sumAllBasesOfEveryBin'][Object.keys(dataFrame['sumAllBasesOfEveryBin'])[parseInt(sliderOneValue)]];
   sumAllFragmentsLengthsOfEveryBinSliderOne = dataFrame['sumAllFragmentsLengthsOfEveryBin'][Object.keys(dataFrame['sumAllFragmentsLengthsOfEveryBin'])[parseInt(sliderOneValue)]];
   maxNumberOfPossibleSamplesSliderOne = dataFrame['maxNumberOfSamplesToSequence'][Object.keys(dataFrame['maxNumberOfSamplesToSequence'])[parseInt(sliderOneValue)]];
   numberBasesToBeSequencedSliderOne = dataFrame['numberBasesToBeSequenced'][Object.keys(dataFrame['numberBasesToBeSequenced'])[parseInt(sliderOneValue)]];

   sumAllBasesOfEveryBinSliderTwo = dataFrame['sumAllBasesOfEveryBin'][Object.keys(dataFrame['sumAllBasesOfEveryBin'])[parseInt(sliderTwoValue)]];
   sumAllFragmentsLengthsOfEveryBinSliderTwo = dataFrame['sumAllFragmentsLengthsOfEveryBin'][Object.keys(dataFrame['sumAllFragmentsLengthsOfEveryBin'])[parseInt(sliderTwoValue)]];
   maxNumberOfPossibleSamplesSliderTwo = dataFrame['maxNumberOfSamplesToSequence'][Object.keys(dataFrame['maxNumberOfSamplesToSequence'])[parseInt(sliderTwoValue)]];
   numberBasesToBeSequencedSliderTwo = dataFrame['numberBasesToBeSequenced'][Object.keys(dataFrame['numberBasesToBeSequenced'])[parseInt(sliderTwoValue)]];

   resultTable.tHead.rows[0].cells[2].innerText = "Difference from Interval ".concat(Object.keys(dataFrame['maxNumberOfSamplesToSequence'])[parseInt(sliderTwoValue)])
   resultTable.tBodies[0].rows[0].cells[2].innerText = sumAllBasesOfEveryBinSliderOne - sumAllBasesOfEveryBinSliderTwo;
   resultTable.tBodies[0].rows[1].cells[2].innerText = sumAllFragmentsLengthsOfEveryBinSliderOne - sumAllFragmentsLengthsOfEveryBinSliderTwo;
   resultTable.tBodies[0].rows[2].cells[2].innerText = maxNumberOfPossibleSamplesSliderTwo - maxNumberOfPossibleSamplesSliderOne;
   resultTable.tBodies[0].rows[3].cells[2].innerText = numberBasesToBeSequencedSliderTwo - numberBasesToBeSequencedSliderOne;
}

function generateDataFrameTableHead(table, restrictionEnzymes) {
  tableCaption = table.createCaption()
  tableCaption.innerHTML = restrictionEnzymes
  let thead = table.createTHead();
  let row = thead.insertRow();

  for (let i = 0; i < 3; i++) {
    let th = document.createElement("th");
    row.appendChild(th);
  }

}

function generateDataframeTableRows(table){

    let tbody = table.createTBody();

    dataFrameTitles.forEach(function(title) {
        let row = tbody.insertRow();
        for (let i = 0; i < 3; i++) {
          let cell = row.insertCell();
          if (i == 0) {
            let titleText = document.createTextNode(title);
            cell.appendChild(titleText);
          }
       }
    })
}

function generateDataframeTable(dataFrameElement, tableId, restrictionEnzymes){
    let table = document.createElement("table");
    table.id = tableId
    table.className = "table"
    dataFrameElement.appendChild(table);
    generateDataFrameTableHead(table, restrictionEnzymes);
    generateDataframeTableRows(table);
}

function generateSlider(inputElement, tableId, idSliderOne, idSliderTwo, dataFrame) {
    let sliderTrack = document.createElement("div");
    sliderTrack.className = "form-group slider-track";
    let firstSlider = document.createElement("input");
    let secondSlider = document.createElement("input");
    let resultTable = document.getElementById(tableId)

    fillSlider(firstSlider, secondSlider, '30', idSliderOne, slideOne, resultTable, dataFrame)
    fillSlider(secondSlider, firstSlider, '70', idSliderTwo, slideTwo, resultTable, dataFrame)

    sliderTrack.appendChild(firstSlider);
    sliderTrack.appendChild(secondSlider);
    inputElement.appendChild(sliderTrack);
}

function fillSlider(selfSlider, otherSlider, startingValue, id, inputFunction, resultTable, dataFrame){
    selfSlider.type = "range";
    selfSlider.className = "form-range";
    selfSlider.min = "0";
    selfSlider.max = "100";
    selfSlider.value = startingValue;
    selfSlider.id = id;
    selfSlider.addEventListener('input', function() {inputFunction(selfSlider, otherSlider, resultTable, dataFrame)}, true);
    selfSlider.addEventListener('change', function() {inputFunction(selfSlider, otherSlider, resultTable, dataFrame)}, true);
}

function buildUpDataFrame(inputElement, tableId, restrictionEnzymes, idSliderOne, idSliderTwo, dataFrame) {
    generateDataframeTable(inputElement, tableId, restrictionEnzymes)
    generateSlider(inputElement, tableId, idSliderOne, idSliderTwo, dataFrame)
}

function initDataframe() {

    if(document.body.contains(document.getElementById("dataFrame")))  {

        sliderOneId = "slider-1"
        sliderTwoId = "slider-2"
        dataFrameTableId = "dataFrameTable"

        buildUpDataFrame(document.getElementById("dataFrame"), dataFrameTableId, firstChosenRestrictionEnzymes, sliderOneId, sliderTwoId, dataFrameData)

        let sliderOne = document.getElementById(sliderOneId);
        let sliderTwo = document.getElementById(sliderTwoId);
        let dataFrameTable = document.getElementById(dataFrameTableId)
        slideOne(sliderOne, sliderTwo, dataFrameTable, dataFrameData)
        slideTwo(sliderTwo, sliderOne, dataFrameTable, dataFrameData)
    }

    if(document.body.contains(document.getElementById("dataFrame1")) &&
       document.body.contains(document.getElementById("dataFrame2")))  {

               firstSliderOneId = "firstSlider-1"
               firstSliderTwoId = "firstSlider-2"
               firstDataFrameTableId = "firstDataFrameTable"

               buildUpDataFrame(document.getElementById("dataFrame1"), firstDataFrameTableId, firstChosenRestrictionEnzymes, firstSliderOneId, firstSliderTwoId, dataFrame1Data)

               let firstSliderOne = document.getElementById(firstSliderOneId);
               let firstSliderTwo = document.getElementById(firstSliderTwoId);
               let firstDataFrameTable = document.getElementById(firstDataFrameTableId);
               slideOne(firstSliderOne, firstSliderTwo, firstDataFrameTable, dataFrame1Data)
               slideTwo(firstSliderTwo, firstSliderOne, firstDataFrameTable, dataFrame1Data)

               secondSliderOneId = "secondSlider-1"
               secondSliderTwoId = "secondSlider-2"
               secondDataFrameTableId = "secondDataFrameTable"

               buildUpDataFrame(document.getElementById("dataFrame2"), secondDataFrameTableId, secondChosenRestrictionEnzymes, secondSliderOneId, secondSliderTwoId, dataFrame2Data)

               let secondSliderOne = document.getElementById(secondSliderOneId);
               let secondSliderTwo = document.getElementById(secondSliderTwoId);
               let secondDataFrameTable = document.getElementById(secondDataFrameTableId);
               slideOne(secondSliderOne, secondSliderTwo, secondDataFrameTable, dataFrame2Data)
               slideTwo(secondSliderTwo, secondSliderOne, secondDataFrameTable, dataFrame2Data)
    }
}


window.addEventListener('load', initDataframe)
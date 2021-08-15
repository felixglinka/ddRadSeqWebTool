const minGap = 1;
const sliderMaxValue = "100";

let dataFrameValueTitles = []
let overlapTitle = ""

function slideOne(sliderOne, sliderTwo, rowId, enzymeData) {

    if(parseInt(sliderTwo.value) - parseInt(sliderOne.value) <= minGap){
        sliderOne.value = parseInt(sliderTwo.value) - minGap;
    }
    updateSliderResult(sliderOne.value, sliderTwo.value, rowId, enzymeData)
}

function slideTwo(sliderTwo, sliderOne, rowId, enzymeData) {

    if(parseInt(sliderTwo.value) - parseInt(sliderOne.value) <= minGap){
        sliderTwo.value = parseInt(sliderOne.value) + minGap;
    }

    if(pairedEndChoice === 'paired end') {
        sliderTwo.value = parseInt(sliderTwo.value) <= basepairLengthToBeSequenced/10*2 ? basepairLengthToBeSequenced/10*2 : parseInt(sliderTwo.value)
    } else {
        sliderTwo.value = parseInt(sliderTwo.value) <= basepairLengthToBeSequenced/10 ? basepairLengthToBeSequenced/10 : parseInt(sliderTwo.value)
    }

    updateSliderResult(sliderOne.value, sliderTwo.value, rowId, enzymeData)
}

function updateSliderResult(sliderOneValue, sliderTwoValue, rowId, enzymeData) {

   let rowElement = document.getElementById(rowId);

   rowElement.firstChild.lastChild.innerText = Object.keys(enzymeData[rowId])[parseInt(sliderOneValue)].split(",")[0].substring(1).concat(" to")
                                    .concat(Object.keys(enzymeData[rowId])[parseInt(sliderTwoValue)].split(",")[1].slice(0, -1)).concat(" bp");

   currentSelectedFragmentSize = sumUpFragmentLengths(Object.values(enzymeData[rowId]).slice(0, parseInt(sliderTwoValue)))[parseInt(sliderOneValue)];
   adaptorContaminationValues = calculateAdaptorContamination(sliderOneValue, sliderTwoValue, enzymeData, currentSelectedFragmentSize)
   theoreticalDataFrameValues = calculateDataFrameValues(sliderOneValue, sliderTwoValue, enzymeData, rowId, currentSelectedFragmentSize,0,0)

   experimentalAdaptorContamination = currentSelectedFragmentSize != 0 ? calculateExperimentalAdapterContamination(enzymeData[rowId], sliderOneValue, basepairLengthToBeSequenced, adaptorContamination) : 0
   experimentalSelectedFragmentSize = currentSelectedFragmentSize + (experimentalAdaptorContamination - adaptorContaminationValues.adaptorContamination)

   let experimentalOverlaps = 0
   if(pairedEndChoice === 'paired end') {
    overlapValues = calculateOverlaps(sliderOneValue, sliderTwoValue, enzymeData, currentSelectedFragmentSize)
    experimentalOverlaps = currentSelectedFragmentSize != 0 ? calculateExperimentalOverlaps(enzymeData[rowId], sliderOneValue, parseInt(basepairLengthToBeSequenced), overlaps) : 0
    experimentalSelectedFragmentSize = sliderOneValue >= basepairLengthToBeSequenced/10 ?  currentSelectedFragmentSize != 0 ? experimentalSelectedFragmentSize + (experimentalOverlaps - overlapValues.overlaps) : 0 : experimentalSelectedFragmentSize
    experimentalOverlapPercentage = currentSelectedFragmentSize === 0 ? 0 : String(Math.round((experimentalOverlaps)/experimentalSelectedFragmentSize*100));

    rowElement.cells[7].firstChild.innerText = String(overlapValues.overlaps).concat().concat(' [').concat(overlapValues.overlapPercentage).concat('%]')
    rowElement.cells[7].lastChild.innerText = String(experimentalOverlaps).concat(' [').concat(experimentalOverlapPercentage).concat('%]');
   }

   experimentalAdaptorContaminationPercentage = currentSelectedFragmentSize === 0 ? 0 : String(Math.round((experimentalAdaptorContamination/experimentalSelectedFragmentSize)*100));
   experimentalDataFrameValues = calculateDataFrameValues(sliderOneValue, sliderTwoValue, enzymeData, rowId, experimentalSelectedFragmentSize, experimentalAdaptorContamination, experimentalOverlaps)

   rowElement.cells[2].firstChild.innerText = currentSelectedFragmentSize;
   rowElement.cells[3].firstChild.innerText = theoreticalDataFrameValues.sumAllBasesOfEveryBin;
   rowElement.cells[4].firstChild.innerText = theoreticalDataFrameValues.maxNumberOfPossibleSamples;
   rowElement.cells[5].firstChild.innerText = (theoreticalDataFrameValues.numberBasesToBeSequenced).toLocaleString(undefined, { minimumFractionDigits: 0 });
   rowElement.cells[6].firstChild.innerText = String(adaptorContaminationValues.adaptorContamination).concat(' [').concat(adaptorContaminationValues.adaptorContaminationPercentage).concat('%]');

   rowElement.cells[2].lastChild.innerText = experimentalSelectedFragmentSize;
   rowElement.cells[3].lastChild.innerText = experimentalDataFrameValues.sumAllBasesOfEveryBin;
   rowElement.cells[4].lastChild.innerText = experimentalDataFrameValues.maxNumberOfPossibleSamples;
   rowElement.cells[5].lastChild.innerText = (experimentalDataFrameValues.numberBasesToBeSequenced).toLocaleString(undefined, { minimumFractionDigits: 0 });
   rowElement.cells[6].lastChild.innerText = String(experimentalAdaptorContamination).concat(' [').concat(experimentalAdaptorContaminationPercentage).concat('%]');

   if (typeof expectedNumberOfSnps !== "undefined") {
       if(theoreticalDataFrameValues.sumAllBasesOfEveryBin * parseFloat(expectPolyMorph) < expectedNumberOfSnps) {
            for (let i = 0; i < 8; i++) {
                rowElement.classList.add("excludingSecondCutter")
            }
       } else {
            for (let i = 0; i < 8; i++) {
                  rowElement.classList.remove("excludingSecondCutter")
            }
       }
   }
}

function generateDataFrameTableHead(table) {
  tableCaption = table.createCaption()
  tableCaption.innerHTML = fileName.concat('<br>').concat(pairedEndChoice).concat("<br>Sequencing Yield: ").concat(sequencingYield).concat(" reads - Coverage: ").concat(coverage)
  let thead = table.createTHead();
  let firstHeaderRow = thead.insertRow();
  firstHeaderRow.style='text-align: center; vertical-align: middle;';

  dataFrameValueTitles.forEach( function(title) {
      let th = document.createElement("th");
      th.innerText = title
      firstHeaderRow.appendChild(th);

      if( title === 'Enzyme Pair') {
        th.style='text-align: left;'
      }

      if(title === "No. basepairs sequenced in the lane") {
       icon = createIcon("basepairsSequencedHelp")
       icon.style = 'display: inline-block; margin-top: 0px; margin-left: 4px;'
       th.appendChild(icon);
      }

      if( title === 'Fragments under '.concat(basepairLengthToBeSequenced) ) {
        th.style="color:red; border-color: black;"
        icon = createIcon("adapterContaminationHelp")
        icon.style = 'display: inline-block; margin-top: 0px; margin-left: 4px;'
        th.appendChild(icon);
      }

      if( title === overlapTitle ) {
        th.style="color:red; border-color: black;"
        icon = createIcon("overlapHelp")
        icon.style = 'display: inline-block; margin-top: 0px; margin-left: 4px;'
        th.appendChild(icon);
     }
  })
}

function generateDataframeTableRow(rowElement, enzymeData, tableId){

        rowElement.id=Object.keys(enzymeData)[0];

        //add row title
        tdRowTitle = document.createElement('td');
        tdRowTitle.style = 'width: 9%;'

        titleElement = document.createElement('th');
        titleElement.innerText = Object.keys(enzymeData)[0];
        tdRowTitle.appendChild(titleElement);
        tdRowTitle.id=Object.keys(enzymeData)[0].concat('Title');
        tdRowTitle.scope='row';

        sliderDisplay = document.createElement('small');
        sliderDisplay.className = 'text-muted'
        tdRowTitle.appendChild(sliderDisplay);

        rowElement.appendChild(tdRowTitle);

        //add row value cells
        dataFrameValueTitles.slice(1, -1).forEach( function(title) {

            let connectedTD = document.createElement("td");

            let theoreticalTD = document.createElement("td");
            let predicationTD = document.createElement("td");
            theoreticalTD.className = 'tableCell';
            predicationTD.className = 'tableCell';

            if (title === '') {
                theoreticalTD.innerText = 'Theoretical'
                predicationTD.innerText = 'Prediction'
            }

            connectedTD.appendChild(theoreticalTD);
            connectedTD.appendChild(predicationTD);
            rowElement.appendChild(connectedTD);
        })

        //add slider
        tdSlider = document.createElement('td');
        tdSlider.style='width:20%'
        tdSlider.appendChild(generateSlider(tableId, rowElement.id, enzymeData))
        rowElement.appendChild(tdSlider);

        let sliderTrackDiv = tdSlider.firstChild
        addSliderMarkers(sliderTrackDiv, parseInt(basepairLengthToBeSequenced))
        if(pairedEndChoice === 'paired end') {
           addSliderMarkers(sliderTrackDiv, parseInt(basepairLengthToBeSequenced)*2)
        }
}

function generateDataframeTableRows(table, dataFrameData) {

    let tbody = table.createTBody();

    dataFrameData.forEach( function(enzymeDataString) {
        let enzymeData = JSON.parse(enzymeDataString)
        let row = tbody.insertRow();
        generateDataframeTableRow(row, enzymeData, table.id)
    })
}

function generateDataframeTable(dataFrameElement, tableId, dataFrameData){
    let table = document.createElement("table");
    table.id = tableId
    table.className = "table table-striped"
    dataFrameElement.appendChild(table);
    generateDataFrameTableHead(table);
    generateDataframeTableRows(table, dataFrameData);
}

function generateSlider(tableId, rowId, enzymeData) {

    let sliderTrack = document.createElement("div");
    sliderTrack.className = "form-group slider-track";
    let firstSlider = document.createElement("input");
    let idSliderOne = rowId.concat('SliderOne')
    let secondSlider = document.createElement("input");
    let idSliderTwo = rowId.concat('SliderTwo')
    let resultTable = document.getElementById(tableId)

    if(pairedEndChoice === 'paired end') {
        sliderTrack.style = 'background: linear-gradient(to right, #ff0000 0%, #ffff00 25%, #00ff00 35%, #00ff00 45%, #ffff00 100%);'
    } else {
        sliderTrack.style = 'background: linear-gradient(to right, #ff0000 0%, #ffff00 25%, #00ff00 35%, #00ff00 45%, #ffff00 100%);'
    }

    fillSlider(firstSlider, secondSlider, '30', idSliderOne, slideOne, rowId, enzymeData)
    fillSlider(secondSlider, firstSlider, '100', idSliderTwo, slideTwo, rowId, enzymeData)

    sliderTrack.appendChild(firstSlider);
    sliderTrack.appendChild(secondSlider);

    slideOne(firstSlider, secondSlider, rowId, enzymeData)
    slideTwo(secondSlider, firstSlider, rowId, enzymeData)

    return sliderTrack
}

function fillSlider(selfSlider, otherSlider, startingValue, id, inputFunction, rowId, enzymeData){

    selfSlider.type = "range";
    selfSlider.className = "form-range";
    selfSlider.min = "0";
    selfSlider.max = "100";
    selfSlider.value = startingValue;
    selfSlider.id = id;
    selfSlider.addEventListener('input', function() {inputFunction(selfSlider, otherSlider, rowId, enzymeData)}, true);
    selfSlider.addEventListener('change', function() {inputFunction(selfSlider, otherSlider, rowId, enzymeData)}, true);
}

function addSliderMarkers(sliderTrackDiv, basepairLengthToBeSequenced){

    if(basepairLengthToBeSequenced > 1000){
        return;
    }

    let markerPosition = basepairLengthToBeSequenced/10;

    let line = document.createElement('div');
    line.className = "line";
    line.style = 'left:'.concat(String(markerPosition > 15 ? markerPosition : markerPosition + 1)).concat("%;")

    let lineTick = document.createElement('label');
    lineTick.className = "lineTick";
    let lineTickText = document.createTextNode(String(basepairLengthToBeSequenced).concat(" bp"));
    lineTick.appendChild(lineTickText);

    line.append(lineTick)
    sliderTrackDiv.appendChild(line)
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

function buildUpDataFrame(inputElement, tableId, dataFrameData) {
    generateDataframeTable(inputElement, tableId, dataFrameData)
}

function initDataframe() {

    if(document.body.contains(document.getElementById("dataFrame")) || document.body.contains(document.getElementById("dataFrames"))) {
        dataFrameValueTitles = ['Enzyme Pair', '', 'No. fragments', 'No. basepairs in insilico digested sample', 'No. samples multiplexable', 'No. basepairs sequenced in the lane', 'Fragments under '.concat(basepairLengthToBeSequenced)]
        overlapTitle = "Fragments between ".concat(basepairLengthToBeSequenced).concat(" and ").concat(parseInt(basepairLengthToBeSequenced)*2)
    }


    if(document.body.contains(document.getElementById("dataFrame")))  {

         if(pairedEndChoice === 'paired end') {
            dataFrameValueTitles.push(overlapTitle);
         }

         dataFrameValueTitles.push('Range adjustment');

         dataFrameTableId = "dataFrameTable"

         buildUpDataFrame(document.getElementById("dataFrame"), dataFrameTableId, dataFrameData)

    }
}


window.addEventListener('load', initDataframe)
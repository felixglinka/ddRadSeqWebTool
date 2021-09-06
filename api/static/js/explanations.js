function initExplanations() {
    fillBeginnerExplanation()
}

function fillBeginnerExplanation() {

    if(typeof explantionTexts != 'undefined') {
        let introductionContent = document.getElementById("introductionContent")
        let goalContent = document.getElementById("goalContent")
        let exampleSNPDensity = document.getElementById("exampleSNPDensity")
        let influencingFactors = document.getElementById("influencingFactors")
        let baseCutters = document.getElementById("baseCutters")
        let tableMetricsGraph = document.getElementById("tableMetricsGraph")
        let tableMetricsTable = document.getElementById("tableMetricsTable")

        introductionContent.innerHTML = explantionTexts.introductionContent
        goalContent.innerHTML = explantionTexts.goalContent
        exampleSNPDensity.innerHTML = explantionTexts.exampleSNPDensity
        influencingFactors.innerHTML = explantionTexts.influencingFactors
        baseCutters.innerHTML = explantionTexts.baseCutters
        tableMetricsGraph.innerHTML = explantionTexts.tableMetricsGraph
        tableMetricsTable.innerHTML = explantionTexts.tableMetricsTable
    }
}

window.addEventListener('load', initExplanations)
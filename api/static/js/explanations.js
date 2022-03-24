function initExplanations() {
    fillBeginnerExplanation()
}

function fillBeginnerExplanation() {

    if(typeof explantionTexts != 'undefined') {
        let introductionContent = document.getElementById("introductionContent")
        let goalContent = document.getElementById("goalContent")
        let estimatingSNPIntro = document.getElementById("estimatingSNPIntro")
        let popStructureAnalysis = document.getElementById("popStructureAnalysis")
        let genomeScan = document.getElementById("genomeScan")
        let exampleSNPDensity = document.getElementById("exampleSNPDensity")
        let influencingFactors = document.getElementById("influencingFactors")
        let baseCutters = document.getElementById("baseCutters")
        let gcContentRestrictionSite = document.getElementById("gcContentRestrictionSite")
        let overlapsContaminationContent = document.getElementById("overlapsContaminationContent")
        let tableMetricsGraph = document.getElementById("tableMetricsGraph")
        let tableMetricsTable = document.getElementById("tableMetricsTable")
        let howToCite = document.getElementById("howToCite")

        introductionContent.innerHTML = explantionTexts.introductionContent
        goalContent.innerHTML = explantionTexts.goalContent
        estimatingSNPIntro.innerHTML = explantionTexts.estimatingSNPIntro
        popStructureAnalysis.innerHTML = explantionTexts.popStructureAnalysis
        genomeScan.innerHTML = explantionTexts.genomeScan
        exampleSNPDensity.innerHTML = explantionTexts.exampleSNPDensity
        influencingFactors.innerHTML = explantionTexts.influencingFactors
        baseCutters.innerHTML = explantionTexts.baseCutters
        gcContentRestrictionSite.innerHTML = explantionTexts.gcContentRestrictionSite
        overlapsContaminationContent.innerHTML = explantionTexts.overlapsContaminationContent
        tableMetricsGraph.innerHTML = explantionTexts.tableMetricsGraph
        tableMetricsTable.innerHTML = explantionTexts.tableMetricsTable
        howToCite.innerHTML = explantionTexts.howToCite
    }
}

window.addEventListener('load', initExplanations)
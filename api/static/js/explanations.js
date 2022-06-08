function initExplanations() {
    fillBeginnerExplanation()
}

function fillBeginnerExplanation() {

    if(typeof explantionTexts != 'undefined') {
        let introductionContent = document.getElementById("introductionContent")
        let sequencyEffiencyOfPairedEndSequencing = document.getElementById("sequencyEffiencyOfPairedEndSequencing")
        let goalContent = document.getElementById("goalContent")
        let noIdea = document.getElementById("noIdea")
        let lemmeTryOut = document.getElementById("lemmeTryOut")
        let estimatingSNPIntro = document.getElementById("estimatingSNPIntro")
        let exampleSNPDensity = document.getElementById("exampleSNPDensity")
        let baseCutters = document.getElementById("baseCutters")
        let gcContentRestrictionSite = document.getElementById("gcContentRestrictionSite")
        let overlapsContaminationContent = document.getElementById("overlapsContaminationContent")
        let tableMetricsGraph = document.getElementById("tableMetricsGraph")
        let tableMetricsTable = document.getElementById("tableMetricsTable")
        let howToCite = document.getElementById("howToCite")

        introductionContent.innerHTML = explantionTexts.introductionContent
        sequencyEffiencyOfPairedEndSequencing.innerHTML = explantionTexts.sequencyEffiencyOfPairedEndSequencing
        goalContent.innerHTML = explantionTexts.goalContent
        noIdea.innerHTML = explantionTexts.noIdea
        lemmeTryOut.innerHTML = explantionTexts.lemmeTryOut
        estimatingSNPIntro.innerHTML = explantionTexts.estimatingSNPIntro
        exampleSNPDensity.innerHTML = explantionTexts.exampleSNPDensity
        baseCutters.innerHTML = explantionTexts.baseCutters
        gcContentRestrictionSite.innerHTML = explantionTexts.gcContentRestrictionSite
        overlapsContaminationContent.innerHTML = explantionTexts.overlapsContaminationContent
        tableMetricsGraph.innerHTML = explantionTexts.tableMetricsGraph
        tableMetricsTable.innerHTML = explantionTexts.tableMetricsTable
        howToCite.innerHTML = explantionTexts.howToCite
    }
}

window.addEventListener('load', initExplanations)
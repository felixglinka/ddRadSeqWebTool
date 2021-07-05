function createTip(){
    let restrictionHelpTooltipElement = document.getElementById('restrictionHelp');
    new bootstrap.Popover(restrictionHelpTooltipElement);


}


function initPopovers() {

    let popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
    let popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
      return new bootstrap.Popover(
        popoverTriggerEl,{
        container: popoverTriggerEl,
        html: true,
        trigger: 'hover focus',

        placement: 'right'}
        )
    })

}

window.addEventListener('load', initPopovers)
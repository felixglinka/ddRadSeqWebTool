function initPopovers() {

    let popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
    let popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
      return new bootstrap.Popover(
        popoverTriggerEl,{
        container: popoverTriggerEl,
        html: true,
        trigger: 'hover focus',
        placement: 'right'
        })
    })

    fillPopovers()

}

function fillPopovers() {

    let popoverList = document.getElementsByClassName("questionIcon")
    for (let popover of popoverList) {

        if(popoverContents[popover.id] !== undefined ) {
            popover.setAttribute("data-bs-original-title", popoverContents[popover.id].title);
            popover.setAttribute("data-bs-content", popoverContents[popover.id].content);
        }
    }
}

window.addEventListener('load', initPopovers)
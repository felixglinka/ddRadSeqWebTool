function createIcon(id){
    questionIcon = document.createElement('div');
    questionIcon.id = id;
    questionIcon.className = "questionIcon";
    questionIcon.setAttribute('data-bs-toggle', 'popover');
    questionIcon.title = "Popover title";
    questionIcon.setAttribute('data-bs-content', "And here's some amazing content. It's very engaging. Right?");

    return questionIcon
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
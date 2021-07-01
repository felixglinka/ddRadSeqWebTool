function createTip(ev){
    let title = this.title;
    this.title = 'Crazy tooltip';
    this.setAttribute("tooltip", title);

    let tooltipWrap = document.createElement("div"); //creates div
    tooltipWrap.className = 'tooltip'; //adds class
    tooltipWrap.appendChild(document.createTextNode(title)); //add the text node to the newly created div.

    let firstChild = document.body.firstChild;//gets the first elem after body
    firstChild.parentNode.insertBefore(tooltipWrap, firstChild); //adds tt before elem

    let padding = 5;
    let linkProps = this.getBoundingClientRect();
    let tooltipProps = tooltipWrap.getBoundingClientRect();
    let topPos = linkProps.top - (tooltipProps.height + padding);
    tooltipWrap.setAttribute('style','top:'+topPos+'px;'+'left:'+linkProps.left+'px;')
}

function cancelTip(ev){
    let title = this.getAttribute("tooltip");
    this.title = title;
    this.removeAttribute("tooltip");
}

function initPopovers() {

    let questionIcons = document.getElementsByClassName("questionIcon");

    Array.prototype.forEach.call(questionIcons, function(questionIcon) {
        questionIcon.addEventListener('mouseover',createTip);
        questionIcon.addEventListener('mouseout',cancelTip);
    })

}

window.addEventListener('load', initPopovers)
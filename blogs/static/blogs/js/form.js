function lineCheck(e) {
    var ta = document.getElementById("text_form");
    var row = ta.getAttribute("max-rows");
    var r = (ta.value.split("\n")).length;
    if (document.all) { // for IE
        if (r > row && window.event.keyCode == 13) { //when input key is Enter
            return false; //ignore
        }
    } else {
        if (r > row && e.which == 13) {
            return false;
        }
    }
}

window.document.onkeypress = lineCheck;


/*
Implementing responsive design in textarea
Should not have specified the attribute "cols", but css .text_area did't affect its style.

*/
window.onload = responsiveTextarea;

(function (){
    var timer = 0;

    window.onresize = function(){
        if(timer > 0){
            clearTimeout(timer);
        }
        timer = setTimeout(responsiveTextarea(), 100)
    }

}());


function responsiveTextarea () {
    var ta = document.getElementById("text_form");
    var w = window.innerWidth;
    const lg = 992;
    const md = 768;
    const sm = 576;
    if (w >= lg) {
        ta.setAttribute("cols", 80)
    } else if (w >= md) {
        ta.setAttribute("cols", 60);
    } else if (w >= sm) {
        ta.setAttribute("cols", 50);
    } else {
        ta.setAttribute("cols", 40);
    }
}
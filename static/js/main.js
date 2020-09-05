function openNav(){
    if(document.getElementById("menu").style.width == "180px") {
        // document.getElementById("menu").style.width = null;
        closeNav();
        // Element.style.width = 0;
        // document.getElementById("menu")
    } else {
        document.getElementById("menu").style.width = "180px";
    }
}
/*function to close the sidepanel*/
function closeNav(){
    document.getElementById("menu").style.width = 0;

}

const url = "REPLACE_ME";
var mainContainer  = document.getElementById("myData");
window.onload = function() {
    counter();
    function counter(){
        fetch(url)
        .then(response => response.text())
        .then(resp => {
            mainContainer.innerHTML = resp
        });
    };
}
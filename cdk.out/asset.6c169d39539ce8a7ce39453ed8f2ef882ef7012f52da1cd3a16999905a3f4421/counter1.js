
const url = "https://eybkgj8sa8.execute-api.eu-central-1.amazonaws.com/default/Website-deploy-website-to-s-CounterHandlerA4ADB636-NC2EYKJMRDA8";
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
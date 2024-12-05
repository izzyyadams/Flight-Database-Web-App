document.addEventListener("DOMContentLoaded", function(){
    const sinceTotal = document.getElementById("userSpentJS");
    const sinceButton = document.getElementById("submitJS")

 
    sinceButton.addEventListener("click", function(){
        sinceTotal.style.display="flex";

    });


});
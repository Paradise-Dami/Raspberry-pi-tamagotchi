
async function boire() {
    try {
    await fetch('/boire', {method: 'POST'});
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

async function nourrir() {
    try {
    await fetch('/nourrir', {method: 'POST'});
    } catch (error) {
        console.error('Error fetching data:', error);
}
}


async function fetchData() {
    try {
        const response = await fetch('/get_db');
        const data = await response.json();
        console.log(data);

    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

const progress = document.querySelector(".progress-done");
const input = document.querySelector('.input');
const maxInput = document.querySelector(".maxInput");
let finalValue = 0;
let max = 0;
const idStats = ["sante", "nourriture", "hydratation", "divertissement"];

/* ajuste le pourcentage de barre à mettre*/
function changerWidth() {
    progress.style.width = `${(finalValue / max)*100}%`;
}

/* tests pour changer les datas et faire fonctionner les barres de stat
input.addEventListener("keyup", function() {
    finalValue = parseInt(input.value, 10); // renvoie un integer en base 10

    changeWidth();
});

maxInput.addEventListener("keyup", function(){
    max = parseInt(maxInput.value, 10);
    changeWidth();
}); */

// pas fini
function majStats() {
    // on met à jour les stats continuellement
    let len = idStats.length;
    for (let i = 0; i < len; i++) {
        idStats[i]
    }

}

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


// pas fini
function majStats() {
    // on met à jour les stats continuellement
    let len = idStats.length;
    for (let i = 0; i < len; i++) {
        idStats[i]
    }

}

async function fetchDataStatsTamagotchi() {
    //appel des données du tamagotchi
    try {
        const response = await fetch('get_stats_tamagotchi', {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        // Convertir la réponse JSON en objet JavaScript
        const data = await response.json();

        // Exemple d'utilisation des données
        console.log(data)
        return data

    } catch (error) {
        console.error("Erreur lors de la récupération des données:", error.message);
    }
    
}

async function gameOver() {
    data = await fetchDataStatsTamagotchi()
    try{
        vie = data["sante"]
        if (vie <= 0) {
            window.location.replace("/mort");
        }
        else {
            console.log("en vie")
        }
    } catch (error) {
        console.error("Erreur lors de la récupération des données:", error.message)
    }
}


setInterval(gameOver,5000)

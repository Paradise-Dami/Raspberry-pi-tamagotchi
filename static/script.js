
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


async function reset() {
    try {
    await fetch('/reset', {method: 'POST'});
    window.location.replace("/");
    console.log("prout")
    } catch (error) {
        console.error('Error fetching data:', error);
}
}


const idStats = {"sante":"progress-done1", "nourri":"progress-done2", "desaltere":"progress-done3", "ennui":"progress-done4"};
const input = document.querySelector('.input');
const maxInput = document.querySelector(".maxInput");


/* ajuste le pourcentage de barre à mettre*/
function changerWidth(progress,finalValue) {
    console.log(progress,finalValue)
    progress.style.width = `${(finalValue)}%`;
}


async function majStats() {
    // on met à jour les stats continuellement
    data = await fetchDataStatsTamagotchi()
    Object.keys(idStats).forEach(function(key) {
        var progress = document.getElementById(idStats[key]);
        let finalValue = data[key];
        changerWidth(progress,finalValue);
    }
)}

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
        sante = data["sante"]
        if (sante == 0) {
            window.location.replace("/mort");
        }
        else {
            console.log("en vie")
        }
    } catch (error) {
        console.error("Erreur lors de la récupération des données:", error.message)
    }
}


async function maj() {
    data = await fetchDataStatsTamagotchi()
    statut = await fetchStatut()
    try {
    await fetch('/maj', {method: 'POST'});
        // on met à jour les stats continuellement
    let etat = "";
    let len = statut.length;
    for (let i = 0; i < len; i++) {
        if (len == 1) {
            etat = statut[i] 
        }
        else {
            etat = etat + " | "+statut[i] 
        }
            
    }
    etat = etat +" | "
    document.getElementById("statut").textContent= etat;
    document.getElementById("nom").textContent=data["nom"];
    console.log("maj")
    } catch (error) {
        console.error('Error fetching data:', error);
}
}


async function fetchStatut() {
    //appel des données du tamagotchi
    try {
        const response = await fetch('get_statut', {
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


setInterval(majStats,10000)
setInterval(gameOver,5000)
setInterval(maj,5000)

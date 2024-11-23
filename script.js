let counter = 0;

const bouton = document.getElementById("button");


function reaction() {
    if (counter > 5) {
        document.getElementById("face").src = "C:/Users/Imad/Documents/Site internet/Tamagotchi/Assets/image2.png"
    } else {
        document.getElementById("face").src = "C:/Users/Imad/Documents/Site internet/Tamagotchi/Assets/image.png"

    }
}

function nourrir(nombre) {
    counter = counter + nombre ;
    console.log(counter)
    document.getElementById("compteur").innerHTML = counter;
    reaction();
}
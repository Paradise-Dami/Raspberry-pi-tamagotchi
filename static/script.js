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

$(document).ready(function() {
    $("#runScriptBtn").click(function(e) {
        e.preventDefault();
        $.ajax({
            url: '/run_script',
            method: 'POST',
            data: JSON.stringify({ script_path: '../Raspberry-pi-tamagotchi/hosting.py' }),
            contentType: "application/json",
            success: function(response) {
                alert('Script execution started!');
                console.log(response);
            },
            error: function(xhr, status, error) {
                alert('Error executing script: ' + error);
                console.error(error);
            }
        });
    });
});
import RPi.GPIO as GPIO
import time
from grove.grove_button import GroveButton
from grove.adc import ADC

def sortie_buzz(pin, quantite, delai, freq=100, dc=1)-> None:
    """Hyp: branchement du capteur sur un pin de type D
        Fait sonner le buzzer [quantite] fois avec une pause de [delai] secondes entre chaque buzz.
    """
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    buzz = GPIO.PWM(pin, freq)
    buzz.start(0)
    try:
        for i in range(quantite):
            buzz.ChangeDutyCycle(dc) #bruit
            time.sleep(delai/2)
            buzz.ChangeDutyCycle(0) #silence
            time.sleep(delai/2)
    finally:
        buzz.stop()
#sortie_buzz(5, 3, 0.5, 500, 1)


class entree_bouton:
    """Hyp: branchement du capteur sur un pin de type D
        Appel des fonctions ci-dessous lorsque le boutton est appuyé/relaché
    """
    def __init__(self, pin):
        self.bouton = GroveButton(pin)
        
        def sur_appui(t)-> None: #Lance un chronomètre lorsque le boutton est pressé
            global temps_debut
            temps_debut = time.time()
        def sur_relache(t)-> None: #Lorsque le boutton est relaché, sauvegarde la durée d'appui du boutton dans une variable globale
            global temps_fin
            temps_fin = time.time()-temps_debut #duration d'appui du boutton
            print("Bouton tenu pendant",temps_fin,"secondes!")
            
        self.bouton.on_press = sur_appui
        self.bouton.on_release = sur_relache
#bouton = entree_bouton(16)


class entree_angle(ADC):
    """Hyp: branchement du capteur sur un pin de type A (et non D !)
        Connecte le capteur afin de pouvoir extraire sa rotation
    """
    def __init__(self, pin):
        self.pin = pin
        self.adc = ADC()
    
    @property
    def valeur(self)-> int:
        """Renvoit l'angle de rotation du potentiomètre (mini: 0 /maxi: 999)"""
        return self.adc.read(self.pin)
    """angle = entree_angle(0)
    while True:
        print(angle.valeur)
        time.sleep(0.1)"""


# ------------------------------ Fonctions pratiques ------------------------------

def temperature(pin)-> str:
    """Hyp: Branchez le potentiomètre sur un pin de type A
    Retourne le statut de la température en fonction de la valeur du potentiomètre,
    la température varie de -10 à 40 degrés Celsius.
    """
    angle = entree_angle(pin)
    temp = angle.valeur/20 - 10

    dico_temp = {"a froid": temp <= 10, "": 10 < temp < 30, "a chaud": 30 <= temp}
    for cle in dico_temp:
        if dico_temp[cle]:
            return cle, temp

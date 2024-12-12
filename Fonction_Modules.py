import RPi.GPIO as GPIO
import time
import math
import sys
from grove.adc import ADC

def buzz(pin, amount=1, delay=1) -> None:
    """Fait sonner le buzzer [amount] fois avec une pause de [delay] secondes entre chaque buzz."""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    buzz = GPIO.PWM(pin, 100)
    buzz.start(0)
    try:
        for i in range(amount):
            buzz.ChangeDutyCycle(1) #bruit
            time.sleep(delay/2)
            buzz.ChangeDutyCycle(0) #silence
            time.sleep(delay/2)
    finally:
        buzz.stop()
        GPIO.cleanup()

#buzz(5, 3, 0.5)


class button_input:
    """Appelle les deux fonctions ci-dessous lorsque le boutton est appuyé/relaché"""
    def __init__(self, pin):
        from grove.grove_button import GroveButton
        self.button = GroveButton(pin)
        
        def on_press(t):
            """Lance un chronomètre lorsque le boutton est pressé"""
            global start_time
            start_time = time.time()
        def on_release(t):
            """Lorsque le boutton est relaché, sauvegarde la durée d'appui du boutton dans une variable globale"""
            global end_time
            end_time = time.time()-start_time #duration d'appui du boutton
        
        self.button.on_press = on_press
        self.button.on_release = on_release

#button1 = button_input(16)


"""class GroveRotaryAngleSensor(ADC):
    def __init__(self, channel):
        self.channel = channel
        self.adc = ADC()
    
    @property
    def value(self):
        Renvoit langle de rotation du potentiomètre
        return self.adc.read(self.channel)

def angle_sensor():
    if len(sys.argv) < 2:
        print('Usage: {} adc_channel'.format(sys.argv[0]))
        sys.exit(1)

    sensor = GroveRotaryAngleSensor(int(sys.argv[1]))

    while True:
        print('Rotary Value: {}'.format(sensor.value))
        time.sleep(.2)

angle_sensor()"""

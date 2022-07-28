import speech_recognition as sr
import RPi.GPIO as GPIO
import time

listener = sr.Recognizer()
mic = sr.Microphone()

''' Configuracion del motor '''
GPIO.setmode(GPIO.BOARD)
control_pins = [7,11,13,15]
for pin in control_pins:
  GPIO.setup(pin, GPIO.OUT)
  GPIO.output(pin, 0)

halfstep_seq = [
  [1,0,0,0],
  [1,1,0,0],
  [0,1,0,0],
  [0,1,1,0],
  [0,0,1,0],
  [0,0,1,1],
  [0,0,0,1],
  [1,0,0,1]
]

counter_clk = [
  [1,0,0,1],
  [0,0,0,1],
  [0,0,1,1],
  [0,0,1,0],
  [0,1,1,0],
  [0,1,0,0],
  [1,1,0,0],
  [1,0,0,0]
]

print("Comienza a hablar prro")

''' Configuracion reconocimiento de voz '''
def escuchar():
    instruccion = ""
    try:
        with mic as source:
            audio = listener.listen(source)
            listener.adjust_for_ambient_noise(source, duration=0.2)
            instruccion = listener.recognize_google(audio, None, "es-Mx", False).lower()
    except sr.UnknownValueError():
        pass
    return instruccion

def activarOrtesis(delay, pasos):
    #Clk wise
    for i in range(pasos):
      for halfstep in range(8):
        for pin in range(4):
          GPIO.output(control_pins[pin], halfstep_seq[halfstep][pin])
        time.sleep(delay)
    
    # 3 seconds delay
    time.sleep(3)
    
    #Counter clkWise
    for i in range(pasos):
      for halfstep in range(8):
        for pin in range(4):
          GPIO.output(control_pins[pin], counter_clk[halfstep][pin])
        time.sleep(delay)
    
    GPIO.cleanup()

comando = escuchar()
if ("max" in comando):
    comando = comando.replace("max ", "")
    if (comando == "ortesis activa velocidad 1"):
        print("Seleccionaste -> ortesis activa velocidad 1")
        activarOrtesis(0.01, 1600)
    elif (comando == "ortesis activa velocidad 2"):
        print("Seleccionaste -> ortesis activa velocidad 2")
        activarOrtesis(0.005, 1600)
    elif (comando == "ortesis activa velocidad 3"):
        print("Seleccionaste -> ortesis activa velocidad 3")
        activarOrtesis(0.001, 1600) 

    


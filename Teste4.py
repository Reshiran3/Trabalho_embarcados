import RPi.GPIO as GPIO
import time
from flask import Flask, jsonify

# Configuração do sensor HC-SR04
TRIG = 14  # Pino de Trigger
ECHO = 15  # Pino de Echo

# Inicializando a biblioteca GPIO
GPIO.setmode(GPIO.BCM)  # Usando a numeração BCM dos pinos
GPIO.setup(TRIG, GPIO.OUT)  # Configura o pino de Trigger como saída
GPIO.setup(ECHO, GPIO.IN)   # Configura o pino de Echo como entrada

# Variável global para armazenar a distância
distancia_global = 0

# Inicializar o servidor Flask
app = Flask(__name__)

@app.route('/')
def mostrar_distancia():
    """Rota principal para exibir a distância."""
    if distancia_global < 15.0:
        mensagem = "A distância é menor que 15 cm!"
    else:
        mensagem = "A distância é maior que 15 cm."
    return jsonify({"distancia": distancia_global, "mensagem": mensagem})

# Função para medir a distância
def medirDist(echo, trig):
    # Aciona o trigger
    GPIO.output(trig, GPIO.LOW)
    time.sleep(0.000002)
    GPIO.output(trig, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(trig, GPIO.LOW)

    # Aguardar a resposta do echo
    while GPIO.input(echo) == GPIO.LOW:
        pass
    inicio = time.time()

    while GPIO.input(echo) == GPIO.HIGH:
        pass
    fim = time.time()

    # Calculando a distância
    duracao = fim - inicio
    resultado = duracao * 34300 / 2  # A velocidade do som é 34300 cm/s

    return round(resultado, 1)

# Loop para medir a distância continuamente
def medir_distancia_continuamente():
    global distancia_global
    while True:
        distancia_global = medirDist(ECHO, TRIG)
        print(f"Distância: {distancia_global} cm", end='\r')
        time.sleep(1)  # Atraso para evitar leituras muito rápidas

# Inicia o loop de medição em um thread separado
if __name__ != "__main__":
    import threading
    threading.Thread(target=medir_distancia_continuamente, daemon=True).start()

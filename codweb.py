from flask import Flask, render_template, jsonify
import RPi.GPIO as GPIO
import time

# Configuração do sensor HC-SR04
TRIG = 14  # Pino de Trigger
ECHO = 15  # Pino de Echo

# Configuração dos pinos GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Inicializando o Flask
app = Flask(__name__)

def medir_distancia():
    """Função para medir a distância usando o sensor HC-SR04."""
    GPIO.output(TRIG, GPIO.LOW)
    time.sleep(0.2)  # Pequeno atraso para estabilização

    # Envia o sinal de Trigger
    GPIO.output(TRIG, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG, GPIO.LOW)

    # Calcula o tempo de ida e volta do sinal
    while GPIO.input(ECHO) == GPIO.LOW:
        inicio = time.time()

    while GPIO.input(ECHO) == GPIO.HIGH:
        fim = time.time()

    duracao = fim - inicio

    # Calcula a distância em centímetros
    distancia = (duracao * 34300) / 2
    return round(distancia, 2)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/distancia")
def distancia():
    try:
        distancia = medir_distancia()
        return jsonify({"distancia_cm": distancia})
    except Exception as e:
        return jsonify({"erro": str(e)})

if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=5000)
    finally:
        GPIO.cleanup()  # Garante que os pinos GPIO sejam liberados ao encerrar

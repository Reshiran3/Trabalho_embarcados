import RPi.GPIO as GPIO
import time
import socket

# Configuração do sensor HC-SR04
TRIG = 14  # Pino de Trigger
ECHO = 15  # Pino de Echo

# Configuração do sinal de comunicação TCP/IP
HOST = '192.168.1.100'  # Endereço IP do servidor
PORT = 5000              # Porta de comunicação TCP/IP

# Inicializando a biblioteca GPIO
GPIO.setmode(GPIO.BCM)  # Usando a numeração BCM dos pinos
GPIO.setup(TRIG, GPIO.OUT)  # Configura o pino de Trigger como saída
GPIO.setup(ECHO, GPIO.IN)   # Configura o pino de Echo como entrada

# Função para medir a distância
def medirDist(echo, trig):
    nova_leitura = False
    contador = 0
    resultado = 0
    duracao = 0

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

# Função para enviar sinal via TCP/IP
def enviar_tcpip(distancia):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(str(distancia).encode())  # Envia a distância como string
    except Exception as e:
        print(f"Erro ao enviar via TCP/IP: {e}")

# Iniciando a flag sinal
sinal = False

# Loop principal
while True:
    distancia = medirDist(ECHO, TRIG)
    print(f"Distância: {distancia} cm", end='\r')

    if distancia < 15.0:
        if not sinal:  # Alterar sinal apenas quando mudar
            sinal = True
            enviar_tcpip(distancia)
        # Se a distância for menor que 15, acende o LedVm (simulado)
        print("Sinal: ATENÇÃO! Distância < 15cm")
    else:
        if sinal:  # Alterar sinal apenas quando mudar
            sinal = False
        # Se a distância for maior que 15, acende o LedVd (simulado)
        print("Distância maior que 15cm")

    time.sleep(1)  # Atraso para evitar leituras muito rápidas


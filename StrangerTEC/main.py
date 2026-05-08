import network
import socket
import time
from machine import Pin

# ── Pines ──────────────────────────────────────
data_pin = Pin(27, Pin.OUT)
clock    = Pin(26, Pin.OUT)

fila1 = Pin(13, Pin.OUT)
fila2 = Pin(14, Pin.OUT)
fila3 = Pin(15, Pin.OUT)

boton = Pin(16, Pin.IN, Pin.PULL_UP)

# ── WiFi ───────────────────────────────────────
SSID     = "LIB-9997367"
PASSWORD = "v4pbwpxuUjpa"

# ── Diccionario letra → (fila, columna) ────────
LETRAS = {
    'A': (1, 1),  'B': (2, 1),
    'C': (1, 2),  'D': (2, 2),
    'E': (1, 3),  'F': (2, 3),
    'G': (1, 4),  'H': (2, 4),
    'I': (1, 5),  'J': (2, 5),
    'K': (1, 6),  'L': (2, 6),
    'M': (1, 7),  'N': (2, 7),
    'O': (1, 8),  'P': (2, 8),
    'Q': (1, 9),  'R': (2, 9),
    'S': (1, 10), 'T': (2, 10),
    'U': (1, 11), 'V': (2, 11),
    'W': (1, 12), 'X': (2, 12),
    'Y': (1, 13), 'Z': (2, 13),
    '0': (3, 1),  '1': (3, 2),
    '2': (3, 3),  '3': (3, 4),
    '4': (3, 5),  '5': (3, 6),
    '6': (3, 7),  '7': (3, 8),
    '8': (3, 9),  '9': (3, 10),
    '-': (3, 11), '+': (3, 12),
}

# ── Registro de corrimiento ────────────────────
def apagar_filas():
    fila1.value(0)
    fila2.value(0)
    fila3.value(0)

COLUMNAS = {
    1: 0,
    2: 1,
    3: 2,
    4: 3,
    5: 4,
    6: 5,
    7: 6,
    8: 7,

    9: 8,
    10: 9,
    11: 10,
    12: 11,
    13: 12
}

def send_columna(col):
    bits = 0

    if col in COLUMNAS:
        bits = 1 << COLUMNAS[col]

    for i in range(15, -1, -1):
        data_pin.value((bits >> i) & 1)

        clock.value(1)
        time.sleep_us(5)

        clock.value(0)
        time.sleep_us(5)

def apagar_todo():
    apagar_filas()
    for i in range(16):
        data_pin.value(0)
        clock.value(1)
        time.sleep_us(5)
        clock.value(0)
        time.sleep_us(5)

def encender_letra(letra):
    letra = letra.upper()
    if letra not in LETRAS:
        apagar_todo()
        return
    fila, col = LETRAS[letra]
    
    apagar_todo()
    time.sleep_ms(2)
    
    send_columna(col)
    time.sleep_ms(2)
    
    if fila == 1:
        fila1.value(1)
    elif fila == 2:
        fila2.value(1)
    elif fila == 3:
        fila3.value(1)

def transmitir_palabra_facil(frase, pausa=3000):
    for letra in frase:
        if letra == ' ':
            apagar_todo()
            time.sleep_ms(2000)
            continue
        encender_letra(letra)
        time.sleep_ms(pausa)
    apagar_todo()
    
def transmitir_palabra_medio(frase, pausa=2000):
    for letra in frase:
        if letra == ' ':
            apagar_todo()
            time.sleep_ms(2000)
            continue
        encender_letra(letra)
        time.sleep_ms(pausa)
    apagar_todo()
    
def transmitir_palabra_dificil(frase, pausa=1000):
    for letra in frase:
        if letra == ' ':
            apagar_todo()
            time.sleep_ms(2000)
            continue
        encender_letra(letra)
        time.sleep_ms(pausa)
    apagar_todo()

      
# ── WiFi ───────────────────────────────────────
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    print("Conectando...", end="")
    start = time.time()
    while not wlan.isconnected():
        if time.time() - start > 20:
            print("\nTimeout!")
            return None
        print(".", end="")
        time.sleep(0.5)
    ip = wlan.ifconfig()[0]
    print("\nConectado! IP:", ip)
    return ip

# ── Servidor TCP ───────────────────────────────
def start_server(ip):
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((ip, 1717))
    s.listen(1)
    print("Esperando conexión en {}:1717".format(ip))
    try:
        conn, addr = s.accept()
        print("Conectado desde:", addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            msg = data.decode().strip().upper()
            print("Recibido:", msg)
            
            partes = msg.split(",")

            dificultad = partes[0]
            palabra = partes[1]
            
            conn.send("Transmitiendo: {}".format(msg).encode())
            
            if dificultad == "FACIL":
                transmitir_palabra_facil(palabra)
            elif dificultad == "MEDIA":
                transmitir_palabra_medio(palabra)
            elif dificultad == "DIFICIL":
                transmitir_palabra_dificil(palabra)
                    
            conn.send("OK".encode())
    except KeyboardInterrupt:
        print("Detenido")
    except Exception as e:
        print("Error:", e)
    finally:
        apagar_todo()
        conn.close()
        s.close()

# ── Main ───────────────────────────────────────
ip = connect_wifi()
if ip:
    start_server(ip)
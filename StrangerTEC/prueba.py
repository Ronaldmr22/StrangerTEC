import socket
import threading
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import random
from PIL import Image, ImageTk
from os import path
import time
 
SERVER_IP = "192.168.0.77"
PORT = 1717
 
palabra = ""
palabra_jugador = ""
palabra_jugador2 = ""
puntaje_jugador1 = 0
puntaje_jugador2 = 0
nombre_jugador = ""
nombre_jugador2 = ""
 
Palabras = ["HOLA", "COMPUTADORA", "LED", "MONITOR", "TECLADO", "PROCESADOR", "SISTEMA", "MESSI", "MINECRAFT", "JUEGO"]
#Palabras = ["MECAGOENCHAVEZ"]
# ── Ventana principal ──────────────────────────────────────────────────────────
ventana_prin = Tk()
ventana_prin.title("STRANGER THINGS")
ventana_prin.state("zoomed")
ventana_prin.resizable(width=NO, height=NO)
 
ancho = ventana_prin.winfo_screenwidth()
alto  = ventana_prin.winfo_screenheight()
 
C_principal = Canvas(ventana_prin, highlightthickness=0, width=ancho, height=alto, bg='black')
C_principal.place(x=0, y=0)
 
imagen_carga     = Image.open("imagenes/fondo1.png").resize((ancho, alto))
imagenprin_fondo = ImageTk.PhotoImage(imagen_carga)
C_principal.create_image(0, 0, image=imagenprin_fondo, anchor="nw")
 
def cargar_imagen(nombre, anch, alt):
    ruta = path.join('imagenes/', nombre)
    img  = Image.open(ruta).resize((anch, alt))
    return ImageTk.PhotoImage(img)
 
 
# ── Estilo de botones compartido ───────────────────────────────────────────────
estilo_btn = dict(
    font=("Stranger Things", 12, "bold"),
    bg="#2d0e5e", fg="#b89ff8",
    activebackground="#4a2080",
    activeforeground="#ffffff",
    relief="flat", padx=30, pady=6,
    cursor="hand2"
)
 
 
# ── Función que abre la ventana de juego individual ───────────────────────────
def ventana_solo():
    global palabra_jugador
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
    ven_solo = Toplevel()
    ven_solo.title("Juego Solo")
    ven_solo.state("zoomed")
    ven_solo.resizable(width=NO, height=NO)
 
    C_solo = Canvas(ven_solo, highlightthickness=0, width=ancho, height=alto, bg='black')
    C_solo.place(x=0, y=0)
 
    imagen_carga_solo = Image.open("imagenes/fondo1v1.png").resize((ancho, alto))
    imagen_fondo_solo = ImageTk.PhotoImage(imagen_carga_solo)
    C_solo.create_image(0, 0, image=imagen_fondo_solo, anchor="nw")
    C_solo.imagen = imagen_fondo_solo
 
    # --- Widgets ---
    nombre_jugador_entry = Entry(ven_solo, width=30,
        font=("Stranger Things", 15),
        bg="#4C326B", fg="#b89ff8",
        insertbackground="#b89ff8",
        relief="flat", bd=2)
    nombre_jugador_entry.pack(pady=6)
 
    palabra_jgdr = Entry(ven_solo, width=30,
        font=("Stranger Things", 13),
        bg="#1a0a2e", fg="#e8d5ff",
        insertbackground="#e8d5ff",
        relief="flat", bd=2)
    palabra_jgdr.pack(pady=6)
 
    status_label = Label(ven_solo, text="Desconectado",
        font=("Stranger Things", 10),
        bg="#1a0a2e", fg="#b89ff8")
    status_label.pack(pady=2)
 
    # --- Funciones internas ---
    def receive_messages():
        while True:
            try:
                msg = client_socket.recv(1024).decode()
                if not msg:
                    break
            except:
                break
 
    def send_message_facil():
        global palabra
        palabra = random.choice(Palabras)
        msg = f"FACIL,{palabra}"
        if msg:
            client_socket.send(msg.encode())
 
    def send_message_medio():
        global palabra
        palabra = random.choice(Palabras)
        msg = f"MEDIA,{palabra}"
        if msg:
            client_socket.send(msg.encode())
 
    def send_message_dificil():
        global palabra
        palabra = random.choice(Palabras)
        msg = f"DIFICIL,{palabra}"
        if msg:
            client_socket.send(msg.encode())
 
    def connect():
        try:
            client_socket.connect((SERVER_IP, PORT))
            threading.Thread(target=receive_messages, daemon=True).start()
            status_label.config(text="Conectado al servidor")
        except Exception as e:
            status_label.config(text=f"Error: {e}")
 
    def salir():
        try:
            client_socket.close()
        except:
            pass
        ven_solo.destroy()
 
    def deshabilitar_facil():
        btn_f.config(state='disabled')
 
    def deshabilitar_medio():
        btn_m.config(state='disabled')
 
    def deshabilitar_dificil():
        btn_d.config(state='disabled')
 
    def habilitar():
        global puntaje_jugador1
        btn_f.config(state='normal')
        btn_m.config(state='normal')
        btn_d.config(state='normal')
        palabra_jgdr.config(state='normal')
        btn_enviar.config(state='normal')
        puntaje_jugador1 = 0
        puntaje_txt.config(text="0")
        nombre_jugador_entry.delete(0, END)
 
    def puntajes_ranking():
        if (btn_d.cget('state') == 'disabled' and
            btn_m.cget('state') == 'disabled' and
            btn_f.cget('state') == 'disabled'):
            palabra_jgdr.config(state='disabled')
            btn_enviar.config(state='disabled')
            rankines(habilitar)
 
    # --- Botones ---
    btn_f = Button(ven_solo, text="FÁCIL",
        **estilo_btn,
        command=lambda: [send_message_facil(), deshabilitar_facil()])
    btn_f.pack(pady=4)
 
    btn_m = Button(ven_solo, text="MEDIA",
        **estilo_btn,
        command=lambda: [send_message_medio(), deshabilitar_medio()])
    btn_m.pack(pady=4)
 
    btn_d = Button(ven_solo, text="DIFÍCIL",
        **estilo_btn,
        command=lambda: [send_message_dificil(), deshabilitar_dificil()])
    btn_d.pack(pady=4)
 
    Button(ven_solo, text="SALIR", **estilo_btn, command=salir).pack(pady=4)
 
    btn_enviar = Button(ven_solo, text="ENVIAR",
        **estilo_btn,
        command=lambda: [puntaje(palabra, palabra_jgdr.get()), puntajes_ranking()])
    btn_enviar.pack(pady=4)
 
    connect()
 
    puntaje_txt = Label(ven_solo, text="0",
        font=("Stranger Things", 20, "bold"),
        bg="#1a0a2e", fg="#e8d5ff")
    puntaje_txt.pack(pady=4)
 
    def puntaje_aux(lista1, lista2):
        if lista1 == []:
            return 0
        if lista2 == []:
            return 0
        elemento1 = lista1[0]
        elemento2 = lista2[0]
        if elemento1 == elemento2:
            return 1 + puntaje_aux(lista1[1:], lista2[1:])
        else:
            return puntaje_aux(lista1[1:], lista2[1:])
 
    def puntaje(palabra1, palabra2):
        global puntaje_jugador1, nombre_jugador
        nombre_jugador = nombre_jugador_entry.get()
        puntaje_jugador1 += puntaje_aux(list(palabra1), list(palabra2))
        puntaje_txt.config(text=puntaje_jugador1)
        palabra_jgdr.delete(0, END)
 
 
def rankines(habilitar):
    global nombre_jugador
    ven_ultima = Toplevel()
    ven_ultima.state("zoomed")
 
    C_final = Canvas(ven_ultima, highlightthickness=0, width=ancho, height=alto)
    C_final.place(x=0, y=0)
    imagen_victoria_carga = Image.open("imagenes/fondo_final.png").resize((ancho, alto))
    imagenvictoria_fondo  = ImageTk.PhotoImage(imagen_victoria_carga)
    C_final.create_image(0, 0, image=imagenvictoria_fondo, anchor="nw")
    C_final.imagenfondo = imagenvictoria_fondo
 
    with open("rank_stranger.txt", "a", encoding="utf-8") as rank:
        rank.write(f"{puntaje_jugador1},{nombre_jugador}\n")
 
    with open("rank_stranger.txt", "r", encoding="utf-8") as archivo:
        texto_ranking = archivo.readlines()
        matriz = []
        for linea in texto_ranking:
            elementos = linea.strip().split(",")
            if len(elementos) == 2:
                elementos[0] = int(elementos[0])
                matriz.append(elementos)
        matriz.sort(reverse=True)
 
    estilo = ttk.Style()
    estilo.theme_use("clam")
    estilo.configure("Treeview",
        background="#1a0a2e", foreground="#e8d5ff",
        fieldbackground="#1a0a2e", rowheight=30,
        font=("Stranger Things", 11)
    )
    estilo.configure("Treeview.Heading",
        background="#2d0e5e", foreground="#b89ff8",
        font=("Stranger Things", 11, "bold"), relief="flat"
    )
    estilo.map("Treeview",
        background=[("selected", "#4a2080")],
        foreground=[("selected", "#ffffff")]
    )
 
    Label(ven_ultima, text="RANKING",
        font=("Stranger Things", 28, "bold"),
        bg="#1a0a2e", fg="#b89ff8").place(x=500, y=240)
 
    tree_ranking = ttk.Treeview(ven_ultima, columns=("nombre", "puntaje"), show="headings", height=10)
    tree_ranking.column("nombre", width=200, anchor="center")
    tree_ranking.column("puntaje", width=150, anchor="center")
    tree_ranking.heading("nombre", text="Nombre")
    tree_ranking.heading("puntaje", text="Puntos")
    tree_ranking.place(x=500, y=300)
 
    for elemento in matriz[:10]:
        tree_ranking.insert("", "end", values=(elemento[1], elemento[0]))
 
    imagen_ranking = cargar_imagen("ranking.png", 400, 300)
    C_final.create_image(1000, 130, image=imagen_ranking)
    C_final.imagenranking = imagen_ranking
 
    def cerrar():
        habilitar()
        ven_ultima.destroy()
 
    Button(ven_ultima, text="SALIR",
        font=("Stranger Things", 12, "bold"),
        bg="#2d0e5e", fg="#b89ff8",
        activebackground="#4a2080", activeforeground="#ffffff",
        relief="flat", padx=20, pady=8,
        command=cerrar).place(x=570, y=580)
    
    
 
 
# ── Botones de la ventana principal ───────────────────────────────────────────
btn_juego_normal = Button(C_principal, text="JUGAR SOLO",
    **estilo_btn, command=ventana_solo)
btn_juego_normal.place(x=ancho//2 - 100, y=alto//2)


def versus():
    global puntaje_jugador1
    global puntaje_jugador2
    puntaje_jugador1 = 0
    puntaje_jugador2 = 0
    ven_versus = Toplevel()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    turno = 1
    ronda = 1
    rondas_maximas = 2
    palabra_actual = ""
    respuesta_j1 = ""
    respuesta_j2 = ""
    ven_versus.title("Juego versus")
    ven_versus.state("zoomed")
    ven_versus.resizable(width=NO, height=NO)

    C_versus = Canvas(ven_versus,highlightthickness=0,width=ancho,height=alto,bg='black')
    C_versus.place(x=0, y=0)

    imagen_carga_versus = Image.open("imagenes/fondovs.png").resize((ancho, alto))
    imagen_fondo_versus = ImageTk.PhotoImage(imagen_carga_versus)

    C_versus.create_image(0,0,image=imagen_fondo_versus,anchor="nw")
    C_versus.imagen = imagen_fondo_versus

    nombre_jugador_entry = Entry(ven_versus,width=30,font=("Stranger Things", 13),bg="#1a0a2e",fg="#b89ff8",insertbackground="#b89ff8",relief="flat",bd=2)
    nombre_jugador_entry.pack(padx=1)

    puntaje_txt1 = Label(ven_versus,text="0",font=("Stranger Things", 20, "bold"),bg="#1a0a2e",fg="#e8d5ff")
    puntaje_txt1.pack(pady=4)

    nombre_jugador2_entry = Entry(ven_versus,width=30,font=("Stranger Things", 13),bg="#1a0a2e",fg="#b89ff8",insertbackground="#b89ff8",relief="flat",bd=2)
    nombre_jugador2_entry.pack(pady=6)

    puntaje_txt2 = Label(ven_versus,text="0",font=("Stranger Things", 20, "bold"),bg="#1a0a2e",fg="#e8d5ff")
    puntaje_txt2.pack(pady=4)

    status_label = Label(ven_versus,text="Desconectado",font=("Stranger Things", 10),bg="#1a0a2e",fg="#b89ff8")
    status_label.pack(pady=2)

    ronda_label = Label(ven_versus,text="RONDA 1",font=("Stranger Things", 15),bg="#1a0a2e",fg="white")
    ronda_label.pack(pady=5)

    turno_label = Label(ven_versus,text="Turno Jugador 1",font=("Stranger Things", 15),bg="#1a0a2e",fg="cyan")
    turno_label.pack(pady=5)


    def receive_messages():
        nonlocal respuesta_j1
        nonlocal turno

        while True:

            try:

                msg_boton = client_socket.recv(1024).decode()

                if not msg_boton:
                    break

                respuesta_j1 = msg_boton.strip().upper()

                print("Jugador 1:", respuesta_j1)

                calcular_puntos_j1()

                turno = 2

                turno_label.config(text="Turno Jugador 2")

            except:
                break

    def connect():

        try:
            client_socket.connect((SERVER_IP, PORT))
            threading.Thread(target=receive_messages,daemon=True).start()

            status_label.config(
                text="Conectado al servidor"
            )

        except Exception as e:

            status_label.config(
                text=f"Error: {e}"
            )

    # ─────────────────────────────────────
    # RONDAS
    # ─────────────────────────────────────

    def iniciar_ronda():
        nonlocal palabra_actual
        palabra_actual = random.choice(Palabras)
        print("Palabra:", palabra_actual)
        client_socket.send(f"VS,{palabra_actual}".encode())

    def siguiente_ronda():

        nonlocal ronda
        nonlocal turno

        ronda += 1

        if ronda > rondas_maximas:

            mostrar_ganador()
            return

        turno = 1

        ronda_label.config(
            text=f"RONDA {ronda}"
        )

        turno_label.config(
            text="Turno Jugador 1"
        )

        iniciar_ronda()

    # ─────────────────────────────────────
    # PUNTAJES
    # ─────────────────────────────────────

    def puntaje_aux(lista1, lista2):

        if lista1 == []:
            return 0

        if lista2 == []:
            return 0

        elemento1 = lista1[0]
        elemento2 = lista2[0]

        if elemento1 == elemento2:

            return 1 + puntaje_aux(
                lista1[1:],
                lista2[1:]
            )

        else:

            return puntaje_aux(
                lista1[1:],
                lista2[1:]
            )

    def calcular_puntos_j1():

        global puntaje_jugador1

        puntos = puntaje_aux(
            list(palabra_actual),
            list(respuesta_j1)
        )

        puntaje_jugador1 += puntos

        ven_versus.after(0, lambda: puntaje_txt1.config(text=str(puntaje_jugador1)))

    def calcular_puntos_j2():

        global puntaje_jugador2

        puntos = puntaje_aux(
            list(palabra_actual),
            list(respuesta_j2)
        )

        puntaje_jugador2 += puntos

        ven_versus.after(0,lambda: puntaje_txt2.config(text=str(puntaje_jugador2)))

    # ─────────────────────────────────────
    # GANADOR
    # ─────────────────────────────────────

    def mostrar_ganador():

        if puntaje_jugador1 > puntaje_jugador2:

            ganador = nombre_jugador_entry.get()

        elif puntaje_jugador2 > puntaje_jugador1:

            ganador = nombre_jugador2_entry.get()

        else:

            ganador = "EMPATE"

        messagebox.showinfo(
            "FIN DEL JUEGO",
            f"Ganador: {ganador}"
        )

    # ─────────────────────────────────────
    # SALIR
    # ─────────────────────────────────────

    def salir():

        try:
            client_socket.close()
        except:
            pass

        ven_versus.destroy()

    # ─────────────────────────────────────
    # MORSE TECLADO
    # ─────────────────────────────────────

    tiempo_inicio = 0
    tiempo_solto = 0
    letra_morse = ""
    palabra = []

    morse_reves = {
        '.-': 'A',
        '-...': 'B',
        '-.-.': 'C',
        '-..': 'D',
        '.': 'E',
        '..-.': 'F',
        '--.': 'G',
        '....': 'H',
        '..': 'I',
        '.---': 'J',
        '-.-': 'K',
        '.-..': 'L',
        '--': 'M',
        '-.': 'N',
        '---': 'O',
        '.--.': 'P',
        '--.-': 'Q',
        '.-.': 'R',
        '...': 'S',
        '-': 'T',
        '..-': 'U',
        '...-': 'V',
        '.--': 'W',
        '-..-': 'X',
        '-.--': 'Y',
        '--..': 'Z'
    }

    def tecla_presion(event):

        nonlocal tiempo_inicio
        nonlocal turno

        if turno != 2:
            return

        if tiempo_inicio == 0:

            tiempo_inicio = time.time()

    def tecla_no(event):

        nonlocal tiempo_inicio
        nonlocal tiempo_solto
        nonlocal letra_morse
        nonlocal turno

        if turno != 2:
            return

        if tiempo_inicio == 0:
            return

        duracion = time.time() - tiempo_inicio

        tiempo_inicio = 0
        tiempo_solto = time.time()

        if duracion < 0.5:

            letra_morse += "."

        else:

            letra_morse += "-"

        print("Morse:", letra_morse)

    def verificar_pausa():

        nonlocal tiempo_solto
        nonlocal letra_morse
        nonlocal palabra
        nonlocal respuesta_j2
        nonlocal turno

        if tiempo_solto > 0:

            pausa = time.time() - tiempo_solto

            # letra
            if pausa > 3 and letra_morse:

                letra = morse_reves.get(
                    letra_morse,
                    '?'
                )

                palabra.append(letra)

                print("Letra:", letra)

                letra_morse = ""

            # palabra completa
            if pausa > 7:

                if palabra:

                    respuesta_j2 = "".join(
                        palabra
                    )

                    print(
                        "Jugador 2:",
                        respuesta_j2
                    )

                    calcular_puntos_j2()

                    palabra.clear()

                    turno = 1

                    siguiente_ronda()

                tiempo_solto = 0

        ven_versus.after(
            100,
            verificar_pausa
        )

    # ─────────────────────────────────────
    # BINDS
    # ─────────────────────────────────────

    ven_versus.bind(
        "<KeyPress-space>",
        tecla_presion
    )

    ven_versus.bind(
        "<KeyRelease-space>",
        tecla_no
    )

    # ─────────────────────────────────────
    # BOTONES
    # ─────────────────────────────────────

    btn_inicio = Button(
        C_versus,
        text="INICIAR",
        **estilo_btn,
        command=iniciar_ronda
    )

    btn_inicio.place(
        x=200,
        y=alto//2
    )

    btn_salir = Button(
        C_versus,
        text="SALIR",
        **estilo_btn,
        command=salir
    )

    btn_salir.place(
        x=500,
        y=alto//2
    )

    connect()
    verificar_pausa()
    
 
btn_juego_vs = Button(C_principal, text="JUGAR VS", **estilo_btn, command=versus)
btn_juego_vs.place(x=ancho//2 + 20, y=alto//2)

 
ventana_prin.mainloop()
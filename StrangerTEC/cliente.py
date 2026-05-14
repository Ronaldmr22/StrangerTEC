import socket
import threading
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import random
from PIL import Image, ImageTk
from os import path
import time
 
SERVER_IP = "192.168.137.161"
PORT = 1717
 
palabra = ""
palabra_jugador = ""
palabra_jugador2 = ""
puntaje_jugador1 = 0
puntaje_jugador2 = 0
nombre_jugador = ""
nombre_jugador2 = ""
 
Palabras = ["HOLA3+", "COMPUTADORA", "LED+12", "MONITOR", "TECLADO", "PROCESADOR", "SISTEMA", "MESSI", "MINECRAFT", "JUEGO"]

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
estilo_btn = dict(font=("Stranger Things", 20, "bold"),bg="#2d0e5e", fg="#b89ff8",activebackground="#4a2080",activeforeground="#ffffff",relief="flat",cursor="hand2")

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
    nombre_jugador_lbl=Label(ven_solo,text="Nombre del jugador",font=("Stranger Things",20))
    nombre_jugador_lbl.place(x=400,y=50)
    nombre_jugador_entry = Entry(ven_solo, width=30,
        font=("Stranger Things", 20),
        bg="#41295F", fg="#e8d5ff",
        relief="flat", bd=2)
    nombre_jugador_entry.place(x=680,y=50)

    palabra_lbl=Label(ven_solo,text="Palabra secreta",font=("Stranger Things",20))
    palabra_lbl.place(x=400,y=120)

    palabra_jgdr = Entry(ven_solo, width=30,
        font=("Stranger Things", 20),
        bg="#41295F", fg="#e8d5ff",
        relief="flat", bd=2)
    palabra_jgdr.place(x=680,y=120)
 
    status_label = Label(ven_solo, text="Desconectado",
        font=("Stranger Things", 10),
        bg="#41295F", fg="#b89ff8")
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
            btn_f.config(state='normal')
            btn_m.config(state='normal')
            btn_d.config(state='normal')
            btn_enviar.config(state='normal')
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
    btn_f.place(x=600,y=300)
 
    btn_m = Button(ven_solo, text="MEDIA",
        **estilo_btn,
        command=lambda: [send_message_medio(), deshabilitar_medio()])
    btn_m.place(x=600,y=400)
 
    btn_d = Button(ven_solo, text="DIFÍCIL",
        **estilo_btn,
        command=lambda: [send_message_dificil(), deshabilitar_dificil()])
    btn_d.place(x=600,y=500)
 
    Button(ven_solo, text="SALIR", **estilo_btn, command=salir).place(x=600,y=600)

    btn_enviar = Button(ven_solo, text="ENVIAR",
        **estilo_btn,
        command=lambda: [puntaje(palabra, palabra_jgdr.get()), puntajes_ranking()])
    btn_enviar.place(x=1070,y=110)
 
    connect()
 
    puntaje_txt = Label(ven_solo, text="0",
        font=("Stranger Things", 20, "bold"),
        bg="#41295F", fg="#e8d5ff")
    puntaje_txt.place(x=680,y=190)
    
    puntaje_lbl= Label(ven_solo, text="Puntaje",font=("Stranger Things",20),bg="#FFFFFF", fg="#000000",relief="flat", bd=2)
    puntaje_lbl.place(x=400,y=190)
 
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
 
    imagen_ranking = cargar_imagen("imagenes/ranking.png", 400, 300)
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
btn_juego_normal.place(x=470,y=350)


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

    nombre_jugador1_lbl= Label(ven_versus,text="Jugador 1",font=("Stranger Things", 25),bg="#1a0a2e",fg="#e8d5ff",relief="flat",bd=2)
    nombre_jugador1_lbl.place(x=50, y=50)
    nombre_jugador1_entry = Entry(ven_versus,width=15,font=("Stranger Things", 25),bg="#1a0a2e",fg="#e8d5ff",relief="flat",bd=2)
    nombre_jugador1_entry.place(x=250, y=50)

    puntaje1_lbl = Label(ven_versus,text="Puntaje - Jugador 1",font=("Stranger Things", 22, "bold"),bg="#1a0a2e",fg="#e8d5ff")
    puntaje1_lbl.place(x=50,y=100)
    puntaje1_txt = Label(ven_versus,text="0",font=("Stranger Things", 22, "bold"),bg="#1a0a2e",fg="#e8d5ff")
    puntaje1_txt.place(x=420,y=250)

    nombre_jugador2_lbl= Label(ven_versus,text="Jugador 2",font=("Stranger Things", 25),bg="#1a0a2e",fg="#e8d5ff",relief="flat",bd=2)
    nombre_jugador2_lbl.place(x=600, y=50)
    nombre_jugador2_entry = Entry(ven_versus,width=16,font=("Stranger Things", 25),bg="#1a0a2e",fg="#e8d5ff",relief="flat",bd=2)
    nombre_jugador2_entry.place(x=800, y=50)

    puntaje2_lbl = Label(ven_versus,text="Puntaje - Jugador 2",font=("Stranger Things", 22, "bold"),bg="#1a0a2e",fg="#e8d5ff")
    puntaje2_lbl.place(x=600,y=100)
    puntaje2_txt = Label(ven_versus,text="0",font=("Stranger Things", 22, "bold"),bg="#1a0a2e",fg="#e8d5ff")
    puntaje2_txt.place(x=1000,y=250)

    status_label = Label(ven_versus,text="Desconectado",font=("Stranger Things", 10),bg="#1a0a2e",fg="#e8d5ff")
    status_label.pack(pady=2)

    ronda_label = Label(ven_versus,text="RONDA 1",font=("Stranger Things", 30),bg="#1a0a2e",fg="white")
    ronda_label.place(x=600, y=250)

    turno_label = Label(ven_versus,text="Turno Jugador 1 (Boton)",font=("Stranger Things", 26),bg="#1a0a2e",fg="white")
    turno_label.place(x=545,y=300)

    # ─────────────────────────────────────
    # RECEIVE: alterna según ronda
    # Ronda 1 → botón = J1, Morse = J2
    # Ronda 2 → botón = J2, Morse = J1
    # ─────────────────────────────────────
    def receive_messages():
        nonlocal respuesta_j1
        nonlocal respuesta_j2
        nonlocal turno

        while True:
            try:
                msg_boton = client_socket.recv(1024).decode()
                if not msg_boton:
                    break

                msg_boton = msg_boton.strip().upper()

                if ronda == 1:
                    # Ronda 1: el botón lo usa J1
                    respuesta_j1 = msg_boton
                    print("Jugador 1 (boton):", respuesta_j1)
                    calcular_puntos_j1()
                    turno = 2
                    ven_versus.after(0, lambda: turno_label.config(text="Turno Jugador 2 (Morse)"))
                else:
                    # Ronda 2: el botón lo usa J2
                    respuesta_j2 = msg_boton
                    print("Jugador 2 (boton):", respuesta_j2)
                    calcular_puntos_j2()
                    turno = 2
                    ven_versus.after(0, lambda: turno_label.config(text="Turno Jugador 1 (Morse)"))

            except:
                break

    def connect():
        try:
            client_socket.connect((SERVER_IP, PORT))
            threading.Thread(target=receive_messages,daemon=True).start()
            status_label.config(text="Conectado al servidor")
        except Exception as e:
            status_label.config(text=f"Error: {e}")

    # ─────────────────────────────────────
    # RONDAS
    # ─────────────────────────────────────

    def iniciar_ronda():
        nonlocal palabra_actual
        nonlocal tiempo_inicio
        nonlocal tiempo_solto
        nonlocal letra_morse

        tiempo_inicio = 0
        tiempo_solto = 0
        letra_morse = ""
        letras_morse.clear()

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
        ronda_label.config(text=f"RONDA {ronda}")
        # Ronda 2: ahora J2 usa botón, J1 espera Morse
        turno_label.config(text="Turno Jugador 2 (Boton)")
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
            return 1 + puntaje_aux(lista1[1:], lista2[1:])
        else:
            return puntaje_aux(lista1[1:], lista2[1:])

    def calcular_puntos_j1():
        global puntaje_jugador1
        puntos = puntaje_aux(list(palabra_actual), list(respuesta_j1))
        puntaje_jugador1 += puntos
        ven_versus.after(0, lambda: puntaje1_txt.config(text=str(puntaje_jugador1)))

    def calcular_puntos_j2():
        global puntaje_jugador2
        puntos = puntaje_aux(list(palabra_actual), list(respuesta_j2))
        puntaje_jugador2 += puntos
        ven_versus.after(0, lambda: puntaje2_txt.config(text=str(puntaje_jugador2)))

    # ─────────────────────────────────────
    # GANADOR
    # ─────────────────────────────────────

    def mostrar_ganador():
        jugador1 = nombre_jugador1_entry.get()
        jugador2 = nombre_jugador2_entry.get()
        puntaje1 = puntaje_jugador1
        puntaje2 = puntaje_jugador2

        if puntaje1 > puntaje2:
            ganador = jugador1
        elif puntaje2 > puntaje1:
            ganador = jugador2
        else:
            ganador = "EMPATE"

        ven_ganador = Toplevel()
        ven_ganador.state('zoomed')
        ven_ganador.title("Fin del juego")
        C_ganador = Canvas(ven_ganador, highlightthickness=0, width=ancho, height=alto, bg='black')
        C_ganador.place(x=0, y=0)

        fondo_ganador = Image.open("imagenes/fondo_final.png").resize((ancho, alto))
        imagen_fondo_solo = ImageTk.PhotoImage(fondo_ganador)
        C_ganador.create_image(0, 0, image=imagen_fondo_solo, anchor="nw")
        C_ganador.imagen = imagen_fondo_solo

        jugador1_lbl=Label(ven_ganador,text=jugador1, font=("Stranger Things",25),bg="#1a0a2e",fg="#e8d5ff")
        jugador1_lbl.place(x=100,y=100)
        puntaje1_lbl=Label(ven_ganador,text=puntaje1,font=("Stranger Things",30),bg="#1a0a2e",fg="#e8d5ff")
        puntaje1_lbl.place(x=150,y=100)

        jugador2_lbl=Label(ven_ganador,text=jugador2, font=("Stranger Things",25),bg="#1a0a2e",fg="#e8d5ff")
        jugador2_lbl.place(x=600,y=100)
        puntaje2_lbl=Label(ven_ganador,text=puntaje2,font=("Stranger Things",30),bg="#1a0a2e",fg="#e8d5ff")
        puntaje2_lbl.place(x=650,y=100)

        ganador_lbl_aux=Label(ven_ganador,text="El ganador es", font=("Stranger Things",20),bg="#1a0a2e",fg="#e8d5ff")
        ganador_lbl_aux.place(x=600,y=450)
        ganador_lbl=Label(ven_ganador,text=ganador, font=("Stranger Things",30),bg="#1a0a2e",fg="#e8d5ff")
        ganador_lbl.place(x=550,y=550)

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
    letras_morse = []

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

    # ─────────────────────────────────────
    # VERIFICAR PAUSA: alterna según ronda
    # Ronda 1 → Morse = J2
    # Ronda 2 → Morse = J1
    # ─────────────────────────────────────
    def verificar_pausa():
        nonlocal tiempo_solto
        nonlocal letra_morse
        nonlocal letras_morse
        nonlocal respuesta_j1
        nonlocal respuesta_j2
        nonlocal turno

        if tiempo_solto > 0:
            pausa = time.time() - tiempo_solto

            # Confirmar letra
            if pausa > 3 and letra_morse:
                letra = morse_reves.get(letra_morse, '?')
                letras_morse.append(letra)
                print("Letra:", letra)
                letra_morse = ""
                tiempo_solto = time.time()

            # Palabra completa
            elif pausa > 7 and not letra_morse:
                if letras_morse:
                    respuesta = "".join(letras_morse)
                    print("Morse completo:", respuesta)

                    if ronda == 1:
                        # Ronda 1: el Morse es de J2
                        respuesta_j2 = respuesta
                        calcular_puntos_j2()
                    else:
                        # Ronda 2: el Morse es de J1
                        respuesta_j1 = respuesta
                        calcular_puntos_j1()

                    letras_morse.clear()
                    turno = 1
                    siguiente_ronda()

                tiempo_solto = 0

        ven_versus.after(100, verificar_pausa)

    # ─────────────────────────────────────
    # BINDS
    # ─────────────────────────────────────

    ven_versus.bind("<KeyPress-space>", tecla_presion)
    ven_versus.bind("<KeyRelease-space>", tecla_no)

    # ─────────────────────────────────────
    # BOTONES
    # ─────────────────────────────────────

    btn_inicio = Button(C_versus, text="INICIAR", **estilo_btn, command=iniciar_ronda)
    btn_inicio.place(x=300,y=550)

    btn_salir = Button(C_versus, text="SALIR", **estilo_btn, command=salir)
    btn_salir.place(x=600,y=550)

    connect()
    verificar_pausa()


btn_juego_vs = Button(C_principal, text="JUGAR VS", **estilo_btn, command=versus)
btn_juego_vs.place(x=720,y=350)

ventana_prin.mainloop()
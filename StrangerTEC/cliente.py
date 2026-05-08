import socket
import threading
from tkinter import *
from tkinter import messagebox
import random
from PIL import Image, ImageTk

SERVER_IP = "192.168.0.77"
PORT = 1717

palabra = ""
palabra_jugador = ""
puntaje_jugador1 = 0
puntaje_jugador2 = 0

Palabras = ["HOLA", "COMPUTADORA", "LED", "MONITOR", "TECLADO", "PROCESADOR", "SISTEMA", "MESSI", "MINECRAFT", "JUEGO"]

# ── Ventana principal ──────────────────────────────────────────────────────────
ventana_prin = Tk()
ventana_prin.title("POKEMON")
ventana_prin.state("zoomed")
ventana_prin.resizable(width=NO, height=NO)

ancho = ventana_prin.winfo_screenwidth()
alto  = ventana_prin.winfo_screenheight()

C_principal = Canvas(ventana_prin, highlightthickness=0, width=ancho, height=alto, bg='white')
C_principal.place(x=0, y=0)

imagen_carga    = Image.open("imagenes/fondo1.png").resize((ancho, alto))
imagenprin_fondo = ImageTk.PhotoImage(imagen_carga)
C_principal.create_image(0, 0, image=imagenprin_fondo, anchor="nw")


# ── Función que abre la ventana de juego individual ───────────────────────────
def ventana_solo():
    global palabra_jugador
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    ven_solo = Toplevel()
    ven_solo.title("Juego Solo")
    ven_solo.state("zoomed")
    ven_solo.resizable(width=NO, height=NO)

    C_solo = Canvas(ven_solo, highlightthickness=0, width=ancho, height=alto, bg='white')
    C_solo.place(x=0, y=0)

    imagen_carga_solo = Image.open("imagenes/fondo1v1.png").resize((ancho, alto))
    imagen_fondo_solo = ImageTk.PhotoImage(imagen_carga_solo)
    C_solo.create_image(0, 0, image=imagen_fondo_solo, anchor="nw")
    C_solo.imagen = imagen_fondo_solo

    # --- Widgets ---
    text_area   = Text(ven_solo, height=10, width=60)
    text_area.pack(pady=5)

    palabra_jgdr= Entry(ven_solo, width=50)
    palabra_jgdr.pack(pady=5)
    palabra_jugador = palabra_jgdr.get()
    print(palabra_jugador)

    status_label = Label(ven_solo, text="Desconectado")
    status_label.pack()

    # --- Funciones internas ---
    def receive_messages():
        while True:
            try:
                msg = client_socket.recv(1024).decode()
                if not msg:
                    break
                def insertar():
                    if text_area.winfo_exists():
                        text_area.insert(END, f"Raspberry: {msg}\n")
                ven_solo.after(0, insertar)
            except:
                break

    def send_message_facil():
        global palabra
        palabra = random.choice(Palabras)
        msg = (f"FACIL,{palabra}")
        if msg:
            client_socket.send(msg.encode())


    def send_message_medio():
        global palabra
        palabra = random.choice(Palabras)
        msg = (f"MEDIA,{palabra}")
        if msg:
            client_socket.send(msg.encode())

    def send_message_dificil():
        global palabra
        palabra = random.choice(Palabras)
        msg = (f"DIFICIL,{palabra}")
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

    #https://youtu.be/0nf6Ldsox1A
    def deshabilitar_facil():
        btn_f.config(state='disabled')
    def deshabilitar_medio():
        btn_m.config(state='disabled')
    def deshabilitar_dificil():
        btn_d.config(state='disabled')
    def puntajes_ranking():
        if btn_d.cget('state') == 'disabled' and btn_m.cget('state') == 'disabled' and btn_f.cget('state') == 'disabled':
            palabra_jgdr.config(state='disabled')
            btn_enviar.config(state='disabled')
            rank = Toplevel()

    # --- Botones ---
    btn_f = Button(ven_solo, text="Fácil", command=lambda:[send_message_facil(), deshabilitar_facil()])
    btn_f.pack(pady=2)
    btn_m = Button(ven_solo, text="Media", command=lambda:[send_message_medio(), deshabilitar_medio()])
    btn_m.pack(pady=2)
    btn_d =Button(ven_solo, text="Difícil",command=lambda:[send_message_dificil(), deshabilitar_dificil()])
    btn_d.pack(pady=2)
    Button(ven_solo, text="Salir",  command=salir).pack(pady=2)

    btn_enviar = Button(ven_solo, text="Enviar",command= lambda : [puntaje(palabra, palabra_jgdr.get()),puntajes_ranking()])
    btn_enviar.pack(pady=2)

    # Conectar al abrir la ventana
    connect()

    # Label de Puntaje
    puntaje_txt = Label(ven_solo, text=puntaje_jugador1)
    puntaje_txt.pack(pady=2)

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
        global puntaje_jugador1
        puntaje_jugador1 += puntaje_aux(list(palabra1), list(palabra2))
        puntaje_txt.config(text=puntaje_jugador1)
        palabra_jgdr.delete(0, END)


# ── Botones de la ventana principal ───────────────────────────────────────────
btn_juego_normal = Button(C_principal, text="JUGAR SOLO", command=ventana_solo)
btn_juego_normal.place(x=ancho//2 - 100, y=alto//2)

btn_juego_vs = Button(C_principal, text="JUGAR VS", command=lambda: print("Próximamente"))
btn_juego_vs.place(x=ancho//2 + 20, y=alto//2)

ventana_prin.mainloop()
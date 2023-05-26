import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import json
import serial


class PaginaLogin(tk.Frame):
    def __init__(self, master, notebook):
        super().__init__(master)

        self.notebook = notebook

        self.label_nombre = tk.Label(self, text="Nombre de usuario:")
        self.label_nombre.pack()
        self.entry_nombre = tk.Entry(self)
        self.entry_nombre.pack()

        self.label_contrasena = tk.Label(self, text="Contraseña:")
        self.label_contrasena.pack()
        self.entry_contrasena = tk.Entry(self, show="*")
        self.entry_contrasena.pack()

        self.boton_login = tk.Button(self, text="Login", command=self.verificar_login)
        self.boton_login.pack()

    def verificar_login(self):
        nombre = self.entry_nombre.get()
        contrasena = self.entry_contrasena.get()

        # Lógica para verificar el login con los datos de usuario
        with open("BD/usuarios.json") as file:
            data = json.load(file)

        usuario_encontrado = None
        for usuario in data["usuarios"]:
            if usuario["nombre"] == nombre and usuario["contrasena"] == contrasena:
                usuario_encontrado = usuario
                break

        if usuario_encontrado:
            # Verificar si el usuario tiene el atributo "tipo" con valor "admin"
            if "tipo" in usuario_encontrado and usuario_encontrado["tipo"] == "admin":
                self.notebook.add(PaginaAdmin(self.notebook), text="Administrador")

            self.notebook.add(PaginaAlertas(self.notebook), text="Alertas")
            self.notebook.add(PaginaEnviarSenal(self.notebook), text="Enviar Señales")
            self.notebook.add(PaginaVerEstatus(self.notebook), text="Ver Estado")
            self.notebook.select(1)  # Seleccionar la página de Alertas
            self.notebook.forget(0)
        else:
            messagebox.showerror("Error de login", "Nombre de usuario o contraseña incorrectos")

class PaginaAdmin(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.label_admin = tk.Label(self, text="¡Bienvenido, Administrador!")
        self.label_admin.pack()

class PaginaAlertas(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.label_alertas = tk.Label(self, text="Alertas:")
        self.label_alertas.pack()

        # Configurar el puerto serial
        puerto = 'COM3'  # Cambia esto al puerto serial correcto en tu sistema
        velocidad = 9600  # Velocidad de comunicación del puerto serial

        # Abrir la conexión con el puerto serial
        self.arduino = serial.Serial(puerto, velocidad)

        # Leer datos del puerto serial
        self.leer_serial()

    def leer_serial(self):
        if self.arduino.in_waiting > 0:
            dato = self.arduino.readline().decode().rstrip()  # Leer una línea de datos y decodificarla
            print("Dato recibido desde Arduino:", dato)

        # Volver a llamar a la función para seguir leyendo los datos
        self.after(100, self.leer_serial)

class PaginaEnviarSenal(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.boton_enviar_senal = tk.Button(self, text="Enviar Señal", command=self.enviar_senal)
        self.boton_enviar_senal.pack()

        # Configurar el puerto serial
        puerto = 'COM3'  # Cambia esto al puerto serial correcto en tu sistema
        velocidad = 9600  # Velocidad de comunicación del puerto serial

        # Abrir la conexión con el puerto serial
        self.arduino = serial.Serial(puerto, velocidad)

    def enviar_senal(self):
        # Aquí puedes enviar la señal al Arduino
        # Por ejemplo, puedes escribir un valor en el puerto serial
        self.arduino.write(b'Senal para apagar el sistema')  # Cambia el contenido de la señal según tus necesidades

class PaginaVerEstatus(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.label_estado_arduino = tk.Label(self, text="Estado del Arduino: Sin conexión")
        self.label_estado_arduino.pack()

class PaginaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("600x600")
        self.title("Aplicación")

        self.notebook = ttk.Notebook(self)

        self.pagina_login = PaginaLogin(self.notebook, self.notebook)
        self.notebook.add(self.pagina_login, text="Login")

        self.notebook.pack()

if __name__ == "__main__":
    app = PaginaPrincipal()
    app.mainloop()

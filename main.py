import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import json
import serial

class PaginaLogin(tk.Frame):
    def __init__(self, master, notebook, puerto_serial):
        super().__init__(master)

        self.notebook = notebook
        self.puerto_serial = puerto_serial

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

            self.notebook.add(PaginaAlertas(self.notebook, self.puerto_serial), text="Alertas")
            self.notebook.add(PaginaVerEstatus(self.notebook, self.puerto_serial), text="Ver Estado")
            self.notebook.select(2)  # Seleccionar la página de Ver Estado
            self.notebook.forget(0)  # Ocultar la página de inicio de sesión
        else:
            messagebox.showerror("Error de login", "Nombre de usuario o contraseña incorrectos")


class PaginaAdmin(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.label_admin = tk.Label(self, text="¡Bienvenido, Administrador!")
        self.label_admin.pack()


class PaginaAlertas(tk.Frame):
    def __init__(self, master, puerto_serial):
        super().__init__(master)

        self.label_alertas = tk.Label(self, text="Alertas:")
        self.label_alertas.pack()

        self.label_datos = tk.Label(self, text="")
        self.label_datos.pack()

        self.boton_enviar = tk.Button(self, text="Apagar alarma", command=self.enviar_caracter_a)
        self.boton_enviar.pack()

        self.puerto_serial = puerto_serial

    def leer_serial(self):
        if self.puerto_serial.in_waiting > 0:
            dato = self.puerto_serial.readline()
            try:
                dato_decodificado = dato.decode('utf-8').rstrip()
                print(dato_decodificado)
                self.label_datos.config(text="Dato recibido desde Arduino: " + dato_decodificado)
            except UnicodeDecodeError:
                print("Error de decodificación en el dato recibido")

        # Programar la siguiente lectura después de 100 ms
        self.after(100, self.leer_serial)

    def enviar_caracter_a(self):
        self.puerto_serial.write(b'A')


class PaginaVerEstatus(tk.Frame):
    def __init__(self, master, puerto_serial):
        super().__init__(master)

        self.label_estado_arduino = tk.Label(self, text="Estado del Arduino: Sin conexión")
        self.label_estado_arduino.pack()

        self.puerto_serial = puerto_serial

        self.boton_enviar = tk.Button(self, text="Apagar/Encender sistema", command=self.enviar_senal)
        self.boton_enviar.pack()

    def actualizar_estado_arduino(self):
        if self.puerto_serial.in_waiting > 0:
            dato = self.puerto_serial.readline()
            try:
                dato_decodificado = dato.decode('utf-8').strip()
                estado = "Estado del Arduino: " + dato_decodificado
                self.label_estado_arduino.config(text=estado)
            except UnicodeDecodeError:
                print("Error de decodificación en el dato recibido")

        # Programar la siguiente actualización después de 100 ms
        self.after(100, self.actualizar_estado_arduino)

    def leer_estado_arduino(self):
        if self.puerto_serial.in_waiting > 0:
            dato = self.puerto_serial.readline()
            try:
                dato_decodificado = dato.decode('utf-8').strip()
                return "Estado del Arduino: " + dato_decodificado
            except UnicodeDecodeError:
                print("Error de decodificación en el dato recibido")
        return "Estado del Arduino: Sin conexión"

    def enviar_senal(self):
        self.puerto_serial.write(b'P')


class PaginaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("600x600")
        self.title("Aplicación")

        self.notebook = ttk.Notebook(self)

        COM = 'COM3'
        velocidad = 9600

        self.puerto_serial = serial.Serial(port=COM, baudrate=velocidad, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, timeout=2)

        self.pagina_login = PaginaLogin(self.notebook, self.notebook, self.puerto_serial)
        self.notebook.add(self.pagina_login, text="Login")

        self.notebook.pack()


if __name__ == "__main__":
    app = PaginaPrincipal()
    app.mainloop()

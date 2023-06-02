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

        self.label_usuario = tk.Label(self, text="Usuario:")
        self.label_usuario.pack()
        self.entry_usuario = tk.Entry(self)
        self.entry_usuario.pack()

        self.label_contrasena = tk.Label(self, text="Contraseña:")
        self.label_contrasena.pack()
        self.entry_contrasena = tk.Entry(self, show="*")
        self.entry_contrasena.pack()

        self.boton_submit = tk.Button(self, text="Submit", command=self.agregar_usuario)
        self.boton_submit.pack()

    def agregar_usuario(self):
        usuario = self.entry_usuario.get()
        contrasena = self.entry_contrasena.get()

        datos_usuario = {
            "nombre": usuario,
            "contrasena": contrasena,
            "tipo": "usuario"
        }

        # Ruta del archivo JSON
        ruta_json = "BD/usuarios.json"

        try:
            with open(ruta_json, "r") as archivo:
                data = json.load(archivo)
        except FileNotFoundError:
            data = {"usuarios": []}

        data["usuarios"].append(datos_usuario)
        with open(ruta_json, "w") as archivo:
            json.dump(data, archivo)

        # Mostrar mensaje de éxito
        tk.messagebox.showinfo("Éxito", "Usuario agregado correctamente")




class PaginaAlertas(tk.Frame):
    def __init__(self, master, puerto_serial):
        super().__init__(master)

        self.label_alertas = tk.Label(self, text="Alertas:")
        self.label_alertas.pack()

        self.label_datos = tk.Label(self, text="Datos recibidos desde Arduino: No se ha detectado movimiento")
        self.label_datos.pack()

        self.boton_enviar = tk.Button(self, text="Apagar alarma", command=self.enviar_caracter_a)
        self.boton_enviar.pack()

        self.puerto_serial = puerto_serial

        self.leer_serial()  # Iniciar la lectura del puerto serial

    def leer_serial(self):
        if self.puerto_serial.in_waiting > 0:
            datos = self.puerto_serial.read(self.puerto_serial.in_waiting)
            try:
                datos_decodificados = datos.decode('utf-8').rstrip()
                if datos_decodificados == "Se detectó movimiento":
                    self.label_datos.config(text="Datos recibidos desde Arduino: " + datos_decodificados)
                elif datos_decodificados == "Sistema apagado":
                    self.label_datos.config(text="Datos recibidos desde Arduino: " + datos_decodificados)
                else:
                    self.label_datos.config(text="Datos recibidos desde Arduino: No se ha detectado movimiento")
            except UnicodeDecodeError:
                print("Error de decodificación en los datos recibidos")

        self.after(100, self.leer_serial)  # Volver a leer el puerto serial después de 100 ms

    def enviar_caracter_a(self):
        self.puerto_serial.write(b'A')


class PaginaVerEstatus(tk.Frame):
    def __init__(self, master, puerto_serial):
        super().__init__(master)

        self.label_estado_arduino = tk.Label(self, text="Estado Sistema")
        self.label_estado_arduino.pack()

        self.puerto_serial = puerto_serial

        self.boton_enviar = tk.Button(self, text="Apagar/Encender sistema", command=self.enviar_senal)
        self.boton_enviar.pack()

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

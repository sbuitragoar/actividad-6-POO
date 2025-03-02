import tkinter as tk
from tkinter import messagebox
import os

ARCHIVO = "amigosContacto.txt"

class GestorContactosGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Contactos")

        tk.Label(root, text="Nombre:").grid(row=0, column=0)
        self.entrada_nombre = tk.Entry(root)
        self.entrada_nombre.grid(row=0, column=1)

        tk.Label(root, text="Número:").grid(row=1, column=0)
        self.entrada_numero = tk.Entry(root)
        self.entrada_numero.grid(row=1, column=1)

        tk.Button(root, text="Agregar Contacto", command=self.crear_contacto).grid(row=2, column=0, columnspan=2)
        tk.Button(root, text="Ver Contactos", command=self.leer_contactos).grid(row=3, column=0, columnspan=2)
        tk.Button(root, text="Actualizar Contacto", command=self.actualizar_contacto).grid(row=4, column=0, columnspan=2)
        tk.Button(root, text="Eliminar Contacto", command=self.eliminar_contacto).grid(row=5, column=0, columnspan=2)

        self.lista_contactos = tk.Text(root, height=10, width=40)
        self.lista_contactos.grid(row=6, column=0, columnspan=2)

    def crear_contacto(self):
        nombre = self.entrada_nombre.get()
        numero = self.entrada_numero.get()
        if not nombre or not numero:
            messagebox.showwarning("Error", "Por favor, ingresa nombre y número.")
            return
        
        with open(ARCHIVO, "a") as archivo:
            archivo.write(f"{nombre}!{numero}\n")
        messagebox.showinfo("Éxito", "Contacto agregado.")
        self.entrada_nombre.delete(0, tk.END)
        self.entrada_numero.delete(0, tk.END)

    def leer_contactos(self):
        self.lista_contactos.delete(1.0, tk.END)
        if not os.path.exists(ARCHIVO):
            self.lista_contactos.insert(tk.END, "No hay contactos guardados.")
            return
        
        with open(ARCHIVO, "r") as archivo:
            for linea in archivo:
                self.lista_contactos.insert(tk.END, linea.replace("!", " - "))

    def actualizar_contacto(self):
        nombre = self.entrada_nombre.get()
        nuevo_numero = self.entrada_numero.get()
        if not nombre or not nuevo_numero:
            messagebox.showwarning("Error", "Por favor, ingresa nombre y nuevo número.")
            return
        
        if not os.path.exists(ARCHIVO):
            messagebox.showwarning("Error", "No hay contactos guardados.")
            return
        
        actualizado = False
        contactos = []
        with open(ARCHIVO, "r") as archivo:
            for linea in archivo:
                nombre_contacto, numero_contacto = linea.strip().split("!")
                if nombre_contacto == nombre:
                    contactos.append(f"{nombre}!{nuevo_numero}\n")
                    actualizado = True
                else:
                    contactos.append(linea)
        
        with open(ARCHIVO, "w") as archivo:
            archivo.writelines(contactos)
        
        if actualizado:
            messagebox.showinfo("Éxito", "Contacto actualizado.")
        else:
            messagebox.showwarning("Error", "Contacto no encontrado.")

    def eliminar_contacto(self):
        nombre = self.entrada_nombre.get()
        if not nombre:
            messagebox.showwarning("Error", "Por favor, ingresa un nombre para eliminar.")
            return
        
        if not os.path.exists(ARCHIVO):
            messagebox.showwarning("Error", "No hay contactos guardados.")
            return
        
        eliminado = False
        contactos = []
        with open(ARCHIVO, "r") as archivo:
            for linea in archivo:
                nombre_contacto, numero_contacto = linea.strip().split("!")
                if nombre_contacto != nombre:
                    contactos.append(linea)
                else:
                    eliminado = True
        
        with open(ARCHIVO, "w") as archivo:
            archivo.writelines(contactos)
        
        if eliminado:
            messagebox.showinfo("Éxito", "Contacto eliminado.")
        else:
            messagebox.showwarning("Error", "Contacto no encontrado.")

if __name__ == "__main__":
    root = tk.Tk()
    app = GestorContactosGUI(root)
    root.mainloop()

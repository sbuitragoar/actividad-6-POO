import tkinter as tk
from tkinter import messagebox
import os

class GestorContactos:
    """Clase que maneja todas las operaciones CRUD de contactos"""
    
    def __init__(self, archivo="amigosContacto.txt"):
        self.archivo = archivo
    
    def crear(self, nombre, numero):
        """Crea un nuevo contacto en el archivo"""
        if not nombre or not numero:
            return False, "Nombre y número son requeridos"
        
        try:
            with open(self.archivo, "a") as archivo:
                archivo.write(f"{nombre}!{numero}\n")
            return True, "Contacto agregado exitosamente"
        except Exception as e:
            return False, f"Error al crear contacto: {str(e)}"
    
    def leer(self):
        """Lee todos los contactos del archivo"""
        if not os.path.exists(self.archivo):
            return False, "No hay contactos guardados"
        
        try:
            contactos = []
            with open(self.archivo, "r") as archivo:
                for linea in archivo:
                    if linea.strip():  # Ignorar líneas vacías
                        nombre, numero = linea.strip().split("!")
                        contactos.append((nombre, numero))
            return True, contactos
        except Exception as e:
            return False, f"Error al leer contactos: {str(e)}"
    
    def actualizar(self, nombre, nuevo_numero):
        """Actualiza el número de un contacto existente"""
        if not nombre or not nuevo_numero:
            return False, "Nombre y nuevo número son requeridos"
        
        if not os.path.exists(self.archivo):
            return False, "No hay contactos guardados"
        
        try:
            actualizado = False
            contactos = []
            with open(self.archivo, "r") as archivo:
                for linea in archivo:
                    if linea.strip():  # Ignorar líneas vacías
                        nombre_contacto, numero_contacto = linea.strip().split("!")
                        if nombre_contacto == nombre:
                            contactos.append(f"{nombre}!{nuevo_numero}\n")
                            actualizado = True
                        else:
                            contactos.append(linea)
            
            with open(self.archivo, "w") as archivo:
                archivo.writelines(contactos)
            
            if actualizado:
                return True, "Contacto actualizado exitosamente"
            else:
                return False, "Contacto no encontrado"
        except Exception as e:
            return False, f"Error al actualizar contacto: {str(e)}"
    
    def eliminar(self, nombre):
        """Elimina un contacto por su nombre"""
        if not nombre:
            return False, "Nombre es requerido"
        
        if not os.path.exists(self.archivo):
            return False, "No hay contactos guardados"
        
        try:
            eliminado = False
            contactos = []
            with open(self.archivo, "r") as archivo:
                for linea in archivo:
                    if linea.strip():  # Ignorar líneas vacías
                        nombre_contacto, numero_contacto = linea.strip().split("!")
                        if nombre_contacto != nombre:
                            contactos.append(linea)
                        else:
                            eliminado = True
            
            with open(self.archivo, "w") as archivo:
                archivo.writelines(contactos)
            
            if eliminado:
                return True, "Contacto eliminado exitosamente"
            else:
                return False, "Contacto no encontrado"
        except Exception as e:
            return False, f"Error al eliminar contacto: {str(e)}"


class GestorContactosGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Contactos")
        # Crear instancia del gestor CRUD
        self.gestor = GestorContactos()

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
        
        exito, mensaje = self.gestor.crear(nombre, numero)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.entrada_nombre.delete(0, tk.END)
            self.entrada_numero.delete(0, tk.END)
        else:
            messagebox.showwarning("Error", mensaje)

    def leer_contactos(self):
        self.lista_contactos.delete(1.0, tk.END)
        
        exito, resultado = self.gestor.leer()
        if exito:
            for nombre, numero in resultado:
                self.lista_contactos.insert(tk.END, f"{nombre} - {numero}\n")
        else:
            self.lista_contactos.insert(tk.END, resultado)

    def actualizar_contacto(self):
        nombre = self.entrada_nombre.get()
        nuevo_numero = self.entrada_numero.get()
        
        exito, mensaje = self.gestor.actualizar(nombre, nuevo_numero)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.entrada_nombre.delete(0, tk.END)
            self.entrada_numero.delete(0, tk.END)
            self.leer_contactos()  # Actualizar la lista después de modificar
        else:
            messagebox.showwarning("Error", mensaje)

    def eliminar_contacto(self):
        nombre = self.entrada_nombre.get()
        
        # Pedir confirmación antes de eliminar
        if messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar el contacto '{nombre}'?"):
            exito, mensaje = self.gestor.eliminar(nombre)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.entrada_nombre.delete(0, tk.END)
                self.entrada_numero.delete(0, tk.END)
                self.leer_contactos()  # Actualizar la lista después de eliminar
            else:
                messagebox.showwarning("Error", mensaje)


if __name__ == "__main__":
    root = tk.Tk()
    app = GestorContactosGUI(root)
    root.mainloop()

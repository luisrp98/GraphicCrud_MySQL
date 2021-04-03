"""
    Autor: Luis Romo
    Descripción: Combinando las dos actividades anteriores que se refierene a el diseño de interfaces graficas y acceso a base de datos. 
    Construye una programa CRUD en Python con Interfaz Grafica (GUI) para controlar la información 
    de uns tabla en una base de datos de MySQL(opcional)
    Fecha: 3/04/21
"""
import sqlite3 as sql
import tkinter as tk
from tkinter import ttk

import mysql.connector


# Clase de ventana principal
class Ventana:
    # Constructor de ventana principal
    def __init__(self, window):
        self.window = window
        self.window.title("Inventario libros")
        self.window.resizable(False, False)
        self.window.config(bg="#669EB1")

        # Frame para lo que no es la tabla
        frame = tk.LabelFrame(self.window, bg="#8DB8C8")
        frame.grid(row=0, column=0, columnspan=6)

        # Texto, botones y tabla
        tk.Label(
            frame, text="Inventario de la libreria 'Abril'", bg="#8DB8C8", font=("", 30)
        ).grid(column=0, columnspan=3, row=0)
        # Renglon en blanco
        frame.grid_rowconfigure(1, minsize=20)

        # Boton registro
        b_insert = tk.Button(
            frame,
            text="Introducir registro",
            command=lambda: [VentanaInsertarDatos(window), self.window.destroy()],
        ).grid(column=0, row=2)

        # Boton eliminar
        b_borrar = tk.Button(
            frame,
            text="Eliminar registro",
            command=lambda: [VentanaEliminarDatos(window), self.window.destroy()],
        ).grid(column=1, row=2)

        # Boton editar
        b_editar = tk.Button(
            frame,
            text="Editar registro",
            command=lambda: [VentanaEditarDatos(window), self.window.destroy()],
        ).grid(column=2, row=2)

        # Renglon en blanco
        frame.grid_rowconfigure(3, minsize=20)

        # Tabla
        self.tree = ttk.Treeview(columns=["#0", "#1", "#2", "#3", "#04"])
        self.tree.grid(row=4, column=0, columnspan=6)
        self.tree.heading("#0", text="ID")
        self.tree.heading("#1", text="Nombre")
        self.tree.heading("#2", text="Autor")
        self.tree.heading("#3", text="Editorial")
        self.tree.heading("#4", text="Cantidad")
        self.tree.heading("#5", text="Precio")

        self.obtenerInventario()

    # Funcion que ejecuta una query, con informacion para conectarse a la db, retorna el resultado de la query
    def ejecutar_query(self, query, parametros=()):
        # Parametro con información para conectar a la db
        mydb = mysql.connector.connect(
            host="localhost", user="root", password="cabazoo98", db="libreria_db"
        )
        mycursor = mydb.cursor()
        mycursor.execute(query, parametros)
        myresult = mycursor.fetchall()
        mydb.commit()
        return myresult

    # Funcion que limpia la tabla y agrega los datos de la db
    def obtenerInventario(self):
        # Borra datos
        datos = self.tree.get_children()
        for dato in datos:
            self.tree.delete(dato)

        # Ejecuta la query y agrega datos de la db a la tabla
        query = "SELECT * FROM inventario;"
        inventario = self.ejecutar_query(query)
        for fila in inventario:
            self.tree.insert(
                "",
                tk.END,
                text=fila[0],
                values=(fila[1], fila[2], fila[3], fila[4], fila[5]),
            )


# Clase de ventana para insertar datos
class VentanaInsertarDatos(Ventana):
    def __init__(self, window):
        self.ventanaDatos = tk.Toplevel(window)
        self.ventanaDatos.title("Datos")
        self.ventanaDatos.resizable(False, False)
        self.ventanaDatos.config(bg="#669EB1")

        # Funcion que cierra la ventana
        def cerrarVentana(self):
            self.ventanaDatos.destroy()

        # Query para agregar registro
        def agregarRegistro(nombre, autor, editorial, cantidad, precio):
            # Obtenemos el id anterior y generamos el nuevo
            myresult = self.ejecutar_query(
                "SELECT inventario_id FROM inventario WHERE inventario_id = (SELECT MAX(inventario_id) FROM inventario);"
            )
            print(myresult)
            a = myresult[0]
            idString = "".join(str(e) for e in a)
            a = int(idString) + 1
            print(a)

            # Creacion de query
            query = "INSERT INTO `libreria_db`.`inventario`(`inventario_id`,`inventario_nombre`,`inventario_autor`,`inventario_editorial`,`inventario_cantidad`,`inventario_precio`) VALUES (%s,%s,%s,%s,%s,%s);"
            parametros = (a, nombre, autor, editorial, cantidad, precio)
            self.ejecutar_query(query, parametros)
            print(query, parametros)

        # Nombre
        lb_nombre = tk.Label(
            self.ventanaDatos, text="Nombre:", bg="#669EB1", font=("", 15)
        ).grid(column=0, row=0)
        e_nombre = tk.Entry(self.ventanaDatos, text="")
        e_nombre.grid(column=1, row=0)
        # Autor
        lb_autor = tk.Label(
            self.ventanaDatos, text="Autor:", bg="#669EB1", font=("", 15)
        ).grid(column=0, row=1)
        e_autor = tk.Entry(self.ventanaDatos, text="")
        e_autor.grid(column=1, row=1)
        # Editorial
        lb_editorial = tk.Label(
            self.ventanaDatos, text="Editorial:", bg="#669EB1", font=("", 15)
        ).grid(column=0, row=2)
        e_editorial = tk.Entry(self.ventanaDatos, text="")
        e_editorial.grid(column=1, row=2)
        # Cantidad
        lb_cantidad = tk.Label(
            self.ventanaDatos, text="Cantidad:", bg="#669EB1", font=("", 15)
        ).grid(column=0, row=3)
        e_cantidad = tk.Entry(self.ventanaDatos, text="")
        e_cantidad.grid(column=1, row=3)
        # Precio
        lb_precio = tk.Label(
            self.ventanaDatos, text="Precio:", bg="#669EB1", font=("", 15)
        ).grid(column=0, row=4)
        e_precio = tk.Entry(self.ventanaDatos, text="")
        e_precio.grid(column=1, row=4)
        # Botones
        b_aceptar = tk.Button(
            self.ventanaDatos,
            text="Aceptar",
            command=lambda: [
                agregarRegistro(
                    e_nombre.get(),
                    e_autor.get(),
                    e_editorial.get(),
                    e_cantidad.get(),
                    e_precio.get(),
                ),
                Ventana(window),
                cerrarVentana(self),
            ],
        ).grid(column=1, row=5)
        b_cancelar = tk.Button(
            self.ventanaDatos, text="Cancelar", command=lambda: cerrarVentana(self)
        ).grid(column=0, row=5)

        self.ventanaDatos.mainloop()


# Clase de ventana para eliminar datos
class VentanaEliminarDatos(Ventana):
    def __init__(self, window):
        self.ventanaDatos = tk.Toplevel(window)
        self.ventanaDatos.title("Datos")
        self.ventanaDatos.resizable(False, False)
        self.ventanaDatos.config(bg="#669EB1")

        # Funcion que cierra la ventana
        def cerrarVentana(self):
            self.ventanaDatos.destroy()

        # Funcion que genera la lista con los ID de los registros
        def contadorID():
            # Ejecuta la query y agrega datos de la db a la tabla
            query = "SELECT inventario_id FROM inventario ORDER BY inventario_id;"
            inventario = self.ejecutar_query(query)
            lista = []
            for fila in inventario:
                lista.append(fila[0])
            for x in range(len(lista)):
                print(lista[x])
            return lista

        # Query para eliminar registro, recibe el id del combobox para utilizarlo como filtro de la funcion sql
        def eliminarRegistro(id):
            # Creacion de query
            query = "DELETE FROM `libreria_db`.`inventario` WHERE inventario_id = %s;"
            parametros = (id,)
            self.ejecutar_query(query, parametros)
            print(query)

        # Renglon en blanco
        self.ventanaDatos.grid_rowconfigure(0, minsize=10)
        # Label
        lb_txt = tk.Label(
            self.ventanaDatos,
            text="Selecciona el ID del registro que deseas eliminar",
            bg="#669EB1",
            font=("", 15),
        ).grid(column=0, row=1, columnspan=2)

        # Combobox
        opt_combo = ttk.Combobox(self.ventanaDatos)
        opt_combo.grid(column=0, row=2, columnspan=2)
        opt_combo["values"] = contadorID()

        # Renglon en blanco
        self.ventanaDatos.grid_rowconfigure(3, minsize=10)

        # Botones
        b_aceptar = tk.Button(
            self.ventanaDatos,
            text="Aceptar",
            command=lambda: [
                eliminarRegistro(str(opt_combo.get())),
                Ventana(window),
                cerrarVentana(self),
            ],
        ).grid(column=1, row=4)
        b_cancelar = tk.Button(
            self.ventanaDatos, text="Cancelar", command=lambda: cerrarVentana(self)
        ).grid(column=0, row=4)

        self.ventanaDatos.mainloop()


# Clase de ventana para editar datos
class VentanaEditarDatos(Ventana):
    def __init__(self, window):
        self.ventanaDatos = tk.Toplevel(window)
        self.ventanaDatos.title("Datos")
        self.ventanaDatos.resizable(False, False)
        self.ventanaDatos.config(bg="#669EB1")

        # Funcion que cierra la ventana
        def cerrarVentana(self):
            self.ventanaDatos.destroy()

        # Crea la ventana en la que se muestran los datos para editar
        def EditarDatos(window, id):
            self.ventanaDatos = tk.Toplevel(window)
            self.ventanaDatos.title("Datos")
            self.ventanaDatos.resizable(False, False)
            self.ventanaDatos.config(bg="#669EB1")
            print("IMRPIMIENDO ID:", id)

            # Funcion que cierra la ventana
            def cerrarVentana(self):
                self.ventanaDatos.destroy()

            def obtenerRegistro(id):
                # Obtenemos los datos del registro seleccionado para ponerlos en el Entry
                query = "SELECT * FROM inventario WHERE inventario_id = %s;"
                parametros = (id,)
                myresult = self.ejecutar_query(query, parametros)
                for data in myresult:
                    id = data[0]
                    nombre = data[1]
                    autor = data[2]
                    editorial = data[3]
                    cantidad = data[4]
                    precio = data[5]
                return id, nombre, autor, editorial, cantidad, precio

            # Agrega la informacion recibida del registro seleccionada en los campos de texto
            def insertarEntry(id, nombre, autor, editorial, cantidad, precio):
                e_nombre.insert(0, nombre)
                e_autor.insert(0, autor)
                e_editorial.insert(0, editorial)
                e_cantidad.insert(0, cantidad)
                e_precio.insert(0, precio)

            # Nombre
            lb_nombre = tk.Label(
                self.ventanaDatos, text="Nombre:", bg="#669EB1", font=("", 15)
            ).grid(column=0, row=0)
            e_nombre = tk.Entry(self.ventanaDatos, text="")
            e_nombre.grid(column=1, row=0)
            # Autor
            lb_autor = tk.Label(
                self.ventanaDatos, text="Autor:", bg="#669EB1", font=("", 15)
            ).grid(column=0, row=1)
            e_autor = tk.Entry(self.ventanaDatos, text="")
            e_autor.grid(column=1, row=1)
            # Editorial
            lb_editorial = tk.Label(
                self.ventanaDatos, text="Editorial:", bg="#669EB1", font=("", 15)
            ).grid(column=0, row=2)
            e_editorial = tk.Entry(self.ventanaDatos, text="")
            e_editorial.grid(column=1, row=2)
            # Cantidad
            lb_cantidad = tk.Label(
                self.ventanaDatos, text="Cantidad:", bg="#669EB1", font=("", 15)
            ).grid(column=0, row=3)
            e_cantidad = tk.Entry(self.ventanaDatos, text="")
            e_cantidad.grid(column=1, row=3)
            # Precio
            lb_precio = tk.Label(
                self.ventanaDatos, text="Precio:", bg="#669EB1", font=("", 15)
            ).grid(column=0, row=4)
            e_precio = tk.Entry(self.ventanaDatos, text="")
            e_precio.grid(column=1, row=4)

            # Llamamiento de funciones
            id, nombre, autor, editorial, cantidad, precio = obtenerRegistro(id)

            insertarEntry(id, nombre, autor, editorial, cantidad, precio)

            # Query para actualizar el registro
            def actualizarDatos(nombre, autor, editorial, cantidad, precio, id):
                query = (
                    "UPDATE `libreria_db`.`inventario` SET`inventario_id` = %s,`inventario_nombre` = '%s',`inventario_autor` = '%s',`inventario_editorial` = '%s',`inventario_cantidad` = %s, `inventario_precio` = %s WHERE `inventario_id` = %s;"
                    % (id, nombre, autor, editorial, cantidad, precio, id)
                )

                print(query)
                self.ejecutar_query(query)

            # Botones
            b_aceptar = tk.Button(
                self.ventanaDatos,
                text="Aceptar",
                command=lambda: [
                    actualizarDatos(
                        e_nombre.get(),
                        e_autor.get(),
                        e_editorial.get(),
                        e_cantidad.get(),
                        e_precio.get(),
                        id,
                    ),
                    Ventana(window),
                    cerrarVentana(self),
                ],
            ).grid(column=1, row=5)
            b_cancelar = tk.Button(
                self.ventanaDatos,
                text="Cancelar",
                command=lambda: [
                    cerrarVentana(self),
                ],
            ).grid(column=0, row=5)

            self.ventanaDatos.mainloop()

        # Funcion que genera la lista con los ID de los registros
        def contadorID():
            # Ejecuta la query y agrega datos de la db a la tabla
            query = "SELECT inventario_id FROM inventario ORDER BY inventario_id;"
            inventario = self.ejecutar_query(query)
            lista = []
            for fila in inventario:
                lista.append(fila[0])
            for x in range(len(lista)):
                print(lista[x])
            return lista

        # Renglon en blanco
        self.ventanaDatos.grid_rowconfigure(0, minsize=10)

        # Label
        lb_txt = tk.Label(
            self.ventanaDatos,
            text="Selecciona el ID del registro que deseas editar",
            bg="#669EB1",
            font=("", 15),
        ).grid(column=0, row=1, columnspan=2)

        # Combobox
        opt_combo = ttk.Combobox(self.ventanaDatos)
        opt_combo.grid(column=0, row=2, columnspan=2)
        opt_combo["values"] = contadorID()

        # Renglon en blanco
        self.ventanaDatos.grid_rowconfigure(3, minsize=10)

        # Botones
        b_aceptar = tk.Button(
            self.ventanaDatos,
            text="Aceptar",
            command=lambda: [
                EditarDatos(window, str(opt_combo.get())),
                cerrarVentana(self),
            ],
        ).grid(column=1, row=4)
        b_cancelar = tk.Button(
            self.ventanaDatos, text="Cancelar", command=lambda: cerrarVentana(self)
        ).grid(column=0, row=4)

        self.ventanaDatos.mainloop()


# Ejecuta el programa si se ejecuta como main
if __name__ == "__main__":
    window = tk.Tk()
    ventanaPrincipal = Ventana(window)
    window.mainloop()

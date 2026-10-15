import tkinter as tk
from tkinter import messagebox

class SimuladorPila:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador Gráfico de Pila (LIFO) - Estructura de Datos")
        self.root.geometry("650x550")
        self.root.configure(bg="#f0f9ff")
        self.root.resizable(False, False)

        # Configuración lógica de la Pila
        self.pila = []
        self.capacidad_maxima = 7  # Límite visual para demostrar el Desbordamiento (Overflow)

        # --- INTERFAZ: PANEL SUPERIOR DE CONTROLES ---
        frame_controles = tk.Frame(root, bg="#ffffff", bd=1, relief="solid", padx=15, pady=15)
        frame_controles.pack(pady=15, padx=20, fill="x")

        tk.Label(frame_controles, text="Valor a insertar:", bg="#ffffff", fg="#0f172a", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, padx=5)
        
        self.entrada_valor = tk.Entry(frame_controles, font=("Segoe UI", 11), width=12, bd=1, relief="solid")
        self.entrada_valor.grid(row=0, column=1, padx=5)
        self.entrada_valor.bind("<Return>", lambda event: self.push()) # Permite insertar con la tecla Enter

        # Botones de operaciones
        tk.Button(frame_controles, text="Push (Apilar)", command=self.push, bg="#0ea5e9", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", padx=10, cursor="hand2").grid(row=0, column=2, padx=5)
        tk.Button(frame_controles, text="Pop (Desapilar)", command=self.pop, bg="#ef4444", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", padx=10, cursor="hand2").grid(row=0, column=3, padx=5)
        tk.Button(frame_controles, text="Peek (Ver Tope)", command=self.peek, bg="#f59e0b", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", padx=10, cursor="hand2").grid(row=0, column=4, padx=5)
        tk.Button(frame_controles, text="Vaciar", command=self.limpiar, bg="#64748b", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", padx=10, cursor="hand2").grid(row=0, column=5, padx=5)

        # --- ETIQUETA DE ESTADO ---
        self.lbl_estado = tk.Label(root, text="Estado: Pila vacía (Tope = -1)", bg="#f0f9ff", fg="#0284c7", font=("Segoe UI", 11, "bold"))
        self.lbl_estado.pack(pady=5)

        # --- LIENZO GRÁFICO (CANVAS) ---
        self.canvas = tk.Canvas(root, width=610, height=400, bg="#ffffff", bd=1, relief="solid", highlightthickness=0)
        self.canvas.pack(padx=20, pady=10)

        self.dibujar_pila()

    # ==========================================
    # OPERACIONES LÓGICAS DE LA PILA
    # ==========================================
    def push(self):
        valor = self.entrada_valor.get().strip()
        if not valor:
            messagebox.showwarning("Campo vacío", "Por favor ingresa un valor para apilar.")
            return

        if len(self.pila) >= self.capacidad_maxima:
            messagebox.showerror("Stack Overflow (Desbordamiento)", f"La pila ha alcanzado su capacidad máxima ({self.capacidad_maxima} elementos).")
            return

        # Insertar al final de la lista (representa el Tope)
        self.pila.append(valor)
        self.entrada_valor.delete(0, tk.END)
        self.lbl_estado.config(text=f"Push('{valor}') realizado | Elementos: {len(self.pila)} | Índice Tope: {len(self.pila)-1}", fg="#059669")
        self.dibujar_pila()

    def pop(self):
        if not self.pila:
            messagebox.showerror("Stack Underflow (Subdesbordamiento)", "La pila está vacía. No hay elementos para eliminar.")
            return

        # Extraer el último elemento ingresado (LIFO)
        valor_eliminado = self.pila.pop()
        tope_actual = len(self.pila) - 1
        texto_tope = f"Índice Tope: {tope_actual}" if tope_actual >= 0 else "Pila vacía (Tope = -1)"
        
        self.lbl_estado.config(text=f"Pop() -> Se eliminó '{valor_eliminado}' | {texto_tope}", fg="#dc2626")
        self.dibujar_pila()

    def peek(self):
        if not self.pila:
            messagebox.showinfo("Peek (Cima)", "La pila está vacía (Tope = None).")
            return

        valor_tope = self.pila[-1]
        self.lbl_estado.config(text=f"Peek() -> El elemento en el Tope es '{valor_tope}' (Índice {len(self.pila)-1})", fg="#d97706")
        # Redibujar resaltando el tope en color dorado
        self.dibujar_pila(resaltar_tope=True)

    def limpiar(self):
        self.pila.clear()
        self.lbl_estado.config(text="Estado: Pila vaciada correctamente (Tope = -1)", fg="#64748b")
        self.dibujar_pila()

    # ==========================================
    # RENDERIZADO GRÁFICO EN EL LIENZO
    # ==========================================
    def dibujar_pila(self, resaltar_tope=False):
        self.canvas.delete("all")

        # Coordenadas del contenedor de la pila ("pozo")
        x_izq = 220
        x_der = 390
        y_base = 360
        y_techo = 45
        alto_bloque = 40

        # Dibujar paredes y base del contenedor de la Pila
        self.canvas.create_line(x_izq, y_techo, x_izq, y_base, width=4, fill="#334155") # Pared izquierda
        self.canvas.create_line(x_der, y_techo, x_der, y_base, width=4, fill="#334155") # Pared derecha
        self.canvas.create_line(x_izq - 2, y_base, x_der + 2, y_base, width=6, fill="#334155") # Base inferior
        self.canvas.create_text(305, 380, text="BASE DE LA PILA (Índice 0)", font=("Segoe UI", 9, "bold"), fill="#64748b")

        # Dibujar cada elemento apilado de abajo hacia arriba
        for i, valor in enumerate(self.pila):
            y_inf = y_base - (i * (alto_bloque + 4)) - 4
            y_sup = y_inf - alto_bloque

            es_tope = (i == len(self.pila) - 1)

            # Selección de color: Naranja si se presionó Peek, Azul intenso si es el Tope, Azul claro para el resto
            if es_tope and resaltar_tope:
                color_bloque = "#f59e0b"
            elif es_tope:
                color_bloque = "#0284c7"
            else:
                color_bloque = "#38bdf8"

            # Dibujar el rectángulo del nodo
            self.canvas.create_rectangle(x_izq + 8, y_sup, x_der - 8, y_inf, fill=color_bloque, outline="#0369a1", width=2)
            
            # Texto con el dato dentro del bloque
            self.canvas.create_text((x_izq + x_der) // 2, (y_sup + y_inf) // 2, text=str(valor), font=("Segoe UI", 11, "bold"), fill="white")
            
            # Índice a la izquierda del contenedor
            self.canvas.create_text(x_izq - 25, (y_sup + y_inf) // 2, text=f"[{i}]", font=("Consolas", 10, "bold"), fill="#475569")

            # Indicador de puntero TOPE a la derecha del último elemento
            if es_tope:
                y_centro = (y_sup + y_inf) // 2
                self.canvas.create_line(x_der + 15, y_centro, x_der + 55, y_centro, arrow=tk.FIRST, width=3, fill="#ef4444")
                self.canvas.create_text(x_der + 95, y_centro, text="TOPE (TOP)", font=("Segoe UI", 10, "bold"), fill="#ef4444")

if __name__ == "__main__":
    ventana = tk.Tk()
    app = SimuladorPila(ventana)
    ventana.mainloop()

import tkinter as tk
import serial
import threading
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Rectangle

class SerialInterface:
    def __init__(self):
        self.serial_port = serial.Serial('COM3', 9600)  # Cambiar 'COM3' por el puerto serial correcto
        self.thread = threading.Thread(target=self.serial_listener)
        self.thread.daemon = True
        self.thread.start()

    def send_command(self, command):
        self.serial_port.write(command.encode())

    def serial_listener(self):
        while True:
            if self.serial_port.in_waiting > 0:
                data = self.serial_port.readline().decode().strip()
                print("Valor del potenciómetro:", data)

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.x = 0
        self.y = 0

class BinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        if self.root is None:
            self.root = TreeNode(value)
        else:
            self._insert_recursive(self.root, value, x=100, y=10, distance=200)

    def _insert_recursive(self, node, value, x, y, distance):
        if value < node.value:
            if node.left is None:
                node.left = TreeNode(value)
                node.left.x = x - distance
                node.left.y = y + 100
            else:
                self._insert_recursive(node.left, value, x - distance, y + 100, distance / 2)
        elif value > node.value:
            if node.right is None:
                node.right = TreeNode(value)
                node.right.x = x + distance
                node.right.y = y + 100
            else:
                self._insert_recursive(node.right, value, x + distance, y + 100, distance / 2)

    def traverse_preorder(self, node, canvas, x_offset, y_offset):
        if node:
            canvas.create_oval(node.x - 15 + x_offset, node.y - 15 + y_offset, node.x + 15 + x_offset, node.y + 15 + y_offset, fill="black")
            canvas.create_text(node.x + x_offset, node.y + y_offset, text=str(node.value), fill="white")
            if node.left:
                canvas.create_line(node.x + x_offset, node.y + y_offset, node.left.x + x_offset, node.left.y + y_offset, fill="black")
            if node.right:
                canvas.create_line(node.x + x_offset, node.y + y_offset, node.right.x + x_offset, node.right.y + y_offset, fill="black")
            self.traverse_preorder(node.left, canvas, x_offset, y_offset)
            self.traverse_preorder(node.right, canvas, x_offset, y_offset)

class Application(tk.Tk):
    def __init__(self, serial_interface):
        super().__init__()

        self.serial_interface = serial_interface
        self.binary_tree = BinaryTree()

        self.title("Control de Árboles Binarios")
        self.geometry("1000x700")

        self.canvas = tk.Canvas(self, bg="white", width=500, height=700)
        self.canvas.pack(side="left")

        self.create_widgets()
        self.visualize_potentiometer()

    def create_widgets(self):
        button_a = tk.Button(self, text="Arbol Preorden", command=lambda: self.create_tree("A"))
        button_a.pack(pady=5)

        button_b = tk.Button(self, text="Arbol Inorden", command=lambda: self.create_tree("B"))
        button_b.pack(pady=5)

        button_c = tk.Button(self, text="Arbol Postorden", command=lambda: self.create_tree("C"))
        button_c.pack(pady=5)

    def create_tree(self, tree_type):
        # Creamos una nueva ventana para la gráfica del árbol
        tree_window = tk.Toplevel(self)
        tree_window.title(f"Árbol {tree_type}")

        # Creamos un lienzo en la nueva ventana para la gráfica del árbol
        tree_canvas = tk.Canvas(tree_window, bg="white", width=1000, height=700)
        tree_canvas.pack()

        tree_canvas.delete("all")  # Borra cualquier dibujo anterior en el lienzo

        self.binary_tree.root = None  # Restablece el árbol binario

        if tree_type == "A":
            self.binary_tree.insert(1)
            self.binary_tree.insert(2)
            self.binary_tree.insert(3)
            self.serial_interface.send_command("A")
        elif tree_type == "B":
            self.binary_tree.insert(4)
            self.binary_tree.insert(5)
            self.binary_tree.insert(6)
            self.serial_interface.send_command("B")
        elif tree_type == "C":
            self.binary_tree.insert(7)
            self.binary_tree.insert(8)
            self.binary_tree.insert(9)
            self.serial_interface.send_command("C")

        # Calcular el desplazamiento necesario para centrar el árbol
        x_offset = (500 - self.binary_tree.root.x) // 2
        y_offset = (700 - self.binary_tree.root.y) // 2

        self.binary_tree.traverse_preorder(self.binary_tree.root, tree_canvas, x_offset, y_offset)

    def visualize_potentiometer(self):
        # Configurar el puerto serial (ajusta el puerto según tu sistema)
        # Crear la figura y el eje para la visualización
        fig = Figure(figsize=(5, 7), dpi=100)
        ax = fig.add_subplot(111)
        ax.set_xlim(0, 10)  # Establecer límites del eje x
        ax.set_ylim(0, 0.2)  # Establecer límites del eje y para la barra (más pequeño)

        # Barra inicial
        bar = Rectangle((0, 0), 0, 0.2, facecolor='blue', alpha=0.7)  # Tamaño inicial más pequeño
        ax.add_patch(bar)

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side="right", fill="both", expand=True)

        # Función para actualizar el tamaño de la barra según el valor del potenciómetro
        def update_plot(value):
            try:
                # Escalar el valor del potenciómetro a un tamaño entre 0 y 1
                size = float(value) / 1023  # Escalar a 1 en lugar de 10
                # Actualizar el ancho de la barra
                bar.set_width(size * 10)  # Escalar nuevamente a 10
                fig.canvas.draw()
            except ValueError:
                print(f"Valor no válido recibido: {value}")

        # Función principal para recibir datos del puerto serial
        def main():
            while True:
                if self.serial_interface.serial_port.in_waiting > 0:  # Usar self.serial_interface.serial_port
                    # Leer valor del potenciómetro desde Arduino
                    try:
                        pot_value = self.serial_interface.serial_port.readline().decode().strip()  # Usar self.serial_interface.serial_port
                        update_plot(pot_value)
                    except UnicodeDecodeError:
                        print("Error al decodificar los datos recibidos.")

        # Ejecutar la función principal en un hilo
        thread = threading.Thread(target=main)
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    serial_interface = SerialInterface()
    app = Application(serial_interface)
    app.mainloop()
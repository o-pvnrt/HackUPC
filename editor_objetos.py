import customtkinter as ctk
from tkinter import simpledialog, messagebox
import pandas as pd

# Dictionary of predefined objects
OBJETOS_DISPONIBLES = {
    "Motor": {"masa": 5.0, "potencia": 100},
    "Sensor": {"masa": 1.0, "precisión": 0.01},
    "Caja": {"masa": 2.0, "material": "madera"}
}

class Objeto:
    def __init__(self, tipo, x, y, atributos):
        self.tipo = tipo
        self.x = x
        self.y = y
        self.atributos = atributos.copy()
        self.id_canvas = None

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("2D Object Editor with Grid")
        self.geometry("900x700")
        ctk.set_appearance_mode("System")  # Options: "System", "Dark", "Light"
        ctk.set_default_color_theme("blue")  # Options: "blue", "green", "dark-blue"

        # Variables
        self.objetos = []
        self.objeto_actual = ctk.StringVar(value="Motor")
        self.seleccionado = None
        self.dx = self.dy = 0
        self.tool = "create"  # Default tool
        self.grid_size = 50  # Size of each grid cell

        # Layout
        self.create_toolbars()
        self.create_canvas()

    def create_toolbars(self):
        """Create the toolbars."""
        # Tool selection toolbar at the top
        tool_frame = ctk.CTkFrame(self)
        tool_frame.pack(side="top", fill="x", padx=5, pady=5)

        # Add tool buttons
        for tool in ["Create Figure", "Drag", "Select"]:
            ctk.CTkButton(tool_frame, text=tool, command=lambda t=tool.lower().replace(" ", "_"): self.select_tool(t)).pack(side="left", padx=5, pady=5)

        # Add grid size input
        ctk.CTkLabel(tool_frame, text="Grid Size:").pack(side="left", padx=5, pady=5)
        self.grid_size_entry = ctk.CTkEntry(tool_frame, width=50)
        self.grid_size_entry.insert(0, str(self.grid_size))  # Set default value
        self.grid_size_entry.pack(side="left", padx=5, pady=5)
        self.grid_size_entry.bind("<Return>", self.update_grid_size)  # Bind Enter key to update grid size

        # Add light/dark mode switch
        mode_switch = ctk.CTkSwitch(tool_frame, text="Switch Color Mode", command=self.toggle_mode)
        mode_switch.pack(side="right", padx=5, pady=5)

        # Add button to open the create menu
        ctk.CTkButton(tool_frame, text="New Object", command=self.open_create_menu).pack(side="right", padx=5, pady=5)

        # Object selection and export toolbar on the right
        object_frame = ctk.CTkFrame(self)
        object_frame.pack(side="right", fill="y", padx=5, pady=5)
        ctk.CTkLabel(object_frame, text="Object:").pack(pady=5)
        ctk.CTkOptionMenu(object_frame, variable=self.objeto_actual, values=list(OBJETOS_DISPONIBLES.keys())).pack(pady=5)
        ctk.CTkButton(object_frame, text="Export to Excel", command=self.export_to_excel).pack(pady=5)

    def toggle_mode(self):
        """Toggle between light and dark mode."""
        current_mode = ctk.get_appearance_mode()
        new_mode = "Light" if current_mode == "Dark" else "Dark"
        ctk.set_appearance_mode(new_mode)

        # Change canvas background color based on mode
        canvas_bg = "white" if new_mode == "Light" else "black"
        self.canvas.configure(bg=canvas_bg)
        self.draw_grid()  # Redraw the grid to match the new background

    def create_canvas(self):
        """Create the drawing canvas with a grid."""
        self.canvas = ctk.CTkCanvas(self, bg="white")
        self.canvas.pack(fill="both", expand=True, padx=5, pady=5)
        self.canvas.bind("<Configure>", self.on_canvas_resize)  # Handle resizing
        self.canvas.bind("<Button-1>", self.on_click)  # Left-click for selecting/placing
        self.canvas.bind("<Button-3>", self.delete_object)  # Right-click for deleting
        self.canvas.bind("<Double-Button-1>", self.edit_object)  # Double-click for editing
        self.canvas.bind("<B1-Motion>", self.on_drag)  # Dragging
        self.canvas.bind("<ButtonRelease-1>", self.release)  # Release after dragging
        self.draw_grid()

    def draw_grid(self):
        """Draw a grid on the canvas."""
        self.canvas.delete("grid_line")  # Clear existing grid lines
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        for x in range(0, width, self.grid_size):
            self.canvas.create_line(x, 0, x, height, fill="lightgray", tags="grid_line")
        for y in range(0, height, self.grid_size):
            self.canvas.create_line(0, y, width, y, fill="lightgray", tags="grid_line")

    def on_canvas_resize(self, event):
        """Redraw the grid when the canvas is resized."""
        self.draw_grid()

    def snap_to_grid(self, x, y):
        """Snap coordinates to the nearest grid point."""
        snapped_x = round(x / self.grid_size) * self.grid_size
        snapped_y = round(y / self.grid_size) * self.grid_size
        return snapped_x, snapped_y

    def select_tool(self, tool):
        """Set the current tool."""
        self.tool = tool

    def on_click(self, event):
        """Handle click events based on the selected tool."""
        if self.tool == "create_figure":
            self.place_object(event)
        elif self.tool == "select":
            self.select_object(event)

    def on_drag(self, event):
        """Handle drag events."""
        if self.tool == "drag":
            self.drag(event)

    def place_object(self, event):
        """Place a new object on the canvas."""
        obj_type = self.objeto_actual.get()
        attributes = OBJETOS_DISPONIBLES[obj_type]
        snapped_x, snapped_y = self.snap_to_grid(event.x, event.y)
        obj = Objeto(obj_type, snapped_x, snapped_y, attributes)

        r = 25  # Half the side length of the square
        color = {"Motor": "red", "Sensor": "blue", "Caja": "green"}.get(obj_type, "gray")
        id_canvas = self.canvas.create_rectangle(snapped_x - r, snapped_y - r, snapped_x + r, snapped_y + r, fill=color)
        text_id = self.canvas.create_text(snapped_x, snapped_y, text=obj_type, fill="white")

        obj.id_canvas = (id_canvas, text_id)
        self.objetos.append(obj)

    def select_object(self, event):
        """Select an object by clicking on it."""
        closest = self.canvas.find_closest(event.x, event.y)[0]
        obj = self.get_object_by_id(closest)
        if obj:
            messagebox.showinfo("Object Selected", f"Type: {obj.tipo}\nPosition: ({obj.x}, {obj.y})\nAttributes: {obj.atributos}")

    def drag(self, event):
        """Drag an object."""
        if self.seleccionado is None:
            # Find the closest object to the mouse pointer
            closest = self.canvas.find_closest(event.x, event.y)[0]
            obj = self.get_object_by_id(closest)
            if not obj:
                return

            # Select the object and calculate the initial offset
            self.seleccionado = obj
            self.dx = event.x - obj.x
            self.dy = event.y - obj.y

        # Calculate the new position dynamically without snapping
        new_x = event.x - self.dx
        new_y = event.y - self.dy

        # Update the object's position
        self.seleccionado.x = new_x
        self.seleccionado.y = new_y
        r = 25
        self.canvas.coords(self.seleccionado.id_canvas[0], new_x - r, new_y - r, new_x + r, new_y + r)
        self.canvas.coords(self.seleccionado.id_canvas[1], new_x, new_y)

    def release(self, event):
        """Snap the selected object to the grid when released."""
        if self.seleccionado:
            # Snap to the nearest grid point
            snapped_x, snapped_y = self.snap_to_grid(self.seleccionado.x, self.seleccionado.y)
            self.seleccionado.x = snapped_x
            self.seleccionado.y = snapped_y
            r = 25
            self.canvas.coords(self.seleccionado.id_canvas[0], snapped_x - r, snapped_y - r, snapped_x + r, snapped_y + r)
            self.canvas.coords(self.seleccionado.id_canvas[1], snapped_x, snapped_y)

        # Deselect the object
        self.seleccionado = None

    def get_object_by_id(self, canvas_id):
        """Find an object by its canvas ID."""
        for obj in self.objetos:
            if canvas_id in obj.id_canvas:
                return obj
        return None

    def edit_object(self, event):
        """Edit an object's attributes."""
        closest = self.canvas.find_closest(event.x, event.y)[0]
        obj = self.get_object_by_id(closest)
        if not obj:
            return
        for k, v in obj.atributos.items():
            new_value = simpledialog.askstring("Edit Attribute", f"{k} ({v}):")
            if new_value:
                try:
                    obj.atributos[k] = type(v)(new_value)
                except ValueError:
                    messagebox.showerror("Error", f"Invalid type for '{k}'")

    def export_to_excel(self):
        """Export object data to an Excel file."""
        data = [{"Type": obj.tipo, "X": obj.x, "Y": obj.y, **obj.atributos} for obj in self.objetos]
        df = pd.DataFrame(data)
        file_path = simpledialog.askstring("Export to Excel", "Enter file name (e.g., objects.xlsx):")
        if file_path:
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Export Successful", f"Data exported to {file_path}")

    def update_grid_size(self, event=None):
        """Update the grid size based on user input."""
        try:
            new_size = int(self.grid_size_entry.get())
            if new_size > 0:
                self.grid_size = new_size
                self.draw_grid()  # Redraw the grid with the new size

                # Snap all objects to the nearest grid corner
                for obj in self.objetos:
                    snapped_x, snapped_y = self.snap_to_grid(obj.x, obj.y)
                    obj.x = snapped_x
                    obj.y = snapped_y
                    r = 25  # Half the side length of the square
                    self.canvas.coords(obj.id_canvas[0], snapped_x - r, snapped_y - r, snapped_x + r, snapped_y + r)
                    self.canvas.coords(obj.id_canvas[1], snapped_x, snapped_y)
            else:
                messagebox.showerror("Invalid Input", "Grid size must be a positive integer.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid integer for the grid size.")

    def open_create_menu(self):
        """Open a menu to create a new object."""
        if hasattr(self, "create_menu_window") and self.create_menu_window is not None and self.create_menu_window.winfo_exists():
            # If the window already exists, bring it to the front
            self.create_menu_window.lift()
            return

        # Create the new window
        self.create_menu_window = ctk.CTkToplevel(self)
        self.create_menu_window.title("Create New Object")
        self.create_menu_window.geometry("400x400")

        # Position the window to the right-hand side of the program window
        main_x = self.winfo_rootx()  # Get the absolute x-coordinate of the main window
        main_y = self.winfo_rooty()  # Get the absolute y-coordinate of the main window
        main_width = self.winfo_width()  # Get the width of the main window
        screen_width = self.winfo_screenwidth()  # Get the width of the screen

        # Ensure the new window doesn't go off-screen
        new_x = min(main_x + main_width + 10, screen_width - 400)  # 400 is the width of the new window
        self.create_menu_window.geometry(f"+{new_x}+{main_y}")

        # Make the window modal
        self.create_menu_window.transient(self)
        self.create_menu_window.grab_set()

        ctk.CTkLabel(self.create_menu_window, text="Object Name:").pack(pady=5)
        nombre = ctk.StringVar()
        ctk.CTkEntry(self.create_menu_window, textvariable=nombre).pack(pady=5)

        ctk.CTkLabel(self.create_menu_window, text="Size X:").pack(pady=5)
        size_x = ctk.StringVar(value="50")
        ctk.CTkEntry(self.create_menu_window, textvariable=size_x).pack(pady=5)

        ctk.CTkLabel(self.create_menu_window, text="Size Y:").pack(pady=5)
        size_y = ctk.StringVar(value="50")
        ctk.CTkEntry(self.create_menu_window, textvariable=size_y).pack(pady=5)

        propiedades_frame = ctk.CTkFrame(self.create_menu_window)
        propiedades_frame.pack(fill="both", expand=True, pady=10)

        ctk.CTkLabel(propiedades_frame, text="New Properties:").pack(pady=5)
        propiedades = []

        def agregar_propiedad():
            """Add a new property to the object."""
            prop_frame = ctk.CTkFrame(propiedades_frame)
            prop_frame.pack(fill="x", pady=5)

            prop_nombre = ctk.StringVar()
            prop_valor = ctk.StringVar()

            ctk.CTkEntry(prop_frame, textvariable=prop_nombre, placeholder_text="Name").pack(side="left", padx=5)
            ctk.CTkEntry(prop_frame, textvariable=prop_valor, placeholder_text="Value").pack(side="left", padx=5)

            def eliminar_propiedad():
                """Remove the current property."""
                propiedades.remove((prop_nombre, prop_valor))
                prop_frame.destroy()

            ctk.CTkButton(prop_frame, text="X", command=eliminar_propiedad, width=20).pack(side="left", padx=5)
            propiedades.append((prop_nombre, prop_valor))

        ctk.CTkButton(self.create_menu_window, text="Add Property", command=agregar_propiedad).pack(pady=5)

        def crear_objeto():
            """Create a new object with the entered properties."""
            nuevo_objeto = {
                "size_x": int(size_x.get()),
                "size_y": int(size_y.get())
            }
            for prop_nombre, prop_valor in propiedades:
                if prop_nombre.get() and prop_valor.get():
                    nuevo_objeto[prop_nombre.get()] = prop_valor.get()

            OBJETOS_DISPONIBLES[nombre.get()] = nuevo_objeto
            self.objeto_actual.set(nombre.get())
            self.create_menu_window.destroy()
            self.create_menu_window = None  # Reset the reference

        ctk.CTkButton(self.create_menu_window, text="Create Object", command=crear_objeto).pack(pady=10)

        # Handle window close event
        def on_close():
            self.create_menu_window.destroy()
            self.create_menu_window = None

        self.create_menu_window.protocol("WM_DELETE_WINDOW", on_close)

    def delete_object(self, event):
        """Delete an object from the canvas."""
        closest = self.canvas.find_closest(event.x, event.y)[0]
        obj = self.get_object_by_id(closest)
        if obj:
            # Delete the object's graphical elements from the canvas
            self.canvas.delete(obj.id_canvas[0])
            self.canvas.delete(obj.id_canvas[1])
            # Remove the object from the list of objects
            self.objetos.remove(obj)

if __name__ == "__main__":
    app = App()
    app.mainloop()
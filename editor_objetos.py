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
        
        # Cable variables
        self.cable_type = None  # Current selected cable type
        self.start_point = None  # Starting point for cable
        self.start_object = None  # Starting object for cable
        self.cables = []  # List to store all cables
        self.is_input_start = None  # Flag to track if we started from input
        self.current_cable_points = []  # Points for the cable being created
        self.current_cable_segments = []  # Canvas IDs for temporary cable segments
        self.temp_point = None  # For preview line
        self.last_click_point = None  # Last clicked point for cable routing

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
            ctk.CTkButton(tool_frame, text=tool, 
                         command=lambda t=tool.lower().replace(" ", "_"): self.select_tool(t)
                         ).pack(side="left", padx=5, pady=5)

        # Add grid size input
        ctk.CTkLabel(tool_frame, text="Grid Size:").pack(side="left", padx=5, pady=5)
        self.grid_size_entry = ctk.CTkEntry(tool_frame, width=50)
        self.grid_size_entry.insert(0, str(self.grid_size))
        self.grid_size_entry.pack(side="left", padx=5, pady=5)
        self.grid_size_entry.bind("<Return>", self.update_grid_size)

        # Add light/dark mode switch
        mode_switch = ctk.CTkSwitch(tool_frame, text="Dark Mode", command=self.toggle_mode)
        mode_switch.pack(side="right", padx=5, pady=5)

        # Object selection and export toolbar on the right
        object_frame = ctk.CTkFrame(self)
        object_frame.pack(side="right", fill="y", padx=5, pady=5)
        
        # Object selection section
        ctk.CTkLabel(object_frame, text="Object:").pack(pady=5)
        self.object_menu = ctk.CTkOptionMenu(object_frame, 
                                           variable=self.objeto_actual, 
                                           values=list(OBJETOS_DISPONIBLES.keys()))
        self.object_menu.pack(pady=5)
        
        # Object management buttons
        ctk.CTkButton(object_frame, text="New Object", 
                     command=self.open_create_menu).pack(pady=5)
        ctk.CTkButton(object_frame, text="Export to CSV", 
                     command=self.export_to_csv).pack(pady=5)
        
        # Cable section
        ctk.CTkLabel(object_frame, text="Cables:").pack(pady=(20,5))
        
        # Water cable (blue)
        ctk.CTkButton(object_frame, text="Water", fg_color="blue",
                     command=lambda: self.select_cable("water"),
                     width=120).pack(pady=2)
        
        # Electric cable (red)
        ctk.CTkButton(object_frame, text="Electric", fg_color="red",
                     command=lambda: self.select_cable("electric"),
                     width=120).pack(pady=2)
        
        # Data cable (black)
        ctk.CTkButton(object_frame, text="Data", fg_color="black",
                     command=lambda: self.select_cable("data"),
                     width=120).pack(pady=2)
                     
        # Delete cable button con icono de goma
        ctk.CTkButton(object_frame, text="🧽", fg_color="gray",
                     command=lambda: self.select_tool("delete_cable"),
                     width=120).pack(pady=(10,2))

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

        # Ensure all figures are above the grid
        self.canvas.tag_raise("figure")

    def on_canvas_resize(self, event):
        """Redraw the grid when the canvas is resized."""
        self.draw_grid()

    def select_tool(self, tool):
        self.tool = tool
        if tool == "delete_cable":
            self.cleanup_cable_preview()
            self.cable_type = None
            self.canvas.config(cursor="circle")  # 'circle' es lo más parecido a una goma en Tkinter
        else:
            self.canvas.config(cursor="")

    def on_click(self, event):
        """Handle click events based on the selected tool."""
        if self.tool == "create_figure":
            self.place_object(event)
        elif self.tool == "select":
            self.select_object(event)
        elif self.tool == "cable":
            self.handle_cable_click(event)
        elif self.tool == "delete_cable":
            self.delete_cable_click(event)

    def on_drag(self, event):
        """Handle drag events."""
        if self.tool == "drag":
            self.drag(event)

    def place_object(self, event):
        """Place a new object on the canvas."""
        obj_type = self.objeto_actual.get()
        attributes = OBJETOS_DISPONIBLES[obj_type]
        # Place at exact coordinates, not snapped
        x, y = event.x, event.y
        obj = Objeto(obj_type, x, y, attributes)

        size_x = attributes.get("size_x", 100)
        size_y = attributes.get("size_y", 100)
        inputs = attributes.get("inputs", 0)
        outputs = attributes.get("outputs", 0)

        # Draw the main shape (rectangle)
        color = {"Motor": "red", "Sensor": "blue", "Caja": "green"}.get(obj_type, "gray")
        id_canvas = [self.canvas.create_rectangle(
            x - size_x // 2, y - size_y // 2,
            x + size_x // 2, y + size_y // 2,
            fill=color, tags="figure"
        )]
        text_id = self.canvas.create_text(x, y, text=obj_type, fill="white", tags="figure")
        id_canvas.append(text_id)

        # Draw inputs as small circles on the left edge
        for i in range(inputs):
            input_y = y - size_y // 2 + (i + 1) * size_y // (inputs + 1)
            input_id = self.canvas.create_oval(
                x - size_x // 2 - 5, input_y - 5,
                x - size_x // 2 + 5, input_y + 5,
                fill="black", tags="figure"
            )
            id_canvas.append(input_id)

        # Draw outputs as small circles on the right edge
        for i in range(outputs):
            output_y = y - size_y // 2 + (i + 1) * size_y // (outputs + 1)
            output_id = self.canvas.create_oval(
                x + size_x // 2 - 5, output_y - 5,
                x + size_x // 2 + 5, output_y + 5,
                fill="black", tags="figure"
            )
            id_canvas.append(output_id)

        obj.id_canvas = id_canvas
        self.objetos.append(obj)

        # Ensure the figure is above the grid
        self.canvas.tag_raise("figure")

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

        # Get the object's attributes
        attributes = self.seleccionado.atributos
        size_x = attributes.get("size_x", 100)
        size_y = attributes.get("size_y", 100)
        inputs = attributes.get("inputs", 0)
        outputs = attributes.get("outputs", 0)

        # Update the main shape (rectangle)
        self.canvas.coords(
            self.seleccionado.id_canvas[0],
            new_x - size_x // 2, new_y - size_y // 2,
            new_x + size_x // 2, new_y + size_y // 2
        )

        # Update the text position
        self.canvas.coords(self.seleccionado.id_canvas[1], new_x, new_y)

        # Update the positions of inputs
        for i in range(inputs):
            input_y = new_y - size_y // 2 + (i + 1) * size_y // (inputs + 1)
            self.canvas.coords(
                self.seleccionado.id_canvas[2 + i],
                new_x - size_x // 2 - 5, input_y - 5,
                new_x - size_x // 2 + 5, input_y + 5
            )

        # Update the positions of outputs
        for i in range(outputs):
            output_y = new_y - size_y // 2 + (i + 1) * size_y // (outputs + 1)
            self.canvas.coords(
                self.seleccionado.id_canvas[2 + inputs + i],
                new_x + size_x // 2 - 5, output_y - 5,
                new_x + size_x // 2 + 5, output_y + 5
            )

    def release(self, event):
        """Release the selected object without snapping to grid."""
        if self.seleccionado:
            # Use the current position, do not snap
            x, y = self.seleccionado.x, self.seleccionado.y

            # Get the object's attributes
            attributes = self.seleccionado.atributos
            size_x = attributes.get("size_x", 100)
            size_y = attributes.get("size_y", 100)
            inputs = attributes.get("inputs", 0)
            outputs = attributes.get("outputs", 0)

            # Update the main shape (rectangle)
            self.canvas.coords(
                self.seleccionado.id_canvas[0],
                x - size_x // 2, y - size_y // 2,
                x + size_x // 2, y + size_y // 2
            )

            # Update the text position
            self.canvas.coords(self.seleccionado.id_canvas[1], x, y)

            # Update the positions of inputs
            for i in range(inputs):
                input_y = y - size_y // 2 + (i + 1) * size_y // (inputs + 1)
                self.canvas.coords(
                    self.seleccionado.id_canvas[2 + i],
                    x - size_x // 2 - 5, input_y - 5,
                    x - size_x // 2 + 5, input_y + 5
                )

            # Update the positions of outputs
            for i in range(outputs):
                output_y = y - size_y // 2 + (i + 1) * size_y // (outputs + 1)
                self.canvas.coords(
                    self.seleccionado.id_canvas[2 + inputs + i],
                    x + size_x // 2 - 5, output_y - 5,
                    x + size_x // 2 + 5, output_y + 5
                )

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

    def export_to_csv(self):
        """Export object data to a CSV file."""
        data = [{"Type": obj.tipo, "X": obj.x, "Y": obj.y, **obj.atributos} for obj in self.objetos]
        df = pd.DataFrame(data)
        file_name = simpledialog.askstring("Export to CSV", "Enter file name (without extension):")
        if file_name:
            file_path = f"{file_name}.csv"  # Automatically add .csv extension
            df.to_csv(file_path, index=False)
            messagebox.showinfo("Export Successful", f"Data exported to {file_path}")

    def update_grid_size(self, event=None):
        """Update the grid size based on user input."""
        try:
            new_size = int(self.grid_size_entry.get())
            if new_size > 0:
                self.grid_size = new_size
                self.draw_grid()  # Redraw the grid with the new size
            else:
                messagebox.showerror("Invalid Input", "Grid size must be a positive integer.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid integer for the grid size.")

    def open_create_menu(self):
        """Open a menu to create a new object with inputs and outputs."""
        if hasattr(self, "create_menu_window") and self.create_menu_window is not None and self.create_menu_window.winfo_exists():
            # If the window already exists, bring it to the front
            self.create_menu_window.lift()
            return

        # Create the new window
        self.create_menu_window = ctk.CTkToplevel(self)
        self.create_menu_window.title("Create New Object")
        self.create_menu_window.geometry("400x600")

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
        size_x = ctk.StringVar(value="100")
        ctk.CTkEntry(self.create_menu_window, textvariable=size_x).pack(pady=5)

        ctk.CTkLabel(self.create_menu_window, text="Size Y:").pack(pady=5)
        size_y = ctk.StringVar(value="100")
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

        # Inputs and Outputs Section
        io_frame = ctk.CTkFrame(self.create_menu_window)
        io_frame.pack(fill="both", expand=True, pady=10)

        ctk.CTkLabel(io_frame, text="Inputs and Outputs:").pack(pady=5)

        inputs = ctk.StringVar(value="0")
        outputs = ctk.StringVar(value="0")

        ctk.CTkLabel(io_frame, text="Number of Inputs:").pack(pady=5)
        ctk.CTkEntry(io_frame, textvariable=inputs).pack(pady=5)

        ctk.CTkLabel(io_frame, text="Number of Outputs:").pack(pady=5)
        ctk.CTkEntry(io_frame, textvariable=outputs).pack(pady=5)

        def crear_objeto():
            """Create a new object with the entered properties, inputs, and outputs."""
            if not nombre.get():
                messagebox.showerror("Error", "Object name cannot be empty.")
                return

            try:
                nuevo_objeto = {
                    "size_x": int(size_x.get()),
                    "size_y": int(size_y.get()),
                    "inputs": int(inputs.get()),
                    "outputs": int(outputs.get())
                }
                for prop_nombre, prop_valor in propiedades:
                    if prop_nombre.get() and prop_valor.get():
                        nuevo_objeto[prop_nombre.get()] = prop_valor.get()

                # Add the new object to the predefined objects
                OBJETOS_DISPONIBLES[nombre.get()] = nuevo_objeto

                # Update the dropdown menu
                self.object_menu.configure(values=list(OBJETOS_DISPONIBLES.keys()))
                self.objeto_actual.set(nombre.get())

                self.create_menu_window.destroy()
                self.create_menu_window = None  # Reset the reference
            except ValueError:
                messagebox.showerror("Error", "Size X, Size Y, Inputs, and Outputs must be integers.")

        ctk.CTkButton(self.create_menu_window, text="Create Object", command=crear_objeto).pack(pady=10)

        # Handle window close event
        def on_close():
            self.create_menu_window.destroy()
            self.create_menu_window = None

        self.create_menu_window.protocol("WM_DELETE_WINDOW", on_close)

    def update_object_menu(self):
        """Update the object selection menu with the latest objects."""
        menu = self.nametowidget(self.objeto_actual._name)  # Access the OptionMenu widget
        menu.configure(values=list(OBJETOS_DISPONIBLES.keys()))

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

    def select_cable(self, cable_type):
        """Select a cable type for connection."""
        self.tool = "cable"
        self.cable_type = cable_type
        self.start_point = None
        self.start_object = None
        self.is_input_start = None

    def is_input_point(self, obj, x, y):
        """Check if the clicked point is near an input connection point."""
        if not obj:
            return False
        attributes = obj.atributos
        size_x = attributes.get("size_x", 100)
        size_y = attributes.get("size_y", 100)
        inputs = attributes.get("inputs", 0)
        
        # Check each input point with increased detection area
        for i in range(inputs):
            input_y = obj.y - size_y // 2 + (i + 1) * size_y // (inputs + 1)
            input_x = obj.x - size_x // 2
            if abs(x - input_x) < 15 and abs(y - input_y) < 15:  # Increased from 10 to 15
                return True
        return False

    def is_output_point(self, obj, x, y):
        """Check if the clicked point is near an output connection point."""
        if not obj:
            return False
        attributes = obj.atributos
        size_x = attributes.get("size_x", 100)
        size_y = attributes.get("size_y", 100)
        outputs = attributes.get("outputs", 0)
        
        # Check each output point with increased detection area
        for i in range(outputs):
            output_y = obj.y - size_y // 2 + (i + 1) * size_y // (outputs + 1)
            output_x = obj.x + size_x // 2
            if abs(x - output_x) < 15 and abs(y - output_y) < 15:  # Increased from 10 to 15
                return True
        return False

    def handle_cable_click(self, event):
        """Handle clicks when creating cables."""
        x, y = event.x, event.y
        
        closest = self.canvas.find_closest(event.x, event.y)[0]
        obj = self.get_object_by_id(closest)

        if not obj and not self.start_point:
            return

        # Cable colors and widths
        cable_colors = {
            "water": "blue",
            "electric": "red",
            "data": "black"
        }
        cable_width = 4

        # If this is the start of a cable
        if self.start_point is None:
            # Check if we clicked on a valid connection point
            is_input = self.is_input_point(obj, event.x, event.y)
            is_output = self.is_output_point(obj, event.x, event.y)
            
            if not (is_input or is_output):
                return
            
            # Check if there's already a connection at this point
            if self.check_existing_connection(obj, event.x, event.y, is_input):
                messagebox.showerror("Error", "There is already a connection at this point.")
                return
                
            self.start_point = (event.x, event.y)
            self.start_object = obj
            self.is_input_start = is_input
            self.current_cable_points = [self.start_point]
            self.last_click_point = (x, y)
            self._current_cable_segment_ids = []
            
            # Bind motion event for preview
            self.canvas.bind("<Motion>", self.update_cable_preview)
            
        else:
            # If we're in the middle of routing
            if not obj:
                # Add a new point to the cable
                self.current_cable_points.append((x, y))
                self.last_click_point = (x, y)
                
                # Draw permanent segment
                self.draw_cable_segment(
                    self.current_cable_points[-2],
                    self.current_cable_points[-1],
                    cable_colors[self.cable_type],
                    cable_width
                )
                return
                
            # If we clicked on an object, check if it's a valid endpoint
            is_input = self.is_input_point(obj, event.x, event.y)
            is_output = self.is_output_point(obj, event.x, event.y)
            
            # Check if trying to connect to the same object
            if obj == self.start_object:
                messagebox.showerror("Error", "Cannot connect an object to itself.")
                self.cleanup_cable_preview()
                return
            
            # Validate connection (input to output or output to input only)
            if (self.is_input_start and is_output) or (not self.is_input_start and is_input):
                # Check if there's already a connection at this point
                if self.check_existing_connection(obj, event.x, event.y, is_input):
                    messagebox.showerror("Error", "There is already a connection at this point.")
                    return
                
                # Add the final point
                end_point = (event.x, event.y)
                self.current_cable_points.append(end_point)
                
                # Draw all segments permanently
                for i in range(len(self.current_cable_points) - 1):
                    self.draw_cable_segment(
                        self.current_cable_points[i],
                        self.current_cable_points[i + 1],
                        cable_colors[self.cable_type],
                        cable_width
                    )
                
                # Store the cable information
                self.cables.append({
                    'type': self.cable_type,
                    'points': self.current_cable_points.copy(),
                    'start_obj': self.start_object,
                    'end_obj': obj,
                    'segment_ids': getattr(self, "_current_cable_segment_ids", [])
                })
                self._current_cable_segment_ids = []
                
            # Reset cable creation state
            self.cleanup_cable_preview()

    def update_cable_preview(self, event):
        """Update the preview line while routing a cable."""
        if not self.start_point or not self.last_click_point:
            return
            
        x, y = event.x, event.y
        
        # Check if we're hovering over a valid connection point
        closest = self.canvas.find_closest(event.x, event.y)[0]
        obj = self.get_object_by_id(closest)
        
        # Only check for valid connections if we're near an object
        if obj and closest in obj.id_canvas:  # Ensure we're actually over the object
            is_input = self.is_input_point(obj, event.x, event.y)
            is_output = self.is_output_point(obj, event.x, event.y)
            
            # If we started from input and found an output, or vice versa
            if ((self.is_input_start and is_output) or (not self.is_input_start and is_input)) and obj != self.start_object:
                # Complete the cable automatically
                end_point = (event.x, event.y)
                if abs(x - self.last_click_point[0]) > abs(y - self.last_click_point[1]):
                    # Horizontal then vertical
                    self.current_cable_points.extend([
                        (x, self.last_click_point[1]),
                        end_point
                    ])
                else:
                    # Vertical then horizontal
                    self.current_cable_points.extend([
                        (self.last_click_point[0], y),
                        end_point
                    ])
                
                cable_colors = {
                    "water": "blue",
                    "electric": "red",
                    "data": "black"
                }
                cable_width = 4
                
                # Draw all segments permanently
                for i in range(len(self.current_cable_points) - 1):
                    self.draw_cable_segment(
                        self.current_cable_points[i],
                        self.current_cable_points[i + 1],
                        cable_colors[self.cable_type],
                        cable_width
                    )
                
                # Store the cable information
                self.cables.append({
                    'type': self.cable_type,
                    'points': self.current_cable_points.copy(),
                    'start_obj': self.start_object,
                    'end_obj': obj,
                    'segment_ids': getattr(self, "_current_cable_segment_ids", [])
                })
                self._current_cable_segment_ids = []
                
                # Clean up and finish cable creation
                self.cleanup_cable_preview()
                return
        
        # Delete previous preview
        for segment_id in self.current_cable_segments:
            self.canvas.delete(segment_id)
        self.current_cable_segments = []
        
        # Calculate orthogonal segments
        last_x, last_y = self.last_click_point
        dx = x - last_x
        dy = y - last_y
        
        cable_colors = {
            "water": "blue",
            "electric": "red",
            "data": "black"
        }
        preview_width = 4
        
        # Draw preview segments
        if abs(dx) > abs(dy):
            # Draw horizontal first
            self.current_cable_segments.append(
                self.canvas.create_line(
                    last_x, last_y, x, last_y,
                    fill=cable_colors[self.cable_type],
                    width=preview_width,
                    dash=(5, 5)
                )
            )
            self.current_cable_segments.append(
                self.canvas.create_line(
                    x, last_y, x, y,
                    fill=cable_colors[self.cable_type],
                    width=preview_width,
                    dash=(5, 5)
                )
            )
        else:
            # Draw vertical first
            self.current_cable_segments.append(
                self.canvas.create_line(
                    last_x, last_y, last_x, y,
                    fill=cable_colors[self.cable_type],
                    width=preview_width,
                    dash=(5, 5)
                )
            )
            self.current_cable_segments.append(
                self.canvas.create_line(
                    last_x, y, x, y,
                    fill=cable_colors[self.cable_type],
                    width=preview_width,
                    dash=(5, 5)
                )
            )

    def draw_cable_segment(self, start, end, color, width):
        """Draw a permanent cable segment between two points."""
        start_x, start_y = start
        end_x, end_y = end
        
        # Calculate orthogonal segments
        dx = end_x - start_x
        dy = end_y - start_y
        
        segment_ids = []
        
        if abs(dx) > abs(dy):
            # Draw horizontal then vertical
            id1 = self.canvas.create_line(
                start_x, start_y, end_x, start_y,
                fill=color, width=width
            )
            id2 = self.canvas.create_line(
                end_x, start_y, end_x, end_y,
                fill=color, width=width
            )
            segment_ids.extend([id1, id2])
        else:
            # Draw vertical then horizontal
            id1 = self.canvas.create_line(
                start_x, start_y, start_x, end_y,
                fill=color, width=width
            )
            id2 = self.canvas.create_line(
                start_x, end_y, end_x, end_y,
                fill=color, width=width
            )
            segment_ids.extend([id1, id2])
        
        if not hasattr(self, "_current_cable_segment_ids"):
            self._current_cable_segment_ids = []
        self._current_cable_segment_ids.extend(segment_ids)

    def cleanup_cable_preview(self):
        """Clean up the cable preview and reset cable creation state."""
        # Delete preview segments
        for segment_id in self.current_cable_segments:
            self.canvas.delete(segment_id)
        
        # Unbind motion event
        self.canvas.unbind("<Motion>")
        
        # Reset cable creation state
        self.start_point = None
        self.start_object = None
        self.is_input_start = None
        self.current_cable_points = []
        self.current_cable_segments = []
        self.last_click_point = None

    def check_existing_connection(self, obj, x, y, is_input):
        """Check if there's already a connection at this point."""
        for cable in self.cables:
            if is_input:
                # Si estamos comprobando un input, verificar si este objeto es el final de algún cable
                if (cable['end_obj'] == obj and 
                    abs(cable['points'][-1][0] - x) < 15 and 
                    abs(cable['points'][-1][1] - y) < 15):
                    return True
            else:
                # Si estamos comprobando un output, verificar si este objeto es el inicio de algún cable
                if (cable['start_obj'] == obj and 
                    abs(cable['points'][0][0] - x) < 15 and 
                    abs(cable['points'][0][1] - y) < 15):
                    return True
        return False

    def delete_cable_click(self, event):
        """Handle clicks when deleting cables."""
        if self.tool != "delete_cable":
            return
            
        x, y = event.x, event.y
        
        # Buscar el cable más cercano al punto de click
        min_distance = float('inf')
        cable_to_delete = None
        
        for cable in self.cables[:]:  # Usar una copia de la lista para evitar problemas durante la iteración
            for i in range(len(cable['points']) - 1):
                start = cable['points'][i]
                end = cable['points'][i + 1]
                
                # Calcular la distancia del punto al segmento
                distance = self.point_to_line_segment(x, y, start[0], start[1], end[0], end[1])
                
                if distance < min_distance and distance < 15:  # Aumentado a 15 pixels de tolerancia
                    min_distance = distance
                    cable_to_delete = cable
        
        if cable_to_delete:
            # Borrar todos los segmentos del cable
            for seg_id in cable_to_delete.get('segment_ids', []):
                self.canvas.delete(seg_id)
            
            # Eliminar el cable de la lista
            self.cables.remove(cable_to_delete)

    def point_to_line_segment(self, px, py, x1, y1, x2, y2):
        """Calculate the shortest distance from a point to a line segment."""
        A = px - x1
        B = py - y1
        C = x2 - x1
        D = y2 - y1

        dot = A * C + B * D
        len_sq = C * C + D * D

        if len_sq == 0:
            # El punto está en el extremo del segmento
            return ((px - x1) ** 2 + (py - y1) ** 2) ** 0.5

        param = dot / len_sq

        if param < 0:
            # El punto más cercano está fuera del segmento, cerca del punto inicial
            return ((px - x1) ** 2 + (py - y1) ** 2) ** 0.5
        elif param > 1:
            # El punto más cercano está fuera del segmento, cerca del punto final
            return ((px - x2) ** 2 + (py - y2) ** 2) ** 0.5
        else:
            # El punto más cercano está dentro del segmento
            x = x1 + param * C
            y = y1 + param * D
            return ((px - x) ** 2 + (py - y) ** 2) ** 0.5

    def is_same_line_segment(self, coords, start, end):
        """Check if a line segment matches the given start and end points."""
        # Permitir una pequeña tolerancia en la comparación
        tolerance = 1
        
        # Comprobar en ambas direcciones (start->end y end->start)
        return ((abs(coords[0] - start[0]) < tolerance and 
                abs(coords[1] - start[1]) < tolerance and
                abs(coords[2] - end[0]) < tolerance and
                abs(coords[3] - end[1]) < tolerance) or
                (abs(coords[0] - end[0]) < tolerance and
                 abs(coords[1] - end[1]) < tolerance and
                 abs(coords[2] - start[0]) < tolerance and
                 abs(coords[3] - start[1]) < tolerance))

if __name__ == "__main__":
    app = App()
    app.mainloop()
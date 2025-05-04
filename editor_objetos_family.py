import customtkinter as ctk
from tkinter import simpledialog, messagebox, Menu
import pandas as pd
from PIL import ImageGrab
import os


# Dictionary of predefined objects
FAMILY_MODULES = {
    "Transformer 100": {
        "family": "Transformer",
        "common": {
            "Space X": 40,
            "Space Y": 45,
            "Price": 1000
        },
        "inputs": {
            "Grid Connection": 1
        },
        "outputs": {
            "Usable Power": 100
        }
    },
    "Transformer 1000": {
        "family": "Transformer",
        "common": {
            "Space X": 100,
            "Space Y": 100,
            "Price": 50000
        },
        "inputs": {
            "Grid Connection": 1
        },
        "outputs": {
            "Usable Power": 1000
        }
    },
    "Transformer 5000": {
        "family": "Transformer",
        "common": {
            "Space X": 200,
            "Space Y": 200,
            "Price": 250000
        },
        "inputs": {
            "Grid Connection": 1
        },
        "outputs": {
            "Usable Power": 5000
        }
    },
    "Water Supply 100": {
        "family": "Water Supply",
        "common": {
            "Space X": 50,
            "Space Y": 50,
            "Price": 200
        },
        "inputs": {
            "Water Connection": 1
        },
        "outputs": {
            "Fresh Water": 100
        }
    },
    "Water Supply 500": {
        "family": "Water Supply",
        "common": {
            "Space X": 150,
            "Space Y": 100,
            "Price": 400
        },
        "inputs": {
            "Water Connection": 1
        },
        "outputs": {
            "Fresh Water": 500
        }
    },
    "Water Treatment 50": {
        "family": "Water Treatment",
        "common": {
            "Space X": 50,
            "Space Y": 50,
            "Price": 10000
        },
        "inputs": {
            "Fresh Water": 50,
            "Usable Power": 50
        },
        "outputs": {
            "Distlled Water": 50
        }
    },
    "Water Treatment 250": {
        "family": "Water Treatment",
        "common": {
            "Space X": 200,
            "Space Y": 200,
            "Price": 40000
        },
        "inputs": {
            "Fresh Water": 250,
            "Usable Power": 90
        },
        "outputs": {
            "Distlled Water": 250
        }
    },
    "Water Treatment 500": {
        "family": "Water Treatment",
        "common": {
            "Space X": 400,
            "Space Y": 400,
            "Price": 70000
        },
        "inputs": {
            "Fresh Water": 500,
            "Usable Power": 150
        },
        "outputs": {
            "Distlled Water": 500
        }
    },
    "Water Chiller 100": {
        "family": "Water Chiller",
        "common": {
            "Space X": 100,
            "Space Y": 100,
            "Price": 40000
        },
        "inputs": {
            "Distlled Water": 100,
            "Usable Power": 500
        },
        "outputs": {
            "Chilled Water": 95
        }
    },
    "Water Chiller 400": {
        "family": "Water Chiller",
        "common": {
            "Space X": 300,
            "Space Y": 100,
            "Price": 150000
        },
        "inputs": {
            "Distlled Water": 400,
            "Usable Power": 1500
        },
        "outputs": {
            "Chilled Water": 390
        }
    },
    "Network Rack 50": {
        "family": "Network Rack",
        "common": {
            "Space X": 40,
            "Space Y": 40,
            "Price": 2000
        },
        "inputs": {
            "Usable Power": 50,
            "Chilled Water": 5,
            "Fresh Water": 5
        },
        "outputs": {
            "Internal Network": 50
        }
    },
    "Network Rack 100": {
        "family": "Network Rack",
        "common": {
            "Space X": 40,
            "Space Y": 40,
            "Price": 8000
        },
        "inputs": {
            "Usable Power": 75,
            "Chilled Water": 7,
            "Fresh Water": 7
        },
        "outputs": {
            "Internal Network": 100
        }
    },
    "Network Rack 200": {
        "family": "Network Rack",
        "common": {
            "Space X": 40,
            "Space Y": 40,
            "Price": 20000
        },
        "inputs": {
            "Usable Power": 95,
            "Chilled Water": 10,
            "Fresh Water": 40
        },
        "outputs": {
            "Internal Network": 200
        }
    },
    "Server Rack 100": {
        "family": "Server Rack",
        "common": {
            "Space X": 40,
            "Space Y": 40,
            "Price": 8000
        },
        "inputs": {
            "Usable Power": 75,
            "Chilled Water": 15,
            "Internal Network": 10,
            "Distilled Water": 15
        },
        "outputs": {
            "Processing": 100,
            "External Network": 100
        }
    },
    "Server Rack 200": {
        "family": "Server Rack",
        "common": {
            "Space X": 40,
            "Space Y": 40,
            "Price": 12000
        },
        "inputs": {
            "Usable Power": 125,
            "Chilled Water": 25,
            "Internal Network": 18,
            "Distilled Water": 25
        },
        "outputs": {
            "Processing": 150,
            "External Network": 200
        }
    },
    "Server Rack 500": {
        "family": "Server Rack",
        "common": {
            "Space X": 40,
            "Space Y": 40,
            "Price": 50000
        },
        "inputs": {
            "Usable Power": 240,
            "Chilled Water": 50,
            "Internal Network": 32,
            "Distilled Water": 50
        },
        "outputs": {
            "Processing": 1000,
            "External Network": 400
        }
    },
    "Data Rack 100": {
        "family": "Data Rack",
        "common": {
            "Space X": 40,
            "Space Y": 40,
            "Price": 2000
        },
        "inputs": {
            "Usable Power": 15,
            "Chilled Water": 3,
            "Internal Network": 5,
            "Distilled Water": 3
        },
        "outputs": {
            "Data Storage": 100
        }
    },
    "Data Rack 250": {
        "family": "Data Rack",
        "common": {
            "Space X": 40,
            "Space Y": 40,
            "Price": 7500
        },
        "inputs": {
            "Usable Power": 25,
            "Chilled Water": 3,
            "Internal Network": 10,
            "Distilled Water": 3
        },
        "outputs": {
            "Data Storage": 250
        }
    }
}

FAMILIES = {}
for module_name, module_data in FAMILY_MODULES.items():
    family = module_data["family"]
    if family not in FAMILIES:
        FAMILIES[family] = []
    FAMILIES[family].append(module_name)

class Objeto:
    def __init__(self, tipo, x, y, atributos):
        self.tipo = tipo
        self.x = x
        self.y = y
        self.atributos = atributos.copy()
        self.id_canvas = None
        self.io_points = []
        
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("DaceCAD")
        self.geometry("900x700")
        ctk.set_appearance_mode("Light")  # Options: "System", "Dark", "Light"
        ctk.set_default_color_theme("blue")  # Options: "blue", "green", "dark-blue"

        # Variables
        self.objetos = []
        self.objeto_actual = ctk.StringVar(value="None")
        self.seleccionado = None
        self.dx = self.dy = 0
        self.tool = "create"  # Default tool
        self.grid_size = 30  # Size of each grid cell
        
        # Cable variables (inicializadas correctamente)
        self.cable_type = None
        self.start_point = None
        self.start_object = None
        self.cables = []
        self.is_input_start = None
        self.current_cable_points = []
        self.current_cable_segments = []
        self.last_click_point = None
        self._current_cable_segment_ids = []

        # Layout
        self.create_toolbars()
        self.create_canvas()
        self.bind('<Escape>', lambda event: self.select_tool('select'))
        self.bind('<Delete>', lambda event: self.select_tool('erase'))
        self.bind('<Escape>', self.cancel_cable_mode_or_select)

    def create_toolbars(self):
        """Create the toolbars."""
        # Top toolbar: grid size, mode, export, screenshot
        tool_frame = ctk.CTkFrame(self)
        tool_frame.pack(side="top", fill="x", padx=5, pady=5)
        ctk.CTkLabel(tool_frame, text="Grid Size:").pack(side="left", padx=5, pady=5)
        self.grid_size_entry = ctk.CTkEntry(tool_frame, width=50)
        self.grid_size_entry.insert(0, str(self.grid_size))
        self.grid_size_entry.pack(side="left", padx=5, pady=5)
        self.grid_size_entry.bind("<Return>", self.update_grid_size)
        ctk.CTkButton(tool_frame, text="Export to CSV", command=self.export_to_csv).pack(side="left", padx=5, pady=5)
        ctk.CTkButton(tool_frame, text="Screenshot Canvas", command=self.screenshot_canvas).pack(side="left", padx=5, pady=5)
        mode_switch = ctk.CTkSwitch(tool_frame, text="Dark Mode", command=self.toggle_mode)
        mode_switch.pack(side="right", padx=5, pady=5)

        # Right menu: tool selection, separator, object tools
        object_frame = ctk.CTkFrame(self)
        object_frame.pack(side="right", fill="y", padx=5, pady=5)
        # Tool selection (Drag/Select/Create Figure/Erase)
        ctk.CTkLabel(object_frame, text="Tools:").pack(pady=(10, 2))
        ctk.CTkButton(object_frame, text="🖐 Drag", command=lambda: self.select_tool("drag")).pack(fill="x", padx=10, pady=2)
        ctk.CTkButton(object_frame, text="🖱 Select", command=lambda: self.select_tool("select")).pack(fill="x", padx=10, pady=2)
        ctk.CTkButton(object_frame, text="➕ Create Figure", command=lambda: self.select_tool("create_figure")).pack(fill="x", padx=10, pady=2)
        ctk.CTkButton(object_frame, text="🧹 Erase", command=lambda: self.select_tool("erase")).pack(fill="x", padx=10, pady=2)
        # Black separator bar
        sep = ctk.CTkFrame(object_frame, height=2, fg_color="black")
        sep.pack(fill="x", padx=5, pady=10)
        # Object tools
        ctk.CTkLabel(object_frame, text="Family:").pack(pady=5)
        self.family_menu = ctk.CTkOptionMenu(
            object_frame,
            values=list(FAMILIES.keys()),
            command=self._on_family_select
        )
        self.family_menu.pack(pady=5)

        ctk.CTkLabel(object_frame, text="Object:").pack(pady=5)
        self.object_menu = ctk.CTkOptionMenu(
            object_frame,
            values=[],
            command=self._on_object_menu_change
        )
        self.object_menu.pack(pady=5)
        self.object_menu.configure(state="disabled")

        ctk.CTkButton(object_frame, text="New Object", 
              command=self.open_create_menu).pack(pady=5)

        # Black separator bar
        sep = ctk.CTkFrame(object_frame, height=2, fg_color="black")
        sep.pack(fill="x", padx=5, pady=10)
        
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
        
    def _on_family_select(self, family):
        """Handle family selection."""
        if family in FAMILIES:
            self.object_menu.configure(
                values=FAMILIES[family],
                state="normal"
            )
            self.object_menu.set(FAMILIES[family][0])
            self._on_object_menu_change(FAMILIES[family][0])

    def _on_object_menu_change(self, value):
        """Handle object selection."""
        self.objeto_actual.set(value)
        self.select_tool("create_figure")
    

    def screenshot_canvas(self):
        self.update()
        x = self.canvas.winfo_rootx()
        y = self.canvas.winfo_rooty()
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        img = ImageGrab.grab(bbox=(x, y, x + w, y + h))
        file_path = simpledialog.askstring("Save Screenshot", "Enter file name (without extension):")
        if file_path:
            img.save(f"{file_path}.png")
            messagebox.showinfo("Screenshot Saved", f"Screenshot saved as {file_path}.png")

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
        self.canvas.bind("<ButtonRelease-1>", self.release)  # Release after dragging
        self.canvas.bind("<B1-Motion>", self.on_drag)  # Dragging (always enabled)
        self.canvas.bind("<Button-3>", self.on_right_click_anywhere)  # Right-click for context menu or cancel cable
        self.canvas.bind("<Double-Button-1>", self.edit_object)  # Double-click for editing
        self.canvas.bind("<Motion>", self.on_mouse_move)  # For preview
        self.canvas.bind("<Button-3>", self.show_object_context_menu)  # Right-click for context menu
        self.draw_grid()

    def cancel_cable_mode_or_select(self, event=None):
        """Cancel cable mode if active, otherwise select tool."""
        if self.tool == "cable":
            self.cleanup_cable_preview()
            self.tool = "select"
            self.cable_type = None
            self.canvas.config(cursor="arrow")
        else:
            self.select_tool('select')

    def on_right_click_anywhere(self, event):
        """Right click: cancel cable mode if active, else show context menu."""
        if self.tool == "cable":
            self.cleanup_cable_preview()
            self.tool = "select"
            self.cable_type = None
            self.canvas.config(cursor="arrow")
        else:
            self.show_object_context_menu(event)


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

    def remove_preview(self):
        if hasattr(self, '_preview_items'):
            for item in self._preview_items:
                self.canvas.delete(item)
            self._preview_items = []

    def select_tool(self, tool):
        self.tool = tool
        if tool == "drag":
            self.canvas.config(cursor="hand2")
        elif tool == "select":
            self.canvas.config(cursor="arrow")
        elif tool == "erase":
            self.canvas.config(cursor="X_cursor")
        elif tool == "delete_cable":
            self.cleanup_cable_preview()
            self.cable_type = None
            self.canvas.config(cursor="X_cursor")  # 'circle' es lo más parecido a una goma en Tkinter
        else:
            self.canvas.config(cursor="tcross")
        # Remove preview if not in create_figure mode
        if tool != "create_figure":
            self.remove_preview()

    def on_click(self, event):
        """Handle mouse click events."""
        self._drag_started = False
        self._click_x = event.x
        self._click_y = event.y
        self._mouse_down_on_obj = False
        
        clicked_id = self.canvas.find_closest(event.x, event.y)[0]
        
        # Si estamos en modo cable o delete_cable, manejamos el click específicamente
        if self.tool == "cable":
            self.handle_cable_click(event)
            return
        elif self.tool == "delete_cable":
            self.delete_cable_click(event)
            return
            
        # Para otros modos, manejamos objetos y IO points
        for obj in self.objetos:
            if clicked_id in obj.id_canvas:
                self._mouse_down_on_obj = True
                if self.tool == "erase":
                    for cid in obj.id_canvas:
                        self.canvas.delete(cid)
                    self.objetos.remove(obj)
                return
                
        if self.tool == "select" and not self._mouse_down_on_obj:
            self.select_object(event)
        elif self.tool == "create_figure":
            self.place_object(event)
            self.remove_preview()
        else:
            self._pending_create = False

    def on_drag(self, event):
        """Handle drag events for objects or IO points. Drag always enabled on left hold, also in select mode."""
        # If dragging IO point
        if hasattr(self, 'dragging_io_index') and self.seleccionado and self.dragging_io_index is not None:
            obj = self.seleccionado
            idx = self.dragging_io_index
            attributes = obj.atributos
            size_x = attributes.get("size_x", 100)
            size_y = attributes.get("size_y", 100)
            x, y = obj.x, obj.y
            io = obj.io_points[idx]
            rel_x = (event.x - (x - size_x // 2)) / size_x
            rel_y = (event.y - (y - size_y // 2)) / size_y
            sides = {
                'left': abs(rel_x),
                'right': abs(rel_x - 1),
                'top': abs(rel_y),
                'bottom': abs(rel_y - 1)
            }
            side = min(sides, key=sides.get)
            if side in ['left', 'right']:
                pos = min(max(rel_y, 0), 1)
            else:
                pos = min(max(rel_x, 0), 1)
            io['side'] = side
            io['pos'] = pos
            if side == 'left':
                px = x - size_x // 2
                py = y - size_y // 2 + pos * size_y
            elif side == 'right':
                px = x + size_x // 2
                py = y - size_y // 2 + pos * size_y
            elif side == 'top':
                px = x - size_x // 2 + pos * size_x
                py = y - size_y // 2
            else:
                px = x - size_x // 2 + pos * size_x
                py = y + size_y // 2
            self.canvas.coords(
                io['canvas_id'],
                px - 5, py - 5, px + 5, py + 5
            )
            self._drag_started = True
            self._pending_create = False
        else:
            # Try to drag a figure if mouse is over it, even if tool is 'select' or 'drag'
            if self.tool in ['select', 'drag', 'create_figure']:
                closest = self.canvas.find_closest(event.x, event.y)[0]
                obj = self.get_object_by_id(closest)
                if obj:
                    if self.seleccionado is None:
                        self.seleccionado = obj
                        self.dx = event.x - obj.x
                        self.dy = event.y - obj.y
                    new_x = event.x - self.dx
                    new_y = event.y - self.dy
                    self.seleccionado.x = new_x
                    self.seleccionado.y = new_y
                    attributes = self.seleccionado.atributos
                    size_x = attributes.get("size_x", 100)
                    size_y = attributes.get("size_y", 100)
                    self.canvas.coords(
                        self.seleccionado.id_canvas[0],
                        new_x - size_x // 2, new_y - size_y // 2,
                        new_x + size_x // 2, new_y + size_y // 2
                    )
                    self.canvas.coords(self.seleccionado.id_canvas[1], new_x, new_y)
                    # Update font size dynamically
                    font_size = max(8, int(min(size_x, size_y) // 6))
                    self.canvas.itemconfig(self.seleccionado.id_canvas[1], font=("Arial", font_size, "bold"))
                    # Move IO points
                    for io in self.seleccionado.io_points:
                        if io['side'] == 'left':
                            px = new_x - size_x // 2
                            py = new_y - size_y // 2 + io['pos'] * size_y
                        elif io['side'] == 'right':
                            px = new_x + size_x // 2
                            py = new_y - size_y // 2 + io['pos'] * size_y
                        elif io['side'] == 'top':
                            px = new_x - size_x // 2 + io['pos'] * size_x
                            py = new_y - size_y // 2
                        else:
                            px = new_x - size_x // 2 + io['pos'] * size_x
                            py = new_y + size_y // 2
                        self.canvas.coords(
                            io['canvas_id'],
                            px - 5, py - 5, px + 5, py + 5
                        )
                    self._drag_started = True
                    self._pending_create = False
                else:
                    self._drag_started = False
            else:
                self._drag_started = False
    def release(self, event):
        """Release the selected object or IO point."""
        if hasattr(self, 'dragging_io_index') and self.dragging_io_index is not None:
            # Si estabas arrastrando un IO point, guarda su posición actual
            io = self.seleccionado.io_points[self.dragging_io_index]
            coords = self.canvas.coords(io['canvas_id'])
            # Guarda el centro del IO point
            io['current_x'] = (coords[0] + coords[2]) / 2
            io['current_y'] = (coords[1] + coords[3]) / 2
            # Limpia el estado de arrastre
            self.dragging_io_index = None
            self.seleccionado = None
        else:
            if self.seleccionado:
                # Si estabas moviendo el objeto completo
                x, y = self.seleccionado.x, self.seleccionado.y
                attributes = self.seleccionado.atributos
                size_x = attributes.get("size_x", 100)
                size_y = attributes.get("size_y", 100)
                
                # Actualiza la posición del rectángulo principal y el texto
                self.canvas.coords(
                    self.seleccionado.id_canvas[0],
                    x - size_x // 2, y - size_y // 2,
                    x + size_x // 2, y + size_y // 2
                )
                self.canvas.coords(self.seleccionado.id_canvas[1], x, y)

                font_size = max(8, int(min(size_x, size_y) // 6))
                self.canvas.itemconfig(self.seleccionado.id_canvas[1], font=("Arial", font_size, "bold"))
                # Al mover el objeto, actualiza los IO points basándose en su posición guardada o calculada
                for io in self.seleccionado.io_points:
                    if hasattr(io, 'current_x') and hasattr(io, 'current_y'):
                        # Si el IO point tiene una posición personalizada, úsala
                        px = io['current_x']
                        py = io['current_y']
                    else:
                        # Si no, calcula la posición basada en side y pos
                        if io['side'] == 'left':
                            px = x - size_x // 2
                            py = y - size_y // 2 + io['pos'] * size_y
                        elif io['side'] == 'right':
                            px = x + size_x // 2
                            py = y - size_y // 2 + io['pos'] * size_y
                        elif io['side'] == 'top':
                            px = x - size_x // 2 + io['pos'] * size_x
                            py = y - size_y // 2
                        else:
                            px = x - size_x // 2 + io['pos'] * size_x
                            py = y + size_y // 2
                        
                    # Actualiza la posición del IO point
                    self.canvas.coords(
                        io['canvas_id'],
                        px - 5, py - 5,
                        px + 5, py + 5
                    )
                self.seleccionado = None

        if getattr(self, '_pending_create', False) and not getattr(self, '_drag_started', False):
            self.place_object(event)
        self._pending_create = False
        self._drag_started = False
        self._mouse_down_on_obj = False

    def place_object(self, event):
        """Place a new object on the canvas."""
        obj_type = self.objeto_actual.get()
        if obj_type not in FAMILY_MODULES:
            return
            
        module_data = FAMILY_MODULES[obj_type]
        common_attrs = module_data["common"]
        
        x, y = event.x, event.y
        
        attributes = {
            "size_x": common_attrs["Space X"],
            "size_y": common_attrs["Space Y"],
            "price": common_attrs["Price"],
            "inputs": len(module_data["inputs"]),
            "outputs": len(module_data["outputs"]),
            "inputs_names": list(module_data["inputs"].keys()),
            "outputs_names": list(module_data["outputs"].keys())
        }
        
        obj = Objeto(obj_type, x, y, attributes)

        size_x = attributes["size_x"]
        size_y = attributes["size_y"]
        inputs = attributes["inputs"]
        outputs = attributes["outputs"]

        # Draw the main shape
        id_canvas = [self.canvas.create_rectangle(
            x - size_x // 2, y - size_y // 2,
            x + size_x // 2, y + size_y // 2,
            fill="gray", outline="black", width=1,
            tags="figure"
        )]
        
        # Calculate font size based on object size (adjust divisor as needed)
        
        #text_id = self.canvas.create_text(x, y, text=obj_type, fill="white", tags="figure")
        #id_canvas.append(text_id)
        # Calculate font size based on object size (adjust divisor as needed)
        font_size = max(8, int(min(size_x, size_y) // 6))
        text_id = self.canvas.create_text(
            x, y, text=obj_type, fill="white", tags="figure",
            font=("Arial", font_size, "bold")
        )
        # Add IO points
        obj.io_points = []
        
        # Add inputs
        for i in range(inputs):
            pos = (i + 1) / (inputs + 1)
            io = {'side': 'left', 'pos': pos}
            input_y = y - size_y // 2 + pos * size_y
            input_id = self.canvas.create_oval(
                x - size_x // 2 - 5, input_y - 5,
                x - size_x // 2 + 5, input_y + 5,
                fill="white", tags="figure"
            )
            id_canvas.append(input_id)
            io['canvas_id'] = input_id
            obj.io_points.append(io)

        # Add outputs
        for i in range(outputs):
            pos = (i + 1) / (outputs + 1)
            io = {'side': 'right', 'pos': pos}
            output_y = y - size_y // 2 + pos * size_y
            output_id = self.canvas.create_rectangle(
                x + size_x // 2 - 5, output_y - 5,
                x + size_x // 2 + 5, output_y + 5,
                fill="white", tags="figure"
            )
            id_canvas.append(output_id)
            io['canvas_id'] = output_id
            obj.io_points.append(io)

        obj.id_canvas = id_canvas
        self.objetos.append(obj)
        
        self.canvas.tag_raise("figure")

    def select_object(self, event):
        """Select an object by clicking on it."""
        closest = self.canvas.find_closest(event.x, event.y)[0]
        obj = self.get_object_by_id(closest)
        if obj:
            messagebox.showinfo("Object Selected", f"Type: {obj.tipo}\nPosition: ({obj.x}, {obj.y})\nAttributes: {obj.atributos}")
    def show_object_context_menu(self, event):
        """Show a right-click context menu for an object (delete, edit attributes, view attributes)."""
        closest = self.canvas.find_closest(event.x, event.y)[0]
        obj = self.get_object_by_id(closest)
        if not obj:
            return
        menu = Menu(self, tearoff=0)
        def delete_obj():
            for cid in obj.id_canvas:
                self.canvas.delete(cid)
            self.objetos.remove(obj)
        def show_attrs():
            attr_text = '\n'.join(f"{k}: {v}" for k, v in obj.atributos.items())
            messagebox.showinfo("Object Attributes", f"Type: {obj.tipo}\nPosition: ({obj.x}, {obj.y})\nAttributes:\n{attr_text}")
        def edit_attrs():
            # Custom dialog for editing all attributes at once
            edit_win = ctk.CTkToplevel(self)
            edit_win.title("Edit Attributes")
            edit_win.geometry("300x400")
            edit_win.lift()  # Bring to front
            edit_win.attributes('-topmost', True)
            entries = {}
            for i, (k, v) in enumerate(obj.atributos.items()):
                ctk.CTkLabel(edit_win, text=f"{k}:", font=("Arial", 12)).pack(anchor="w", padx=10, pady=(10 if i==0 else 2, 2))
                entry = ctk.CTkEntry(edit_win, font=("Arial", 12))
                entry.insert(0, str(v))
                entry.pack(fill="x", padx=10, pady=2)
                entries[k] = (entry, type(v))
            def save():
                for k, (entry, typ) in entries.items():
                    val = entry.get()
                    try:
                        obj.atributos[k] = typ(val)
                    except Exception:
                        obj.atributos[k] = val
                edit_win.destroy()
            ctk.CTkButton(edit_win, text="OK", command=save, font=("Arial", 12)).pack(pady=15)
            edit_win.focus_force()
        menu.add_command(label="View Attributes", command=show_attrs)
        menu.add_command(label="Edit Attributes", command=edit_attrs)
        menu.add_command(label="Delete", command=delete_obj)
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

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
                    "family": "Custom",
                    "common": {
                        "Space X": int(size_x.get()),
                        "Space Y": int(size_y.get()),
                        "Price": 0
                    },
                    "inputs": {},
                    "outputs": {}
                }

                # Añadir inputs y outputs numerados
                for i in range(int(inputs.get())):
                    nuevo_objeto["inputs"][f"Input {i+1}"] = 0

                for i in range(int(outputs.get())):
                    nuevo_objeto["outputs"][f"Output {i+1}"] = 0

                # Add the new object to FAMILY_MODULES
                FAMILY_MODULES[nombre.get()] = nuevo_objeto

                # Actualizar FAMILIES
                if "Custom" not in FAMILIES:
                    FAMILIES["Custom"] = []
                FAMILIES["Custom"].append(nombre.get())
                # Save the updated FAMILY_MODULES to the file

                # Update the dropdown menu
                self.object_menu.configure(values=list(FAMILY_MODULES.keys()))
                self.objeto_actual.set(nombre.get())

                self.create_menu_window.destroy()
                self.create_menu_window = None  # Reset the reference
                # Switch to create_figure tool after creating a new object
                self.select_tool("create_figure")
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
        menu.configure(values=list(FAMILY_MODULES.keys()))

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
    def on_mouse_move(self, event):
        if self.tool == "create_figure":
            self.show_preview(event)
        else:
            self.remove_preview()

    def select_cable(self, cable_type):
        """Select a cable type for connection."""
        self.tool = "cable"
        self.cable_type = cable_type
        self.start_point = None
        self.start_object = None
        self.is_input_start = None
    
    def show_preview(self, event):
        # Remove previous preview if any
        self.remove_preview()
        obj_type = self.objeto_actual.get()
        attributes = FAMILY_MODULES.get(obj_type, {})
        x, y = event.x, event.y
        size_x = attributes.get("size_x", 100)
        size_y = attributes.get("size_y", 100)
        inputs = attributes.get("inputs", 0)
        outputs = attributes.get("outputs", 0)
        color = {"Motor": "red", "Sensor": "blue", "Caja": "green"}.get(obj_type, "gray")
        # Draw preview rectangle
        self._preview_items = []
        rect = self.canvas.create_rectangle(
            x - size_x // 2, y - size_y // 2,
            x + size_x // 2, y + size_y // 2,
            outline=color, width=2, dash=(4, 2), tags="preview"
        )
        self._preview_items.append(rect)
        text_id = self.canvas.create_text(x, y, text=obj_type, fill=color, tags="preview")
        self._preview_items.append(text_id)
        # Draw IO points as preview
        for i in range(inputs):
            pos = (i + 1) / (inputs + 1)
            input_y = y - size_y // 2 + pos * size_y
            oval = self.canvas.create_oval(
                x - size_x // 2 - 5, input_y - 5,
                x - size_x // 2 + 5, input_y + 5,
                outline=color, width=2, tags="preview"
            )
            self._preview_items.append(oval)
        for i in range(outputs):
            pos = (i + 1) / (outputs + 1)
            output_y = y - size_y // 2 + pos * size_y
            oval = self.canvas.create_oval(
                x + size_x // 2 - 5, output_y - 5,
                x + size_x // 2 + 5, output_y + 5,
                outline=color, width=2, tags="preview"
            )
            self._preview_items.append(oval)

    def remove_preview(self):
        if hasattr(self, '_preview_items'):
            for item in self._preview_items:
                self.canvas.delete(item)
            self._preview_items = []

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
import wx
from wx.lib.colourselect import ColourSelect
from PIL import Image, ImageGrab
import numpy as np
from .base_tool import BaseTool

class ColorPicker(BaseTool):
    def __init__(self, parent):
        super().__init__(parent)
        self.image = None
        self.photo = None
        self.canvas = None
        self.current_color = "#000000"
        self.predefined_palettes = {
            "Material": ["#F44336", "#E91E63", "#9C27B0", "#673AB7", "#3F51B5", "#2196F3"],
            "Nature": ["#4CAF50", "#8BC34A", "#CDDC39", "#FFEB3B", "#FFC107", "#FF9800"],
            "Grayscale": ["#000000", "#424242", "#616161", "#9E9E9E", "#BDBDBD", "#FFFFFF"],
            "Ocean": ["#006064", "#0097A7", "#00BCD4", "#4DD0E1", "#80DEEA", "#B2EBF2"],
            "Sunset": ["#BF360C", "#E64A19", "#FF5722", "#FF8A65", "#FFAB91", "#FFCCBC"]
        }
        self.setup_ui()

    def setup_ui(self):
        main_frame = wx.Panel(self)
        main_layout = wx.BoxSizer(wx.HORIZONTAL)
        main_frame.SetSizer(main_layout)
        self.layout.Add(main_frame, 1, wx.EXPAND)

        # Left panel
        left_panel = wx.Panel(main_frame)
        left_layout = wx.BoxSizer(wx.VERTICAL)
        left_panel.SetSizer(left_layout)
        main_layout.Add(left_panel, 1, wx.EXPAND)

        # Color Picker Section
        picker_frame = wx.Panel(left_panel)
        picker_layout = wx.BoxSizer(wx.VERTICAL)
        picker_frame.SetSizer(picker_layout)
        left_layout.Add(picker_frame, 0, wx.EXPAND | wx.ALL, 5)

        # Current color display
        self.color_display = wx.Panel(picker_frame, size=(100, 50))
        self.color_display.SetBackgroundColour(self.current_color)
        picker_layout.Add(self.color_display, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        # Color values
        values_frame = wx.Panel(picker_frame)
        values_layout = wx.GridBagSizer(5, 5)
        values_frame.SetSizer(values_layout)
        picker_layout.Add(values_frame, 0, wx.EXPAND | wx.ALL, 5)

        self.hex_var = wx.TextCtrl(values_frame, value=self.current_color)
        self.rgb_var = wx.TextCtrl(values_frame, value="0, 0, 0")
        
        values_layout.Add(wx.StaticText(values_frame, label="HEX:"), pos=(0, 0))
        values_layout.Add(self.hex_var, pos=(0, 1))
        
        values_layout.Add(wx.StaticText(values_frame, label="RGB:"), pos=(1, 0))
        values_layout.Add(self.rgb_var, pos=(1, 1))

        # Color picker buttons
        btn_frame = wx.Panel(picker_frame)
        btn_layout = wx.BoxSizer(wx.HORIZONTAL)
        btn_frame.SetSizer(btn_layout)
        picker_layout.Add(btn_frame, 0, wx.EXPAND | wx.ALL, 5)
        
        choose_color_btn = wx.Button(btn_frame, label="Choose Color")
        choose_color_btn.Bind(wx.EVT_BUTTON, self.open_color_chooser)
        btn_layout.Add(choose_color_btn, 0, wx.ALL, 5)
        
        copy_hex_btn = wx.Button(btn_frame, label="Copy HEX")
        copy_hex_btn.Bind(wx.EVT_BUTTON, lambda event: self.copy_color(self.hex_var.GetValue()))
        btn_layout.Add(copy_hex_btn, 0, wx.ALL, 5)
        
        copy_rgb_btn = wx.Button(btn_frame, label="Copy RGB")
        copy_rgb_btn.Bind(wx.EVT_BUTTON, lambda event: self.copy_color(self.rgb_var.GetValue()))
        btn_layout.Add(copy_rgb_btn, 0, wx.ALL, 5)

        # Separator
        separator = wx.StaticLine(left_panel)
        left_layout.Add(separator, 0, wx.EXPAND | wx.ALL, 5)

        # Image Section
        left_layout.Add(wx.StaticText(left_panel, label="Image Source:"), 0, wx.ALL, 5)
        browse_image_btn = wx.Button(left_panel, label="Browse Image")
        browse_image_btn.Bind(wx.EVT_BUTTON, self.browse_image)
        left_layout.Add(browse_image_btn, 0, wx.ALL, 5)
        
        paste_clipboard_btn = wx.Button(left_panel, label="Paste from Clipboard")
        paste_clipboard_btn.Bind(wx.EVT_BUTTON, self.paste_from_clipboard)
        left_layout.Add(paste_clipboard_btn, 0, wx.ALL, 5)

        # Predefined palettes
        left_layout.Add(wx.StaticText(left_panel, label="Color Palettes:"), 0, wx.ALL, 5)
        for palette_name in self.predefined_palettes:
            palette_btn = wx.Button(left_panel, label=palette_name)
            palette_btn.Bind(wx.EVT_BUTTON, lambda event, p=palette_name: self.show_palette(p))
            left_layout.Add(palette_btn, 0, wx.ALL, 5)

        # Right panel
        right_panel = wx.Panel(main_frame)
        right_layout = wx.BoxSizer(wx.VERTICAL)
        right_panel.SetSizer(right_layout)
        main_layout.Add(right_panel, 1, wx.EXPAND)

        # Canvas for image/color display
        self.canvas = wx.StaticBitmap(right_panel, size=(400, 300))
        self.canvas.SetBackgroundColour("white")
        self.canvas.Bind(wx.EVT_LEFT_DOWN, self.pick_color)
        right_layout.Add(self.canvas, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        # Colors display frame
        self.colors_frame = wx.Panel(right_panel)
        self.colors_layout = wx.BoxSizer(wx.VERTICAL)
        self.colors_frame.SetSizer(self.colors_layout)
        right_layout.Add(self.colors_frame, 1, wx.EXPAND | wx.ALL, 5)

        # Instructions
        self.colors_layout.Add(wx.StaticText(self.colors_frame, label="Click on image to pick colors or select a predefined palette"), 0, wx.ALL, 5)

    def browse_image(self, event):
        with wx.FileDialog(self, "Open Image", wildcard="Image files (*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.webp)|*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.webp") as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fileDialog.GetPath()
            self.load_image(Image.open(pathname))

    def paste_from_clipboard(self, event):
        try:
            image = ImageGrab.grabclipboard()
            if image:
                self.load_image(image)
            else:
                wx.MessageBox("No image found in clipboard", "Warning", wx.OK | wx.ICON_WARNING)
        except Exception as e:
            wx.MessageBox(f"Failed to paste image: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)

    def load_image(self, image):
        try:
            self.image = image
            
            # Calculate resize ratio
            canvas_width = self.canvas.GetSize().GetWidth()
            canvas_height = self.canvas.GetSize().GetHeight()
            image_ratio = image.width / image.height
            canvas_ratio = canvas_width / canvas_height
            
            if image_ratio > canvas_ratio:
                width = canvas_width
                height = int(canvas_width / image_ratio)
            else:
                height = canvas_height
                width = int(canvas_height * image_ratio)
            
            resized = image.resize((width, height), Image.LANCZOS)
            self.photo = wx.Bitmap.FromBuffer(resized.width, resized.height, np.array(resized))
            
            self.canvas.SetBitmap(self.photo)
            
        except Exception as e:
            wx.MessageBox(f"Failed to load image: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)

    def show_palette(self, palette_name):
        self.clear_colors()
        colors = self.predefined_palettes[palette_name]
        self.display_colors(colors)
        
        # Show palette preview on canvas
        self.canvas.SetBitmap(wx.NullBitmap)
        width = self.canvas.GetSize().GetWidth()
        height = self.canvas.GetSize().GetHeight()
        color_width = width / len(colors)
        
        for i, color in enumerate(colors):
            x1 = i * color_width
            x2 = (i + 1) * color_width
            self.canvas.SetBackgroundColour(color)

    def open_color_chooser(self, event):
        color_data = wx.ColourData()
        color_data.SetColour(self.current_color)
        dialog = wx.ColourDialog(self, color_data)
        if dialog.ShowModal() == wx.ID_OK:
            color = dialog.GetColourData().GetColour()
            self.current_color = color.GetAsString(wx.C2S_HTML_SYNTAX)
            self.update_color_display(color.Get(includeAlpha=False))

    def update_color_display(self, rgb):
        self.current_color = '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))
        self.color_display.SetBackgroundColour(self.current_color)
        self.hex_var.SetValue(self.current_color.upper())
        self.rgb_var.SetValue(f"{int(rgb[0])}, {int(rgb[1])}, {int(rgb[2])}")

    def pick_color(self, event):
        if not self.image:
            return

        try:
            # Get canvas coordinates
            canvas_x = event.GetPosition().x
            canvas_y = event.GetPosition().y
            
            # Convert to image coordinates
            image_x = int((canvas_x / self.canvas.GetSize().GetWidth()) * self.image.width)
            image_y = int((canvas_y / self.canvas.GetSize().GetHeight()) * self.image.height)
            
            # Get color at point
            color = self.image.getpixel((image_x, image_y))
            if len(color) == 4:  # RGBA
                color = color[:3]
            
            # Update color display
            self.update_color_display(color)
            self.add_color(self.current_color)
            
        except Exception as e:
            wx.MessageBox(f"Failed to pick color: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)

    def add_color(self, color):
        frame = wx.Panel(self.colors_frame)
        frame_layout = wx.BoxSizer(wx.VERTICAL)
        frame.SetSizer(frame_layout)
        self.colors_layout.Add(frame, 0, wx.EXPAND | wx.ALL, 5)
        
        # Color box
        color_box = wx.Panel(frame, size=(50, 50))
        color_box.SetBackgroundColour(color)
        frame_layout.Add(color_box, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        
        # Color code
        frame_layout.Add(wx.StaticText(frame, label=color.upper()), 0, wx.ALIGN_CENTER | wx.ALL, 5)
        
        # Copy button
        copy_btn = wx.Button(frame, label="Copy")
        copy_btn.Bind(wx.EVT_BUTTON, lambda event: self.copy_color(color))
        frame_layout.Add(copy_btn, 0, wx.ALIGN_CENTER | wx.ALL, 5)

    def display_colors(self, colors):
        for color in colors:
            self.add_color(color)

    def clear_colors(self):
        for child in self.colors_frame.GetChildren():
            child.Destroy()

    def copy_color(self, color_value):
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(wx.TextDataObject(color_value.upper()))
            wx.TheClipboard.Close()
            wx.MessageBox(f"Color value copied: {color_value}", "Success", wx.OK | wx.ICON_INFORMATION)
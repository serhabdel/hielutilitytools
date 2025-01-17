import wx
from PIL import Image
from rembg import remove
import io
from .base_tool import BaseTool

class ImageTools(BaseTool):
    def __init__(self, parent):
        super().__init__(parent)
        self.input_path = None
        self.output_path = None
        self.tool_type = None
        self.quality = None
        self.width = None
        self.height = None
        self.maintain_ratio = None
        self.setup_ui()

    def setup_ui(self):
        main_layout = wx.BoxSizer(wx.VERTICAL)

        # Tool type selection
        tool_group = wx.StaticBox(self, label="Tool:")
        tool_layout = wx.StaticBoxSizer(tool_group, wx.HORIZONTAL)
        self.tool_type = wx.RadioBox(self, choices=["Format Converter", "Compressor", "Resizer", "Background Remover", "ICO Converter", "Upscaler"], majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.tool_type.SetSelection(0)
        tool_layout.Add(self.tool_type, 1, wx.EXPAND)
        main_layout.Add(tool_layout, 0, wx.EXPAND | wx.ALL, 5)

        # Input file
        input_layout = wx.BoxSizer(wx.HORIZONTAL)
        input_layout.Add(wx.StaticText(self, label="Input Image:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.input_path = wx.TextCtrl(self)
        input_layout.Add(self.input_path, 1, wx.EXPAND | wx.ALL, 5)
        browse_input_btn = wx.Button(self, label="Browse")
        browse_input_btn.Bind(wx.EVT_BUTTON, self.browse_input)
        input_layout.Add(browse_input_btn, 0, wx.ALL, 5)
        main_layout.Add(input_layout, 0, wx.EXPAND | wx.ALL, 5)

        # Output file
        output_layout = wx.BoxSizer(wx.HORIZONTAL)
        output_layout.Add(wx.StaticText(self, label="Output:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.output_path = wx.TextCtrl(self)
        output_layout.Add(self.output_path, 1, wx.EXPAND | wx.ALL, 5)
        browse_output_btn = wx.Button(self, label="Browse")
        browse_output_btn.Bind(wx.EVT_BUTTON, self.browse_output)
        output_layout.Add(browse_output_btn, 0, wx.ALL, 5)
        main_layout.Add(output_layout, 0, wx.EXPAND | wx.ALL, 5)

        # Quality frame
        self.quality_frame = wx.StaticBox(self, label="Quality Settings")
        quality_layout = wx.StaticBoxSizer(self.quality_frame, wx.HORIZONTAL)
        self.quality = wx.Slider(self, minValue=1, maxValue=100, value=85, style=wx.SL_HORIZONTAL)
        quality_layout.Add(wx.StaticText(self, label="Quality:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        quality_layout.Add(self.quality, 1, wx.EXPAND | wx.ALL, 5)
        self.quality_label = wx.StaticText(self, label="85")
        quality_layout.Add(self.quality_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.quality.Bind(wx.EVT_SLIDER, lambda event: self.quality_label.SetLabel(str(self.quality.GetValue())))
        main_layout.Add(quality_layout, 0, wx.EXPAND | wx.ALL, 5)

        # Size frame
        self.size_frame = wx.StaticBox(self, label="Size Settings")
        size_layout = wx.StaticBoxSizer(self.size_frame, wx.HORIZONTAL)
        self.width = wx.TextCtrl(self)
        self.height = wx.TextCtrl(self)
        self.maintain_ratio = wx.CheckBox(self, label="Maintain Aspect Ratio")
        self.maintain_ratio.SetValue(True)
        size_layout.Add(wx.StaticText(self, label="Width:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        size_layout.Add(self.width, 1, wx.EXPAND | wx.ALL, 5)
        size_layout.Add(wx.StaticText(self, label="Height:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        size_layout.Add(self.height, 1, wx.EXPAND | wx.ALL, 5)
        size_layout.Add(self.maintain_ratio, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        main_layout.Add(size_layout, 0, wx.EXPAND | wx.ALL, 5)

        # Process button
        process_btn = wx.Button(self, label="Process Image")
        process_btn.Bind(wx.EVT_BUTTON, self.process_image)
        main_layout.Add(process_btn, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.SetSizer(main_layout)
        self.update_ui()

    def update_ui(self):
        tool = self.tool_type.GetStringSelection().lower()
        # Show/hide frames based on tool type
        if tool in ['compress']:
            self.quality_frame.Show()
            self.size_frame.Hide()
        elif tool in ['resize', 'upscale']:
            self.quality_frame.Show()
            self.size_frame.Show()
        else:
            self.quality_frame.Hide()
            self.size_frame.Hide()
        self.Layout()

    def browse_input(self, event):
        with wx.FileDialog(self, "Select Input Image", wildcard="Image files (*.png;*.jpg;*.jpeg;*.bmp;*.tiff;*.webp)", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            self.input_path.SetValue(fileDialog.GetPath())
            if not self.output_path.GetValue():
                self.suggest_output_path(fileDialog.GetPath())

    def browse_output(self, event):
        tool = self.tool_type.GetStringSelection().lower()
        wildcard = "Icon files (*.ico)" if tool == "ico" else "PNG files (*.png);;JPEG files (*.jpg)"
        with wx.FileDialog(self, "Select Output File", wildcard=wildcard, style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            self.output_path.SetValue(fileDialog.GetPath())

    def suggest_output_path(self, input_path):
        tool = self.tool_type.GetStringSelection().lower()
        base_name = os.path.splitext(input_path)[0]
        
        if tool == "ico":
            self.output_path.SetValue(f"{base_name}.ico")
        elif tool == "rembg":
            self.output_path.SetValue(f"{base_name}_nobg.png")
        elif tool == "compress":
            self.output_path.SetValue(f"{base_name}_compressed.jpg")
        elif tool in ["resize", "upscale"]:
            self.output_path.SetValue(f"{base_name}_resized.png")
        else:
            self.output_path.SetValue(f"{base_name}_converted.png")

    def process_image(self, event):
        input_path = self.input_path.GetValue()
        output_path = self.output_path.GetValue()
        tool = self.tool_type.GetStringSelection().lower()

        if not input_path or not output_path:
            wx.MessageBox("Please select both input and output files", "Error", wx.OK | wx.ICON_ERROR)
            return

        try:
            if tool == "convert":
                self.convert_image(input_path, output_path)
            elif tool == "compress":
                self.compress_image(input_path, output_path)
            elif tool == "resize":
                self.resize_image(input_path, output_path)
            elif tool == "rembg":
                self.remove_background(input_path, output_path)
            elif tool == "ico":
                self.convert_to_ico(input_path, output_path)
            elif tool == "upscale":
                self.upscale_image(input_path, output_path)

            wx.MessageBox("Image processed successfully!", "Success", wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            wx.MessageBox(f"An error occurred: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)

    def convert_image(self, input_path, output_path):
        with Image.open(input_path) as img:
            if img.mode in ('RGBA', 'LA'):
                background = Image.new('RGB', img.size, 'white')
                background.paste(img, mask=img.split()[-1])
                background.save(output_path, quality=95)
            else:
                img.convert('RGB').save(output_path, quality=95)

    def compress_image(self, input_path, output_path):
        quality = self.quality.GetValue()
        with Image.open(input_path) as img:
            img.save(output_path, quality=quality, optimize=True)

    def resize_image(self, input_path, output_path):
        try:
            width = int(self.width.GetValue()) if self.width.GetValue() else None
            height = int(self.height.GetValue()) if self.height.GetValue() else None
        except ValueError:
            wx.MessageBox("Please enter valid numbers for width and height", "Error", wx.OK | wx.ICON_ERROR)
            return

        if not width and not height:
            wx.MessageBox("Please specify at least one dimension", "Error", wx.OK | wx.ICON_ERROR)
            return

        with Image.open(input_path) as img:
            if self.maintain_ratio.GetValue():
                if width and height:
                    img.thumbnail((width, height), Image.Resampling.LANCZOS)
                elif width:
                    ratio = width / img.size[0]
                    height = int(img.size[1] * ratio)
                    img = img.resize((width, height), Image.Resampling.LANCZOS)
                else:
                    ratio = height / img.size[1]
                    width = int(img.size[0] * ratio)
                    img = img.resize((width, height), Image.Resampling.LANCZOS)
            else:
                if not width:
                    width = img.size[0]
                if not height:
                    height = img.size[1]
                img = img.resize((width, height), Image.Resampling.LANCZOS)
            
            img.save(output_path, quality=self.quality.GetValue())

    def remove_background(self, input_path, output_path):
        with open(input_path, 'rb') as i:
            input_data = i.read()
            output_data = remove(input_data)
            img = Image.open(io.BytesIO(output_data))
            img.save(output_path)

    def convert_to_ico(self, input_path, output_path):
        sizes = [(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)]
        with Image.open(input_path) as img:
            img.save(output_path, format='ICO', sizes=sizes)

    def upscale_image(self, input_path, output_path):
        try:
            width = int(self.width.GetValue()) if self.width.GetValue() else None
            height = int(self.height.GetValue()) if self.height.GetValue() else None
        except ValueError:
            wx.MessageBox("Please enter valid numbers for width and height", "Error", wx.OK | wx.ICON_ERROR)
            return

        with Image.open(input_path) as img:
            if not width and not height:
                width = img.size[0] * 2
                height = img.size[1] * 2
            elif self.maintain_ratio.GetValue():
                if width:
                    ratio = width / img.size[0]
                    height = int(img.size[1] * ratio)
                else:
                    ratio = height / img.size[1]
                    width = int(img.size[0] * ratio)
            
            img = img.resize((width, height), Image.Resampling.LANCZOS)
            img.save(output_path, quality=self.quality.GetValue())
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageDraw, ImageTk, ImageFont
import logging
from udp_server import UDPServer
from command_parser import DisplayCommandParser


class DisplayDrawer:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.image = Image.new('RGB', (width, height), 'black')
        self.draw = ImageDraw.Draw(self.image)
        self.font = ImageFont.load_default()

    def rgb565_to_rgb888(self, color565):
        r = (color565 >> 11) & 0x1F
        g = (color565 >> 5) & 0x3F
        b = color565 & 0x1F
        
        r = (r * 255) // 31
        g = (g * 255) // 63
        b = (b * 255) // 31
        
        return (r, g, b)

    def clear_display(self):
        self.draw.rectangle([0, 0, self.width, self.height], fill='black')

    def draw_pixel(self, x, y, color):
        color = self.rgb565_to_rgb888(color)
        self.draw.point((x, y), fill=color)

    def draw_line(self, x0, y0, x1, y1, color):
        color = self.rgb565_to_rgb888(color)
        self.draw.line([(x0, y0), (x1, y1)], fill=color, width=2)

    def draw_rectangle(self, x0, y0, w, h, color, filled=False):
        color = self.rgb565_to_rgb888(color)
        if filled:
            self.draw.rectangle([x0, y0, x0 + w, y0 + h], fill=color)
        else:
            self.draw.rectangle([x0, y0, x0 + w, y0 + h], outline=color, width=2)

    def draw_circle(self, x0, y0, radius, color, filled=False):
        color = self.rgb565_to_rgb888(color)
        if filled:
            self.draw.ellipse([x0 - radius, y0 - radius, x0 + radius, y0 + radius], fill=color)
        else:
            self.draw.ellipse([x0 - radius, y0 - radius, x0 + radius, y0 + radius], outline=color, width=2)

    def draw_ellipse(self, x0, y0, w, h, color, filled=False):
        color = self.rgb565_to_rgb888(color)
        if filled:
            self.draw.ellipse([x0, y0, x0 + w, y0 + h], fill=color)
        else:
            self.draw.ellipse([x0, y0, x0 + w, y0 + h], outline=color, width=2)

    def draw_rounded_rectangle(self, x0, y0, w, h, radius, color, filled=False):
        color = self.rgb565_to_rgb888(color)
        if filled:
            self.draw.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=radius, fill=color)
        else:
            self.draw.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=radius, outline=color, width=2)

    def draw_text(self, x0, y0, text, color):
        color = self.rgb565_to_rgb888(color)
        self.draw.text((x0, y0), text, fill=color, font=self.font)

    def get_image(self):
        return self.image


class DisplayEmulator:
    def __init__(self, width=1024, height=768):
        self.width = width
        self.height = height

        # Налаштування UDP сервера
        self.HOST = '127.0.0.1'
        self.PORT = 12345

        # Ініціалізація парсера команд
        self.command_parser = DisplayCommandParser()
        
        # Створення головного вікна
        self.root = tk.Tk()
        self.root.title("Display Emulator")
        
        # Встановлення розміру вікна
        self.root.geometry(f"{width + 200}x{height}")  # +200 для панелі керування
        
        # Налаштування мінімального розміру вікна
        self.root.minsize(width + 200, height)
        
        # Ініціалізація DisplayDrawer
        self.display_drawer = DisplayDrawer(width, height)

        # Обробник закриття вікна
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Флаг для контролю роботи сервера
        self.running = True
        
         # Створення UDP сервера
        self.udp_server = UDPServer(self.HOST, self.PORT, self.handle_udp_command)
        self.udp_server.start()

        # Словник для зберігання доступних команд
        self.commands = {
            "Clear Display": b'\x01\x00\x00',
            "Draw Pixel": b'\x02\x00\x32\x00\x32\x0F\xFF',
            "Draw Line": b'\x03\x00\x00\x00\x00\x00\x64\x00\x64\x0F\xFF',
            "Draw Rectangle": b'\x04\x00\x32\x00\x32\x00\x64\x00\x64\x0F\xFF',
            "Fill Rectangle": b'\x05\x00\x32\x00\x32\x00\x64\x00\x64\x0F\xFF',
            "Draw Ellipse": b'\x06\x00\x32\x00\x32\x00\x64\x00\x32\x0F\xFF',
            "Fill Ellipse": b'\x07\x00\x32\x00\x32\x00\x64\x00\x32\x0F\xFF',
            "Draw Circle": b'\x08\x00\x64\x00\x64\x00\x32\x0F\xFF',
            "Fill Circle ": b'\x09\x00\x64\x00\x64\x00\x32\x0F\xFF',
            "Draw Rounded Rectangle": b'\x0A\x00\x32\x00\x32\x00\x64\x00\x64\x00\x0A\x0F\xFF',
            "Fill Rounded Rectangle": b'\x0B\x00\x32\x00\x32\x00\x64\x00\x64\x00\x0A\x0F\xFF',
            "Draw Text": b'\x0C\x00\x32\x00\x32\xFF\xFF\x0C\x05Hello'
        }

        # Створення віджетів
        self.create_widgets()

    def create_widgets(self):
        # Головний контейнер
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Фрейм для канваса
        self.canvas_frame = ttk.Frame(main_container)
        self.canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Канвас для відображення зображення
        self.canvas = tk.Canvas(self.canvas_frame, width=self.width, height=self.height, bg='black')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Фрейм для контролів
        self.control_frame = ttk.Frame(main_container, width=190)  # Фіксована ширина панелі керування
        self.control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        self.control_frame.pack_propagate(False)  # Заборона зміни розміру фрейму
        
        # Заголовок панелі керування
        control_label = ttk.Label(self.control_frame, text="Control Panel", font=('Arial', 12, 'bold'))
        control_label.pack(pady=10)
        
        # Комбобокс для вибору команди
        command_label = ttk.Label(self.control_frame, text="Select Command:")
        command_label.pack(pady=(5, 0))
        
        self.command_var = tk.StringVar()
        self.command_combo = ttk.Combobox(self.control_frame, textvariable=self.command_var, width=25)
        self.command_combo['values'] = list(self.commands.keys())
        self.command_combo.pack(pady=5)
        
        # Кнопка виконання
        self.execute_button = ttk.Button(self.control_frame, text="Execute Command", 
                                       command=self.execute_command, width=20)
        self.execute_button.pack(pady=5)
        
        # Кнопка очищення
        self.clear_button = ttk.Button(self.control_frame, text="Clear Display", 
                                     command=self.clear_display, width=20)
        self.clear_button.pack(pady=5)
        
        # Додавання роздільника
        ttk.Separator(self.control_frame, orient='horizontal').pack(fill='x', pady=10)
        
        # Інформація про розмір дисплея
        size_info = ttk.Label(self.control_frame, 
                            text=f"Display Size:\n{self.width}x{self.height}",
                            justify=tk.CENTER)
        size_info.pack(pady=5)

    def handle_udp_command(self, command_data):
        """Обробка отриманих команд через UDP."""
        # Виконання команди в головному потоці GUI
        self.root.after(0, lambda: self.process_command(command_data))

    def execute_command(self):
        """
        Виконує команду, вибрану через GUI.
        Викликається при натисканні кнопки "Execute Command".
        """
        selected_command = self.command_var.get()
        if selected_command in self.commands:
            try:
                # Отримуємо байти команди
                command_bytes = self.commands[selected_command]
                logging.info(f"Executing {selected_command}: {command_bytes.hex()}")
            
                # Парсимо команду
                result = self.command_parser.parse(command_bytes)
            
                if result:
                    logging.info(f"Parsed command: {result}")
                    # Виконуємо команду
                    self.process_command(result)
                    # Оновлюємо дисплей
                    self.update_display()
                else:
                    logging.error(f"Failed to parse command: {selected_command}")
            except Exception as e:
                logging.error(f"Error executing command {selected_command}: {str(e)}")

    def process_command(self, command_data):
        command_id = command_data['command_id']
        
        if command_id == 0x01:  # Clear Display
            self.display_drawer.clear_display()
            
        elif command_id == 0x02:  # Draw Pixel
            x, y = command_data['x'], command_data['y']
            color = command_data['color']
            self.display_drawer.draw_pixel(x, y, color)
            
        elif command_id == 0x03:  # Draw Line
            x0, y0 = command_data['x0'], command_data['y0']
            x1, y1 = command_data['x1'], command_data['y1']
            color = command_data['color']
            self.display_drawer.draw_line(x0, y0, x1, y1, color)
            
        elif command_id == 0x04:  # Draw Rectangle
            x0, y0 = command_data['x0'], command_data['y0']
            w, h = command_data['w'], command_data['h']
            color = command_data['color']
            self.display_drawer.draw_rectangle(x0, y0, w, h, color)
            
        elif command_id == 0x05:  # Fill Rectangle
            x0, y0 = command_data['x0'], command_data['y0']
            w, h = command_data['w'], command_data['h']
            color = command_data['color']
            self.display_drawer.draw_rectangle(x0, y0, w, h, color, filled=True)

        elif command_id in (0x06, 0x07):  # DrawEllipse, FillEllipse
            x0, y0 = command_data['x0'], command_data['y0']
            radius_x, radius_y = command_data['radius_x'], command_data['radius_y']
            color = command_data['color']
            filled = command_id == 0x07
            self.display_drawer.draw_ellipse(x0, y0, radius_x, radius_y, color, filled)

        elif command_id in (0x08, 0x09):  # Draw/Fill Circle
            x0, y0 = command_data['x0'], command_data['y0']
            radius = command_data['radius']
            color = command_data['color']
            self.display_drawer.draw_circle(x0, y0, radius, color, filled=(command_id == 0x09))

        elif command_id in (0x0A, 0x0B):  # DrawRoundedRectangle, FillRoundedRectangle
            x0, y0 = command_data['x0'], command_data['y0']
            w, h = command_data['w'], command_data['h']
            radius = command_data['radius']
            color = command_data['color']
            filled = command_id == 0x0B
            self.display_drawer.draw_rounded_rectangle(x0, y0, w, h, radius, color, filled)

        elif command_id == 0x0C:  # Draw Text
            x0, y0 = command_data['x0'], command_data['y0']
            text = command_data['text']
            color = command_data['color']
            self.display_drawer.draw_text(x0, y0, text, color)

        self.update_display()

    def clear_display(self):
        self.display_drawer.clear_display()
        self.update_display()

    def update_display(self):
        image = self.display_drawer.get_image()
        image_tk = ImageTk.PhotoImage(image)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=image_tk)
        self.canvas._image = image_tk

    def on_closing(self):
        """Обробник закриття вікна"""
        self.udp_server.stop()  
        self.root.quit()
        self.root.destroy()

    def run(self):
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.on_closing()
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
        finally:
            self.running = False

if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO, 
                          format='%(asctime)s - %(levelname)s - %(message)s')
        emulator = DisplayEmulator()
        emulator.run()
    except Exception as e:
        logging.error(f"Fatal error: {str(e)}")
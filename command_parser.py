import struct
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Command:
    def __init__(self, command_id):
        self.id = command_id

    @staticmethod
    def parse_color(params):
        if len(params) != 2:
            raise ValueError("Invalid color format")
        return struct.unpack(">H", params)[0]


class ClearDisplayCommand(Command):
    def __init__(self, params):
        super().__init__(0x01)
        self.color = self.parse_color(params)
    
    def execute(self):
        logger.info(f"Clear display with color: RGB565({self.color})")
        return {"color": self.color}


class DrawPixelCommand(Command):
    def __init__(self, params):
        super().__init__(0x02)
        self.x, self.y = struct.unpack(">hh", params[:4])
        self.color = self.parse_color(params[4:])
    
    def execute(self):
        logger.info(f"Draw pixel at ({self.x}, {self.y}) with color RGB565({self.color})")
        return {"x": self.x, "y": self.y, "color": self.color}


class DrawLineCommand(Command):
    def __init__(self, params):
        super().__init__(0x03)
        self.x0, self.y0, self.x1, self.y1 = struct.unpack(">hhhh", params[:8])
        self.color = self.parse_color(params[8:])
    
    def execute(self):
        logger.info(f"Draw line from ({self.x0}, {self.y0}) to ({self.x1}, {self.y1}) with color RGB565({self.color})")
        return {"x0": self.x0, "y0": self.y0, "x1": self.x1, "y1": self.y1, "color": self.color}


class DrawRectangleCommand(Command):
    def __init__(self, params):
        super().__init__(0x04)
        self.x0, self.y0, self.w, self.h = struct.unpack(">hhhh", params[:8])
        self.color = self.parse_color(params[8:])
    
    def execute(self):
        logger.info(f"Draw rectangle at ({self.x0}, {self.y0}), width {self.w}, height {self.h}, with color RGB565({self.color})")
        return {"x0": self.x0, "y0": self.y0, "w": self.w, "h": self.h, "color": self.color}


class FillRectangleCommand(Command):
    def __init__(self, params):
        super().__init__(0x05)
        self.x0, self.y0, self.w, self.h = struct.unpack(">hhhh", params[:8])
        self.color = self.parse_color(params[8:])
    
    def execute(self):
        logger.info(f"Fill rectangle at ({self.x0}, {self.y0}), width {self.w}, height {self.h}, with color RGB565({self.color})")
        return {"x0": self.x0, "y0": self.y0, "w": self.w, "h": self.h, "color": self.color}


class DrawEllipseCommand(Command):
    def __init__(self, params):
        super().__init__(0x06)
        self.x0, self.y0, self.radius_x, self.radius_y = struct.unpack(">hhhh", params[:8])
        self.color = self.parse_color(params[8:])
    
    def execute(self):
        logger.info(f"Draw ellipse at ({self.x0}, {self.y0}), radius-x {self.radius_x}, radius-y {self.radius_y}, with color RGB565({self.color})")
        return {"x0": self.x0, "y0": self.y0, "radius_x": self.radius_x, "radius_y": self.radius_y, "color": self.color}


class FillEllipseCommand(Command):
    def __init__(self, params):
        super().__init__(0x07)
        self.x0, self.y0, self.radius_x, self.radius_y = struct.unpack(">hhhh", params[:8])
        self.color = self.parse_color(params[8:])
    
    def execute(self):
        logger.info(f"Fill ellipse at ({self.x0}, {self.y0}), radius-x {self.radius_x}, radius-y {self.radius_y}, with color RGB565({self.color})")
        return {"x0": self.x0, "y0": self.y0, "radius_x": self.radius_x, "radius_y": self.radius_y, "color": self.color}


class DrawCircleCommand(Command):
    def __init__(self, params):
        super().__init__(0x08)
        self.x0, self.y0, self.radius = struct.unpack(">hhH", params[:6])
        self.color = self.parse_color(params[6:])
    
    def execute(self):
        logger.info(f"Draw circle at ({self.x0}, {self.y0}), radius {self.radius}, with color RGB565({self.color})")
        return {"x0": self.x0, "y0": self.y0, "radius": self.radius, "color": self.color}


class FillCircleCommand(Command):
    def __init__(self, params):
        super().__init__(0x09)
        self.x0, self.y0, self.radius = struct.unpack(">hhH", params[:6])
        self.color = self.parse_color(params[6:])
    
    def execute(self):
        logger.info(f"Fill circle at ({self.x0}, {self.y0}), radius {self.radius}, with color RGB565({self.color})")
        return {"x0": self.x0, "y0": self.y0, "radius": self.radius, "color": self.color}


class DrawRoundedRectangleCommand(Command):
    def __init__(self, params):
        super().__init__(0x0A)
        self.x0, self.y0, self.w, self.h = struct.unpack(">hhhh", params[:8])
        self.radius = struct.unpack(">H", params[8:10])[0]
        self.color = self.parse_color(params[10:])
    
    def execute(self):
        logger.info(f"Draw rounded rectangle at ({self.x0}, {self.y0}), width {self.w}, height {self.h}, radius {self.radius}, with color RGB565({self.color})")
        return {"x0": self.x0, "y0": self.y0, "w": self.w, "h": self.h, "radius": self.radius, "color": self.color}


class FillRoundedRectangleCommand(Command):
    def __init__(self, params):
        super().__init__(0x0B)
        self.x0, self.y0, self.w, self.h = struct.unpack(">hhhh", params[:8])
        self.radius = struct.unpack(">H", params[8:10])[0]
        self.color = self.parse_color(params[10:])
    
    def execute(self):
        logger.info(f"Fill rounded rectangle at ({self.x0}, {self.y0}), width {self.w}, height {self.h}, radius {self.radius}, with color RGB565({self.color})")
        return {"x0": self.x0, "y0": self.y0, "w": self.w, "h": self.h, "radius": self.radius, "color": self.color}


class DrawTextCommand(Command):
    def __init__(self, params):
        super().__init__(0x0C)
        logger.info(f"Initializing DrawTextCommand with params: {params.hex()}")
        if len(params) < 8:
            raise ValueError("Insufficient bytes for Draw Text command.")
        
        self.x0, self.y0 = struct.unpack(">hh", params[:4])
        self.color = self.parse_color(params[4:6])
        self.font_number = params[6]
        self.length = params[7]
        
        logger.info(f"Parsed values: x0={self.x0}, y0={self.y0}, color={self.color}, font={self.font_number}, length={self.length}")
        
        if len(params) < 8 + self.length:
            raise ValueError(f"Insufficient bytes for text data. Expected {8 + self.length}, got {len(params)}")
        
        self.text = params[8:8 + self.length].decode('utf-8', errors='ignore')
        logger.info(f"Decoded text: {self.text}")

    def execute(self):
        logger.info(f"Draw text '{self.text}' at ({self.x0}, {self.y0}) with color RGB565({self.color}), font {self.font_number}")
        return {
            "x0": self.x0,
            "y0": self.y0,
            "color": self.color,
            "font_number": self.font_number,
            "text": self.text
        }


class DisplayCommandParser:
    logger = logging.getLogger('command_parser')
    
    def __init__(self):
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

        self.commands = {
            0x01: ClearDisplayCommand,
            0x02: DrawPixelCommand,
            0x03: DrawLineCommand,
            0x04: DrawRectangleCommand,
            0x05: FillRectangleCommand,
            0x06: DrawEllipseCommand,
            0x07: FillEllipseCommand,
            0x08: DrawCircleCommand,
            0x09: FillCircleCommand,
            0x0A: DrawRoundedRectangleCommand,
            0x0B: FillRoundedRectangleCommand,
            0x0C: DrawTextCommand
        }

        # Очікувана кількість байтів для кожної команди
        self.expected_lengths = {
            0x01: 2,   
            0x02: 6,   
            0x03: 10,  
            0x04: 10,  
            0x05: 10,  
            0x06: 10,  
            0x07: 10, 
            0x08: 8,   
            0x09: 8,   
            0x0A: 12,  
            0x0B: 12, 
            0x0C: None, 
        }

    
    def parse(self, byte_array):
        self.logger.info(f"Received byte array: {byte_array.hex()}")
        if not byte_array:
            raise ValueError("Byte array is empty")
        command_id = byte_array[0]
        params = byte_array[1:]
        self.logger.info(f"Command ID: {command_id}, Params: {params.hex()}")

        if command_id not in self.commands:
            self.logger.warning(f"Unknown command ID: {command_id}")
            return None

        if command_id == 0x0C:  
            self.logger.info(f"Processing Draw Text command. Params length: {len(params)}")
            if len(params) < 8:
                self.logger.error(f"Invalid number of parameters for command ID {command_id}: expected at least 8, got {len(params)}")
                return None
            text_length = params[7]
            self.logger.info(f"Text length from params: {text_length}")
            expected_length = 8 + text_length
            self.logger.info(f"Expected total length: {expected_length}")
            if len(params) < expected_length:
                self.logger.error(f"Invalid number of parameters for command ID {command_id}: expected {expected_length}, got {len(params)}")
                return None
            self.logger.info("Draw Text command validation passed")
        else:
            expected_length = self.expected_lengths.get(command_id)
            if expected_length is not None and len(params) != expected_length:
                self.logger.error(f"Invalid number of parameters for command ID {command_id}: expected {expected_length}, got {len(params)}")
                return None

        command_class = self.commands[command_id]
        try:
            command_instance = command_class(params)
            result = command_instance.execute()
            result['command_id'] = command_id
            return result
        except Exception as e:
            self.logger.error(f"Error executing command {command_id}: {str(e)}", exc_info=True)
            return None
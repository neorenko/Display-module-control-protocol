import struct
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Command:
    def __init__(self, command_id, **kwargs):
        self.id = command_id
        for key, value in kwargs.items():
            setattr(self, key, value)


class DisplayCommandParser:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(handler)

        self.commands = {
            0x01: self._clear_display,
            0x02: self._draw_pixel,
            0x03: self._draw_line,
            0x04: self._draw_rectangle,
            0x05: self._fill_rectangle,
            0x06: self._draw_ellipse,
            0x07: self._fill_ellipse,
            0x08: self._draw_circle,
            0x09: self._fill_circle,
            0xA: self._draw_rounded_rectangle,
            0xB: self._fill_rounded_rectangle,
            0xC: self._draw_text
        }



    def parse(self, byte_array):
        if not byte_array:
            raise ValueError("Byte array is empty")
        command_id = byte_array[0]
        params = byte_array[1:]
        if command_id in self.commands:
            try:
                result = self.commands[command_id](params)
                return Command(command_id, **result)
            except ValueError as e:
                raise e
        else:
            raise ValueError(f"Unknown command ID: {command_id}")

   
        
    def _clear_display(self, params):
        if len(params) != 2:
            raise ValueError("Invalid parameters for Clear Display")
        color = self._parse_color(params)
        logger.info(f"Clear display with color: RGB565({color})")
        return {"color": color}
    
    
    def _draw_pixel(self, params):
        if len(params) != 6:
            raise ValueError("Invalid parameters for Draw Pixel")
        x, y = struct.unpack(">hh", params[:4])
        color = self._parse_color(params[4:])
        logger.info(f"Draw pixel at ({x}, {y}) with color RGB565({color})")
        return {"x": x, "y": y, "color": color}
    

    def _draw_line(self, params):
        if len(params) != 10:
            raise ValueError("Invalid parameters for Draw Line")
        x0, y0, x1, y1 = struct.unpack(">hhhh", params[:8])
        color = self._parse_color(params[8:])
        logger.info(f"Draw line from ({x0}, {y0}) to ({x1}, {y1}) with color RGB565({color})")
        return {"x0": x0, "y0": y0, "x1": x1, "y1": y1, "color": color}
    

    def _draw_rectangle(self, params):
        if len(params) != 10:
            raise ValueError("Invalid parameters for Draw Rectangle")
        x0, y0, w, h = struct.unpack(">hhhh", params[:8])
        color = self._parse_color(params[8:])
        logger.info(f"Draw rectangle at ({x0}, {y0}), width {w}, height {h}, with color RGB565({color})")
        return {"x0": x0, "y0": y0, "w": w, "h": h, "color": color}
    

    def _fill_rectangle(self, params):
        if len(params) != 10:
            raise ValueError("Invalid parameters for Fill Rectangle")
        x0, y0, w, h = struct.unpack(">hhhh", params[:8])
        color = self._parse_color(params[8:])
        logger.info(f"Fill rectangle at ({x0}, {y0}), width {w}, height {h}, with color RGB565({color})")
        return {"x0": x0, "y0": y0, "w": w, "h": h, "color": color}
    

    def _draw_ellipse(self, params):
        if len(params) != 10:
            raise ValueError("Invalid parameters for Draw Ellipse")
        x0, y0, radius_x, radius_y = struct.unpack(">hhhh", params[:8])
        color = self._parse_color(params[8:])
        logger.info(f"Draw ellipse at ({x0}, {y0}), radius-x {radius_x}, radius-y {radius_y}, with color RGB565({color})")
        return {"x0": x0, "y0": y0, "radius_x": radius_x, "radius_y": radius_y, "color": color}
    

    def _fill_ellipse(self, params):
        if len(params) != 10:
            raise ValueError("Invalid parameters for Fill Ellipse")
        x0, y0, radius_x, radius_y = struct.unpack(">hhhh", params[:8])
        color = self._parse_color(params[8:])
        logger.info(f"Fill ellipse at ({x0}, {y0}), radius-x {radius_x}, radius-y {radius_y}, with color RGB565({color})")
        return {"x0": x0, "y0": y0, "radius_x": radius_x, "radius_y": radius_y, "color": color}
    

    def _draw_circle(self, params):
        if len(params) != 8:
            raise ValueError("Invalid parameters for Draw Circle")
        x0, y0, radius = struct.unpack(">hhH", params[:6])
        color = self._parse_color(params[6:])
        logger.info(f"Draw circle at ({x0}, {y0}), radius {radius}, with color RGB565({color})")
        return {"x0": x0, "y0": y0, "radius": radius, "color": color}
    

    def _fill_circle(self, params):
        if len(params) != 8:
            raise ValueError("Invalid parameters for Fill Circle")
        x0, y0, radius = struct.unpack(">hhH", params[:6])
        color = self._parse_color(params[6:])
        logger.info(f"Fill circle at ({x0}, {y0}), radius {radius}, with color RGB565({color})")
        return {"x0": x0, "y0": y0, "radius": radius, "color": color}


    def _draw_rounded_rectangle(self, params):
        if len(params) != 12:
            raise ValueError("Invalid parameters for Draw Rounded Rectangle")
        x0, y0, w, h = struct.unpack(">hhhh", params[:8])
        radius = struct.unpack(">H", params[8:10])[0]
        color = self._parse_color(params[10:])
        logger.info(f"Draw rounded rectangle at ({x0}, {y0}), width {w}, height {h}, radius {radius}, with color RGB565({color})")
        return {"x0": x0, "y0": y0, "w": w, "h": h, "radius": radius, "color": color}


    def _fill_rounded_rectangle(self, params):
        if len(params) != 12:
            raise ValueError("Invalid parameters for Fill Rounded Rectangle")
        x0, y0, w, h = struct.unpack(">hhhh", params[:8])
        radius = struct.unpack(">H", params[8:10])[0]
        color = self._parse_color(params[10:])
        logger.info(f"Fill rounded rectangle at ({x0}, {y0}), width {w}, height {h}, radius {radius}, with color RGB565({color})")
        return {"x0": x0, "y0": y0, "w": w, "h": h, "radius": radius, "color": color}
    

    def _draw_text(self, params):
        if len(params) < 8:
            raise ValueError("Invalid parameters for Draw Text")
        x0, y0 = struct.unpack(">hh", params[:4])
        color = self._parse_color(params[4:6])
        font_number = params[6]
        length = params[7]
        text = params[8:8 + length].decode('utf-8')
        logger.info(f"Draw text '{text}' at ({x0}, {y0}) with color RGB565({color}), font number {font_number}")
        return {"x0": x0, "y0": y0, "color": color, "font_number": font_number, "text": text}


    def _parse_color(self, params):
        if len(params) < 2:
            raise ValueError("Invalid color format")
        return struct.unpack(">H", params)[0]
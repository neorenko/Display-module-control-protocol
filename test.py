import struct
import unittest
from command_parser import DisplayCommandParser, logger  

class TestDisplayCommandParser(unittest.TestCase):

    def setUp(self):
        self.parser = DisplayCommandParser()


    def test_unknown_command(self):
        byte_array = bytearray([0xFF])  
        with self.assertRaises(ValueError) as context:
            self.parser.parse(byte_array)
        self.assertEqual(str(context.exception), "Unknown command ID: 255")


    def test_clear_display_correct(self):
        byte_array = bytearray([0x01, 0xFF, 0xFF])
        with self.assertLogs(logger, level='INFO') as log:
            command = self.parser.parse(byte_array)
            self.assertEqual(command.id, 0x01)
            self.assertEqual(command.color, 0xFFFF)
            self.assertIn("Clear display with color: RGB565(65535)", log.output[0])


    def test_clear_display_incorrect_params(self):
        byte_array = bytearray([0x01])  
        with self.assertRaises(ValueError) as context:
            self.parser.parse(byte_array)
        self.assertEqual(str(context.exception), "Invalid parameters for Clear Display")


    def test_draw_pixel_correct(self):
        byte_array = bytearray([0x02, 0x00, 0x10, 0x00, 0x20, 0xFF, 0xFF])  # ID команди, x=16, y=32, color=0xFFFF
        with self.assertLogs(logger, level='INFO') as log:
            command = self.parser.parse(byte_array)
            self.assertEqual(command.id, 0x02)
            self.assertEqual(command.x, 16)
            self.assertEqual(command.y, 32)
            self.assertEqual(command.color, 0xFFFF)
            self.assertIn("Draw pixel at (16, 32) with color RGB565(65535)", log.output[0])

        
    def test_draw_pixel_incorrect_params(self):
        byte_array = bytearray([0x02, 0x00, 0x10, 0x00, 0x20])  
        with self.assertRaises(ValueError) as context:
            self.parser.parse(byte_array)
        self.assertEqual(str(context.exception), "Invalid parameters for Draw Pixel")    

    
    def test_invalid_color_format(self):
        byte_array = bytearray([0x02, 0x00, 0x10, 0x00, 0x20, 0xFF])  
        with self.assertRaises(ValueError) as context:
            self.parser.parse(byte_array)
            self.assertEqual(str(context.exception), "Invalid parameters for Draw Pixel")


    def test_draw_line_correct(self):
        byte_array = bytearray([0x03, 0x00, 0x10, 0x00, 0x20, 0x00, 0x30, 0x00, 0x40, 0xFF, 0xFF])  # ID команди, x0=16, y0=32, x1=48, y1=64, color=0xFFFF
        with self.assertLogs(logger, level='INFO') as log:
            command = self.parser.parse(byte_array)
            self.assertEqual(command.id, 0x03)
            self.assertEqual(command.x0, 16)
            self.assertEqual(command.y0, 32)
            self.assertEqual(command.x1, 48)
            self.assertEqual(command.y1, 64)
            self.assertEqual(command.color, 0xFFFF)
            self.assertIn("Draw line from (16, 32) to (48, 64) with color RGB565(65535)", log.output[0])


    def test_draw_line_incorrect_params(self):
        byte_array = bytearray([0x03, 0x00, 0x10, 0x00, 0x20, 0x00, 0x30])  
        with self.assertRaises(ValueError) as context:
            self.parser.parse(byte_array)
        self.assertEqual(str(context.exception), "Invalid parameters for Draw Line")

    
    def test_draw_rectangle_correct(self):
        byte_array = bytearray([0x04, 0x00, 0x10, 0x00, 0x20, 0x00, 0x30, 0x00, 0x40, 0xFF, 0xFF])  # ID команди, x0=16, y0=32, w=48, h=64, color=0xFFFF
        with self.assertLogs(logger, level='INFO') as log:
            command = self.parser.parse(byte_array)
            self.assertEqual(command.id, 0x04)
            self.assertEqual(command.x0, 16)
            self.assertEqual(command.y0, 32)
            self.assertEqual(command.w, 48)
            self.assertEqual(command.h, 64)
            self.assertEqual(command.color, 0xFFFF)
            self.assertIn("Draw rectangle at (16, 32), width 48, height 64, with color RGB565(65535)", log.output[0])


    def test_draw_rectangle_incorrect_params(self):
        byte_array = bytearray([0x04, 0x00, 0x10, 0x00, 0x20, 0x00, 0x30])  
        with self.assertRaises(ValueError) as context:
            self.parser.parse(byte_array)
        self.assertEqual(str(context.exception), "Invalid parameters for Draw Rectangle")


    def test_fill_rectangle_correct(self):
        byte_array = bytearray([0x05, 0x00, 0x10, 0x00, 0x20, 0x00, 0x30, 0x00, 0x40, 0xFF, 0xFF])  # ID команди, x0=16, y0=32, w=48, h=64, color=0xFFFF
        with self.assertLogs(logger, level='INFO') as log:
            command = self.parser.parse(byte_array)
            self.assertEqual(command.id, 0x05)
            self.assertEqual(command.x0, 16)
            self.assertEqual(command.y0, 32)
            self.assertEqual(command.w, 48)
            self.assertEqual(command.h, 64)
            self.assertEqual(command.color, 0xFFFF)
            self.assertIn("Fill rectangle at (16, 32), width 48, height 64, with color RGB565(65535)", log.output[0])
    

    def test_fill_rectangle_incorrect_params(self):
        byte_array = bytearray([0x05, 0x00, 0x10, 0x00, 0x20, 0x00, 0x30])  
        with self.assertRaises(ValueError) as context:
            self.parser.parse(byte_array)
        self.assertEqual(str(context.exception), "Invalid parameters for Fill Rectangle")


    def test_draw_ellipse_correct(self):
        byte_array = bytearray([0x06, 0x00, 0x10, 0x00, 0x20, 0x00, 0x30, 0x00, 0x40, 0xFF, 0xFF])  # ID команди, x0=16, y0=32, radius_x=48, radius_y=64, color=0xFFFF
        with self.assertLogs(logger, level='INFO') as log:
            command = self.parser.parse(byte_array)
            self.assertEqual(command.id, 0x06)
            self.assertEqual(command.x0, 16)
            self.assertEqual(command.y0, 32)
            self.assertEqual(command.radius_x, 48)
            self.assertEqual(command.radius_y, 64)
            self.assertEqual(command.color, 0xFFFF)
            self.assertIn("Draw ellipse at (16, 32), radius-x 48, radius-y 64, with color RGB565(65535)", log.output[0])


    def test_draw_ellipse_incorrect_params(self):
        byte_array = bytearray([0x06, 0x00, 0x10, 0x00, 0x20, 0x00, 0x30])  
        with self.assertRaises(ValueError) as context:
            self.parser.parse(byte_array)
        self.assertEqual(str(context.exception), "Invalid parameters for Draw Ellipse")


    def test_fill_ellipse_correct(self):
        byte_array = bytearray([0x07, 0x00, 0x10, 0x00, 0x20, 0x00, 0x30, 0x00, 0x40, 0xFF, 0xFF])  # ID команди, x0=16, y0=32, radius_x=48, radius_y=64, color=0xFFFF
        with self.assertLogs(logger, level='INFO') as log:
            command = self.parser.parse(byte_array)
            self.assertEqual(command.id, 0x07)
            self.assertEqual(command.x0, 16)
            self.assertEqual(command.y0, 32)
            self.assertEqual(command.radius_x, 48)
            self.assertEqual(command.radius_y, 64)
            self.assertEqual(command.color, 0xFFFF)
            self.assertIn("Fill ellipse at (16, 32), radius-x 48, radius-y 64, with color RGB565(65535)", log.output[0])


    def test_fill_ellipse_incorrect_params(self):
        byte_array = bytearray([0x07, 0x00, 0x10, 0x00, 0x20, 0x00, 0x30])  
        with self.assertRaises(ValueError) as context:
            self.parser.parse(byte_array)
        self.assertEqual(str(context.exception), "Invalid parameters for Fill Ellipse")


    def test_draw_circle_correct(self):
        byte_array = bytearray([0x08, 0x00, 0x10, 0x00, 0x20, 0x00, 0x30, 0xFF, 0xFF])  # ID команди, x0=16, y0=32, radius=48, color=0xFFFF
        with self.assertLogs(logger, level='INFO') as log:
            command = self.parser.parse(byte_array)
            self.assertEqual(command.id, 0x08)
            self.assertEqual(command.x0, 16)
            self.assertEqual(command.y0, 32)
            self.assertEqual(command.radius, 48)
            self.assertEqual(command.color, 0xFFFF)
            self.assertIn("Draw circle at (16, 32), radius 48, with color RGB565(65535)", log.output[0])


    def test_draw_circle_incorrect_params(self):
        byte_array = bytearray([0x08, 0x00, 0x10, 0x00, 0x20])  
        with self.assertRaises(ValueError) as context:
            self.parser.parse(byte_array)
        self.assertEqual(str(context.exception), "Invalid parameters for Draw Circle")


    def test_fill_circle_correct(self):
        byte_array = bytearray([0x09, 0x00, 0x10, 0x00, 0x20, 0x00, 0x30, 0xFF, 0xFF])  # ID команди, x0=16, y0=32, radius=48, color=0xFFFF
        with self.assertLogs(logger, level='INFO') as log:
            command = self.parser.parse(byte_array)
            self.assertEqual(command.id, 0x09)
            self.assertEqual(command.x0, 16)
            self.assertEqual(command.y0, 32)
            self.assertEqual(command.radius, 48)
            self.assertEqual(command.color, 0xFFFF)
            self.assertIn("Fill circle at (16, 32), radius 48, with color RGB565(65535)", log.output[0])
    

    def test_fill_circle_incorrect_params(self):
        byte_array = bytearray([0x09, 0x00, 0x10, 0x00, 0x20])  
        with self.assertRaises(ValueError) as context:
            self.parser.parse(byte_array)
        self.assertEqual(str(context.exception), "Invalid parameters for Fill Circle")


    def test_draw_rounded_rectangle_correct(self):
        byte_array = bytearray([0x0A, 0x00, 0x10, 0x00, 0x20, 0x00, 0x30, 0x00, 0x40, 0x00, 0x05, 0xFF, 0xFF])  # ID команди, x0=16, y0=32, w=48, h=64, radius=5, color=0xFFFF
        with self.assertLogs(logger, level='INFO') as log:
            command = self.parser.parse(byte_array)
            self.assertEqual(command.id, 0x0A)
            self.assertEqual(command.x0, 16)
            self.assertEqual(command.y0, 32)
            self.assertEqual(command.w, 48)
            self.assertEqual(command.h, 64)
            self.assertEqual(command.radius, 5)
            self.assertEqual(command.color, 0xFFFF)
            self.assertIn("Draw rounded rectangle at (16, 32), width 48, height 64, radius 5, with color RGB565(65535)", log.output[0])


    def test_draw_rounded_rectangle_incorrect_params(self):
        byte_array = bytearray([0x0A, 0x00, 0x10, 0x00, 0x20, 0x00, 0x30])  
        with self.assertRaises(ValueError) as context:
            self.parser.parse(byte_array)
        self.assertEqual(str(context.exception), "Invalid parameters for Draw Rounded Rectangle") 


    def test_fill_rounded_rectangle_correct(self):
        byte_array = bytearray([0x0B, 0x00, 0x10, 0x00, 0x20, 0x00, 0x30, 0x00, 0x40, 0x00, 0x05, 0xFF, 0xFF])  # ID команди, x0=16, y0=32, w=48, h=64, radius=5, color=0xFFFF
        with self.assertLogs(logger, level='INFO') as log:
            command = self.parser.parse(byte_array)
            self.assertEqual(command.id, 0x0B)
            self.assertEqual(command.x0, 16)
            self.assertEqual(command.y0, 32)
            self.assertEqual(command.w, 48)
            self.assertEqual(command.h, 64)
            self.assertEqual(command.radius, 5)
            self.assertEqual(command.color, 0xFFFF)
            self.assertIn("Fill rounded rectangle at (16, 32), width 48, height 64, radius 5, with color RGB565(65535)", log.output[0])


    def test_fill_rounded_rectangle_incorrect_params(self):
        byte_array = bytearray([0x0B, 0x00, 0x10, 0x00, 0x20, 0x00, 0x30])  
        with self.assertRaises(ValueError) as context:
            self.parser.parse(byte_array)
        self.assertEqual(str(context.exception), "Invalid parameters for Fill Rounded Rectangle")      


    def test_draw_text_correct(self):
        text = "Hello"
        text_bytes = text.encode('utf-8')
        byte_array = bytearray([0x0C, 0x00, 0x10, 0x00, 0x20, 0xFF, 0xFF, 0x01, len(text_bytes)]) + bytearray(text_bytes)
        # ID команди, x0=16, y0=32, color=0xFFFF, font_number=1, text="Hello"
        with self.assertLogs(logger, level='INFO') as log:
            command = self.parser.parse(byte_array)
            self.assertEqual(command.id, 0x0C)
            self.assertEqual(command.x0, 16)
            self.assertEqual(command.y0, 32)
            self.assertEqual(command.color, 0xFFFF)
            self.assertEqual(command.font_number, 1)
            self.assertEqual(command.text, "Hello")
            self.assertIn("Draw text 'Hello' at (16, 32) with color RGB565(65535), font number 1", log.output[0])


    def test_draw_text_incorrect_params(self):
        byte_array = bytearray([0x0C, 0x00, 0x10, 0x00, 0x20])  
        with self.assertRaises(ValueError) as context:
            self.parser.parse(byte_array)
        self.assertEqual(str(context.exception), "Invalid parameters for Draw Text")

if __name__ == '__main__':
    unittest.main()


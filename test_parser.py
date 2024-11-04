import unittest
import logging
from command_parser import DisplayCommandParser

class TestDisplayCommandParser(unittest.TestCase):
    def setUp(self):
        self.parser = DisplayCommandParser()
        logging.getLogger('command_parser').handlers = []

    logging.getLogger('command_parser').handlers = []
    logging.basicConfig(level=logging.INFO)

    def test_clear_display(self):
        command = bytes([0x01, 0xFF, 0xFF])  
        result = self.parser.parse(command)
        self.assertEqual(result['command_id'], 0x01)
        self.assertEqual(result['color'], 0xFFFF)

    def test_clear_display_invalid_params(self):
        command = bytes([0x01, 0xFF])
        result = self.parser.parse(command)
        self.assertIsNone(result, "Parse result should be None for invalid number of parameters")

    def test_draw_pixel(self):
        command = bytes([0x02, 0x00, 0x64, 0x00, 0xC8, 0x07, 0xE0])  
        result = self.parser.parse(command)
        self.assertEqual(result['command_id'], 0x02)
        self.assertEqual(result['x'], 100)
        self.assertEqual(result['y'], 200)
        self.assertEqual(result['color'], 0x07E0)

    def test_draw_pixel_invalid_params(self):
        command = bytes([0x02, 0x00, 0x64, 0x00, 0xC8, 0x07, 0xE0, 0xFF])
        result = self.parser.parse(command)
        self.assertIsNone(result, "Parse result should be None for invalid color format")

    def test_draw_line(self):
        command = bytes([0x03, 0x00, 0x0A, 0x00, 0x14, 0x00, 0x32, 0x00, 0x3C, 0x07, 0xFF])  
        result = self.parser.parse(command)
        self.assertEqual(result['command_id'], 0x03)
        self.assertEqual(result['x0'], 10)
        self.assertEqual(result['y0'], 20)
        self.assertEqual(result['x1'], 50)
        self.assertEqual(result['y1'], 60)
        self.assertEqual(result['color'], 0x07FF)

    def test_draw_line_invalid_params(self):
        command = bytes([0x03, 0x00, 0x0A, 0x00, 0x14, 0x00, 0x32, 0x00, 0x3C])
        result = self.parser.parse(command)
        self.assertIsNone(result, "Parse result should be None for invalid number of parameters")

    def test_draw_rectangle(self):
        command = bytes([0x04, 0x00, 0x0A, 0x00, 0x14, 0x00, 0x64, 0x00, 0x32, 0x07, 0xE0])
        result = self.parser.parse(command)
        self.assertIsNotNone(result, "Parse result should not be None for valid command")
        self.assertEqual(result['command_id'], 0x04, "Command ID should be 0x04 for DrawRectangle")
        self.assertEqual(result['x0'], 10, "x0 should be 10")
        self.assertEqual(result['y0'], 20, "y0 should be 20")
        self.assertEqual(result['w'], 100, "Width should be 100")
        self.assertEqual(result['h'], 50, "Height should be 50")
        self.assertEqual(result['color'], 0x07E0, "Color should be 0x07E0 (green in RGB565)")

    def test_draw_rectangle_incorrect(self):
        command = bytes([0x04, 0x00, 0x0A, 0x00, 0x14, 0x00, 0x64, 0x00, 0x32])
        result = self.parser.parse(command)
        self.assertIsNone(result, "Parse result should be None for invalid number of parameters")

    def test_fill_rectangle(self):
        command = bytes([0x05, 0x00, 0x0F, 0x00, 0x19, 0x00, 0x50, 0x00, 0x3C, 0xF8, 0x00])
        result = self.parser.parse(command)
        self.assertIsNotNone(result, "Parse result should not be None for valid command")
        self.assertEqual(result['command_id'], 0x05, "Command ID should be 0x05 for FillRectangle")
        self.assertEqual(result['x0'], 15, "x0 should be 15")
        self.assertEqual(result['y0'], 25, "y0 should be 25")
        self.assertEqual(result['w'], 80, "Width should be 80")
        self.assertEqual(result['h'], 60, "Height should be 60")
        self.assertEqual(result['color'], 0xF800, "Color should be 0xF800 (red in RGB565)")

    def test_fill_rectangle_incorrect(self):
        command = bytes([0x05, 0x00, 0x0F, 0x00, 0x19, 0x00, 0x50, 0x00, 0x3C])
        result = self.parser.parse(command)
        self.assertIsNone(result, "Parse result should be None for invalid number of parameters")

    def test_draw_ellipse(self):
        command = bytes([0x06, 0x00, 0x64, 0x00, 0x64, 0x00, 0x32, 0x00, 0x1E, 0x84, 0x1F])
        result = self.parser.parse(command)
        self.assertIsNotNone(result, "Parse result should not be None for valid command")
        self.assertEqual(result['command_id'], 0x06, "Command ID should be 0x06 for DrawEllipse")
        self.assertEqual(result['x0'], 100, "x0 should be 100")
        self.assertEqual(result['y0'], 100, "y0 should be 100")
        self.assertEqual(result['radius_x'], 50, "radius_x should be 50")
        self.assertEqual(result['radius_y'], 30, "radius_y should be 30")
        self.assertEqual(result['color'], 0x841F, "Color should be 0x841F (purple in RGB565)")

    def test_draw_ellipse_incorrect(self):
        command = bytes([0x06, 0x00, 0x64, 0x00, 0x64, 0x00, 0x32, 0x00, 0x1E])
        result = self.parser.parse(command)
        self.assertIsNone(result, "Parse result should be None for invalid number of parameters")

    def test_fill_ellipse(self):
       command = bytes([0x07, 0x00, 0x96, 0x00, 0x78, 0x00, 0x46, 0x00, 0x28, 0x03, 0xEF])
       result = self.parser.parse(command)
       self.assertIsNotNone(result, "Parse result should not be None for valid command")
       self.assertEqual(result['command_id'], 0x07, "Command ID should be 0x07 for FillEllipse")
       self.assertEqual(result['x0'], 150, "x0 should be 150")
       self.assertEqual(result['y0'], 120, "y0 should be 120")
       self.assertEqual(result['radius_x'], 70, "radius_x should be 70")
       self.assertEqual(result['radius_y'], 40, "radius_y should be 40")
       self.assertEqual(result['color'], 0x03EF, "Color should be 0x03EF (cyan in RGB565)")

    def test_fill_ellipse_incorrect(self):
        command = bytes([0x07, 0x00, 0x96, 0x00, 0x78, 0x00, 0x46, 0x00, 0x28])
        result = self.parser.parse(command)
        self.assertIsNone(result, "Parse result should be None for invalid number of parameters")

    def test_draw_circle(self):
        command = bytes([0x08, 0x00, 0xC8, 0x00, 0x96, 0x00, 0x3C, 0x07, 0xE0])
        result = self.parser.parse(command)
        self.assertIsNotNone(result, "Parse result should not be None for valid command")
        self.assertEqual(result['command_id'], 0x08, "Command ID should be 0x08 for DrawCircle")
        self.assertEqual(result['x0'], 200, "x0 should be 200")
        self.assertEqual(result['y0'], 150, "y0 should be 150")
        self.assertEqual(result['radius'], 60, "radius should be 60")
        self.assertEqual(result['color'], 0x07E0, "Color should be 0x07E0 (green in RGB565)")

    def test_draw_circle_incorrect(self):
        command = bytes([0x08, 0x00, 0xC8, 0x00, 0x96, 0x00, 0x3C])
        result = self.parser.parse(command)
        self.assertIsNone(result, "Parse result should be None for invalid number of parameters")

    def test_fill_circle(self):
        command = bytes([0x09, 0x00, 0xB4, 0x00, 0xDC, 0x00, 0x4B, 0xF8, 0x00])
        result = self.parser.parse(command)
        self.assertIsNotNone(result, "Parse result should not be None for valid command")
        self.assertEqual(result['command_id'], 0x09, "Command ID should be 0x09 for FillCircle")
        self.assertEqual(result['x0'], 180, "x0 should be 180")
        self.assertEqual(result['y0'], 220, "y0 should be 220")
        self.assertEqual(result['radius'], 75, "radius should be 75")
        self.assertEqual(result['color'], 0xF800, "Color should be 0xF800 (red in RGB565)")

    def test_fill_circle_incorrect(self):
        command = bytes([0x09, 0x00, 0xB4, 0x00, 0xDC, 0x00, 0x4B])
        result = self.parser.parse(command)
        self.assertIsNone(result, "Parse result should be None for invalid number of parameters")

    def test_draw_rounded_rectangl(self):
        command = bytes([0x0A, 0x00, 0x32, 0x00, 0x32, 0x00, 0xC8, 0x00, 0x96, 0x00, 0x14, 0x78, 0x0F])
        result = self.parser.parse(command)
        self.assertIsNotNone(result, "Parse result should not be None for valid command")
        self.assertEqual(result['command_id'], 0x0A, "Command ID should be 0x0A for DrawRoundedRectangle")
        self.assertEqual(result['x0'], 50, "x0 should be 50")
        self.assertEqual(result['y0'], 50, "y0 should be 50")
        self.assertEqual(result['w'], 200, "width should be 200")
        self.assertEqual(result['h'], 150, "height should be 150")
        self.assertEqual(result['radius'], 20, "radius should be 20")
        self.assertEqual(result['color'], 0x780F, "Color should be 0x780F (purple in RGB565)")

    def test_draw_rounded_rectangle_incorrect(self):
        command = bytes([0x0A, 0x00, 0x32, 0x00, 0x32, 0x00, 0xC8, 0x00, 0x96, 0x00, 0x14])
        result = self.parser.parse(command)
        self.assertIsNone(result, "Parse result should be None for invalid number of parameters")

    def test_fill_rounded_rectangle(self):
        command = bytes([0x0B, 0x00, 0x64, 0x00, 0x4B, 0x00, 0xFA, 0x00, 0xB4, 0x00, 0x0F, 0x03, 0xEF])
        result = self.parser.parse(command)
        self.assertIsNotNone(result, "Parse result should not be None for valid command")
        self.assertEqual(result['command_id'], 0x0B, "Command ID should be 0x0B for FillRoundedRectangle")
        self.assertEqual(result['x0'], 100, "x0 should be 100")
        self.assertEqual(result['y0'], 75, "y0 should be 75")
        self.assertEqual(result['w'], 250, "width should be 250")
        self.assertEqual(result['h'], 180, "height should be 180")
        self.assertEqual(result['radius'], 15, "radius should be 15")
        self.assertEqual(result['color'], 0x03EF, "Color should be 0x03EF (light blue in RGB565)")

    def test_fill_rounded_rectangle_incorrect(self):
        command = bytes([0x0B, 0x00, 0x64, 0x00, 0x4B, 0x00, 0xFA, 0x00, 0xB4, 0x00, 0x0F])
        result = self.parser.parse(command)
        self.assertIsNone(result, "Parse result should be None for invalid number of parameters")

    def test_draw_text_correct(self):
        command = bytes([0x0C, 0x00, 0x32, 0x00, 0x64, 0xF8, 0x00, 0x01, 0x05, 0x48, 0x65, 0x6C, 0x6C, 0x6F])
        result = self.parser.parse(command)
        self.assertIsNotNone(result, "Parse result should not be None for valid command")
        self.assertEqual(result['command_id'], 0x0C, "Command ID should be 0x0C for DrawText")
        self.assertEqual(result['x0'], 50, "x0 should be 50")
        self.assertEqual(result['y0'], 100, "y0 should be 100")
        self.assertEqual(result['color'], 0xF800, "Color should be 0xF800 (red in RGB565)")
        self.assertEqual(result['font_number'], 1, "Font number should be 1")
        self.assertEqual(result['text'], "Hello", "Text should be 'Hello'")

    def test_draw_text_incorrect(self):
        command = bytes([0x0C, 0x00, 0x32, 0x00, 0x64, 0xF8, 0x00, 0x01])
        result = self.parser.parse(command)
        self.assertIsNone(result, "Parse result should be None for invalid number of parameters")

    def test_invalid_command(self):
        command = bytes([0xFF, 0x00, 0x00])  
        result = self.parser.parse(command)
        self.assertIsNone(result)

    def test_invalid_params_length(self):
        command = bytes([0x01, 0x00])  
        result = self.parser.parse(command)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
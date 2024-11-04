import socket
import struct

def send_command(command_bytes):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 12345)
    sock.sendto(command_bytes, server_address)
    print(f"Sent: {command_bytes.hex()}")

# 1. Clear Display (0x01)
send_command(b'\x01\x1F\x00')  # Clear with color RGB565(0x1F00)

# 2. Draw Pixel (0x02)
send_command(b'\x02\x00\x64\x00\xC8\x07\xE0')  # Draw pixel at (100, 200) with color RGB565(0x07E0)

# 3. Draw Line (0x03)
send_command(b'\x03\x00\x0A\x00\x14\x00\x64\x00\xC8\x1F\x00')  # Line from (10, 20) to (100, 200) with color RGB565(0x1F00)

# 4. Draw Rectangle (0x04)
send_command(b'\x04\x00\x32\x00\x32\x00\x64\x00\x64\xF8\x00')  # Rectangle at (50, 50), width 100, height 100, color RGB565(0xF800)

# 5. Fill Rectangle (0x05)
send_command(b'\x05\x00\x64\x00\x64\x00\x32\x00\x32\x07\xE0')  # Fill rectangle at (100, 100), width 50, height 50, color RGB565(0x07E0)

# 6. Draw Ellipse (0x06)
send_command(b'\x06\x00\x96\x00\x96\x00\x32\x00\x1E\x1F\x00')  # Ellipse at (150, 150), radius_x 50, radius_y 30, color RGB565(0x1F00)

# 7. Fill Ellipse (0x07)
send_command(b'\x07\x00\xC8\x00\xC8\x00\x28\x00\x28\xF8\x00')  # Fill ellipse at (200, 200), radius_x 40, radius_y 40, color RGB565(0xF800)

# 8. Draw Circle (0x08)
send_command(b'\x08\x00\xFA\x00\xFA\x00\x32\x07\xE0')  # Circle at (250, 250), radius 50, color RGB565(0x07E0)

# 9. Fill Circle (0x09)
send_command(b'\x09\x01\x2C\x01\x2C\x00\x28\x1F\x00')  # Fill circle at (300, 300), radius 40, color RGB565(0x1F00)

# 10. Draw Rounded Rectangle (0x0A)
send_command(b'\x0A\x00\x32\x01\x5E\x00\x64\x00\x32\x00\x0A\xF8\x00')  # Rounded rectangle at (50, 350), width 100, height 50, radius 10, color RGB565(0xF800)

# 11. Fill Rounded Rectangle (0x0B)
send_command(b'\x0B\x00\x96\x01\x5E\x00\x64\x00\x32\x00\x0A\x07\xE0')  # Fill rounded rectangle at (150, 350), width 100, height 50, radius 10, color RGB565(0x 07E0)

# 12. Draw Text (0x0C)
text = "Hello, World!"
text_bytes = text.encode('utf-8')
font_number = 2  

command = struct.pack(">BhhHBB", 0x0C, 50, 50, 0x1F00, font_number, len(text_bytes)) + text_bytes
send_command(command)

# 13. Invalid command ID
send_command(b'\xFF\x00\x00')  # FF is not a valid command ID

# 14. Invalid parameters for Draw Pixel command
send_command(b'\x02\x00\x64')  # Not enough parameters for Draw Pixel

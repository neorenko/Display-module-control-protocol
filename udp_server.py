import socket
import threading
import logging
from typing import Optional, Callable
from command_parser import DisplayCommandParser  

class UDPServer:
    def __init__(self, host: str, port: int, command_callback: Callable):
        self.host = host
        self.port = port
        self.command_callback = command_callback
        self.running = False
        self.command_parser = DisplayCommandParser()  
        
        
        self.logger = logging.getLogger('UDPServer')
        self.logger.setLevel(logging.INFO)
        
        if not self.logger.handlers:
            console_handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def validate_and_parse_packet(self, data: bytes) -> Optional[dict]:
        """
        Валідація та розбір отриманого пакету.
        
        Args:
            data: Отримані байти
            
        Returns:
            Optional[dict]: Розібрана команда або None, якщо пакет невалідний
        """
        try:
            if len(data) < 1:
                self.logger.error("Received empty packet")
                return None
            
            parsed_command = self.command_parser.parse(data)
            if parsed_command:
                self.logger.info(f"Received command: {parsed_command}")
                return parsed_command
            else:
                self.logger.error("Failed to parse command")
                return None
            
        except Exception as e:
            self.logger.error(f"Packet parsing error: {str(e)}")
            return None

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._run_server)
        self.thread.daemon = True
        self.thread.start()
        self.logger.info(f"UDP server started on {self.host}:{self.port}")

    def stop(self):
        self.running = False
        if hasattr(self, 'thread'):
            self.thread.join()
        self.logger.info("UDP server stopped")

    def _run_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            try:
                s.bind((self.host, self.port))
                s.settimeout(0.1)
                self.logger.info(f"UDP server listening on {self.host}:{self.port}")

                while self.running:
                    try:
                        data, addr = s.recvfrom(1024)
                        self.logger.debug(f"Raw data from {addr}: {data.hex()}")
                        
                        parsed_command = self.validate_and_parse_packet(data)
                        if parsed_command and self.command_callback:
                            try:
                                self.command_callback(parsed_command)
                            except Exception as e:
                                self.logger.error(f"Error in command callback: {str(e)}")
                        
                    except socket.timeout:
                        continue
                    except Exception as e:
                        if self.running:
                            self.logger.error(f"Error processing packet: {str(e)}")
                            
            except Exception as e:
                self.logger.error(f"Server error: {str(e)}")
            finally:
                self.logger.info("Server socket closed")
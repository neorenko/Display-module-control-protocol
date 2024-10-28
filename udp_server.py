import socket
import logging
from command_parser import DisplayCommandParser


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Налаштування сервера
HOST = '127.0.0.1'  # localhost
PORT = 12345        # Порт для прийому команд

parser = DisplayCommandParser()

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, PORT))
        logger.info(f"UDP server listening on {HOST}:{PORT}")

        while True:
            try:
                data, addr = s.recvfrom(1024)
                logger.info(f"Received packet from {addr}: {data.hex()}")

                try:
                    result = parser.parse(data)
                    if result:
                        logger.info(f"Parsed command: {result['command_id']}")
                        logger.info(f"Command parameters: {result}")
                    else:
                        logger.warning("Failed to parse command")
                except ValueError as e:
                    logger.error(f"Error parsing command: {str(e)}")
                except Exception as e:
                    logger.error(f"Unexpected error: {str(e)}")

            except Exception as e:
                logger.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    start_server()
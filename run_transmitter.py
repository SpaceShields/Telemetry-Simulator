# # Add the src path to use nested files
# sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.transmitter import transmit_packets

if __name__ == "__main__":
    transmit_packets()
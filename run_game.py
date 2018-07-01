import train as tbt

def run_game(neural_networks, generation_number, id):
        app = tbt.Game(neural_networks, generation_number, id)
        app.play()
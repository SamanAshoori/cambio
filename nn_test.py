import numpy as np
from cambio import Cambio

game = Cambio()
game.starting_peek()
print(game.get_state_vector(1))
print(f"vector length: {len(game.get_state_vector(1))}")
print(game.get_state_vector(2))
print(f"vector length: {len(game.get_state_vector(2))}")
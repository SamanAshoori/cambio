from cambio import Cambio
from agent import Agent

agent = Agent()
agent.epsilon = 1.0  # always random, never learns

episodes = 5000
wins = 0

for episode in range(episodes):
    game = Cambio()
    game.starting_peek()

    while not game.game_over:
        state = game.get_state_vector(player=1)
        action = agent.act(state)
        game.agent_step(action, player=1)

    result = game.get_winner()
    if "P1" in result:
        wins += 1

    if episode % 100 == 0:
        print(f"episode {episode}, win rate: {wins/(episode+1):.2f}")

print(f"\nfinal win rate: {wins/episodes:.2f}")

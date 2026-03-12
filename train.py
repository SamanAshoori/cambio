from cambio import Cambio
from agent import Agent

agent = Agent()
episodes = 2000
wins = 0

for episode in range(episodes):
    game = Cambio()
    game.starting_peek()

    while not game.game_over:
        state = game.get_state_vector(player=1)
        action = agent.act(state)
        game.agent_step(action, player=1)
        reward = game.get_reward(player=1)
        next_state = game.get_state_vector(player=1)
        done = game.game_over
        agent.train(state, action, reward, next_state, done)

    result = game.get_winner()
    if "P1" in result:
        wins += 1

    # decay epsilon
    agent.epsilon = max(0.1, agent.epsilon * 0.995)

    if episode % 100 == 0:
        print(f"episode {episode}, epsilon: {agent.epsilon:.3f}, win rate: {wins/(episode+1):.2f}")
        
agent.save()

print(f"\nfinal win rate: {wins/episodes:.2f}")


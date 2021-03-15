import random


def random_activation(agents):
    random_agents = random.sample(agents, len(agents))
    for agent in random_agents:
        agent.step()

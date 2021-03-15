class Model:
    scheduler = None
    agents = []

    def step(self):
        self.scheduler(self.agents)

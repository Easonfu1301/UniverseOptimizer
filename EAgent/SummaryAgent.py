from BaseAgent import BaseAgent








class SummaryAgent(BaseAgent):
    def __init__(self):
        super().__init__()



    def __str__(self):
        return f"SummaryAgent(config={self.config})"

















if __name__ == "__main__":
    agent = SummaryAgent()
    print(agent)










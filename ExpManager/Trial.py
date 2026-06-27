









class Trial:
    def __init__(self, name, config):
        self.name = name
        self.config = config

    def __str__(self):
        return f"Trial(name={self.name}, config={self.config})"







if __name__ == "__main__":
    trial = Trial(name="Test Trial", config={"param1": 10, "param2": 20})
    print(f"Trial Name: {trial.name}")
    print(f"Trial Config: {trial.config}")










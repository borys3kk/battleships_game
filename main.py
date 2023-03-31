from game import Game
import json

if __name__ == "__main__":
    with open("fleet.json", "r") as f:
        data = json.load(f)
        print(data)
        # json not working TODO rework them
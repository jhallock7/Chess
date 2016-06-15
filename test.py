from Game import Game

games = 10

outcomes = {"white" : 0,
            "black" : 0
            }

for game in range(games):
    print("Game", game + 1)
    print("Game", game + 1)
    print("Game", game + 1)
    print("Game", game + 1)
    print("Game", game + 1)
    white_won, black_won = Game("AI", 3, "AI", 3).play_game()
    if white_won:
        outcomes["white"] += 1
    if black_won:
        outcomes["black"] += 1

print(outcomes)

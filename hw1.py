from hw1_trainer import *

import sys
import time
import argparse

def parse_cli():
    parser = argparse.ArgumentParser(description='Virtual Texas Hold\'em Game')
    parser.add_argument('-hP', '--humanPlayers', type=int, default=0, help='Specify the number of human players in the game.')
    parser.add_argument('-aP', '--aiPlayers', default=3, type=int, help='Specify the number of AI players in the game.')
    parser.add_argument('-n', '--trials', default=1, type=int, help='The number of games played.')
    parser.add_argument('-s', '--logStats', action="store_true", help='Log statistics on game play.')
    parser.add_argument('-wF', '--weightFile', nargs="*", help='Location of weight file(s) for AI.')
    parser.add_argument('-m', '--startMoney', default=1000, type=int, help='Amount of money for each player at the start.')
    parser.add_argument('-v', '--verbose', default=False, type=bool, help='Outputs searching info for each AI player. Default on for a single run.')
    parser.add_argument('-mS', '--maxSampleSize', default=10000, type=int, help='Caps the randomly generated sample depth for AI agents.')
    parser.add_argument('-rr', '--regenerateRandom', action="store_true", help='Regenerates random weights every trial instead of using one set of random weights generated at the start.')

    args = parser.parse_args()
    return args

def print_results(args, playerStats, totalHandsEval, elapsedTime, winner, pokerGame):
    totalPlayers = args.humanPlayers + args.aiPlayers
    print("\nResults:")
    if args.trials == 1:
        print("Winner: Player", winner)
        print("Winning Pot Value:", pokerGame.potValue)
    else:
        print("Games Played:", args.trials)
        for player in range(totalPlayers):
            print("Player", player, ":")
            print("\tGames Won:", playerStats[player]["wins"])
            print("\tMoney Won:", playerStats[player]["moneyWon"])
        print("Hands Evaluated:", totalHandsEval, "hands")
        print("\tHands/Second:", totalHandsEval/elapsedTime)
        print("Time for {0} games:".format(args.trials), elapsedTime)


if __name__ == "__main__":
    args = parse_cli()

    playerStats, totalHandsEval, elapsedTime, winner, pokerGame = playSeries(args)

    print_results(args, playerStats, totalHandsEval, elapsedTime, winner, pokerGame)

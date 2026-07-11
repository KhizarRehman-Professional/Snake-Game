from game import Game

if __name__ == "__main__":
    print("=" * 50)
    print("   Snake Game + AI Stats Dashboard")
    print("=" * 50)
    print("Controls:")
    print("  Arrow Keys  - Move snake")
    print("  A           - Toggle AI mode ON/OFF")
    print("  R           - Restart after game over")
    print("  S           - Show Stats Dashboard (matplotlib)")
    print("  Q           - Quit")
    print("=" * 50)

    game = Game()
    game.run()

import argparse

def home():
    print("Home Menu")

def play():
    print("Play Menu")

def scoreboard():
    print("Scoreboard Menu")

def exit_program():
    print("Exiting...")
    exit(0)

def main():
    parser = argparse.ArgumentParser(description="Simple CLI Menu")
    parser.add_argument('command', choices=['home', 'play', 'scoreboard', 'exit'], help="Menu command")

    args = parser.parse_args()

    if args.command == 'home':
        home()
    elif args.command == 'play':
        play()
    elif args.command == 'scoreboard':
        scoreboard()
    elif args.command == 'exit':
        exit_program()

if __name__ == "__main__":
    main()

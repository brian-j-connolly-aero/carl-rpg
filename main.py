import argparse
import threading
import flask_app
import models
# import your_tui_module
# import database_module

def initialize_database():
    #Will implement this after local working

    pass


def run_gui():
    app = flask_app.create_app()
    with app.app_context():
        models.db.create_all()
    app.run(debug=True)
    pass


def run_tui():
    # your_tui_module.start_tui()
    pass


def run_both():
    gui_thread = threading.Thread(target=run_gui)
    tui_thread = threading.Thread(target=run_tui)
    gui_thread.start()
    tui_thread.start()
    gui_thread.join()
    tui_thread.join()


def main():
    parser = argparse.ArgumentParser(
        description='Run the application in TUI, GUI, or both modes.')
    parser.add_argument('--mode', choices=['tui', 'gui', 'both'],
                        required=False, help='Mode to run the application in.')
    args = parser.parse_args()
    initialize_database()

    if args.mode == 'tui':
        run_tui()
    elif args.mode == 'gui':
        run_gui()
    elif args.mode == 'both':
        run_both()
    elif args.mode == None:
        run_both()


if __name__ == "__main__":
    main()

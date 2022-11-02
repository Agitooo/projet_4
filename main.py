from views.base import View
from controllers.base import Controller


def main():
    view = View()
    tournament = Controller(view)
    tournament.get_menu_choice()


if __name__ == '__main__':
    main()

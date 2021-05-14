import json
import mimetypes
import random
import string


class Colors:
    """
    Add colors to text in command line.
    """

    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class Tools:
    """
    Helper class with awesome and useful functions.
    """

    @staticmethod
    def generate_file_name(path, content_type):
        return f"{path}/{Tools.random_string()}{mimetypes.guess_extension(content_type)}"

    @staticmethod
    def handle_menu_options(menu):
        """
        Prints menu (choose dict)
        Args:
            menu: Dict[choose]

        Returns:
            String - user choice.
        """
        Tools.print_choose_dict(menu)
        user_input = input()
        return user_input

    @staticmethod
    def get_choices(choices):
        """Return chooses list  with base_actions
        Args:
            choices: Dictionary with some options user can choose.
        Returns:
            Extended choices Dictionary.
        """
        from states import ExitState, PreviousState  # Avoid import loop

        base_actions = {"Выход": ExitState, "Назад": PreviousState}

        result = {"choose": choices}
        result["choose"].extend(list(base_actions.keys()))
        return result

    @staticmethod
    def print_ok_message(text):
        """Prints text with OKGREEN color
        Args:
            text: message
        """
        print(f"{Colors.OKGREEN}{text}{Colors.ENDC}")

    @staticmethod
    def handle_response(response):
        """Prints message from server response
        Args:
            response: Response from API
        Returns:
            Bool: True if status == ok or False
        """
        response = json.loads(response.text)
        if response["status"] == "success":
            Tools.print_ok_message(response["message"])
            return True
        if response["status"] == "fail":
            Tools.print_error(response["message"])
            return False

    @staticmethod
    def print_error(text):
        """Prints text with FAIL color
        Args:
            text: message
        """
        print(f"{Colors.FAIL}{text}{Colors.BOLD}{Colors.ENDC}")

    @staticmethod
    def print_choose_dict(data):
        """Prints a menu consisting of data
        Args:
            data: dict with choose options
        """
        print("Какое действие вы хотите сделать? (Ответ пишите в виде цифры)")
        for d in sorted(data.keys()):
            print(f"{int(d)}) {data[d]}.")

    @staticmethod
    def get_choose_dict(data):
        """Makes dict for menu with choose options
        Args:
            data: options
        Returns:
            dict: dict with choose options
        """
        return {str(i): data["choose"][i] for i in range(len(data["choose"]))}

    @staticmethod
    def random_string():
        """Makes a random string 5 characters long
        Returns:
            String: random string 5 characters long
        """
        return "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))


def try_except_decorator(func):
    """Wraps the function in a try ... except ... block so that no need to handle KeyError manually
    Args:
        func: function to wrap
    """

    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except KeyError:
            Tools.print_error("Пожалуйста введите корректные данные.")

    return wrapper


def format_to_choose(categories, unpack_value):
    """Unpack categories (response from Server) with given unpack value. And formatting it to choose dict.
    Args:
        categories: List of Dict[categories]
        unpack_value: String with value to get from Dict[categories]
    Returns:
        Choices Dict.
    """
    return Tools.get_choices([d[unpack_value] for d in categories])

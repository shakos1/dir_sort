import os
import argparse
import time
import shutil
from colorama import Fore, Style

VERSION = "0.0.1"


def init_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Sort directory contents to folders by creation date."
    )
    parser.add_argument('-V', '--version', action='version', version=f'{parser.prog} {VERSION}')
    parser.add_argument('--path', help="Directory path to sort", type=str, default='.')
    return parser


def get_creation_time(path: str) -> time.struct_time:
    """Get path's creation time as time object"""
    c_time_epoch = os.path.getctime(path)
    c_time_full = time.ctime(c_time_epoch)
    c_time_obj = time.strptime(c_time_full)
    return c_time_obj


def main(args):
    user_path = input("Enter path to the folder you want to sort (Press enter for current folder):\n")
    dir_path = args.path if not user_path else user_path
    user_quiet = input("Ask before moving? ('YES', 'NO')\n")
    while user_quiet.upper() not in ('YES', 'NO'):
        user_quiet = input("Please enter only 'YES' or 'NO':\n")
    quiet = user_quiet == 'YES'
    input(f"""
Folder to sort: {os.path.abspath(dir_path)}
Are you sure you want to sort the specified folder?
(Press Enter to continue)
""")
    print("\nSorting...\n")
    dir_contents = os.listdir(dir_path)
    dir_contents.remove(parser.prog)
    for file_dir in dir_contents:
        f_d_path = f'{dir_path}/{file_dir}'
        t_f_dir_creation_full = get_creation_time(f_d_path)
        t_f_dir = time.strftime("%Y-%m", t_f_dir_creation_full)
        new_dir = f"{dir_path}/{t_f_dir}"
        if new_dir == f_d_path:
            continue

        if not os.path.exists(new_dir):
            os.mkdir(new_dir)

        if not quiet:
            input(Style.RESET_ALL + f'Moving {f_d_path} to folder {t_f_dir} (Press Enter to continue) ')
        print(Fore.GREEN + f"Moving {f_d_path} to folder {t_f_dir}")
        shutil.move(f_d_path, new_dir)

    input(Style.RESET_ALL + """
Done!
Press Enter to exit.
""")


if __name__ == '__main__':
    parser = init_parser()
    args = parser.parse_args()
    if not os.path.isdir(args.path) or not os.path.exists(args.path):
        raise NotADirectoryError
    main(args)

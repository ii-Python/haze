# Haze Cipher
# Copyright 2021 iiPython
#
# x = character code
# c = randomly generated key
# o = offset (to prevent the same end result)
# (x * (c / 3.5)) + ((x / 2) + o)

# Modules
import os
import sys
import random

# Initialization
__version__ = "1.2a"

# Handlers
class Haze(object):
    def __init__(self) -> None:
        pass

    def cipher(self, data: str, key: int) -> tuple:
        offset = random.randint(10**10, 11**10)
        return (":".join([str((ord(char) * (key / 3.5)) + ((ord(char) / 2) + offset)) for char in data]), f"{key}:{offset}")

    def decipher(self, data: str, key: int, offset: int):
        return "".join([chr(round((float(char) - offset) / ((key / 3.5) + .5))) for char in data.split(":")])

haze = Haze()

# Argument parser
class Arguments(object):
    def __init__(self) -> None:
        self.args = sys.argv[1:]
        self.cmds = {
            "help": self.help,
            "cipher": self.cipher,
            "decipher": self.decipher
        }

    def exit(self, code: int, message: str = None) -> None:
        if message is not None:
            print(message)

        return sys.exit(code)

    def print(self, text: str, no_print: bool = False) -> None:
        data = "\n".join([_.split("~ ")[1] for _ in text.split("\n") if _.strip()])
        if no_print:
            return data

        return print(data)

    def help(self, args: list) -> None:
        self.print("""
        ~ Haze Cipher
        ~ ===============================
        ~ 
        ~ Command usage:
        ~ haze <option> <data/file>
        ~ haze cipher [data/file] [key]
        ~ haze decipher [data/file] [key]
        ~ haze help
        ~ 
        ~ Copyright 2021 iiPython
        """)  # noqa

    def save_to_file(self, text: str) -> None:
        print("NOTICE: output is > 2000 characters; enter a filename to save to (or hit enter for stdout):")
        try:
            fn = input("> ")
            if fn.strip():
                if os.path.isfile(fn):
                    if input(f"\n'{fn}' already exists, overwrite (y/N)? ").lower() != "y":
                        return self.exit(0, "Canceled file save.")

                with open(fn, "w") as file:
                    file.write(text)

                return self.exit(0, "\nSaved to file.")

        except KeyboardInterrupt:
            return self.exit(0, "^C")

    def cipher(self, args: list) -> None:
        try:
            if not args:
                try:
                    print("STDIN:")
                    data = input()

                except KeyboardInterrupt:
                    return self.exit(1, "KeyboardInterrupt while reading STDIN.")

            else:
                data = args[0]

            try:
                key = int(args[1]) if len(args) > 1 else random.randint(1000, 9999)

            except ValueError:
                return self.exit(1, "Error in cipher arguments: key must be an integer.")

        except IndexError:
            return self.exit(1, "Missing required arguments for cipher.\nUsage: haze cipher [data/file] [key]")

        # Handle files
        if os.path.isfile(data):
            with open(data, "r") as file:
                data = file.read()

        # Cipher
        res, key = haze.cipher(data, key)
        text = self.print(f"""
        ~ Haze Cipher v{__version__}; copyright 2021 iiPython
        ~ Result:
        ~ {res}
        ~ 
        ~ Key: {key}
        """, no_print = True)  # noqa
        if len(text) > 2000:
            self.save_to_file(text)

        print(text)

    def decipher(self, args: list) -> None:
        try:
            try:
                data, key = args[0], None

            except IndexError:
                try:
                    print("STDIN:")
                    data = input()

                except KeyboardInterrupt:
                    return self.exit(1, "KeyboardInterrupt while reading STDIN.")

            if len(args) > 1:
                key = args[1].split(":")
                if not (key[0].strip() and key[1].strip() and len(key) == 2):
                    return self.exit(1, "Invalid decipher key.")

                try:
                    key, offset = int(key[0]), int(key[1])

                except ValueError:
                    return self.exit(1, "Invalid decipher key.")

        except IndexError:
            return self.exit(1, "Missing required arguments for decipher.\nUsage: haze decipher <data/file> [key]")

        # Handle files
        if os.path.isfile(data):
            with open(data, "r") as file:
                fdata = file.read().lower()

                # Handle autofill
                try:
                    if "result:\n" in fdata and key is None:
                        data = fdata.split("result:\n")[1].split("\n")[0]
                        key, offset = fdata.split("key: ")[1].split(":")
                        key, offset = int(key), int(offset)

                    else:
                        data = fdata

                except Exception:
                    pass

        if key is None:
            return self.exit(1, "No key was provided and no key was found in provided file.")

        # Decipher
        res = haze.decipher(data, key, offset)
        text = self.print(f"""
        ~ Haze Cipher v{__version__}; copyright 2021 iiPython
        ~ Deciphered Result:
        """, no_print = True) + "\n" + res  # noqa
        if len(text) > 2000:
            self.save_to_file(text)

        print(text)

    def parse(self) -> None:
        if not self.args:
            return self.cmds["help"]([])

        base = self.args[0]
        if base not in self.cmds:
            return self.exit(1, f"haze: no such command '{base}'")

        return self.cmds[base](self.args[1:])

Arguments().parse()

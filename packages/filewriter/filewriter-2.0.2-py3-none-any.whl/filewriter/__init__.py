import collections
import json
import os

WRITER_DEFAULT_FILENAME = os.getenv('READABLE_GLOBAL_VARIABLE_NAME', "debug")


class Reverse:
    __slots__ = [
        'item',
    ]

    def __init__(self, item):
        self.item = item

    def __rshift__(self, other):
        return other.__lshift__(self.item)

    def __lshift__(self, other):
        return other.__rshift__(self.item)


def get_filename(filename, ext='log'):
    if filename:
        if filename.endswith(f".{ext}"):
            return filename
        return f"{filename}.{ext}"
    return f"{WRITER_DEFAULT_FILENAME}.{ext}"


def read_data(data, is_json=True):
    if is_json:
        return json.loads(data)
    return data


def parse_data(data, is_json=True):
    if is_json:
        return json.dumps(data)
    return data


class Base:
    __slots__ = [
        "callback",
        "debug",
        "ext",
        "filename",
        "fopen_mode",
        "json",
        "_shift",
    ]

    def __init__(
            self,
            fopen_mode,
            filename=WRITER_DEFAULT_FILENAME,
            debug=True,
            json=True,
            callback=None,
            ext='log',
    ):
        self.debug = debug
        self.ext = ext
        self.filename = get_filename(filename, self.ext)
        self.fopen_mode = fopen_mode
        self.json = json
        self.callback = callback


class Writer(Base):
    def __init__(
            self,
            filename=WRITER_DEFAULT_FILENAME,
            debug=True,
            json=True,
            callback=None,
            ext='log',
    ):
        super().__init__(
            "w+",
            filename=filename,
            debug=debug,
            json=json,
            callback=callback,
            ext=ext,
        )

    def __lshift__(self, other):
        filename = get_filename(self.filename, self.ext)
        if (isinstance(other, list)
                or isinstance(other, set)
                or (isinstance(other, collections.Iterable)
                    and not isinstance(other, dict))):
            with open(filename, self.fopen_mode) as file:
                file_data = []
                for data in other:
                    line = parse_data(data, is_json=self.json)
                    file.write(f"{line}\r\n")
                    if self.debug:
                        print(line)
                    file_data.append(line)
        else:
            with open(filename, self.fopen_mode) as file:
                data = parse_data(other, is_json=self.json)
                file.write(f"{data}")
                if self.debug:
                    print(data)
                file_data = data
        if self.callback:
            self.callback(filename)

        return file_data


class Reader(Base):
    def __init__(
            self,
            filename=WRITER_DEFAULT_FILENAME,
            debug=True,
            json=True,
            ext='log',
    ):
        super().__init__(
            "r",
            filename=filename,
            debug=debug,
            json=json,
            ext=ext,
        )
        self.data = Reader._define(
            self.filename,
            fopen_mode=self.fopen_mode,
            debug=self.debug,
            json=self.json,
            ext=self.ext,
        )

    @classmethod
    def _define(cls, filename, fopen_mode="r", debug=True, json=True, ext='log'):
        filename = get_filename(filename, ext=ext)
        file_data = []
        with open(filename, fopen_mode) as file:
            for line in file.readlines():
                data_line = line
                file_data.append(read_data(data_line, is_json=json))
                if debug:
                    print(read_data(data_line, is_json=json))
        data = file_data[0] if len(file_data) == 1 else file_data
        return data

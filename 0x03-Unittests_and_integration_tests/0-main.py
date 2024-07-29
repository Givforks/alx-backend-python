#!/usr/bin/env python3

from utils import get_json


if __name__ == "__main__":
    print(get_json("https://jsonplaceholder.typicode.com/todos/1"))

import requests
import sys
import time
import os

class StupidRNG():
    GOOGLE_QUERY_URL = 'https://www.google.com/search?q={}'

    MIN_SEED_TIME = 0.1

    ASCII_MIN = 48
    ASCII_MAX = 122

    MAX_QUERY_LEN = 1023

    def __init__(self, seed_time_in_seconds = 0.1):
        self.set_seed_time(seed_time_in_seconds)

        self.seed()

    def set_seed_time(self, seed_time_in_seconds):
        if seed_time_in_seconds < self.MIN_SEED_TIME:
            seed_time_in_seconds = self.MIN_SEED_TIME

        self.seed_time = seed_time_in_seconds

    def _isAscii(self, char):
        byteValue = ord(char)

        if byteValue < self.ASCII_MIN:
            return False
        if byteValue > self.ASCII_MAX:
            return False

        return True

    def _get_n_bytes_from_urandom(self, n):
        if n < 1:
            return -1

        return os.urandom(n)

    def _get_byte_from_urandom(self):
        return self._get_n_bytes_from_urandom(1)

    def _get_random_int_from_urandom(self):
        found_int = False
        
        while found_int == False:
            found_int = True

            byte = self._get_byte_from_urandom()
            try:
                num = ord(byte)
            except UnicodeDecodeError:
                found_int = False

        return num

    def _get_string_from_urandom(self, str_len):
        found_chars = ''

        while len(found_chars) < str_len:
            try:
                char = self._get_byte_from_urandom().decode("UTF-8")
            except UnicodeDecodeError:
                continue
            
            if self._isAscii(char):
                found_chars += char

        return found_chars


    def _perform_random_query(self, query_string):
        query_url = self.GOOGLE_QUERY_URL.format(query_string)

        request = requests.get(query_url)

        return request.content

    def seed(self):
        self.seed_value = 1

        start_time = time.time()
        end_time = start_time + self.seed_time

        while time.time() < end_time:
            self.seed_value += self._get_random_int_from_urandom()

    def rand(self, min_num = 0, max_num = sys.maxsize):
        offset = max_num - min_num


if __name__ == "__main__":
    rng = StupidRNG()

    print(rng.seed_value)

    rng.set_seed_time(2)
    rng.seed()

    print(rng.seed_value)

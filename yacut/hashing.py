import time
import threading
from string import ascii_letters, digits


class Snowflake:
    def __init__(self, datacenter_id, worker_id, epoch=1288834974657):
        self.datacenter_id = datacenter_id
        self.worker_id = worker_id
        self.epoch = epoch
        self.sequence = 0
        self.last_timestamp = -1
        self.lock = threading.Lock()

        # Define the bit lengths for the different parts
        self.timestamp_bits = 41
        self.datacenter_id_bits = 5
        self.worker_id_bits = 5
        self.sequence_bits = 12

        # Calculate the maximum values
        self.max_datacenter_id = -1 ^ (-1 << self.datacenter_id_bits)
        self.max_worker_id = -1 ^ (-1 << self.worker_id_bits)
        self.max_sequence = -1 ^ (-1 << self.sequence_bits)

        # Calculate the bit shifts
        self.worker_id_shift = self.sequence_bits
        self.datacenter_id_shift = self.sequence_bits + self.worker_id_bits
        self.timestamp_shift = (
            self.sequence_bits + self.worker_id_bits + self.datacenter_id_bits
        )

    def _current_timestamp(self):
        return int(time.time() * 1000)

    def _to_base62(self, num):
        """Convert a number to a base62 string."""
        chars = digits + ascii_letters
        base62 = ''
        while num:
            num, i = divmod(num, 62)
            base62 = chars[i] + base62
        return base62 or '0'

    def generate_id(self):
        with self.lock:
            timestamp = self._current_timestamp()

            if timestamp < self.last_timestamp:
                raise Exception(
                    "Clock moved backwards. Refusing to generate id"
                )

            if timestamp == self.last_timestamp:
                self.sequence = (self.sequence + 1) & self.max_sequence
                if self.sequence == 0:
                    while timestamp <= self.last_timestamp:
                        timestamp = self._current_timestamp()
            else:
                self.sequence = 0

            self.last_timestamp = timestamp

            generated_id = (
                ((timestamp - self.epoch) << self.timestamp_shift)
                | (self.datacenter_id << self.datacenter_id_shift)
                | (self.worker_id << self.worker_id_shift)
                | self.sequence
            )

            # Convert the generated ID to base62
            base62_id = self._to_base62(generated_id)

            # Ensure the ID is 6 characters long
            if len(base62_id) > 6:
                # Truncate to 6 characters if necessary
                base62_id = base62_id[:6]
            elif len(base62_id) < 6:
                # Pad with leading zeros if necessary
                base62_id = base62_id.zfill(6)

            return base62_id

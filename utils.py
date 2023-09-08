def from_megabytes_to_bytes(val: int) -> int:
    return val * (2 ** 20)


def from_bytes_to_megabytes(val: int) -> float:
    return round(val / (2 ** 20), 3)


def from_kilobytes_to_bytes(val: int) -> int:
    return val * (2 ** 10)

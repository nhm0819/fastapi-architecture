from enum import Enum


class BigEndian(Enum):
    float16 = ">f2"
    float32 = ">f4"
    float64 = ">f8"

import logging

class invalid_marks(Exception):
    pass

def ch_marks(marks):
    if marks < 0 or marks > 100:
        raise invalid_marks("marks should be between 0 and 100")

try:
    ch_marks(102)
except invalid_marks as e:
    logging.error(e)
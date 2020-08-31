from tinkoff_voicekit_client import ClientSTT
import logging
import datetime
import os
from db import *
import random

API_KEY = "ZU4KjCJojHDcIc93vuFeobqyh35t0F1jP8KTDTbhkwo=TestCandidate"
SECRET_KEY = "L1+iWOCHtxbLftTsAf1jyfKFm1bYwE86i3cT/t+IczE="

negative_answers = ["не", "неудобно", "ни"]
positive_answers = ["да", "конечно", "удобно"]

logger = logging.getLogger("test_task")
logger.setLevel(logging.INFO)
fh = logging.FileHandler("test_task.log")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

def uniqueid():
    seed = random.getrandbits(32)
    while True:
       yield seed
       seed += 1

def first_stage(text):
    if "втоответчик" in text:
        return 0, "АО"
    else:
        return 1, "человек"

def second_stage(text):
    for ans in negative_answers:
        if ans in text:
            return 0
    for ans in positive_answers:
        if ans in text:
            return 1

def main():
    database = DB()

    file_name, file_dest, tel_number, flag, stage = input().split()

    audio_config = {
        "encoding": "LINEAR16",
        "sample_rate_hertz": 8000,
        "num_channels": 1
    }

    client = ClientSTT(API_KEY, SECRET_KEY)

    responses = client.recognize(file_dest, audio_config)
    print(responses)
    text = responses[0]["alternatives"][0]["transcript"]
    print(text)
    result, person = first_stage(text)
    result2 = 0
    if stage == "2":
        if result:
            result2 = second_stage(text)


    id = uniqueid()
    un_id = next(id)
    logger.info(str(un_id)+' '+person+ ' ' + str(result2) + ' ' + tel_number + ' ' + responses[0]["start_time"] + ' ' + text)

    if flag == '1':
        database.insert(str(datetime.datetime()), id, person, result2, tel_number, responses[0]["start_time"], text)

    os.remove(file_dest)



if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.error(e)








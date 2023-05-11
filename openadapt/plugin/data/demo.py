from pynput.keyboard import Key, Controller
from dotenv import load_dotenv
import os
import openai
import time

load_dotenv()

openai.api_key = os.getenv("API_KEY")

params = {
    "engine": "text-davinci-003",
    "prompt": "",
    "max_tokens": 1000,
    "temperature": 0.7,
}

endpoint = "localhost:3333"

keyboard = Controller()


def sendkeys(args):
    # # open sublime in new terminal window
    # keyboard.press(Key.cmd)
    # keyboard.press(Key.space)
    # keyboard.release(Key.cmd)
    # keyboard.release(Key.space)
    # time.sleep(1.2)
    # keyboard.type("safari")
    # keyboard.press(Key.enter)
    # time.sleep(0.2)
    # keyboard.release(Key.enter)
    # time.sleep(1.2)
    # keyboard.type("https://www.office.com/launch/word")
    # keyboard.press(Key.enter)
    # keyboard.release(Key.enter)
    # time.sleep(6)
    # for _ in range(0, 3):
    #     keyboard.press(Key.tab)
    #     time.sleep(.2)
    #     keyboard.release(Key.tab)
    # keyboard.press(Key.enter)
    # keyboard.release(Key.enter)
    # time.sleep(4.5)
    # keyboard.press(Key.tab)
    # keyboard.release(Key.tab)

    params.update({"prompt": args})
    response = openai.Completion.create(**params)
    print(
        "Sending keys: ", response["choices"][0]["text"], file=__import__("sys").stderr
    )
    keyboard.type(response["choices"][0]["text"])
    return 200


def test():
    __import__("openadapt.replay").replay("NaiveReplayStrategy")
    a = sendkeys("Hello, world!")
    if a == 200:
        print("Success!")


if __name__ == "__main__":
    print("api key: ", os.getenv("API_KEY"))
    test()

import re
import os
import random

def main():
    path = "./text"

    list_file = os.listdir(path)

    res_str_ob = re.compile(r"[A-Z][^`,\,^,:,=,(,),0-9,~]{249,349}\s")
    string = ""

    for file in list_file:
        with open("./text/"+file, "r", encoding="utf-8") as txt:
            res = " ".join("".join(txt.readlines()).split())

        string += res_str_ob.findall(res)

    for i in string:
        print(i)
        print("")

    with open("text/test.txt", "w+") as txt:
        txt.write("\n".join(string))


def text_genirate():
    with open("./text/test.txt", "r", encoding="utf-8") as fl:
        texts = fl.readlines()
    time_maskc = re.compile(r".{49,71}\s")
    return time_maskc.findall(random.choice(texts).replace("\n", ""))


print(text_genirate())

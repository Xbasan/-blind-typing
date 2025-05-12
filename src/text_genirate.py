import re
import os
import random
import PyPDF2


def main():
    path = "./text"

    list_file = os.listdir(path)

    res_str_ob = re.compile(r"[A-Z][^`\~]{200,400}\s")
    string = ""

    for file in list_file:
        with open("./text/"+file, "rb") as txt:
            reader = PyPDF2.PdfReader(txt)
            res = ""

            for page in reader.pages:
                res += page.extract_text()
            res = " ".join(res.split("\n"))
            print(res)
        string += "\n".join(res_str_ob.findall(re.sub(r"\s+", " ", res)))

    string = re.sub(r'"\\u[0-9a-fA-F]{4}"', "", string)
    print(string)

    with open("test/test.txt", "w+") as txt:
        txt.write(string)


def text_genirate():
    with open("./text/test.txt", "r", encoding="utf-8") as fl:
        texts = fl.readlines()

    time_maskc = re.compile(r"\b\w{2,}\b")
    rand = random.choice(texts)

    print(rand)
    return time_maskc.findall(rand.replace("\n", ""))[:int(input())]


def test_():
    with open("./text/test.txt", "r", encoding="utf-8") as fl:
        texts = fl.readlines()

    arr = []
    for i in texts:
        print(len(i.replace("\n", " ").split(" ")))
        arr.append(len(i.replace("\n", " ").split(" ")))
    print(len("".join(texts).replace("\n", " ").split(" ")))
    print(max(arr))


def bly():
    with open("./test.txt", "r", encoding="utf-8") as fl:
        texts = type(fl)

    return texts


main()

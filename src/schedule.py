import json

schedule_sign = {
    1: "⣀",
    2: "⣤",
    3: "⣶",
    4: "⣿", 
    -3: "⣀",
    -2: "⣤",
    -1: "⣶",
    0: "⣿",
    -4: "⣿"
}


def schedule(date_s: list) -> dict:
    """Приоброзовыает json в красивый график"""
    res_js = {}
    for dat in date_s:
        aa = date_s[dat]
        res = [[]]
        for i, k in enumerate(aa):
            sa = aa[k]
            iter = 1
            while sa >= 0:
                if iter >= len(res):
                    res.append([])
                    for p in aa:
                        res[iter].append(" ")
                if sa <= 4:
                    res[iter][i] = schedule_sign[sa]
                    break
                else:
                    sa -= 4
                    res[iter][i] = schedule_sign[4]
                iter += 1
            res[0].append(k)
        res_js[dat] = res

    ser = {}
    for i in res_js:
        ser[i] = []
        for q, j in enumerate(reversed(res_js[i])):
            if q != len(res_js[i])-1:
                ser[i].append(f"{str(q+1):^5}{"".join(j)}")
            else:
                ser[i].append(f"{' ':^5}{"".join(j)}")
    return ser


if __name__ == "__main__":

    JSON = {
        "d": {
            "w": 1,
            "q": 3,
        },
        "b": {
            "s": 2,
            "f": 5
        },
        "a": {
            "s": 1
        },
        "w": {
            "s": 10
        }
    }
    with open("/home/khamzat/.config/blind-typing/analyticsData.json", "r") as file:
        _analytics_data = json.load(file)

    awre = schedule(JSON)
    print(awre)

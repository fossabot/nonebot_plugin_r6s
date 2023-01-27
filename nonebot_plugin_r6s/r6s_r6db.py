def rank(mmr: int) -> str:
    head = ["紫铜", "黄铜", "白银", "黄金", "白金", "钻石", "冠军"]
    feet2 = ["III", "II", "I"]
    if mmr < 2600:
        mmrd = int(mmr // 100 - 11)
        feet1 = ["V", "IV", "III", "II", "I"]
        if mmrd < 5:
            return head[0] + feet1[mmrd]
        elif mmrd < 10:
            return head[1] + feet1[mmrd - 5]
        else:
            return head[2] + feet1[mmrd - 10]
    elif mmr < 4400:
        mmrd = int(mmr // 200 - 13)
        return head[3] + feet2[mmrd] if mmrd < 3 else head[4] + feet2[(mmrd - 3) // 2]
    elif mmr < 5000:
        return head[-2]
    else:
        return head[-1]


def con(*args) -> str:
    r = "".join(arg + "\n" for arg in args)
    return r[:-1]


def gen_stat(data: dict) -> str:
    return con(
        "KD：%.2f"
        % (
                data["payload"]["stats"]["general"]["kills"]
                / data["payload"]["stats"]["general"]["deaths"]
        )
        if data["payload"]["stats"]["general"]["deaths"] != 0
        else (
                "KD：%d/%d"
                % (
                    data["payload"]["stats"]["general"]["kills"],
                    data["payload"]["stats"]["general"]["deaths"],
                )
        ),
        "胜负比：%.2f"
        % (
                data["payload"]["stats"]["general"]["wins"]
                / data["payload"]["stats"]["general"]["losses"]
        )
        if data["payload"]["stats"]["general"]["losses"] != 0
        else (
                "胜负比：%d/%d"
                % (
                    data["payload"]["stats"]["general"]["wins"],
                    data["payload"]["stats"]["general"]["losses"],
                )
        ),
        "总场数：%d" % data["played"],
        "游戏时长：%.1f" % (data["timePlayed"] / 3600),
    )


def base(data: dict) -> str:
    return con(
        data["payload"]["user"]["nickname"],
        "等级：" + data["payload"]["stats"]["progression"]["level"], "",
        "综合数据",
        gen_stat(data["StatGeneral"][0])
    )


def pro(data: dict) -> str:
    r = ""
    casual = True
    for stat in data["StatCR"]:
        r = con(r, "休闲数据" if casual else "\n排位数据", gen_stat(stat))
        casual = False
    return con(
        data["username"],
        r,
        "",
        "休闲隐藏MMR：%d" % data["Casualstat"]["mmr"]
        if casual
        else "排位MMR：%d\n隐藏MMR：%d\n隐藏Rank：%s"
             % (
                 data["Basicstat"][0]["mmr"],
                 data["Casualstat"]["mmr"],
                 rank(data["Casualstat"]["mmr"]),
             ),
        "爆头击杀率：%.2f"
        % (
                data["StatGeneral"][0]["headshot"]
                / data['StatGeneral'][0]['kills']
        ),
    )

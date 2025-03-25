import os

def get_data(filename):
    if not os.path.exists(filename):
        return {"message": "File not found", "error": 1}
    ret = list()
    with open(filename, "r", encoding='UTF-8') as f:
        filestr = f.read()
        for num in filestr.split():
            if num.isdigit():
                ret.append(int(num))
            else:
                return {"message": "The file contains invalid data", "error": 2}
    if len(ret):
        return {"result": ret, "message": "Ok"}
    return {"message": "The file is empty", "error": 3}


def calc_data(result):
    return {
        "summa": sum(result),
        "minimum": min(result),
        "maximum": max(result),
        "average": float(f"{sum(result) / len(result):.2f}"),
    }


if __name__ == "__main__":
    data_dct = get_data(input())
    print(data_dct)
    stat_data = dict()
    if data_dct.get("result"):
        stat_data = calc_data(data_dct["result"])
        print(stat_data)

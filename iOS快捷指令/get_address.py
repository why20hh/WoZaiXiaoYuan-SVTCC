from urllib.parse import urlencode
import time
import hashlib

dk_address = {
            "timestampHeader":"",
            "answers": "['0']",
            "latitude": "30.534273",
            "longitude": "104.057148",
            "country": "中国",
            "city": "成都市",
            "district": "双流区",
            "province": "四川省",
            "township": "",
            "street": "",
            "city_code": "156440100"
        }


def first_get_time():
    get_time = int(round(time.time() * 1000))
    timestampHeader = str(get_time)
    content = f"四川省_{get_time}_成都市"
    signature = hashlib.sha256(content.encode('utf-8')).hexdigest()
    dk_address["timestampHeader"] = timestampHeader
    dk_address["signatureHeader"] = signature
    address =urlencode(dk_address)
    print(address)
    return address

import hashlib

def get_sign(params, kAppKey, kAppSecret):
    if isinstance(params, str):
        return params_str_sort(params,kAppKey, kAppSecret)
    elif isinstance(params, dict):
        arr = []
        for key, value in params.items():
            arr.append(f"{key}={value}")
        return params_str_sort("&".join(arr), kAppKey, kAppSecret)

def params_str_sort(params_str, kAppKey, kAppSecret):
    url = f"{params_str}&appKey="+kAppKey
    url_str = "&".join(sorted(url.split("&")))
    new_url = f"{url_str}&key="+kAppSecret
    return hashlib.md5(new_url.encode()).hexdigest()


def test_get_sign():
    params = "id=23730"
    kAppKey = "sino"
    kAppSecret = "SINO@2022"

    signature = get_sign(params, kAppKey, kAppSecret)
    print(f"Signature for params '{params}': {signature}")

# 调用测试方法
test_get_sign()

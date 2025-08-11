import os
import requests
import sys

KOA_SESS = os.getenv("KOA_SESS")
KOA_SESS_SIG = os.getenv("KOA_SESS_SIG")
UA = os.getenv("UA")

headers = {
    "cookie": f"koa:sess={KOA_SESS}; koa:sess.sig={KOA_SESS_SIG}",
    "user-agent": UA,
    "content-type": "application/json;charset=UTF-8"
}

# 签到请求
checkin_resp = requests.post("https://glados.rocks/api/user/checkin", headers=headers, json={"token": "glados.one"})
try:
    result = checkin_resp.json()
except Exception:
    print("Error: 返回内容不是 JSON：", checkin_resp.text)
    sys.exit(6)

message = result.get("message", "")
print(f"[返回信息] {message}")

# 判断签到是否成功
success_keywords = [
    "Checkin Repeats! Please Try Tomorrow",
    "Checkin! Got"  # 例如 "Checkin! Got 3 Points"
]

if any(kw in message for kw in success_keywords):
    print("[OK] 签到成功")
else:
    print("Error: 未识别的签到返回：", message)
    sys.exit(6)

# 获取账户信息
info_resp = requests.get("https://glados.rocks/api/user/status", headers=headers)
try:
    info = info_resp.json()
except Exception:
    print("Error: 账户信息返回内容不是 JSON：", info_resp.text)
    sys.exit(6)

print("[账户信息]", info)

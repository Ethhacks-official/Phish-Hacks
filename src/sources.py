import subprocess
import netifaces
from scapy.all import *
import psutil
import requests
import pyudev # type: ignore
import os
import json
from scapy.layers.http import HTTPRequest
from colorama import init, Fore
init()
GREEN = Fore.GREEN
RED   = Fore.RED
BLUE   = Fore.BLUE
RESET = Fore.RESET


class Sources:
    def __init__(self):
        pass

    def copy_directory(self,frompath,topath):
        result = subprocess.run(f"cp -r {frompath} {topath}", shell=True, capture_output=True, text=True)
        print(result.stderr)

    def list_directory(self,path=""):
        command = f"ls -l {path} " + "| grep '^d' | awk '{print $9}'"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        list_of_directories = []
        n = 0
        print(f"{GREEN}[+] Following Directories are found in {path} directory.{RESET}")
        for directories in result.stdout.split("\n"):
            if directories == "":
                pass
            else:
                print(f"{GREEN}{n}.{directories}{RESET}")
                n+=1
                list_of_directories.append(directories)
        return list_of_directories
    
    def list_files(self,path=""):
        command = f"ls -p {path} | grep -v /"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        list_of_files = []
        n = 0
        print(f"{GREEN}[+] Following files are found in {path} directory.{RESET}")
        for files in result.stdout.split("\n"):
            if files == "":
                pass
            else:
                print(f"{GREEN}{n}.{files}{RESET}")
                n+=1
                list_of_files.append(files)
        return list_of_files

    def create_folder(self,name):
        result = subprocess.run(f"mkdir {name}", shell=True, capture_output=True, text=True)
        if result.stderr == "":
            print(f"{GREEN}\n[+] {name} Folder is created successfully!!!!\n{RESET}")
        else:
            print(f"{RED}[-] {result.stderr}{RESET}")

    def create_file(self,name):
        result = subprocess.run(f"touch {name}", shell=True, capture_output=True, text=True)
        if result.stderr == "":
            print(f"\n{GREEN}[+] {name} file is created successfully!!!!\n{RESET}")
        else:
            print(f"{RED}\n[-] {result.stderr}{RESET}")


    def kill_process(self,name):
        result = subprocess.run(f"killall {name}", shell=True, capture_output=True, text=True)
        print(f"{RED}[-]Killing All Process with name {name}{RESET}")
        print(result.stderr)


    def get_ip_address(self,interface):
        try:
            addresses = netifaces.ifaddresses(interface)
            ip_address = addresses[netifaces.AF_INET][0]['addr']
            return ip_address
        except KeyError:
            print(f"{RED}[--]Interface {interface} not found or does not have an IPv4 address.{RESET}")
            return None
        
    def get_external_ip(self):
        response = requests.get('https://api.ipify.org?format=json')
        if response.status_code == 200:
            return response.json()['ip']
        else:
            return None

    def get_interface_menufacturer_name(self,interface):

        context = pyudev.Context()
        for device in context.list_devices(subsystem='net'):
            if device.sys_name.startswith(interface):
                try:
                    manufacturer = str(device.get('ID_VENDOR_FROM_DATABASE')) + " " + str(device.get('ID_MODEL_FROM_DATABASE'))
                    return manufacturer
                except KeyError:
                    return ""

    def listinterfaces(self):
        list_of_interfaces = []
        self.i = 0
        self.addrs = psutil.net_if_addrs()
        os.system("clear")
        print(" Network Interfaces:- ")
        for interfaces in self.addrs.keys():
            print(str(self.i) + ". " +interfaces + "   \t|\t" + self.get_interface_menufacturer_name(interfaces))
            self.i+=1
            list_of_interfaces.append(interfaces)

        return list_of_interfaces
    
    def selectadapter(self):
        list_of_interface = self.listinterfaces()
        interface_input = input(f"{GREEN}Select wireless interface by typing 0-{str(self.i-1)}: -->{RESET} ")
        try:
            wireless_interface = list_of_interface[int(interface_input)]
            print(f"\n\n{GREEN}[++]Selected interface is {wireless_interface}.{RESET}")
            return wireless_interface
        except (IndexError, ValueError) as e:
            print(f"{RED}[--] Please Select correct index number for wireless adaptor or Select Correct WIreless Adaptor...{RESET}")
            return None

    def capture_logins(self,login_path):

        
        import time
        from watchdog.observers import Observer # type: ignore
        from watchdog.events import FileSystemEventHandler # type: ignore

        class FileChangeHandler(FileSystemEventHandler):
            def __init__(self, file_path):
                self.file_path = file_path
                self.file = open(file_path, 'r')
                self.file.seek(0, 2)  # Move the pointer to the end of the file

            def on_modified(self, event):
                if event.src_path == self.file_path:
                    for line in self.file:
                        print(line.strip())
                        print("\r")

        def monitor_file(file_path):
            event_handler = FileChangeHandler(file_path)
            observer = Observer()
            observer.schedule(event_handler, path=file_path, recursive=False)
            print(f"\n\n{BLUE}[+] Capturing Login Details............\n[-] Press CTRL+C to quit!!!!!\n\n{RESET}")
            observer.start()
            
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                observer.stop()
            observer.join()

        
        monitor_file(login_path)


    def saving_captured(self,login_path):
        with open(login_path, 'r', encoding='utf-8') as file:
            content = file.read()
        print(f"\n{GREEN}[=] Below is the data for cureent website captured previously and in this session.")
        print(f"--------------------------------------------------------------------------------------------------------{RESET}\n")
        print(content)
        print(f"{GREEN}--------------------------------------------------------------------------------------------------------{RESET}\n")

        save_check = input(f"\nDo you want to save this data into a file. Type 'y' to save data in file --> ").lower()
        if save_check == "y":
            filename = input("Provide the name of file --> ")
            if filename == "":
                filename = "data.txt"
            with open(filename, 'w') as file:
                file.write(content)



    def generate_ssh_key(self):
        try:
            files = self.list_files(os.getcwd())
            os.system("clear")
            no_of_key_files = 0
            keys = []
            for file in files:
                if ".pub" in file:
                    print(f"{no_of_key_files}.{file}")
                    keys.append(file)
                    no_of_key_files+=1
            if no_of_key_files == 0:
                key_name = input(f"{GREEN}[?] Provide the name for SSH Key --> {RESET}")
                if key_name == "":
                    key_name = f"{os.getcwd()}/key"
                else:
                    key_name = f"{os.getcwd()}/{key_name}"
                passphrase = ""
                cmd = ['ssh-keygen','-t', 'rsa','-b', '2048','-f', key_name,'-N', passphrase]
                result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                public_key_path = key_name
                if public_key_path == os.path.abspath(key_name):
                    os.system("clear")
                    print(f"{GREEN}SSH key generated successfully:{RESET}")
                    print(f"{BLUE}--> Public key:{RESET}{GREEN} {public_key_path}{RESET}")
                    return public_key_path
                else:
                    print(f"{RED}[-] Can't generate SSH key........ Try Agian.{RESET}")
                    return None
            else:
                key_select = input(f"{GREEN}[?] Following keys are found that are previous generated for this process. Select key by specifing index number or type 'n' to generate new key -->{RESET} ")
                if key_select == "n" or key_select == "N":
                    key_name = input(f"{GREEN}[?] Provide the name for SSH Key -->{RESET} ")
                    if key_name == "":
                        key_name = f"{os.getcwd()}/key"
                    else:
                        key_name = f"{os.getcwd()}/{key_name}"
                    passphrase = ""
                    cmd = ['ssh-keygen','-t', 'rsa','-b', '2048','-f', key_name,'-N', passphrase]
                    result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    public_key_path = key_name
                    if public_key_path == os.path.abspath(key_name):
                        os.system("clear")
                        print(f"{GREEN}SSH key generated successfully:{RESET}")
                        print(f"{BLUE}--> Public key:{RESET} {GREEN}{public_key_path}{RESET}")
                        return public_key_path
                    else:
                        print(f"{RED}[-] Can't generate SSH key........ Try Agian.{RESET}")
                        return None
                else:
                    key_name = keys[int(key_select)]
                    key_name = key_name.split(".pub")[0]
                    public_key_path = f"{os.getcwd()}/{key_name}"
                    if public_key_path == str(os.path.abspath(key_name)):
                        os.system("clear")
                        print(f"{GREEN}SSH key generated successfully:{RESET}")
                        print(f"{BLUE}Public key:{RESET} {GREEN}{public_key_path}{RESET}")
                        return public_key_path
                    else:
                        print(f"{RED}[-] Can't generate SSH key........ Try Agian.{RESET}")
                        return None 
        except subprocess.CalledProcessError as e:
            print(f"Error generating SSH key: {e.stderr.decode()}")
            return None
        
    def port_forward_using_localhostrun(self,key_name):
        url_no = 0
        try:
            ports = []
            try:
                with open("/etc/apache2/ports.conf", 'r') as file:
                    for line in file:
                        if line.startswith('Listen'):
                            match = re.search(r'Listen\s+(\d+)', line)
                            if match:
                                port = match.group(1)
                                ports.append(port)
                if len(ports) > 1:
                    print("Found Ports: ")
                    for port in ports:
                        print(port)
                    port = input("Select by typing the port like 80 or 8080 --> ")
                elif len(ports) == 1:
                    port = ports[0]
                elif len(ports) < 1:
                    port = input("Typing port that apache2 is using like 80 or 8080 --> ")
            except FileNotFoundError:
                print(f"Error: The file /etc/apache2/ports.conf was not found.")
                port = input("Typing port that apache2 is using like 80 or 8080 --> ")
            except Exception as e:
                print(f"An error occurred: {e}")
                port = input("Typing port that apache2 is using like 80 or 8080 --> ")

            cmd = [
    'ssh',
    '-o', 'StrictHostKeyChecking=no',
    '-o', 'UserKnownHostsFile=/dev/null',
    '-i', key_name,
    '-R', f'80:localhost:{port}',
    'localhost.run',
    '--', '--output', 'json'
]
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            while True:
                output = process.stdout.readline()
                try:
                    json_output = json.loads(output)
                except json.JSONDecodeError as e:
                    pass
                if isinstance(json_output, dict):
                    if "address" in json_output:
                        url = json_output["address"]
                        if url_no == 0:
                            os.system("clear")
                            print(f"{BLUE}\rURL -->{RESET}{GREEN} https://{url}{RESET}")
                            print(f"{RED}\r[-] Sometimes localhost.run change url. New url will be provided when it is changed..")
                            print(f"{BLUE}\rCapturing Login details..... Press CTRL+C to close SSH tunneling and Press CTRL+C twice to close both SSH tunneling and Capturng.... {RESET}")
                            print("\r")
                            url_no += 1
                        elif url_no > 0:
                            print("\n\n\r-----------------------------------------------------------------------------------")
                            print(f"{BLUE}\r[--] Localhost.run have changed the url.... {RESET}")
                            print(f"{BLUE}\rURL -->{RESET}{GREEN} https://{url}{RESET}")
                            print(f"{BLUE}\rCapturing Login details..... Press CTRL+C to close SSH tunneling and Press CTRL+C twice to close both SSH tunneling and Capturng.... {RESET}")
                            print("\r")
                            url_no += 1
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(f"Error in port forwarding: {e}")
            return None
        
    def port_forward_using_serveo(self,key_name):
        url_no = 0
        try:
            ports = []
            try:
                with open("/etc/apache2/ports.conf", 'r') as file:
                    for line in file:
                        if line.startswith('Listen'):
                            match = re.search(r'Listen\s+(\d+)', line)
                            if match:
                                port = match.group(1)
                                ports.append(port)
                if len(ports) > 1:
                    print("Found Ports: ")
                    for port in ports:
                        print(port)
                    port = input("Select by typing the port like 80 or 8080 --> ")
                elif len(ports) == 1:
                    port = ports[0]
                elif len(ports) < 1:
                    port = input("Typing port that apache2 is using like 80 or 8080 --> ")
            except FileNotFoundError:
                print(f"Error: The file /etc/apache2/ports.conf was not found.")
                port = input("Typing port that apache2 is using like 80 or 8080 --> ")
            except Exception as e:
                print(f"An error occurred: {e}")
                port = input("Typing port that apache2 is using like 80 or 8080 --> ")

            cmd = [
    'ssh',
    '-o', 'StrictHostKeyChecking=no',  # Accept unknown host keys automatically
    '-o', 'UserKnownHostsFile=/dev/null',  # Don't store the host key
    '-i', key_name,
    '-R', f'80:localhost:{port}',
    'serveo.net'
]

            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            while True:
                output = process.stdout.readline()
                if process.poll() is not None:
                    break
                if "Forwarding HTTP traffic from https://" in output and ".serveo.net" in output:
                    url_check = output.split(" ")
                    for url in url_check:
                        if ("https://" in url or "http://" in url) and ".serveo.net" in url:
                            url = url.replace(" ","").replace("\n","").replace("\t","")
                            if url_no == 0:
                                os.system("clear")
                                print(f"{BLUE}\rURL -->{RESET}{GREEN} {url}{RESET}")
                                print(f"{RED}\r[-] Sometimes serveo.net change url. New url will be provided when it is changed..")
                                print(f"{BLUE}\rCapturing Login details..... Press CTRL+C to close SSH tunneling and Press CTRL+C twice to close both SSH tunneling and Capturng.... {RESET}")
                                print("\r")
                                url_no += 1
                            elif url_no > 0:
                                print("\n\n\r-----------------------------------------------------------------------------------")
                                print(f"{BLUE}\r[--] Serveo.net have changed the url.... {RESET}")
                                print(f"{BLUE}\rURL -->{RESET}{GREEN} {url}{RESET}")
                                print(f"{BLUE}\rCapturing Login details..... Press CTRL+C to close SSH tunneling and Press CTRL+C twice to close both SSH tunneling and Capturng.... {RESET}")
                                print("\r")
                                url_no += 1


            rc = process.poll()
            return rc
        except Exception as e:
            print(f"Error in port forwarding: {e}")
            return None
        
    def port_apache(self):
        ports = []
        try:
            with open("/etc/apache2/ports.conf", 'r') as file:
                for line in file:
                    if line.startswith('Listen'):
                        match = re.search(r'Listen\s+(\d+)', line)
                        if match:
                            port = match.group(1)
                            ports.append(port)
            if len(ports) > 1:
                print("Found Ports: ")
                for port in ports:
                    print(port)
                port = input("Select by typing the port like 80 or 8080 --> ")
            elif len(ports) == 1:
                port = ports[0]
            elif len(ports) < 1:
                port = input("Typing port that apache2 is using like 80 or 8080 --> ")
        except FileNotFoundError:
            print(f"Error: The file /etc/apache2/ports.conf was not found.")
            port = input("Typing port that apache2 is using like 80 or 8080 --> ")
        except Exception as e:
            print(f"An error occurred: {e}")
            port = input("Typing port that apache2 is using like 80 or 8080 --> ")

        return port
        
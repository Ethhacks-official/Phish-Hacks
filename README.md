
# PhishHacks

An open source Phishing Attacks Toolkit could be used to practice different types phishing attacks and provide awareness. It is created for educational purpose only. Any harm using this tool will be on that person who used this tool for unethical purposes.

- Language: Python 3

- Operating System type : Linux

- Tested On: Kali Linux 2024 , Respberry Pi 4


## Requirements
The Phish-Hacks folder contains  "requirements.txt" file. Its contains all the required python libraries for this tool.
Install them manualy by using:
```
sudo pip3 install [library]
```
OR use the requirements.txt file and install as:
```
sudo pip3 install -r requirements.txt
```

## Features

- Create Phishing Page for within the network:
It will create the Phishing page which could be used for targets within the networks (targets that are connected to same network as of the attacker). It will provide url that can be sent to target and tool will start capturing credentials and will show on screen.
- Create Phishing Page for outside the network using Port Forwording:
It will create Phishing page which could be used within the network and also against the target that are outside the network (not connected to same network). But you need to configure your router to forword ports in order to make it work. It will provide url that can be sent to target and tool will start capturing credentials and will show on screen.
- Create Phishing Page outside the network using Localhost.run:
It will create Phishing page which could be used within and outside the network. Localhost.run is free service to expose your Localhost to internet using ssh tunneling. Tool will setup ssh key and then using it will create public url using Localhost.run service. Tool will start capturing credentials and will show on screen.
- Create Phishing Page outside the network using ngrok:
It will create Phishing page which could be used within and outside the network. Ngrok is one of the famous service to expose your Localhost to internet. Free ngrok token is not recommended for Phishing page as it warns the target before going to phishing page which will reduce the success of phishing. For ngrok, you will need first to signup to ngrok website and will need ngrok auth-token to provide to this tool in order for this attack to work.
- Create Phishing Page outside the network using serveo:
It will create Phishing page which could be used within and outside the network. Serveo is free service to expose your Localhost to internet using ssh tunneling. It is similar to Localhost.run.   Tool will setup ssh key and then using it will create public url using serveo service. Tool will start capturing credentials and will show on screen.
- Create Phishing Page for your onlne hosting or domain:
It will create Phishing page which could be used for your online hosting and domain. You need to place these file in your online hosting and whenever user login using credentials, the login credentials will be saved in login_data,txt file that will be present in files provided by this tool. If you found that credentials are not being saved in login_data.txt file, try providing all permissions of read, write and execute to login_data.txt file in your online hosting platform.
- Phishing Page Options:
Phishing Page creation menu is used to create phishing page. It includes 3 different method to setup the phishing page.
1. Phishing Page of Login Page of Website using URL:
It requires the url of login page of target website to create the phishing page exactly similar to that login page. It will also ask for name, it could be random and is just to differentiate websites with different name in apache2 folder.

Note: You must be connected to internet to create Phishing page with url. Phishing page of some websites like FaceBook or Google could not be created using url. So, try using already created phishing page of famous websites.

2. Phishing Page of famous websites:
It include login pages of 43 famous websites. By selecting one of these,it will create phishing page of login page of website.

3. Want to place your own phishing page files:
If you want to place phishing page created by you, then use this option. First place your phishing page files in a folder and place this folder in "/var/www/html" folder. It will list all folders present in "/var/www/hrml". Select your folder and it will create phishing page using it.  

## Usage/Installation

After installing the requirements using "requirements.txt". Run the program using following command:

```bash
sudo python3 main.py
```

First program will try to install the required linux tools. It will try to install these using "apt" manager. It your linux don't have "apt" manager then try to install below listed tools manually as without these tools it will not work.

- Apache2


## License

This project is licensed under the GNU LESSER GENERAL PUBLIC LICENSE Version 2.1 - see the [LICENSE] file for details.

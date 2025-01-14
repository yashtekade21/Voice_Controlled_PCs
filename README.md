The project uses secure shell (ssh) for remotely controlling the PC's via a single main PC.
It also take care of unauhorized access and only authorized person can control all the PC's. 

**For Windows System**
**Step 1:** Install chocolatey in windows installed client PCs. 
Powershell commands:
1) Get-ExecutionPolicy (if restricted then execute below command) 

2) Set-ExecutionPolicy AllSigned

3) [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

**Step 2:** Install OpenSSH server (Optional Feature) on Windows Client PC

**Step 3:** Open Windows Defender Firewall with Advanced Security:
Under Inbound Rules:
-- OpenSSH Server (sshd) - Change the profile to all (i.e. Public, Private, Domain). 

**Step 4:** Open services. msc and change OpenSSH Server to start Automatically on startup of windows. 

**Step 5:** Fill the json file with IP address, username and password of Microsoft account. 

**Step 6:** Run the python program and give the commands

import paramiko
import speech_recognition as sr
import json
import os

# Dictionary mapping app names to actual Chocolatey package names
app_map = {
    "vscode": "visualstudiocode",
    "visual studio code": "visualstudiocode",
    "chrome": "googlechrome",
    "google chrome": "googlechrome",
    "notepad++": "notepadplusplus",
    "git": "git",
    "nodejs": "nodejs",
    "python": "python",
    "7zip": "7zip",
    "vlc": "vlc",
    "discord": "discord",
    "steam": "steam",
    "spotify": "spotify",
    "skype": "skype",
    "firefox": "firefox",
    "opera": "opera",
    "java jdk": "jdk8",
    "jdk": "jdk8",
    "mysql": "mysql",
    "docker": "docker-desktop",
    "mongodb": "mongodb",
    "postgresql": "postgresql",
    "visual studio community": "visualstudio2019community",
    "intellij": "intellijidea-community",
    "pycharm": "pycharm-community",
    "eclipse": "eclipse",
    "sublime text": "sublimetext3",
    "audacity": "audacity",
    "filezilla": "filezilla",
    "winrar": "winrar",
    "teamviewer": "teamviewer",
    "slack": "slack",
    "zoom": "zoom",
    "virtualbox": "virtualbox",
    "kodi": "kodi",
    "gimp": "gimp",
    "inkscape": "inkscape",
    "powershell core": "powershell-core",
    "terraform": "terraform",
    "dotnet sdk": "dotnetcore-sdk",
    "microsoft edge": "microsoft-edge",
    "libreoffice": "libreoffice-fresh",
    "obs studio": "obs-studio",
    "blender": "blender",
    "brave": "brave",
    "kubernetes": "kubernetes-cli",
    "go": "golang",
    "ruby": "ruby",
    "winmerge": "winmerge",
    "cmake": "cmake",
    "putty": "putty",
    "xampp": "xampp",
    "cygwin": "cygwin",
    "postman": "postman",
    "dotnet framework": "dotnetfx"
}

def recognize_speech():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("\nSay your command ")
        audio = r.listen(source, phrase_time_limit=3)

    try:
        command = r.recognize_google(audio).lower().strip()
        print("You said:", command)
        return command
    except sr.UnknownValueError:
        print("Could not understand command.")
        return None

def map_application_name(app_name):
    for key, value in app_map.items():
        if key in app_name:
            return value
    return app_name 

def execute_command(host, username, password, command):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        client.connect(host, username=username, password=password)

        stdin, stdout, stderr = client.exec_command(command)
        
        output = stdout.read().decode()
        error = stderr.read().decode()
        
        if output:
            print(f"Output from {host}:")
            print(output)
        if error:
            print(f"Error from {host}:")
            print(error)
        
        client.close()
    except Exception as e:
        print(f"Error executing command on {host}: {str(e)}")

# Load hosts, usernames, and passwords from the JSON file
def load_hosts_from_json(filename):
    with open(filename, 'r') as file:
        config = json.load(file)
    return config["hosts"]

# Securely load sensitive data from environment variables
def get_env_variable(key, default=None):
    return os.getenv(key, default)

def main():
    hosts = load_hosts_from_json('hosts_config.json')
    
    while True:
        command = recognize_speech()
        
        if command:
            if command.startswith(("exit", "terminate")):
                break
            elif "shutdown" in command:
                want = "shutdown -s -t 0"
                for host in hosts:
                    execute_command(host['ip'], host['username'], host['password'], want)
            elif "restart" in command or "reboot" in command:
                want = "shutdown -r -t 0"
                for host in hosts:
                    execute_command(host['ip'], host['username'], host['password'], want)
            elif "install" in command:
                app_name = command.split("install", 1)[1].strip()
                mapped_app_name = map_application_name(app_name)
                want = f"C:\\ProgramData\\chocolatey\\bin\\choco install {mapped_app_name} -y"
                for host in hosts:
                    execute_command(host['ip'], host['username'], host['password'], want)
            elif "uninstall" in command:
                app_name = command.split("uninstall", 1)[1].strip()
                mapped_app_name = map_application_name(app_name)
                want = f"C:\\ProgramData\\chocolatey\\bin\\choco uninstall {mapped_app_name} -y"
                for host in hosts:
                    execute_command(host['ip'], host['username'], host['password'], want)
            else:
                print("Command not recognized.")
        else:
            print("Command not recognized.")

if __name__ == "__main__":
    main()


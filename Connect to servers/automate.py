import subprocess
import vars

def main():
    print("\n$$ Welcome to my automation program $$\n\n--- Please choose what to do ?\n\n")
    user = input(
        "\n1- Connect to VPS01\n"
        "2- Connect to VPS02\n"
        "3- Connect to VPS03\n"
        "4- Connect to VPS04\n"
        "5- Connect to VPS05\n"
        "6- Connect to VPS06\n"
        "7- Connect to Dev-Jenkins\n"
        "9- Exit\n"
        "Enter server number to connect (1-9):\n\n"
    )

    if user == "1":
        connect_to_vps(vars.VPS_USERNAME01, vars.VPS_PASSWORD01, vars.VPS_IP01)

    elif user == "2":
        connect_to_vps(vars.VPS_USERNAME02, vars.VPS_PASSWORD02, vars.VPS_IP02)

    elif user == "3":
        connect_to_vps(vars.VPS_USERNAME03, vars.VPS_PASSWORD03, vars.VPS_IP03)

    elif user == "4":
        connect_to_vps(vars.VPS_USERNAME04, vars.VPS_PASSWORD04, vars.VPS_IP04)

    elif user == "5":
        connect_to_vps(vars.VPS_USERNAME05, vars.VPS_PASSWORD05, vars.VPS_IP05)

    elif user == "6":
        connect_to_vps(vars.VPS_USERNAME06, vars.VPS_PASSWORD06, vars.VPS_IP06)

    elif user == "7":
        jenkins()

    elif user == "9":
        exit()
    else:
        print("Please enter a valid server number")
        main()

def connect_to_vps(username, password, ip):
    print(f"\nConnecting to VPS at IP: {ip} ... \n")
    subprocess.run(["sshpass", "-p", password, "ssh", "-o", "StrictHostKeyChecking=no", f"{username}@{ip}"])

def jenkins():
    print("\nStarting Jenkins on port http:localhost:6060... \n")  
    subprocess.run(["kubectl", "port-forward", "-n", "devops-tools", "svc/jenkins-service", "6060:8080"])

main()

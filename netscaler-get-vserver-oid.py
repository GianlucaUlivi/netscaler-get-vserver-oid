import warnings
from cryptography.utils import CryptographyDeprecationWarning
with warnings.catch_warnings():
    # Ignore blowfish deprecation warning currently affecting transport in paramiko library
    warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)
    from paramiko import SSHClient, AutoAddPolicy, AuthenticationException, BadHostKeyException, SSHException
from getpass import getpass
from re import match
import json
import regex

vserver_list = []

# Load source list
try:
    with open("in.json") as f:
        json_input = json.load(f)
        for entry in json_input:
            vserver_list.append(entry["Name"])
except OSError as err:
    print(err)

except json.JSONDecodeError as err:
    print(err)

# Output JSON array
vserver_oid_out = []

# Get login informations
SSH_IP = input("IP Address: ")
SSH_PORT = input("SSH Port: ")
SSH_USERNAME = input("Username: ")
SSH_PASSWORD = getpass()

# Create SSH Client with AutoAddPolicy for unknown hosts
ssh_client = SSHClient()
ssh_client.set_missing_host_key_policy(AutoAddPolicy())

try:
    ssh_client.connect(SSH_IP, port=SSH_PORT, username=SSH_USERNAME, password=SSH_PASSWORD)    # Connect to host
    ssh_in, ssh_out, ssh_err = ssh_client.exec_command("show snmp oid vserver")            # Execute oid command

    for line in ssh_out.readlines():
        line = line.rstrip()
        if line.rstrip().strip() == "Done":
            continue    # Skip this line

        id = line.split(")")[0]
        vserver_name = line.split(":")[1].split(" ")[0].rstrip()
        vserver_oid = line.split(":")[2].rstrip()

        if vserver_name in vserver_list:
            # Printing results
            print(f"ID: {id}")
            print(f"Name: {vserver_name}")
            print(f"OID: {vserver_oid}")
            print("-" * 30)

            # Format commands outputs into JSON
            json_vserver_oid_output = {
                                       "ID"     : id,
                                       "Name"   : vserver_name,
                                       "OID"    : vserver_oid
            }
            # Append results to JSON output array
            vserver_oid_out.append(json_vserver_oid_output)

except AuthenticationException as err:
    print("AuthenticationException")
    print(err)

except BadHostKeyException as err:
    print("BadHostKeyException")
    print(err)

except SSHException as err:
    print("SSHException")
    print(err)

finally:
    ssh_client.close()

# Write all hosts' data into JSON file
try:
    with open("out.json", "w") as output:
        output.write(json.dumps(vserver_oid_out))
        
except OSError as err:
    print(err)
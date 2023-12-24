import paramiko
import configparser
import getpass
import logging
import dns.update

logging.basicConfig(filename='error.log', level=logging.ERROR)

ipv6_prefix = "2001:db8:1234::"
subnet_prefix_length = 64

def assign_ipv6_address(device, ssh_client):
    ipv6_address = f"{ipv6_prefix}{device['Name']}::1/{subnet_prefix_length}"
    try:
        ssh_client.invoke_shell()
        ssh_client.send(f"configure terminal\ninterface {device['Interface']}\nipv6 address {ipv6_address}\nexit\n")
        print(f"IPv6 address assigned to {device['Name']} successfully.")
    except paramiko.AuthenticationException as auth_error:
        logging.error(f"Authentication failed for {device['Hostname']}: {str(auth_error)}")
    except paramiko.SSHException as ssh_error:
        logging.error(f"SSH error occurred while connecting to {device['Hostname']}: {str(ssh_error)}")
    except Exception as e:
        logging.error(f"Error connecting to {device['Hostname']}: {str(e)}")

def update_dns(device, ssh_client):
    hostname = device['Name']
    ipv6_address = f"{ipv6_prefix}{hostname}::1"
    try:
        # Implement a secure method to update DNS records with credentials here
        # For example, you can use a secure API or a credentials manager
        update_record = dns.update.DNSUpdate()
        update_record.add(hostname, "AAAA", ipv6_address)
        update_record.update()
        print(f"DNS record updated for {device['Name']} successfully.")
    except Exception as e:
        logging.error(f"Error updating DNS record for {device['Name']}: {str(e)}")

def main():
    authorized_users = ["user1", "user2"]  # List of authorized usernames
    current_user = getpass.getuser()
    if current_user not in authorized_users:
        print(f"Access denied for user: {current_user}")
        exit(1)

    config = configparser.ConfigParser()
    config.read('config.ini')
    ssh_key_file = config['General']['SSHPrivateKeyPath']
    ssh_username = config['General']['SSHUsername']

    # Validate configuration values
    if not ipv6_prefix.startswith("2001:db8:"):
        raise ValueError("IPv6 prefix must start with 2001:db8:")
    if not subnet_prefix_length.isdigit() or subnet_prefix_length < 0 or subnet_prefix_length > 128:
        raise ValueError("Subnet prefix length must be a positive integer less than or equal to 128")

    devices_section = config['Devices']
    devices = []
    for section_name in devices_section.sections():
        device_config = dict(devices_section[section_name])
        devices.append(device_config)

    # Parameterize configuration
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for device in devices:
        ssh_client.connect(device['Hostname'], username=ssh_username, key_filename=ssh_key_file)
        assign_ipv6_address(device, ssh_client)
        update_dns(device, ssh_client)
        ssh_client.close()

    print("IPv6 configuration completed successfully.")

if __name__ == "__main__":
    main()

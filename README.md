# Installation and Configuration:


- Install the required dependencies:


    Paramiko: pip install paramiko

    ConfigParser: pip install configparser
    

- Create a configuration file named ***config.ini*** in the same directory as the script. The configuration file should have the following structure:

      [General]
      SSHPrivateKeyPath = /path/to/private/key
      SSHUsername = your_ssh_username
      
      [Devices]
      device1 = 
          Hostname = device1.example.com
          Interface = eth0
      device2 = 
          Hostname = device2.example.com
          Interface = eth1
      ...

- Replace ***/path/to/private/key*** with the path to your SSH private key file, and ***your_ssh_username*** with your ***SSH username.*** Add as many devices as needed, following the same format.


# Usage:


- Open a terminal or command prompt.


- Navigate to the directory where the script and the config.ini file are located.


- Run the script using the following command:


`python ipv6aut.py`


- The script will prompt for your username and ensure that you are an authorized user before proceeding.



- The script will establish SSH connections to each device listed in the ***config.ini file.***



- For each device, the script will assign an IPv6 address to the specified interface using the provided IPv6 prefix and subnet prefix length.



- The script will then update the DNS record for each device with the assigned IPv6 address. You should implement a secure method for updating DNS records, such as using a secure API or a credentials manager. Modify the ***update_dns() function*** in the script to include your secure method.



- Any errors encountered during the process will be logged in the ***error.log file*** in the same directory as the script.


# Possible Problems and Solutions:



***SSH Authentication Failure:***


- Ensure that the SSH private key file path and username in the ***config.ini file*** are correct.

- Verify that the SSH private key file has the appropriate permissions ***(e.g., only readable by the owner).***



***SSH Connection Error:***


- Check the hostname and network connectivity of the device.

- Verify that the SSH service is running on the device.

- Ensure that the SSH username has sufficient privileges to connect to the device.




***DNS Update Error:***


- Implement a secure method for updating DNS records and modify the ***update_dns() function***.



***General Errors:***


- Check the ***error.log file*** for detailed error messages and troubleshooting information.





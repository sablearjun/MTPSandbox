import os
import time
from os import listdir
from os.path import isfile, join
import logging

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# VirtualBox VM configuration
vm_name = 'Ret Ka Baksa'  # replace with the name of your VM
snapshot_name = 'Clean1'

# Directory with malware samples and log path
main_dir = 'samples'
malware_dir = join(main_dir, "queue")
log_dir = join(main_dir, "logs")
completed_dir = join(main_dir, "completed")

# Ensure necessary directories exist
os.makedirs(log_dir, exist_ok=True)
os.makedirs(completed_dir, exist_ok=True)

# Function to revert VM to a snapshot
def revert_vm_to_snapshot():
    # Check if the VM is running and power it off if necessary
    vm_info = os.popen(f'VBoxManage showvminfo "{vm_name}" --machinereadable').read()
    if 'VMState="running"' in vm_info:
        logging.info("VM is running, powering off before restoring snapshot.")
        os.system(f'VBoxManage controlvm "{vm_name}" poweroff')
        time.sleep(5)  # Wait for VM to power off
    
    logging.info("Reverting to snapshot.")
    os.system(f'VBoxManage snapshot "{vm_name}" restore "{snapshot_name}"')
    time.sleep(5)


# Function to start VM
def start_vm():
    logging.info("Starting VM.")
    os.system(f'VBoxManage startvm "{vm_name}" --type headless')
    time.sleep(15)

# Function to set up and mount shared folder in VM
def setup_shared_folder():
    shared_folder_name = "malware_share"
    logging.info("Setting up shared folder.")
    os.system(f'VBoxManage sharedfolder add "{vm_name}" --name "{shared_folder_name}" --hostpath "{malware_dir}" --automount')
    time.sleep(5)

# Function to copy the malware sample to a specific path in the VM
def copy_malware_to_vm(malware):
    shared_folder_path = f'{malware_dir}/{malware}'  # Adjust path based on VM shared folder mounting
    vm_malware_path = "/tmp/malware"
    logging.info("Copying malware from shared folder to VM execution path.")
    os.system(f'VBoxManage guestcontrol "{vm_name}" copyfrom "{shared_folder_path}" "{vm_malware_path}" --username "retkabaksa" --password "retkabaksa"')
    time.sleep(5)

# Function to run malware in VM
def run_malware_in_vm():
    logging.info("Running malware in VM.")
    os.system(f'VBoxManage guestcontrol "{vm_name}" run --username retkabaksa --password retkabaksa -- /tmp/malware')
    time.sleep(120)

# Function to copy logs from VM to host
def copy_logs_from_vm(malware_log):
    logging.info("Copying logs from VM to host.")
    os.system(f'VBoxManage guestcontrol "{vm_name}" copyfrom "/var/log/osquery/osqueryd.results.log" "{malware_log}" --username retkabaksa --password retkabaksa')
    time.sleep(10)

# Function to stop VM
def stop_vm():
    logging.info("Stopping VM.")
    os.system(f'VBoxManage controlvm "{vm_name}" poweroff')
    time.sleep(5)

# Main malware processing loop
def process_malware_samples():
    malware_files = [f for f in listdir(malware_dir) if isfile(join(malware_dir, f))]
    
    for malware in malware_files:
        malware_path = join(malware_dir, malware)
        log_path = join(log_dir, f"{malware}.log")
        
        try:
            logging.info(f"Processing malware: {malware}")

            # Workflow steps
            revert_vm_to_snapshot()
            start_vm()
            setup_shared_folder()
            copy_malware_to_vm(malware)
            run_malware_in_vm()
            copy_logs_from_vm(log_path)
            stop_vm()
            
            # Move malware to completed/ directory
            os.rename(malware_path, join(completed_dir, malware))
            logging.info(f"Moved {malware} to completed/ directory.")
        
        except Exception as e:
            logging.error(f"An error occurred while processing {malware}: {e}")

# Run the main malware automation process
if __name__ == "__main__":
    process_malware_samples()

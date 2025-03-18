import subprocess
import json

# List all disks that are in use by VMs
print("Fetching disks attached to VMs...")

list_command = 'gcloud compute disks list --filter="users:*" --format="table(name,sizeGb,zone,status,users)"'
list_result = subprocess.run(list_command, shell=True, capture_output=True, text=True)

if list_result.returncode == 0:
    print("✅ Successfully retrieved disks in use:")
    print(list_result.stdout)
else:
    print("❌ Failed to fetch disks.")
    print(list_result.stderr)
    exit(1)  # Exit the script if we can't fetch disk info

# Process disks
attached_disks = []
for line in list_result.stdout.split("\n")[1:]:  # Skip table headers
    if line.strip():
        parts = line.split()
        disk_name, size_gb, zone, status, *users = parts
        attached_vm = ", ".join(users) if users else "No attached VM"

        print(f"🔹 Disk Name: {disk_name}, Size: {size_gb} GiB, "
              f"Status: {status}, Zone: {zone}, Attached to: {attached_vm}")

        attached_disks.append(disk_name)

print("\nAll in-use disks processed ✅")

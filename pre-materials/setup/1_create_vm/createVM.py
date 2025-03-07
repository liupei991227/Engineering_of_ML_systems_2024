import os
from openstack.compute.v2.keypair import Keypair


def create_keypair(conn: Connection, keypair_name: str) -> Keypair:
    keypair = conn.compute.find_keypair(keypair_name)
    print("Keypair found: {keypair}")

    if not keypair:
        print("Creating Key Pair...")
        keypair = conn.compute.create_keypair(name=keypair_name)
        ssh_dir_name = os.path.join(os.environ["HOME"], ".ssh")
        
        # create .ssh folder under your home directory if not existing
        os.makedirs(ssh_dir_name, exist_ok=True)
        
        private_keypair_file_path = os.path.join(
            ssh_dir_name, keypair_name
        )
        
        with open(private_keypair_file_path, "w") as f:
            f.write("%s" % keypair.private_key)

        os.chmod(private_keypair_file_path, 0o400)
        print("Done.")
    else:
        print(f"The keypair {keypair_name} is already in the system.")

    return keypair


keypair = create_keypair(conn, f"{conn.auth['username']}-tutorial")
print(f"\n\tKey pair: {keypair.name} - {keypair.location.project.name}\n")

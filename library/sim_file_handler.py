import os
import json
from datetime import datetime

def _get_existing_metadata_names(dest_folder):
    """
    Scan all JSON files in the destination folder and
    return a set of all simulation metadata names.
    """
    names = set()
    if not os.path.exists(dest_folder):
        return names

    for fname in os.listdir(dest_folder):
        if not fname.endswith(".json"):
            continue
        try:
            with open(os.path.join(dest_folder, fname), "r") as f:
                config = json.load(f)
            meta_name = config.get("metadata", {}).get("name")
            if meta_name:
                names.add(meta_name)
        except Exception:
            # Ignore broken files
            pass
    return names


def _generate_unique_metadata_name(base_name, existing_names):
    '''
    Given a name and a set of existing names, increment name until it is
    unique from set of existing_names such as name (1), name(2), and incrementing
    until name(x) is unique
    '''
    if base_name not in existing_names:
        return base_name

    counter = 1
    while f"{base_name}({counter})" in existing_names:
        counter += 1
    return f"{base_name}({counter})"


def create_new_sim_file(template_path, dest_folder="library/simulations", name=None):
    """
    Create a new simulation JSON file from a template, with metadata
    including a unique name and creation timestamp.

    Args:
        template_path (str): Path to the template JSON file.
        dest_folder (str): Folder to create the new JSON file.
        name (str): Optional requested name. Defaults to "New Simulation".

    Returns:
        str: Path to the newly created JSON file.
    """
    os.makedirs(dest_folder, exist_ok=True)

    with open(template_path, "r") as f:
        config = json.load(f)

    requested_name = name or "New Simulation"
    existing_names = _get_existing_metadata_names(dest_folder)
    unique_name = _generate_unique_metadata_name(requested_name, existing_names)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    config["metadata"] = {
        "name": unique_name,
        "created_at": timestamp
    }

    file_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_filename = unique_name.replace(" ", "_")
    new_file_path = os.path.join(dest_folder, f"{safe_filename}_{file_timestamp}.json")

    with open(new_file_path, "w") as f:
        json.dump(config, f, indent=4)

    return new_file_path

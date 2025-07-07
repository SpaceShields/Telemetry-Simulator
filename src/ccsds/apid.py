# Purpose of apid.py:
# Provide a single source of truth for subsystem Application Process IDs (APIDs)
# Act as a lookup table so all encoders, decoders, and dashboards can stay consistent

# APIDs for various subsystems
# These values are defined by the CCSDS standards and may vary by mission or implementation.
CDH = 0x01
POWER = 0x02
COMMS = 0x03
THERMAL = 0x04
ADCS = 0x05
PROPULSION = 0x06
PAYLOAD = 0x07

# Custom exception for APID handling
# This exception can be raised for any errors related to APID operations, such as invalid AP
class ApidError(Exception):
    """Custom exception for APID handling errors."""
    pass

# Dictionary mapping subsystem names to their APIDs
# This serves as the single source of truth for APIDs across the system
apid_dict = {
    "cdh": CDH,
    "power": POWER,
    "comms": COMMS,
    "thermal": THERMAL,
    "adcs": ADCS,
    "propulsion": PROPULSION,
    "payload": PAYLOAD,
}

# get_apid function retrieves the APID for a given subsystem
# It returns None if the subsystem is not found in the dictionary
def get_apid(subsystem: str) -> int:
    try:
        """
        Get the APID for a given subsystem.

        Args:
            subsystem (str): The name of the subsystem.

        Returns:
            int: The APID of the subsystem, or None if not found.
        """
        # Convert subsystem name to lowercase for case-insensitive matching
        return apid_dict[subsystem.lower()]
    except KeyError:
        # If the subsystem is not found, raise an ApidError
        raise ApidError(f"Subsystem '{subsystem}' not found in APID dictionary.")

# get_subsystem function retrieves the subsystem name for a given APID
# 
def get_subsystem(apid: int) -> str:
    # Get the subsystem name for a given APID.
    for subsystem, apid_value in apid_dict.items():
        if apid_value == apid:
            return subsystem
    raise ApidError(f"Error retrieving subsystem for APID {apid}")

# get_all_apids function returns a copy of the APID dictionary
# This allows other parts of the system to access all APIDs without modifying the original dictionary
def get_all_apids() -> dict:
    """
    Get a dictionary of all subsystems and their APIDs.

    Returns:
        dict: A dictionary mapping subsystem names to their APIDs.
    """
    return apid_dict.copy()

# is_valid_apid function checks if a given APID is valid
# It returns True if the APID exists in the dictionary, otherwise False
def is_valid_apid(apid: int) -> bool:
    """
    Check if a given APID is valid.

    Args:
        apid (int): The APID to check.

    Returns:
        bool: True if the APID is valid, False otherwise.
    """
    return apid in apid_dict.values()

# is_valid_subsystem function checks if a given subsystem name is valid
# It returns True if the subsystem exists in the dictionary, otherwise False
def is_valid_subsystem(subsystem: str) -> bool:
    """
    Check if a given subsystem is valid.

    Args:
        subsystem (str): The name of the subsystem to check.

    Returns:
        bool: True if the subsystem is valid, False otherwise.
    """
    return subsystem.lower() in apid_dict

# get_subsystem_count function returns the total number of subsystems
# This is useful for understanding how many subsystems are defined in the system
# It returns the length of the apid_dict dictionary
def get_subsystem_count() -> int:
    """
    Get the total number of subsystems.

    Returns:
        int: The number of subsystems.
    """
    return len(apid_dict)

# get_subsystem_list function returns a list of all subsystem names
# This allows other parts of the system to easily access the names of all subsystems
# It returns the keys of the apid_dict dictionary as a list
def get_subsystem_list() -> list:
    """
    Get a list of all subsystem names.

    Returns:
        list: A list of subsystem names.
    """
    return list(apid_dict.keys())

# get_apid_list function returns a list of all APIDs
# This allows other parts of the system to easily access the APIDs without modifying the original dictionary
# It returns the values of the apid_dict dictionary as a list
def get_apid_list() -> list:
    """
    Get a list of all APIDs.

    Returns:
        list: A list of APIDs.
    """
    return list(apid_dict.values())
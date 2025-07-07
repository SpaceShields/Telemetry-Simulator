from src.ccsds import apid
import pytest

def test_get_apid_invalid():
    with pytest.raises(apid.ApidError):
        apid.get_apid("unknown")

def test_get_subsystem_invalid():
    with pytest.raises(apid.ApidError):
        apid.get_subsystem(0x08)


# Test cases for the APID module using pytest
# These tests cover the functionality of getting APIDs, subsystems, and validating them.

# test_get_apid function checks if the correct APID is returned for a given subsystem name
# It raises an AssertionError if the expected APID does not match the actual APID returned by the function
def test_get_apid():
    assert apid.get_apid("cdh") == 0x01
    assert apid.get_apid("power") == 0x02
    assert apid.get_apid("comms") == 0x03
    assert apid.get_apid("thermal") == 0x04
    assert apid.get_apid("adcs") == 0x05
    assert apid.get_apid("propulsion") == 0x06
    assert apid.get_apid("payload") == 0x07
    with pytest.raises(apid.ApidError):
        apid.get_apid("unknown")
# test_get_subsystem function checks if the correct subsystem name is returned for a given APID
# It raises an AssertionError if the expected subsystem name does not match the actual subsystem name returned
# by the function
def test_get_subsystem():
    assert apid.get_subsystem(0x01) == "cdh"
    assert apid.get_subsystem(0x02) == "power"
    assert apid.get_subsystem(0x03) == "comms"
    assert apid.get_subsystem(0x04) == "thermal"
    assert apid.get_subsystem(0x05) == "adcs"
    assert apid.get_subsystem(0x06) == "propulsion"
    assert apid.get_subsystem(0x07) == "payload"
    with pytest.raises(apid.ApidError):
        apid.get_subsystem(0x08)

# test_get_all_apids function checks if the dictionary of all APIDs is correctly returned
# It asserts that the returned dictionary is of type dict, has the correct number of entries,
# and that each subsystem has the expected APID value
def test_get_all_apids():
    apids = apid.get_all_apids()
    assert isinstance(apids, dict)
    assert len(apids) == 7
    assert apids["cdh"] == 0x01
    assert apids["power"] == 0x02
    assert apids["comms"] == 0x03
    assert apids["thermal"] == 0x04
    assert apids["adcs"] == 0x05
    assert apids["propulsion"] == 0x06
    assert apids["payload"] == 0x07

# test_get_subsystem_list function checks if the list of subsystem names is correctly returned
# It asserts that the returned list is of type list, has the correct number of entries,
# and that each expected subsystem name is present in the list
def test_get_subsystem_list():
    subsystems = apid.get_subsystem_list()
    assert isinstance(subsystems, list)
    assert len(subsystems) == 7
    assert "cdh" in subsystems
    assert "power" in subsystems
    assert "comms" in subsystems
    assert "thermal" in subsystems
    assert "adcs" in subsystems
    assert "propulsion" in subsystems
    assert "payload" in subsystems

# test_get_apid_list function checks if the list of APIDs is correctly returned
# It asserts that the returned list is of type list, has the correct number of entries,
# and that each expected APID is present in the list
def test_get_apid_list():
    apids = apid.get_apid_list()
    assert isinstance(apids, list)
    assert len(apids) == 7
    assert 0x01 in apids
    assert 0x02 in apids
    assert 0x03 in apids
    assert 0x04 in apids
    assert 0x05 in apids
    assert 0x06 in apids
    assert 0x07 in apids

# test_is_valid_apid function checks if the APID validation works correctly
# It asserts that valid APIDs return True and invalid APIDs return False
def test_is_valid_apid():
    assert apid.is_valid_apid(0x01) is True
    assert apid.is_valid_apid(0x02) is True
    assert apid.is_valid_apid(0x03) is True
    assert apid.is_valid_apid(0x04) is True
    assert apid.is_valid_apid(0x05) is True
    assert apid.is_valid_apid(0x06) is True
    assert apid.is_valid_apid(0x07) is True
    assert apid.is_valid_apid(0x08) is False

# test_is_valid_subsystem function checks if the subsystem validation works correctly
# It asserts that valid subsystem names return True and invalid ones return False
def test_is_valid_subsystem():
    assert apid.is_valid_subsystem("cdh") is True
    assert apid.is_valid_subsystem("comms") is True
    assert apid.is_valid_subsystem("power") is True
    assert apid.is_valid_subsystem("propulsion") is True
    assert apid.is_valid_subsystem("thermal") is True
    assert apid.is_valid_subsystem("adcs") is True
    assert apid.is_valid_subsystem("payload") is True
    assert apid.is_valid_subsystem("unknown") is False

# test_get_subsystem_count function checks if the count of subsystems is correct
# It asserts that the count is an integer and matches the expected number of subsystems
def test_get_subsystem_count():
    count = apid.get_subsystem_count()
    assert isinstance(count, int)
    assert count == 7


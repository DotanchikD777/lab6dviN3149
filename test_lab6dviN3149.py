import pytest
from lab6dviN3149 import FormatError, UndoError, RedoError, MACAddressDict

def test_setitem_valid_mac():
    mac_dict = MACAddressDict()
    mac_dict['key1'] = '01:23:45:67:89:AB'
    assert mac_dict['key1'] == '01:23:45:67:89:AB'

def test_setitem_invalid_mac():
    mac_dict = MACAddressDict()
    with pytest.raises(FormatError):
        mac_dict['key1'] = 'инвалид_mac'

def test_delitem():
    mac_dict = MACAddressDict({'key1': '01:23:45:67:89:AB'})
    del mac_dict['key1']
    assert 'key1' not in mac_dict

def test_update_valid_macs():
    mac_dict = MACAddressDict()
    mac_dict.update({'key1': '01:23:45:67:89:AB', 'key2': 'CD:EF:01:23:45:67'})
    assert mac_dict['key1'] == '01:23:45:67:89:AB'
    assert mac_dict['key2'] == 'CD:EF:01:23:45:67'

def test_update_invalid_mac():
    mac_dict = MACAddressDict()
    with pytest.raises(FormatError):
        mac_dict.update({'key1': '01:23:45:67:89:AB', 'key2': 'инвалид_mac'})

def test_undo_setitem():
    mac_dict = MACAddressDict()
    mac_dict['key1'] = '01:23:45:67:89:AB'
    mac_dict.undo()
    assert 'key1' not in mac_dict

def test_undo_delitem():
    mac_dict = MACAddressDict({'key1': '01:23:45:67:89:AB'})
    del mac_dict['key1']
    mac_dict.undo()
    assert mac_dict['key1'] == '01:23:45:67:89:AB'

def test_undo_update():
    mac_dict = MACAddressDict()
    mac_dict.update({'key1': '01:23:45:67:89:AB', 'key2': 'CD:EF:01:23:45:67'})
    mac_dict.undo()
    assert 'key1' not in mac_dict
    assert 'key2' not in mac_dict

def test_redo_setitem():
    mac_dict = MACAddressDict()
    mac_dict['key1'] = '01:23:45:67:89:AB'
    mac_dict.undo()
    mac_dict.redo()
    assert mac_dict['key1'] == '01:23:45:67:89:AB'

def test_redo_delitem():
    mac_dict = MACAddressDict({'key1': '01:23:45:67:89:AB'})
    del mac_dict['key1']
    mac_dict.undo()
    mac_dict.redo()
    assert 'key1' not in mac_dict

def test_redo_update():
    mac_dict = MACAddressDict()
    mac_dict.update({'key1': '01:23:45:67:89:AB', 'key2': 'CD:EF:01:23:45:67'})
    mac_dict.undo()
    mac_dict.redo()
    assert mac_dict['key1'] == '01:23:45:67:89:AB'
    assert mac_dict['key2'] == 'CD:EF:01:23:45:67'

def test_undo_error_empty_history():
    mac_dict = MACAddressDict()
    with pytest.raises(UndoError):
        mac_dict.undo()

def test_redo_error_empty_future():
    mac_diict = MACAddressDict()
    with pytest.raises(RedoError):
        mac_diict.redo()

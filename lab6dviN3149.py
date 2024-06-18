import collections
import re

class FormatError(Exception):
    pass

class UndoError(Exception):
    pass

class RedoError(Exception):
    pass

class MACAddressDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.history = []
        self.redo_stack = []

    def __setitem__(self, key, value):
        if not self._validate_mac(value):
            raise FormatError(f"Неправильный формат MAC адреса: {value}")
        super().__setitem__(key, value)
        self.history.append(('setitem', key, value))
        self.redo_stack.clear()  # Очистить redo stack после действия

    def __delitem__(self, key):
        value = self[key]
        super().__delitem__(key)
        self.history.append(('delitem', key, value))
        self.redo_stack.clear()  # как и раньше

    def update(self, *args, **kwargs):
        for key, value in dict(*args, **kwargs).items():
            if not self._validate_mac(value):
                raise FormatError(f"Неправильный формат MAC адреса: {value}")
        super().update(*args, **kwargs)
        self.history.append(('update', dict(*args, **kwargs)))
        self.redo_stack.clear()  # на западном фронте без перемен

    def undo(self):
        if not self.history:
            raise UndoError("Нет действий для отмены")
        action, *data = self.history.pop()
        if action == 'setitem':
            key, value = data
            if key in self and self[key] == value:
                super().__delitem__(key)
        elif action == 'delitem':
            key, value = data
            super().__setitem__(key, value)
        elif action == 'update':
            for key in data[0]:
                super().__delitem__(key)
        self.redo_stack.append((action, *data))

    def redo(self):
        if not self.redo_stack:
            raise RedoError("Нет действий для отмены отмены")
        action, *data = self.redo_stack.pop()
        if action == 'setitem':
            key, value = data
            self.__setitem__(key, value)
            self.history.pop()  # Удалить повторяющееся действие из истории
        elif action == 'delitem':
            key, value = data
            self.__delitem__(key)
            self.history.pop()  # Удалить повторяющееся действие из истории
        elif action == 'update':
            self.update(data[0])
            self.history.pop()  # Удалить повторяющееся действие из истории

    def _validate_mac(self, mac): #проверка MAC адреса
        pattern = r'^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$'
        return re.match(pattern, mac) is not None

from src.unique_exceptions.exceptions import UndoRedoException
from src.unique_exceptions import exceptions


class Command:

    def __init__(self, fn, *args):
        self._fn = fn
        self._params = args

    def execute(self):
        self._fn(*self._params)


class Operation:

    def __init__(self, undo_action: Command, redo_action: Command):
        self.__undo_action = undo_action
        self.__redo_action = redo_action

    def undo(self):
        self.__undo_action.execute()

    def redo(self):
        return self.__redo_action.execute()

class CascadedOperation:

    def __init__(self, operation_list: list[Operation]):
        self.__operation_list = operation_list

    def undo(self):
        for operation in self.__operation_list:
            operation.undo()

    def redo(self):
        for operation in reversed(self.__operation_list):
            operation.redo()

class UndoService:
    def __init__(self):
        self.__undo_stack = []
        self.__redo_stack = []
        self.__is_undoredo_op = False

    def clear_redo_stack(self):
        self.__redo_stack = []

    def record_for_undo(self, operation: Operation):
        if self.__is_undoredo_op:
            return

        self.clear_redo_stack()
        self.__undo_stack.append(operation)

    def undo(self):
        if len(self.__undo_stack) == 0:
            raise exceptions.UndoRedoException("No more undos")
        self.__is_undoredo_op = True
        operation = self.__undo_stack.pop()
        operation.undo()
        self.__redo_stack.append(operation)
        self.__is_undoredo_op = False

    def redo(self):
        if len(self.__redo_stack) == 0:
            raise exceptions.UndoRedoException("No more redo")
        self.__is_undoredo_op = True
        operation = self.__redo_stack.pop()
        operation.redo()
        self.__undo_stack.append(operation)
        self.__is_undoredo_op = False

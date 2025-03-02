from CANTreeItem import CANTreeItem

from PyQt5.QtCore import QModelIndex, Qt, QAbstractItemModel
from PyQt5.QtWidgets import QTreeModel

class CANTreeModel(QTreeModel):

    def __init__(self, headers: list, data: str, parent=None):
        super().__init__(parent)

        self.root_data = headers
        self.root_item = CANTreeItem(self.root_data.copy())
        self.setup_model_data(data.split("\n"), self.root_item)

    def columnCount(self, parent: QModelIndex = None) -> int:
        return self.root_item.column_count()

    def data(self, index: QModelIndex, role: int = None):
        if not index.isValid():
            return None

        if role != Qt.ItemDataRole.DisplayRole and role != Qt.ItemDataRole.EditRole:
            return None

        item: CANTreeItem = self.get_item(index)

        return item.data(index.column())

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags

        return Qt.ItemFlag.ItemIsEditable | QAbstractItemModel.flags(self, index)

    def get_item(self, index: QModelIndex = QModelIndex()) -> CANTreeItem:
        if index.isValid():
            item: CANTreeItem = index.internalPointer()
            if item:
                return item

        return self.root_item

    def headerData(self, section: int, orientation: Qt.Orientation,
                   role: int = Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.root_item.data(section)

        return None

    def index(self, row: int, column: int, parent: QModelIndex = QModelIndex()) -> QModelIndex:
        if parent.isValid() and parent.column() != 0:
            return QModelIndex()

        parent_item: CANTreeItem = self.get_item(parent)
        if not parent_item:
            return QModelIndex()

        child_item: CANTreeItem = parent_item.child(row)
        if child_item:
            return self.createIndex(row, column, child_item)
        return QModelIndex()

    def insertColumns(self, position: int, columns: int,
                      parent: QModelIndex = QModelIndex()) -> bool:
        self.beginInsertColumns(parent, position, position + columns - 1)
        success: bool = self.root_item.insert_columns(position, columns)
        self.endInsertColumns()

        return success

    def insertRows(self, position: int, rows: int,
                   parent: QModelIndex = QModelIndex()) -> bool:
        parent_item: CANTreeItem = self.get_item(parent)
        if not parent_item:
            return False

        self.beginInsertRows(parent, position, position + rows - 1)
        column_count = self.root_item.column_count()
        success: bool = parent_item.insert_children(position, rows, column_count)
        self.endInsertRows()

        return success

    def parent(self, index: QModelIndex = QModelIndex()) -> QModelIndex:
        if not index.isValid():
            return QModelIndex()

        child_item: CANTreeItem = self.get_item(index)
        if child_item:
            parent_item: CANTreeItem = child_item.parent()
        else:
            parent_item = None

        if parent_item == self.root_item or not parent_item:
            return QModelIndex()

        return self.createIndex(parent_item.child_number(), 0, parent_item)

    def removeColumns(self, position: int, columns: int,
                      parent: QModelIndex = QModelIndex()) -> bool:
        self.beginRemoveColumns(parent, position, position + columns - 1)
        success: bool = self.root_item.remove_columns(position, columns)
        self.endRemoveColumns()

        if self.root_item.column_count() == 0:
            self.removeRows(0, self.rowCount())

        return success

    def removeRows(self, position: int, rows: int,
                   parent: QModelIndex = QModelIndex()) -> bool:
        parent_item: CANTreeItem = self.get_item(parent)
        if not parent_item:
            return False

        self.beginRemoveRows(parent, position, position + rows - 1)
        success: bool = parent_item.remove_children(position, rows)
        self.endRemoveRows()

        return success

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        if parent.isValid() and parent.column() > 0:
            return 0

        parent_item: CANTreeItem = self.get_item(parent)
        if not parent_item:
            return 0
        return parent_item.child_count()

    def setData(self, index: QModelIndex, value, role: int) -> bool:
        if role != Qt.ItemDataRole.EditRole:
            return False

        item: CANTreeItem = self.get_item(index)
        result: bool = item.set_data(index.column(), value)

        if result:
            self.dataChanged.emit(index, index,
                                  [Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole])

        return result

    def setHeaderData(self, section: int, orientation: Qt.Orientation, value,
                      role: int = None) -> bool:
        if role != Qt.ItemDataRole.EditRole or orientation != Qt.Orientation.Horizontal:
            return False

        result: bool = self.root_item.set_data(section, value)

        if result:
            self.headerDataChanged.emit(orientation, section, section)

        return result

    def setup_model_data(self, lines: list, parent: CANTreeItem):
        parents = [parent]
        indentations = [0]

        for line in lines:
            line = line.rstrip()
            if line and "\t" in line:

                position = 0
                while position < len(line):
                    if line[position] != " ":
                        break
                    position += 1

                column_data = line[position:].split("\t")
                column_data = [string for string in column_data if string]

                if position > indentations[-1]:
                    if parents[-1].child_count() > 0:
                        parents.append(parents[-1].last_child())
                        indentations.append(position)
                else:
                    while position < indentations[-1] and parents:
                        parents.pop()
                        indentations.pop()

                parent: CANTreeItem = parents[-1]
                col_count = self.root_item.column_count()
                parent.insert_children(parent.child_count(), 1, col_count)

                for column in range(len(column_data)):
                    child = parent.last_child()
                    child.set_data(column, column_data[column])

    def _repr_recursion(self, item: CANTreeItem, indent: int = 0) -> str:
        result = " " * indent + repr(item) + "\n"
        for child in item.child_items:
            result += self._repr_recursion(child, indent + 2)
        return result

    def __repr__(self) -> str:
        return self._repr_recursion(self.root_item)
from collections import deque


class BSTNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1


class BST:
    def __init__(self):
        self.root = None
        self.size = 0

# пользователи могут взаимодействовать
    def insert(self, key):  # добавление элемента
        self.root = self._insert(self.root, key)
        self.size += 1

    def delete(self, key):  # удаление элемента
        before = self.size
        self.root = self._delete(self.root, key)
        if self.size < before:
            return

    def search(self, key):  # поиск эл-та
        return self._search(self.root, key)

    def get_height(self):   # высота дерева
        return self._get_height(self.root)

    def inorder_traversal(self):    # центрированный проход
        result = []
        self._inorder(self.root, result)
        return result

    def preorder_traversal(self):   # прямой проход
        result = []
        self._preorder(self.root, result)
        return result

    def postorder_traversal(self):  # обратный проход
        result = []
        self._postorder(self.root, result)
        return result

    def level_order_traversal(self):    # обход в ширину
        result = []
        if not self.root:
            return result

        queue = deque([self.root])
        while queue:
            node = queue.popleft()
            result.append(node.key)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return result

    def find_min(self):     # минимальный эл-т
        if not self.root:
            return None
        node = self.root
        while node.left:
            node = node.left
        return node.key

    def find_max(self):     # максимальный эл-т
        if not self.root:
            return None
        node = self.root
        while node.right:
            node = node.right
        return node.key

# пользователи не могут взаимодействовать
    def _insert(self, node, key):
        if not node:
            return BSTNode(key)

        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)

        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        return node

    def _delete(self, node, key):
        if not node:
            return None

        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            else:
                min_node = self._find_min(node.right)
                node.key = min_node.key
                node.right = self._delete(node.right, min_node.key)

        if node:
            node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        return node

    def _find_min(self, node):
        while node.left:
            node = node.left
        return node

    def _search(self, node, key):
        if not node:
            return False
        if key == node.key:
            return True
        return self._search(node.left if key < node.key else node.right, key)

    def _get_height(self, node):
        return node.height if node else 0

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.key)
            self._inorder(node.right, result)

    def _preorder(self, node, result):
        if node:
            result.append(node.key)
            self._preorder(node.left, result)
            self._preorder(node.right, result)

    def _postorder(self, node, result):
        if node:
            self._postorder(node.left, result)
            self._postorder(node.right, result)
            result.append(node.key)
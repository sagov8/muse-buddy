class AppState:
    def __init__(self, root: dict):
        self.root = root
        self.current_node = root
        self.path = [root]
        self.ai_result = ""
        self.is_generating = False

    def reset(self):
        self.current_node = self.root
        self.path = [self.root]
        self.ai_result = ""
        self.is_generating = False

    def go_to_node(self, node: dict):
        self.current_node = node
        self.path.append(node)
        self.ai_result = ""

    def go_back(self):
        if len(self.path) > 1:
            self.path.pop()
            self.current_node = self.path[-1]
            self.ai_result = ""

    def go_to_path_index(self, index: int):
        self.path = self.path[: index + 1]
        self.current_node = self.path[-1]
        self.ai_result = ""

    def is_leaf(self) -> bool:
        return len(self.current_node.get("hijos", [])) == 0

    def get_context(self):
        valores = [n.get("valor", "") for n in self.path]
        tema = valores[0] if len(valores) > 0 else ""
        categoria = valores[1] if len(valores) > 1 else ""
        mood = valores[2] if len(valores) > 2 else ""
        return tema, categoria, mood
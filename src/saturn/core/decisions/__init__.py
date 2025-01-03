import saturn.core.decisions.nodes as nodes
from saturn.core.decisions.DecisionNode import DecisionNode
from saturn.utils.ClassUtil import get_special_modules

node_map = {m.__name__: m() for m in get_special_modules(nodes.__name__, DecisionNode)}  # type:ignore[abstract]


import pydot
import tempfile

class TreeRender:
  def __init__(self, tree_data):
    self.tree_data = tree_data
    self.dot_index = 0
    self.data = None

  def _create_dot_node(self, layer, name):
    print 'add node: ix: %d, lyr: %d, name: %s' % (self.dot_index, layer, name)
    dot_node = pydot.Node('index_%d_layer_%d' % (self.dot_index, layer), label=name)
    self.dot_index += 1
    return dot_node

  def _draw_nodes(self, nodes, graph, parent_dot_node, layer):
    for node in nodes:
      dot_node = self._create_dot_node(layer, node['name'])
      graph.add_node(dot_node)
      graph.add_edge(pydot.Edge(parent_dot_node, dot_node))
      self._draw_nodes(node['lower_nodes'], graph, dot_node, layer+1)

  def create(self):
    graph = pydot.Dot(graph_type='graph')
    layer = 0
    self.dot_index = 0
    dot_node = self._create_dot_node(layer, self.tree_data['name'])
    graph.add_node(dot_node)
    self._draw_nodes(self.tree_data['lower_nodes'], graph, dot_node, layer+1)

    (_, filename) = tempfile.mkstemp()
    graph.write_svg(filename)
    print 'writing to: %s' % (filename)
    with open(filename) as fh:
      self.data = fh.read()

#    os.remove(filename)

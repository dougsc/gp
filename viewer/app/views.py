from flask import render_template, jsonify
from app import app
from utils import stats
from utils.tree_render import TreeRender


def _tree_render(index):
  resp_data = {'index': index, 'tree': 'tree index %s not found' % (index)}
  tree_data = stats.get_data('Runner:best_tree')
  tree_render = TreeRender(tree_data[index]['tree'])
  tree_render.create()
  resp_data['tree'] = tree_render.data
  return jsonify(**resp_data)

@app.route('/tree/<int:index>')
def tree_render_ix(index):
  return _tree_render(index)

@app.route('/tree/latest')
def tree_render_latest():
  return _tree_render(-1)

@app.route('/')
@app.route('/graph')
def graph():
  return render_template('graph.html',
                         title='Home')

@app.route('/graph/line/<string:data_id>')
def graph_data(data_id):
  data_id_map = {
    'lowest_error': {
      'data_key': 'Runner:lowest_error',
      'title': 'Lowest Error',
      'x_title': 'Generation',
      'y_title': 'Abs Error',
      'data_label': 'Abs Error'
    },
    'best_individual': {
      'data_key': 'Runner:best_individual',
      'title': 'Best Individual',
      'x_title': 'Generation',
      'y_title': 'Individual Index',
      'data_label': 'Best Individual'
    },
    'target_samples': {
      'data_key': 'Runner:target_samples',
      'title': 'Target Samples',
      'x_title': 'Index',
      'y_title': 'Value',
      'data_label': 'Target'
    },
    'actual_samples': {
      'data_key': 'Runner:actual_samples',
      'title': 'Actual Samples',
      'x_title': 'Index',
      'y_title': 'Value',
      'data_label': 'Actual'
    },
  }
  resp_data = data_id_map[data_id]
  resp_data['data'] = stats.get_data(resp_data['data_key'])
  return jsonify(**resp_data)

"""
quiz2!

Use path finding algorithm to find your way through dark dungeon!

Tecchnical detail wise, you will need to find path from node 7f3dc077574c013d98b2de8f735058b4
to f1f131f647621a4be7c71292e79613f9

TODO: implement BFS
TODO: implement Dijkstra utilizing the path with highest effect number
"""

import json
import codecs
from queue import *

# http lib import for Python 2 and 3: alternative 4
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

GET_STATE_URL = "http://192.241.218.106:9000/getState"
STATE_TRANSITION_URL = "http://192.241.218.106:9000/state"


def get_state(room_id):
    """
    get the room by its id and its neighbor
    """
    body = {'id': room_id}
    return __json_request(GET_STATE_URL, body)


def transition_state(room_id, next_room_id):
    """
    transition from one room to another to see event detail from one room to
    the other.

    You will be able to get the weight of edge between two rooms using this method
    """
    body = {'id': room_id, 'action': next_room_id}
    return __json_request(STATE_TRANSITION_URL, body)


def __json_request(target_url, body):
    """
    private helper method to send JSON request and parse response JSON
    """
    req = Request(target_url)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(body)
    jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))
    reader = codecs.getreader("utf-8")
    response = json.load(reader(urlopen(req, jsondataasbytes)))
    return response


def bfs(initial_node, dest_node):
    queue = Queue()
    graph = {}
    path = []
    got_result = False

    queue.put(initial_node)

    while queue.not_empty and got_result == False:
        room_id = queue.get()
        room_state = get_state(room_id)
        for node in room_state['neighbors']:
            if node['id'] not in graph:
                graph[node['id']] = room_id
                if dest_node == node['id']:
                    got_result = True
                    break
                queue.put(node['id'])

    current_position_id = dest_node
    room_state = get_state(current_position_id)
    current_room_name = room_state['location']['name'] + ' (' + current_position_id + ') HP'
    while current_position_id != initial_node:
        room_id = graph[current_position_id]
        room_state = get_state(room_id)
        room_name = room_state['location']['name']+ ' (' + room_id + ') HP'
        path.append(room_name + ':' + current_room_name + ':' + str(transition_state(room_id, current_position_id)['event']['effect']))
        current_position_id = room_id
        room_state = get_state(current_position_id)
        current_room_name = room_state['location']['name'] + ' (' + current_position_id + ') HP'

    path.reverse()
    return path


def dijstra(initial_node, dest_node):
    queue = []
    path = []
    queue.append((0, initial_node))
    distance = []
    distance[initial_node] = 0
    parent = {}
    edge = {}
    node_passed = []

    while bool(queue):
        current_room = get_state(queue.pop()[1])
        node_passed.append(current_room['id'])
        neighbors = current_room['neighbors']

        for i in range(len(neighbors)):
            pass




if __name__ == "__main__":
    # Your code starts here

    initial_node = '7f3dc077574c013d98b2de8f735058b4'
    dest_node = 'dadbd109410c73d838efec4867e4db57'

    path = bfs(initial_node, dest_node)

    for value in path:
        print(value)
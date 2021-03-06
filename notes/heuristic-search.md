# Heuristic Search

## Objective

* A* search
* Levels of optimization
* Exercise

## Metrics

* Able to implement A* search against GWCF game

## Levels of optimization

We have learned how to implement BFS, DFS and Dijkstra search so far. While those
search algorithms, given enough time and resource, will eventually find the answer,
they are not particularly good with performance aspect.

Lets say you are developing a game engine and want to host such game engine for
other developers to build games on top of your game engine. The path finding
API given in the game must be fast and efficient considering they will be used
over and over again in the game. E.g. the NPCs (non player characters) will be
using path finding API to find path almost on the daily basis.

That being said, there are usually two runtime limitations:

* Time
* Space

Time limitation usually refers to the memory consumption limitation. Lets say
you are developing a path finding algorithm for [cleaning roomba](http://www.irobotweb.com/-/media/Images/Product-Pages/Roomba-Learn/Feature-Callouts/Dirt-Detect.jpg?h=320&la=en&w=320) running with
its own hardware. A cleaning roomba usually doesn't have a lot of memory like
your laptop. Lets say it has at most 32MB of memory. It implies your search
algorithm cannot be using as much memory as you can. In other word, you will need
to create less variables or cut out the function stack for the memory.

On the other hand, the runtime limitation is trivial -- how fast the program
runs. DFS, BFS and Dijkstra are all considered to be under uninformed search,
which itself has no idea what tile is closer to goal until it finds the goal.

In this section, we will be learning over the informed search (sometimes refers
as heuristic search) to optimize the runtime as well as discuss about some other
algorithms used to avoid high memory problem.

### Depth-limited search

Depth-limited search is a modification off the Depth First Search to avoid the
memory limit issue. Its idea is to limit the depth while searching for the
solution so that it doesn't create an infinite loop searching for a path to
solution.

```js
function depthLimitedSearch(problem, limit) {
  return recursiveDLS(problem.initialState, problem, limit);
}

function recursiveDLS(node, problem, limit) {
  if (problem.goalTest(node))
    return solution(node);
  if (limit == 0) {
    return cutoff;
  }
  var cutoffOccurred = false;
  for (action in problem.actions(node)) {
    var childNode = childNode(problem, node, action);
    var result = recursiveDLS(child, problem, limit - 1);
    if (result == cutoff) {
      cutoffOccurred = true;
    } else if (result != failure) {
      return result;
    }
  }
  if (cutoffOccurred) {
    return cutoff;
  } else {
    return failure;
  }
}
```

### Iterative deepening depth-first search

Iterative deepening Depth-First Search, on the other hand, utilizes the depth
limit search above to search from the closest tile over to the larger depth to
simulate this breadth first search aspect.

```js
function iterativeDeepeningDFS(problem) {
  for (var depth = 0; depth < INTEGER.MAX_VALUE; depth ++) {
    var result = depthLimitedSearch(problem, depth);
    if (result != cutoff) {
      return result;
    }
  }
}
```

### Continue back to heuristic search

Golden article explaining A* search: http://www.redblobgames.com/pathfinding/a-star/introduction.html

Sometimes also being called **informed search** -- one that uses problem-specific
knowledge beyond the definition of the problem itself -- can find solutions more
efficiently than uninformed strategy like BFS, DFS and Dijkstra search.

The general approach we consider is called **best-first search**. Best-first
search is an instance of general graph-search algorithm in which a node is
selected for expansion based on an evaluation function, f(n). The evaluation
function is constructed as a cost estimate, so the node with lowest evaluation is
expanded first.

## Greedy best-first search

Greedy best-first search tries to expand the node that is closest to the goal, on
the grounds that this is likely to lead to a solution quickly.

For the grid based path finding, we will use the straight line distance heuristic.

> example of showing how important heuristic function is

## A* Search

> Minimizing the total estimated solution cost

The most widely known form of best-first search is called A* search. It combines
the cost to reach the node and the cost to get from node to the goal:

```js
f(n) = g(n) + h(n)

// g(n) is the path cost from the start node to node n
// h(n) is the estimated cost of the cheapest path from n to goal
```

Thus, if we are trying to find the cheapest solution, a reasonable thing to try
first is the node with lowest value of g(n) + h(n). It turns out that this
strategy is more than just reasonable: provide that heuristic function h(n)
satisfies certain conditions, A* search is both complete and optimal. The
algorithm is almost identical to uniform-cost-search (best-first search) except
that A* uses g+h instead of g.

### Conditions for optimality: Admissibility and consistency

The first condition we require for optimality is that h(n) be an **admissible
heuristic**. An admissible heuristic is one that *never overestimates* the cost
to reach the goal. Because g(n) is the actual cost to reach n along the current
path, and f(n) = g(n) + h(n), we have as an immediate consequence that f(n) never
overestimates the true cost of a solution along with current path through n.

An example of admissible heuristic is straight line distance between the node
to the goal because straight line cost will never over estimate the cost to goal.

Second condition is called **consistency** (or sometimes **monotonicity**) is
required only for applications of A* to graph search. A heuristic function is
consistent if, for every node n and every successor n' of n generated by any
action a, the estimated cost of reaching the goal from n is no greater than the
step cost of getting to n' plus the estimated cost of reaching the goal from n':

```
h(n) < c(n, a, n') + h(n')
```

This is a form of the general **triangle inequality**, which stipulates that each
side of a triangle cannot be longer than the sum of the other two sides.

```js
function AstarSearch(start, goal) {
    // create empty queue Q      
    var frontier = new Queue();
    var exploredSet = new HashSet();
    var parents = new Map();

    // use priority queue instead of normal queue
    frontier.enqueue(v);

    // initialize gScore and hScore
    gScore = new Map(); // given every cost is infinite by default
    gScore.put(start, 0);

    fScore = new Map();
    fScore.put(start, heuristicCost(start, goal));

    while (!frontier.isEmpty()) {
        // pop with the lowest fScore
        var u = queue.dequeue();
        if (u === goal) {
          return constructPath(u)
        }
        exploredSet.push(u);

        for (node in Graph.neighbors(u)) {
            if (exploredSet.contains(node)) {
                continue;
            }
            var tempGScore = gScore.get(u) + distance(u, node);
            if (!frontier.contains(node)) {
                frontier.push(node);
            } else if (tempGScore >= gScore.get(node)) {
                continue; // skip because we are at the worse path
            }

            parent.put(node, u);
            gScore.put(node, tempGScore);
            fScore.put(node, gScore.get(node) + heuristicCost(node, goal))
        }
    }

    // no answer!
    return false;
}
```

### Memory-bounded heuristic search

Regardless of how good A* search algorithm is, A* search algorithm still uses a
lot of memory. What if we have the memory limitation? How do we modify the
algorithm?

The simplest way to reduce memory requirement for A* is to adapt the idea of
iterative deepening to the heuristic search context, resulting in the
iterative-deepening A* (IDA*) algorithm. The main difference between IDA* and
standard iterative deepening is that the cutoff used is the f-cost rather than
the depth; each iteration, the cutoff value is the smallest f-cost of any node
that exceeded the cutoff on the previous iteration.

```js
function IDA(start) {
  var bound = heuristic(start)
  while (true) {
    var t = search(start, 0, bound)
    if (t = FOUND)
      return bound
    if (t = ∞)
      return NOT_FOUND
    bound = t
  }
}

function search(node, g, bound) {
  var f = g + h(node)
  if (f > bound)
    return f
  if is_goal(node)
    return FOUND
  var min = ∞
  for neighbors in neighbors(node) {
    var t = search(neighbor, g + cost(node, neighbor), bound)
    if (t = FOUND)
      return FOUND
    if (t < min)
      min = t
  }
  return min
}
```

### Exercise: Wolf Goat Cabbage Farmer game

play game: http://jeux.lulu.pagesperso-orange.fr/html/anglais/loupChe/loupChe1.htm

xkcd solution: http://xkcd.com/1134/

Please implement WGCFGameAgent and WGCFGameAgentLevel2 with BFS, and A*;

### Wolf Goat Cabbage Farmer game discussion

TBD.

### Homework discussion

TBD.

### Heuristic function design

The heuristic function can be used to control A* search behavior:

1. If the heuristic function always returns 0, A* will perform the same as Dijkstra search algorithm -- which is guaranteed to find the shortest path.
2. If the heuristic function is always lower than (or equals to) the cost moving from node n to goal, then A* is also guaranteed to find the shortest path. The lower value heuristic function returns the more nodes it expands and thus slower.
3. If the heuristic function always returns the actual cost from node n to goal, then A* will only travel along the best possible path and nothing else. This is often not possible unless under some certain conditions. It's good to know that A* can perform perfectly at some cases.
4. If the heuristic function returns the value sometimes larger than the actual cost, A* is not sure to get the shortest path but it can run faster.
5. At the extreme case, if heuristic function returns way larger value than the actual cost, A* behaves like greedy-best-first-search.

We come to an interesting case, we can adjust our heuristic function to aim for performance or accuracy. Say if you are building a game agent that has to find path all the time but doesn't need always find the best path, you might increase the heuristic cost a bit for better performance.


#### Grid map heuristic functions

##### Manhattan distance

```js
function heuristic(node, goal) {
  var dx = Math.abs(node.x - goal.x);
  var dy = Math.abs(node.y - goal.y);
  // D is a scale value for you to adjust performance vs accuracy
  return D * (dx + dy);
}
```

When allowing diagonal movement consider the following heuristic function:

```js
// use when allowing diagonal movements between grid tiles
function heuristic(node, goal) {
  var dx = Math.abs(node.x - goal.x);
  var dy = Math.abs(node.y - goal.y);
  return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy);
}
```

> When D and D2 = 1, this is called Chebyshev distance.  
> When D = 1 and D2 = sqrt(2), this is called the octile distance.

##### Euclidean distance

```js
function heuristic(node, goal) {
  var dx = Math.abs(node.x - goal.x);
  var dy = Math.abs(node.y - goal.y);
  return D * Math.sqrt(dx * dx + dy * dy);
}
```

However, for this case, since the Euclidean distance is always shorter than the actual cost. You will get the shortest path with the cost of running slower.

### A* toward multiple goals

What happens when you want to search A* toward multiple goals?

You can adjust your A* search heuristic to take multiple heuristic functions and work toward the shortest one!

### Tie breaker

What happened when you have tie between the F value, your A* search algorithm start to go off random places!

How do we deal with this situation?

We can adjust the heuristic value slightly. For example, we can multiple the heuristic values we get from the function by 1%!

> The factor we choose should be less than `(minimal steps to goal)/(maximum steps to goal)`

Or another modification to the tie breaker is always prefer the newly inserted node than the old nodes!

Credit: http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html

More visualization notes: http://www.redblobgames.com/pathfinding/a-star/introduction.html

### Performance improvement of A*

> When we talk about performance, the first thing is to **monitor** (or sometimes called profiling your methods)

For the A* search algorithm, we have a couple ways we can optimize the run time:

* Decrease the size of graph. Generalizing the graph like [navigation mesh](http://theory.stanford.edu/~amitp/GameProgramming/MapRepresentations.html#polygonal-maps)
* Adjust heuristic (as discussed above)
* Make priority queue faster (what other data structure we can use for priority queue? *ahem* heap!)
* Cache heuristic function value?

### More example of path finding

https://www.kevanahlquist.com/osm_pathfinding/

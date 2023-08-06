# nxquickplot

Convenient plotting for graphs in NetworkX.

## API

### Draw the graph with a force-directed layout

    import quickplot from nxquickplot
    import networkx

    g = networkx.DiGraph()

    g.add_node('Alice')
    g.add_node('Bob')
    g.add_edge('Alice', 'Bob')

    qp(g)



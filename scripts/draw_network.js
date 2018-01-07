var graph = null;
var partial_graph = null;

function cache_network(response, param) {
    console.log(response);
    graph = JSON.parse(response);
    console.log("draw_chart: number of nodes " + graph["nodes"].length);
    console.log("draw_chart: number of edges " + graph["edges"].length);
    draw_chart();
}

function network_nodes() {
    return graph["nodes"];
}

function network_edges() {
    return graph["edges"]
}

function reset_chart() {
    draw_chart(); 
}

function set_avl_node_types(nodes, select_type_id) {


}

function set_avl_nodes(nodes, select_node_id) {

}

function draw_chart() {

    var nodes = new vis.DataSet(network_nodes());
    var edges = new vis.DataSet(network_edges());

    var optionsIO = {
        groups: {
            org: {
                shape: 'icon',
                icon: {
                    face: 'FontAwesome',
                    code: '\uf1ad',
                    size: 50,
                    color: '#f0a30a'
                }
            },
            case: {
                shape: 'icon',
                icon: {
                    face: 'FontAwesome',
                    code: '\uf02d',
                    size: 50,
                    color: '#57169a'
                }
            },
            article: {
                shape: 'icon',
                icon: {
                    face: 'FontAwesome',
                    code: '\uf1ea',
                    size: 50,
                    color: '#57169a'
                }
            },
            person: {
                shape: 'icon',
                icon: {
                    face: 'FontAwesome',
                    code: '\uf007',
                    size: 50,
                    color: '#aa00ff'
                }
            }
        }
    };

    // create a network
    var container = document.getElementById("myNetwork");

    // provide the data in the vis format
    var data = {
        nodes: nodes,
        edges: edges
    };

    // initialize your network!
    // Check if there are any elements already existing

    var network = new vis.Network(container, data, optionsIO);
}
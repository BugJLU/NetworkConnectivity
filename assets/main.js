var s = null;

$(document).ready(function () {

    function isArrayFn(value) {
        if (typeof Array.isArray === "function") {
            return Array.isArray(value);
        } else {
            return Object.prototype.toString.call(value) === "[object Array]";
        }
    }

    sigma.classes.graph.addMethod('neighbors', function (nodeId) {
        var k,
            neighbors = {},
            index = this.allNeighborsIndex[nodeId] || {};

        for (k in index)
            neighbors[k] = this.nodesIndex[k];

        return neighbors;
    });

    s = new sigma('container');

    function read(graph, callback) {
        s.graph.clear();
        s.graph.read(graph);

        function set_color(o) {
            if (o.color === undefined) {
                o.color = '#B30000';
            }
            o.originalColor = o.color;
        }

        if (callback)
            callback(s);

        s.graph.nodes().forEach(set_color);
        s.graph.edges().forEach(set_color);

        s.refresh();
    }

    function try_save(content, filename) {

        if ($('#ask_download')[0].checked &&
            confirm('Do you want to save file as "' + filename + '"?')) {
            window.open('data:application/json:' + JSON.stringify(content), '_blank');
        }
    }

    $('#generate').click(function () {
        $.ajax({
            url: '/generate',
            data: {
                node_num: $('#node_num').val(),
                edge_num: $('#edge_num').val()
            },
            success: function (data) {
                if (data['result'] === true) {
                    $.ajax({
                        url: '/raw_graph',
                        success: function (data) {
                            read(data['graph']);
                            try_save(data, 'random.json');
                        }
                    });

                } else {
                    alert("Generate Fail!");
                }
            }
        });
    });

    $('#refresh').click(function () {
        $.ajax({
            url: '/raw_graph',
            success: function (data) {
                read(data['graph']);
                try_save(data, 'raw_graph.json');
            }
        });
        //refresh();
    });

    $('#redundancy').click(function () {
        $.ajax({
            url: '/redundancy',
            success: function (data) {
                read(data['graph']);
                try_save(data, 'no_redundancy.json');
            }
        });
        /*$.ajax({
         url: '/redundancy',
         success: function (data) {
         if (isArrayFn(data['result'])) {
         data['result'].forEach(function (e) {
         s.graph.edges()[e].color = '#c79c9c';
         });
         s.refresh();
         } else {
         alert("Check Redundancy Error!")
         }
         }
         });*/
    });

    $('#reliability').click(function () {
        $.ajax({
            url: '/reliability',
            success: function (data) {
                if (data['result'] === true) {
                    alert('The graph is reliable.');
                } else {
                    read(data['graph'], function (s) {
                        data['edges'].forEach(function (e) {
                            s.graph.edges()[e].color = '#000';
                        });
                    });
                }
                try_save(data, 'reliability.json')
            }
        });
    });

    $('#key_node').click(function () {
        $.ajax({
            url: '/key_node',
            success: function (data) {
                if (isArrayFn(data['result'])) {
                    data['result'].forEach(function (e) {
                        s.graph.nodes()[e].color = '#000';
                    });
                    s.refresh();
                } else {
                    alert("Check Key Node Error!")
                }
            }
        });
    });

    s.bind('clickStage', function (e) {
        s.graph.nodes().forEach(function (n) {
            n.color = n.originalColor;
        });

        s.graph.edges().forEach(function (e) {
            e.color = e.originalColor;
        });

        // Same as in the previous event:
        s.refresh();
    });

    s.bind('clickNode', function (e) {
        var nodeId = e.data.node.id,
            toKeep = s.graph.neighbors(nodeId);
        toKeep[nodeId] = e.data.node;

        s.graph.nodes().forEach(function (n) {
            if (toKeep[n.id])
                n.color = n.originalColor;
            else
                n.color = '#c79c9c';
        });

        s.graph.edges().forEach(function (e) {
            if (toKeep[e.source] && toKeep[e.target])
                e.color = e.originalColor;
            else
                e.color = '#c79c9c';
        });

        s.refresh();

    });
});


/*sigma.parsers.json(
 '/json',
 {
 container: 'container'
 },
 function (s) {
 sigma_instance = s;

 s.graph.nodes().forEach(function (n) {
 n.originalColor = n.color;
 });
 s.graph.edges().forEach(function (e) {
 e.originalColor = e.color;
 });


 }
 );*/





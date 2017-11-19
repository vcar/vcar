$(window).load(function() {
    // ----------------- Vehicle Speed
    client.search(
        getData('vehicle_speed')
    ).then(function(resp) {
        speed = drawChart(resp.hits.hits, 'vehicle_speed', 'Vehicle Speed')
    }, function(err) {
        console.trace(err.message);
    });

    // ----------------- Engine Speed
    client.search(
        getData('engine_speed')
    ).then(function(resp) {
        engine = drawChart(resp.hits.hits, 'engine_speed', 'Engine Speed', 'yellow-chart')
    }, function(err) {
        console.trace(err.message);
    });

    // ----------------- Fuel Level
    client.search(
        getData('fuel_level')
    ).then(function(resp) {
        fuel = drawChart(resp.hits.hits, 'fuel_level', 'Fuel Level', 'purple-chart')
    }, function(err) {
        console.trace(err.message);
    });

    // ----------------- Fuel Consumed
    client.search(
        getData('fuel_consumed_since_restart')
    ).then(function(resp) {
        fuel_consumed = drawChart(resp.hits.hits, 'fuel_consumed_since_restart', 'Fuel Consumed', 'red-chart')
    }, function(err) {
        console.trace(err.message);
    });

    // ----------------- Odometer
    client.search(
        getData('odometer')
    ).then(function(resp) {
        odometer = drawChart(resp.hits.hits, 'odometer', 'Odometer', 'green-chart')
    }, function(err) {
        console.trace(err.message);
    });

    // ----------------- Pedal Position
    client.search(
        getData('accelerator_pedal_position')
    ).then(function(resp) {
        pedal = drawChart(resp.hits.hits, 'accelerator_pedal_position', 'Pedal Position', 'red-chart')
    }, function(err) {
        console.trace(err.message);
    });

    // ----------------- Torque
    client.search(
        getData('torque_at_transmission')
    ).then(function(resp) {
        torque = drawChart(resp.hits.hits, 'torque_at_transmission', 'Torque', 'blue-chart')
    }, function(err) {
        console.trace(err.message);
    });

    // ----------------- Steering Wheel
    client.search(
        getData('steering_wheel_angle')
    ).then(function(resp) {
        steering = drawChart(resp.hits.hits, 'steering_wheel_angle', 'Steering Wheel', 'blue-chart')
    }, function(err) {
        console.trace(err.message);
    });
});

// ----------------------------- Local functions -----------------------------

function getData(query, size, type, index) {
    index = index || 'openxc';
    type = type || 'driver_1';
    size = size || 3000;
    return {
        index: index,
        type: type,
        size: size,
        body: {
            query: {
                term: {
                    name: query
                }
            }
        }
    }
}

function drawChart(hits, id, title, chartClass) {
    items = []
    var i = 0;
    for (i = 0; i < hits.length; i++) {
        items[i] = {
            x: new Date(parseInt(hits[i]._source.timestamp)),
            y: hits[i]._source.value,
            group: 1
        }
    }
    var start = items[0].x;
    var end = items[i - 1].x;
    var container = document.getElementById(id);
    // $("#"+id).parents(".vcar-box").find('span.badge').text(i + ' hits');
    var dataset = new vis.DataSet(items);
    var groups = new vis.DataSet();
    groups.add({
        id: 1,
        content: title,
        className: chartClass || "",
        options: {
            drawPoints: false,
            shaded: {
                orientation: 'bottom', // top, bottom4
            }
        }
    })
    var options = {
        sampling: true,
        clickToUse: true,
        showCurrentTime: false,
        width: '100%',
        dataAxis: {
            showMinorLabels: true,
            icons: true,
            left: {
                title: {
                    text: title
                }
            }
        },
        legend: true,
        start: start,
        end: end
    };
    return graph2d = new vis.Graph2d(container, dataset, groups, options);
}

// ---------------------------------- Noise ----------------------------------

// var dark = L.tileLayer('http://{s}.tile.thunderforest.com/transport-dark/{z}/{x}/{y}.png', {
// 	attribution: '&copy; <a href="http://www.thunderforest.com/">Thunderforest</a>, &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
// 	maxZoom: 19
// }).addTo(mymap);
// var layer = L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
// 	attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
// }).addTo(openMap);




// var dark = L.tileLayer('http://{s}.basemaps.cartocdn.com/dark_nolabels/{z}/{x}/{y}.png', {
// 	attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="http://cartodb.com/attributions">CartoDB</a>',
// 	subdomains: 'abcd',
// 	maxZoom: 19
// }).addTo(mymap);

// var layer = L.esri.basemapLayer('DarkGray').addTo(mymap);



// EventSource
// var source = new EventSource('/dashboard/stream');
// source.onmessage = function(event) {
//     console.log(event.data);
// };

// Elasticsearch
var client = new $.es.Client({
    host: 'localhost:9200',
    // log: 'trace'
});

// client.ping({
//     requestTimeout: 30000,
//     hello: "elasticsearch"
// }, function(error) {
//     if (error) {
//         console.error('elasticsearch cluster is down!');
//     } else {
//         console.log('All is well');
//     }
// });

//
// client.search({
//   q: 'vehicle_speed'
// }).then(function (body) {
//   var hits = body.hits.hits;
// }, function (error) {
//   console.trace(error.message);
// });
//
//
// client.search({
//     q: 'pants'
// }).then(function(body) {
//     var hits = body.hits.hits;
//     console.log(body);
// }, function(error) {
//     console.trace(error.message);
// });
//
//
// client.indices.exists({
//   index: 'openxcc',
//   ignore: [404]
// }).then(function (body) {
//   // since we told the client to ignore 404 errors, the
//   // promise is resolved even if the index does not exist
//   console.log('index was deleted or never existed');
// }, function (error) {
//   // oh no!
//   console.error(error);
// });

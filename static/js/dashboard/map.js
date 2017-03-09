// Elasticsearch
var client = new $.es.Client({
    host: 'localhost:9200',
    // log: 'trace'
});

$(window).load(function() {
    // ----------------- Map
    client.search(
        getMapData()
    ).then(function(resp) {
        drawMap(resp.hits.hits, "map");
    }, function(err) {
        console.trace(err.message);
    });

});

// ----------------------------- Local functions -----------------------------

function getMapData(size, type, index) {
    index = index || 'openxc';
    type = type || 'driver_1';
    size = size || 10000;
    return {
        index: index,
        type: type,
        size: size,
        body: {
            sort: [{
                timestamp: {
                    order: "asc"
                }
            }, ],
            query: {
                bool: {
                    should: [{
                        term: {
                            name: 'latitude'
                        }
                    }, {
                        term: {
                            name: 'longitude'
                        }
                    }]
                }
            }
        }
    }
}

function drawMap(query, id){
    coordinates = [];
    latitude = undefined;
    longitude = undefined;
    var i = 0;
    for (var i = 0; i < query.length; i++) {
        var value = query[i]._source.value;
        name = query[i]._source.name;
        if(name === "latitude") {
            latitude = value;
        }else if(name === "longitude"){
            longitude = value;
        }
        if(latitude != undefined && longitude != undefined){
            coordinates.push([longitude, latitude])
            latitude = longitude = undefined;
        }
    }
    $("#"+id).parents(".vcar-box").find('span.badge').text(i + ' points');

    var openMap = L.map(id, {
        fullscreenControl: {
            pseudoFullscreen: true
        }
    }).setView([coordinates[0][1], coordinates[0][0]], 14);

    var cartoUrl = 'http://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png';
    var osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
    var layers = {
        DarkMap:  L.tileLayer(cartoUrl, {minZoom: 5, maxZoom: 18}),
        LightMap: L.tileLayer(osmUrl, {minZoom: 5, maxZoom: 18})
    };
    openMap.addLayer(layers.DarkMap);
    L.control.layers(layers).addTo(openMap);
    var locations = {
        "type": "FeatureCollection",
        "features": [{
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": coordinates
            }
        }]
    };
    L.geoJson(locations).addTo(openMap);
    return openMap;
}

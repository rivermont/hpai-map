// TODO: Load color classes from settings file

var map = L.map('map', {
    center: [38, -92],  // map is moved to data bounds later
    zoom: 5,
    maxZoom: 12,
    minZoom: 3,
    detectRetina: true
});

L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {
    attribution: 'Basemap style &copy; CartoDB | Basemap data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap contributors</a> | County shapes: <a href="https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.html">U.S. Census Bureau, 2020</a> | Avian Flu data: <a href="https://www.aphis.usda.gov/aphis/ourfocus/animalhealth/animal-disease-information/avian/avian-influenza/hpai-2022/">USDA</a>'
}).addTo(map);

L.control.scale({position: 'bottomleft'}).addTo(map);


// Process captive bird data
var counties_captive = null;

colorsc = chroma.scale('YlGn').colors(11);
gradesc = [null, null, 1, 2, 3, 4, 5, 6, 7, 8];

function colorc(reports) {
    return colorsc[reports+2];
}

function stylec(feature) {
    return {
        fillColor: colorc(Number(feature.properties.num_report_cap)),
        fillOpacity: 0.4,
        weight: 2,
        opacity: 0.94,
        color: '#b4b4b4'
    };
}

counties_captive = L.geoJson.ajax("./hpai_counties_cap.geojson", {
    onEachFeature: function (feature, layer) {
        layer.bindPopup('<b>' + feature.name + ', ' + feature.properties.STUSPS + '</b><br>' + feature.properties.description);
    },
    style: stylec
}).addTo(map);


// process wild bird data
var counties_wild = null;

colorsw = chroma.scale('Oranges').colors(7);
gradesw1 = [1, 5, 10, 25, 50];
gradesw2 = [5, 10, 25, 50];

function colorw(reports) {
    if ( reports == 1 ) { return colorsw[1] }
    if ( reports > 1 && reports <= 5 ) { return colorsw[2] }
    if ( reports > 5 && reports <= 10 ) { return colorsw[3] }
    if ( reports > 10 && reports <= 25 ) { return colorsw[4] }
    if ( reports > 25 && reports <= 50 ) { return colorsw[5] }
    else { return colorsw[6] }
}

function stylew(feature) {
    return {
        fillColor: colorw(Number(feature.properties.num_report_wild)),
        fillOpacity: 0.4,
        weight: 2,
        opacity: 0.94,
        color: '#b4b4b4'
    }
}

counties_wild = L.geoJson.ajax("./hpai_counties_wild.geojson", {
    onEachFeature: function (feature, layer) {
        layer.bindPopup('<b>' + feature.name + ', ' + feature.properties.STUSPS + '</b><br>' + feature.properties.description);
    },
    style: stylew
}).addTo(map);


// map.fitBounds(counties_captive.getBounds());  // zoom to data bounds TODO: wait for geojson to render before calling this


// create legend
var legend = [];

for (var i = 0; i < colorsw.length - 3; i++) {
    legend.push(gradesw1[i] + ' - ' + gradesw2[i] + ' <i style="background:' + colorsw[i] + '"></i>');
}

legend.push(gradesw1[gradesw1.length - 1] + '+ ' + ' <i style="background:' + colorsw[gradesw1.length - 1] + '"></i>');

$("#legendw").html(legend.join('<br>'));


var legend = [];

for (var i = 2; i < colorsc.length - 1; i++) {
    legend.push('<i style="background:' + colorsc[i] + '"></i>' + gradesc[i]);
}

//legend.push('<i style="background:' + colorsw[gradesw1.length - 1] + '"></i>' + gradesw1[gradesw1.length - 1] + ' +');

$("#legendc").html(legend.join('<br>'));


#!/usr/bin/env

"""
 SQL2JSON_mooring_timeline.py
 
 build a JSON driven html file for Mooring timelines

 Using Anaconda packaged Python 
"""

# System Stack
import datetime
import pymysql
import argparse

#User Stack
import utilities.ConfigParserLocal as ConfigParserLocal

__author__   = 'Shaun Bell'
__email__    = 'shaun.bell@noaa.gov'
__created__  = datetime.datetime(2014, 04, 04)
__modified__ = datetime.datetime(2014, 04, 04)
__version__  = "0.1.0"
__status__   = "Development"
__keywords__ = 'CTD', 'MetaInformation', 'Cruise', 'MySQL', 'website', 'PMEL', 'JSON'

"""--------------------------------SQL Init----------------------------------------"""

def connect_to_DB(host, user, password, database, port):
    # Open database connection
    try:
        db = pymysql.connect(host, user, password, database, port)
    except:
        print "db error"
        
    # prepare a cursor object using cursor() method
    cursor = db.cursor(pymysql.cursors.DictCursor)
    return(db,cursor)


def close_DB(db):
    # disconnect from server
    db.close()
    
def read_mooring(db, cursor, table):
    sql = "SELECT * from `%s`" % (table)
    print sql
    
    #print sql
    result_dic = {}
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Get column names
        rowid = {}
        counter = 0
        for i in cursor.description:
            rowid[i[0]] = counter
            counter = counter +1 
        #print rowid
        # Fetch all the rows in a list of lists.
        results = cursor.fetchall()
        for row in results:
            result_dic[row['MooringID']] ={keys: row[keys] for val, keys in enumerate(row.keys())} 
        return (result_dic)
    except:
        print "Error: unable to fecth data"


"""------------------------   html   Modules   ----------------------------------------"""

def json_swimlanes(items, deployment, recovery, lanes_count, mooring_noyear, mooringID):
        
    items = ""
    ### valid deployment and recovery date
    if (not deployment[mooringID]['DeploymentDateTimeGMT'] == None) and (not recovery[mooringID]['RecoveryDateTimeGMT'] == None):
        items = items + ('{{"id":"{0} {5}","lane":{1},"label":"{0}","start": new Date("{2}"), "end": new Date("{3}"), "desc":"test","class":"{4}"}},\n').format(mooring_noyear, lanes_count,deployment[mooringID]['DeploymentDateTimeGMT'].strftime('%Y,%m,%d'),recovery[mooringID]['RecoveryDateTimeGMT'].strftime('%Y,%m,%d'),'Recovered',mooring)
        ### valid deployment, no recovery date - use estimated recovery date if available
        ### no recovery date but valid deployment date
    elif (not deployment[mooringID]['DeploymentDateTimeGMT'] == None) and (recovery[mooringID]['RecoveryDateTimeGMT'] == None):
        if (not deployment[mooringID]['EstimatedRecoveryDate'] == None):
            items = items + ('{{"id":"{0} {5}","lane":{1},"label":"{0}","start": new Date("{3}"), "end": new Date("{2}"), "desc":"test","class":"{4}"}},\n').format(mooring_noyear, lanes_count,deployment[mooringID]['EstimatedRecoveryDate'].strftime('%Y,%m,%d'),deployment[mooringID]['DeploymentDateTimeGMT'].strftime('%Y,%m,%d'),'Deployed',mooring)
        else:
            tempdate = deployment[mooringID]['DeploymentDateTimeGMT']+datetime.timedelta(360)
            items = items + ('{{"id":"{0} {5}","lane":{1},"label":"{0}","start": new Date("{3}"), "end": new Date("{2}"), "desc":"test","class":"{4}"}},\n').format(mooring_noyear, lanes_count,tempdate.strftime('%Y,%m,%d'),deployment[mooringID]['DeploymentDateTimeGMT'].strftime('%Y,%m,%d'),'Deployed',mooring)

    return items
    
    
def json_swimlanes_header():
    outstr = '''<!--
The MIT License (MIT)

Copyright (c) 2013 bill@bunkat.com

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
-->


<html>
<head>
<title>Swimlane using d3.js</title>
  <script src="../scripts/d3/d3.min.js" charset="utf-8"></script>
<style>
.chart {
	shape-rendering: crispEdges;
}

.mini text {
	font: 0px sans-serif;	
}

.main text {
	font: 10px sans-serif;	
}

.month text {
	text-anchor: start;
}

.todayLine {
	stroke: green;
	stroke-width: 1.5;
}

.axis line, .axis path {
	stroke: black;
}

.miniItem {
	stroke-width: 3;	
}

/*blue*/
.UnRecovered {
	fill: #66CCFF;
	stroke: #66CCFF;
}

/*red*/
.Recovered {
	fill: #FF0000;
	stroke: #FF0000;
}

/*green*/
.Deployed {
	fill: #66FF66;
	stroke: #66FF66;
}

/*yellow*/
.PreDeployment {
	fill: #FFFF00;
	stroke: #FFFF00;
}

/*orange*/
.MissingDates {
	fill: #FF9900;
	stroke: #FF9900;
}

/*purple*/
.Calibration {
	fill: #CC00FF;
	stroke: #CC00FF;
}
.brush .extent {
	stroke: gray;
	fill: blue;
	fill-opacity: .165;
}
</style>
</head>
<body>

<script type="text/javascript">

var data = 
'''

    return outstr
def json_swimlanes_footer():

        
    outstr = """
//var data = randomData()
  , lanes = data.lanes
  , items = data.items
  , now = new Date();

var height;
var margin = {top: 20, right: 15, bottom: 15, left: 120};
//  , width = 1400 - margin.left - margin.right
//  , height = lanes.length * 36 * 1 - margin.top - margin.bottom
if(document.body.clientHeight >= 960) { height = document.body.clientHeight * 1.0 - margin.top - margin.bottom-20; }
else { 
var margin = {top: 20, right: 15, bottom: 15, left: 60}
  , width = 960 - margin.left - margin.right
  , height = 2400 - margin.top - margin.bottom
  , miniHeight = lanes.length * 2 + 5
  , mainHeight = height - miniHeight  - 5; }
var width = document.body.clientWidth - margin.right - margin.left-20
  , miniHeight = lanes.length * 3 + 50
  , mainHeight = height - miniHeight - 50;

var x = d3.time.scale()
	.domain([d3.time.sunday(d3.min(items, function(d) { return d.start; })),
			 d3.max(items, function(d) { return d.end; })])
	.range([0, width]);
var x1 = d3.time.scale().range([0, width]);

var ext = d3.extent(lanes, function(d) { return d.id; });
var y1 = d3.scale.linear().domain([ext[0], ext[1] + 1]).range([0, mainHeight]);
var y2 = d3.scale.linear().domain([ext[0], ext[1] + 1]).range([0, miniHeight]);

var chart = d3.select('body')
	.append('svg:svg')
	.attr('width', width + margin.right + margin.left)
	.attr('height', height + margin.top + margin.bottom)
	.attr('class', 'chart');

chart.append('defs').append('clipPath')
	.attr('id', 'clip')
	.append('rect')
		.attr('width', width)
		.attr('height', mainHeight);

var main = chart.append('g')
	.attr('transform', 'translate(' + margin.left + ',' + margin.top + ')')
	.attr('width', width)
	.attr('height', mainHeight)
	.attr('class', 'main');

var mini = chart.append('g')
	.attr('transform', 'translate(' + margin.left + ',' + (mainHeight + 60) + ')')
	.attr('width', width)
	.attr('height', miniHeight)
	.attr('class', 'mini');

// draw the lanes for the main chart
main.append('g').selectAll('.laneLines')
	.data(lanes)
	.enter().append('line')
	.attr('x1', 0)
	.attr('y1', function(d) { return d3.round(y1(d.id)) + 0.5; })
	.attr('x2', width)
	.attr('y2', function(d) { return d3.round(y1(d.id)) + 0.5; })
	.attr('stroke', function(d) { return d.label === '' ? 'white' : 'lightgray' });

main.append('g').selectAll('.laneText')
	.data(lanes)
	.enter().append('text')
	.text(function(d) { return d.label; })
	.attr('x', -10)
	.attr('y', function(d) { return y1(d.id + .5); })
	.attr('dy', '0.5ex')
	.attr('text-anchor', 'end')
	.attr('class', 'laneText');

// draw the lanes for the mini chart
mini.append('g').selectAll('.laneLines')
	.data(lanes)
	.enter().append('line')
	.attr('x1', 0)
	.attr('y1', function(d) { return d3.round(y2(d.id)) + 0.5; })
	.attr('x2', width)
	.attr('y2', function(d) { return d3.round(y2(d.id)) + 0.5; })
	.attr('stroke', function(d) { return d.label === '' ? 'white' : 'lightgray' });

mini.append('g').selectAll('.laneText')
	.data(lanes)
	.enter().append('text')
	.text(function(d) { return d.label; })
	.attr('x', -10)
	.attr('y', function(d) { return y2(d.id + .5); })
	.attr('dy', '0.5ex')
	.attr('text-anchor', 'end')
	.attr('class', 'laneText');

// draw the x axis
var xDateAxis = d3.svg.axis()
	.scale(x)
	.orient('bottom')
	.ticks(d3.time.year, 1)
	.tickFormat(d3.time.format('%Y'))
	.tickSize(6, 0, 0);

var x1DateAxis = d3.svg.axis()
	.scale(x1)
	.orient('bottom')
	.ticks(d3.time.month, 1)
	.tickFormat(d3.time.format('%b %Y'))
	.tickSize(6, 0, 0);

var xMonthAxis = d3.svg.axis()
	.scale(x)
	.orient('top')
	.ticks(d3.time.year, 1)
	.tickFormat(d3.time.format('%Y'))
	.tickSize(15, 0, 0);

var x1MonthAxis = d3.svg.axis()
	.scale(x1)
	.orient('top')
	.ticks(d3.time.month, 1)
	.tickFormat(d3.time.format('%b'))
	.tickSize(15, 0, 0);

main.append('g')
	.attr('transform', 'translate(0,' + mainHeight + ')')
	.attr('class', 'main axis date')
	.call(x1DateAxis);

main.append('g')
	.attr('transform', 'translate(0,0.5)')
	.attr('class', 'main axis month')
	.call(x1MonthAxis)
	.selectAll('text')
		.attr('dx', 5)
		.attr('dy', 12);

mini.append('g')
	.attr('transform', 'translate(0,' + miniHeight + ')')
	.attr('class', 'axis date')
	.call(xDateAxis)
	.selectAll('text')
		.attr('dx', 18)
		.attr('dy', 5);

mini.append('g')
	.attr('transform', 'translate(0,0.5)')
	.attr('class', 'axis month')
	.call(xMonthAxis)
	.selectAll('text')
		.attr('dx', 18)
		.attr('dy', 12);

// draw a line representing today's date
main.append('line')
	.attr('y1', 0)
	.attr('y2', mainHeight)
	.attr('class', 'main todayLine')
	.attr('clip-path', 'url(#clip)');
	
mini.append('line')
	.attr('x1', x(now) + 0.5)
	.attr('y1', 0)
	.attr('x2', x(now) + 0.5)
	.attr('y2', miniHeight)
	.attr('class', 'todayLine');

// draw the items
var itemRects = main.append('g')
	.attr('clip-path', 'url(#clip)');

mini.append('g').selectAll('miniItems')
	.data(getPaths(items))
	.enter().append('path')
	.attr('class', function(d) { return 'miniItem ' + d.class; })
	.attr('d', function(d) { return d.path; });

// invisible hit area to move around the selection window
mini.append('rect')
	.attr('pointer-events', 'painted')
	.attr('width', width)
	.attr('height', miniHeight)
	.attr('visibility', 'hidden')
	.on('mouseup', moveBrush);

// draw the selection area
var brush = d3.svg.brush()
	.x(x)
	.extent([d3.time.monday(now),d3.time.saturday.ceil(now)])
	.on("brush", display);

mini.append('g')
	.attr('class', 'x brush')
	.call(brush)
	.selectAll('rect')
		.attr('y', 1)
		.attr('height', miniHeight - 1);

mini.selectAll('rect.background').remove();
display();

function display () {

	var rects, labels
	  , minExtent = d3.time.day(brush.extent()[0])
	  , maxExtent = d3.time.day(brush.extent()[1])
	  , visItems = items.filter(function (d) { return d.start < maxExtent && d.end > minExtent});

	mini.select('.brush').call(brush.extent([minExtent, maxExtent]));		

	x1.domain([minExtent, maxExtent]);

	if ((maxExtent - minExtent) > 1000*60*60*24*550) {
		x1DateAxis.ticks(d3.time.year, 1).tickFormat(d3.time.format('%b %Y'))
		x1MonthAxis.ticks(d3.time.year, 1).tickFormat(d3.time.format('%b %Y'))		
	}
	else if ((maxExtent - minExtent) > 1000*60*60*24*14) {
		x1DateAxis.ticks(d3.time.month, 2).tickFormat(d3.time.format('%b %Y'))
		x1MonthAxis.ticks(d3.time.month, 2).tickFormat(d3.time.format('%b %Y'))
	}
	else {
		x1DateAxis.ticks(d3.time.day, 1).tickFormat(d3.time.format('%d %b %Y'))
		x1MonthAxis.ticks(d3.time.day, 1).tickFormat(d3.time.format('%d %b %Y'))
	}


	//x1Offset.range([0, x1(d3.time.day.ceil(now) - x1(d3.time.day.floor(now)))]);

	// shift the today line
	main.select('.main.todayLine')
		.attr('x1', x1(now) + 0.5)
		.attr('x2', x1(now) + 0.5);

	// update the axis
	main.select('.main.axis.date').call(x1DateAxis);
	main.select('.main.axis.month').call(x1MonthAxis)
		.selectAll('text')
			.attr('dx', 5)
			.attr('dy', 12);

	// upate the item rects
	rects = itemRects.selectAll('rect')
		.data(visItems, function (d) { return d.id; })
		.attr('x', function(d) { return x1(d.start); })
		.attr('width', function(d) { return x1(d.end) - x1(d.start); });

	rects.enter().append('rect')
		.attr('x', function(d) { return x1(d.start); })
		.attr('y', function(d) { return y1(d.lane) + .1 * y1(1) + 0.5; })
		.attr('width', function(d) { return x1(d.end) - x1(d.start); })
		.attr('height', function(d) { return .8 * y1(1); })
		.attr('class', function(d) { return 'mainItem ' + d.class; });

	rects.exit().remove();

	// update the item labels
	labels = itemRects.selectAll('text')
		.data(visItems, function (d) { return d.id; })
		.attr('x', function(d) { return x1(Math.max(d.start, minExtent)) + 2; });
				
	labels.enter().append('text')
		.text(function (d) { return d.label; })
		.attr('x', function(d) { return x1(Math.max(d.start, minExtent)) + 2; })
		.attr('y', function(d) { return y1(d.lane) + .4 * y1(1) + 5.5; })
		.attr('text-anchor', 'start')
		.attr('class', 'itemLabel');

	labels.exit().remove();
}

function moveBrush () {
	var origin = d3.mouse(this)
	  , point = x.invert(origin[0])
	  , halfExtent = (brush.extent()[1].getTime() - brush.extent()[0].getTime()) / 2
	  , start = new Date(point.getTime() - halfExtent)
	  , end = new Date(point.getTime() + halfExtent);

	brush.extent([start,end]);
	display();
}

// generates a single path for each item class in the mini display
// ugly - but draws mini 2x faster than append lines or line generator
// is there a better way to do a bunch of lines as a single path with d3?
function getPaths(items) {
	var paths = {}, d, offset = .5 * y2(1) + 0.5, result = [];
	for (var i = 0; i < items.length; i++) {
		d = items[i];
		if (!paths[d.class]) paths[d.class] = '';	
		paths[d.class] += ['M',x(d.start),(y2(d.lane) + offset),'H',x(d.end)].join(' ');
	}

	for (var className in paths) {
		result.push({class: className, path: paths[className]});
	}

	return result;
}

</script>
</body>
</html>
"""
    return outstr
"""----------------------------------Main----------------------------------------------"""

parser = argparse.ArgumentParser(description='DB -> JSON -- Instrument Timelines')
parser.add_argument('OutputPath', metavar='OutputPath', type=str, help='path to output files (eg. /full/path/to/data/')
args = parser.parse_args()

#get information from local config file - a json formatted file
db_config = ConfigParserLocal.get_config('../db_connection_config_files/db_config_mooring.pyini')

tablelist=['mooringdeploymentlogs','mooringrecoverylogs']



lanes = "lanes:["
lanes_count = 0
items = "items:["
cal_items = ""


outfilename = args.OutputPath + 'all_mooring_swimlane.html'
    
(db,cursor) = connect_to_DB(db_config['host'], db_config['user'], db_config['password'], db_config['database'], db_config['port'])
Mooring_Meta_dep = read_mooring(db, cursor, tablelist[0])
Mooring_Meta_rec = read_mooring(db, cursor, tablelist[1])
close_DB(db)
 
mooring_stas = sorted(list(set([x[2:-1] for x in sorted(Mooring_Meta_dep.keys())])))
for mooring_sta in mooring_stas:
    has_record = False
    for mooring in sorted(Mooring_Meta_dep.keys()):
        print mooring_sta
        
        if mooring_sta == Mooring_Meta_dep[mooring]['MooringID'][2:-1] and has_record == False:
            lanes = lanes + ('{{"id":{0},"label":"{1}"}},\n').format(lanes_count, Mooring_Meta_dep[mooring]['MooringID'][2:-1])
            items = items + json_swimlanes(items, Mooring_Meta_dep, Mooring_Meta_rec, lanes_count, Mooring_Meta_dep[mooring]['MooringID'][2:-1],Mooring_Meta_dep[mooring]['MooringID'])
            has_record = True
        elif mooring_sta == Mooring_Meta_dep[mooring]['MooringID'][2:-1] and has_record == True:
            items = items + json_swimlanes(items, Mooring_Meta_dep, Mooring_Meta_rec, lanes_count, Mooring_Meta_dep[mooring]['MooringID'][2:-1],Mooring_Meta_dep[mooring]['MooringID'])
            
    lanes_count +=1 


with open(outfilename, 'w') as outfile:
    outfile.write(json_swimlanes_header())
    outfile.write('{')
    outfile.write(lanes)
    outfile.write('],')
    outfile.write(items)
    outfile.write(cal_items)
    outfile.write('],}')
    outfile.write(json_swimlanes_footer())

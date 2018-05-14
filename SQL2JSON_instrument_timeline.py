#!/usr/bin/env

"""
 SQL2JSON_instrument_timeline.py
 
 build a JSON driven html file for instrument deployment start/end dates and cal dates

 Using Anaconda packaged Python 
"""

# System Stack
import datetime
import pymysql
import argparse

#User Stack
import io_utils.ConfigParserLocal as ConfigParserLocal

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
    
def read_inst(db, cursor, table, ActiveOnly=False):
    sql = "SELECT * from `%s`" % (table)
    
    if ActiveOnly:
        sql = sql + " WHERE IsActive !='n'"
    
    sql = sql + " ORDER BY `InstID` asc"
    
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
            result_dic[row['InstID']] ={keys: row[keys] for val, keys in enumerate(row.keys())} 
        return (result_dic)
    except:
        print "Error: unable to fecth data"

def read_cal(db, cursor, table, InstID):
    sql = ("SELECT * from `{0}` WHERE InstID='{1}' AND `CalDate` > '1990'").format(table, InstID)
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
            result_dic[row['id']] ={keys: row[keys] for val, keys in enumerate(row.keys())} 
        return (result_dic)
    except:
        print "Error: unable to fecth data"

def read_times(db, cursor, table, instrument):
    """
    SELECT * FROM (
    SELECT `EcoFOCI`.`mooringrecoverylogs`.`RecoveryDateTimeGMT`, `EcoFOCI`.`mooringdeploymentlogs`.`DeploymentDateTimeGMT`,`EcoFOCI`.`mooringdeployedinstruments`.`MooringID`, `EcoFOCI`.`mooringdeployedinstruments`.`InstID` as mID, `EcoFOCI_instruments`.`inst_sbe37`.`InstID`  FROM `EcoFOCI`.`mooringdeployedinstruments`
            right Join `EcoFOCI_instruments`.`inst_sbe37`
            on `EcoFOCI_instruments`.`inst_sbe37`.`InstID` = `EcoFOCI`.`mooringdeployedinstruments`.`InstID`
            left join `EcoFOCI`.`mooringdeploymentlogs`
            on `EcoFOCI`.`mooringdeploymentlogs`.`MooringID` = `EcoFOCI`.`mooringdeployedinstruments`.`MooringID`
            left join `EcoFOCI`.`mooringrecoverylogs`
            on `EcoFOCI`.`mooringrecoverylogs`.`MooringID` = `EcoFOCI`.`mooringdeployedinstruments`.`MooringID`
            ORDER BY `EcoFOCI_instruments`.`inst_sbe37`.`InstID`,`EcoFOCI`.`mooringdeployedinstruments`.`MooringID` DESC) as inst
            WHERE InstID = 'SBE-37 1678'
        """
    sql = ("SELECT * FROM ("
           " SELECT `EcoFOCI`.`mooringrecoverylogs`.`RecoveryDateTimeGMT`, "
           " `EcoFOCI`.`mooringdeploymentlogs`.`DeploymentDateTimeGMT`, "
           " `EcoFOCI`.`mooringdeploymentlogs`.`EstimatedRecoveryDate`, "
           " `EcoFOCI`.`mooringdeployedinstruments`.`MooringID`, `EcoFOCI`.`mooringdeployedinstruments`.`InstID` as mID,"
           " `EcoFOCI_instruments`.`{0}`.`InstID`  FROM `EcoFOCI`.`mooringdeployedinstruments`"
           " right Join `EcoFOCI_instruments`.`{0}`"
           " on `EcoFOCI_instruments`.`{0}`.`InstID` = `EcoFOCI`.`mooringdeployedinstruments`.`InstID`"
           " left join `EcoFOCI`.`mooringdeploymentlogs`"
           " on `EcoFOCI`.`mooringdeploymentlogs`.`MooringID` = `EcoFOCI`.`mooringdeployedinstruments`.`MooringID`"
           " right join `EcoFOCI`.`mooringrecoverylogs`"
           " on `EcoFOCI`.`mooringrecoverylogs`.`MooringID` = `EcoFOCI`.`mooringdeployedinstruments`.`MooringID`"
           " ORDER BY `EcoFOCI_instruments`.`{0}`.`InstID`,`EcoFOCI`.`mooringdeployedinstruments`.`MooringID` DESC) as inst"
           " WHERE InstID = '{1}'"
            ).format(table, instrument)
       
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

def json_swimlanes(items, data, mkey, activestatus, lanes_count, instrument):
    if activestatus == 'yes':
        statuslabel = 'Active'
    else:
        statuslabel = 'InActive'
        
    items = ""
    ### valid deployment and recovery date
    if not (data[mkey]['DeploymentDateTimeGMT'] == None) and not (data[mkey]['RecoveryDateTimeGMT'] == None):
        items = items + ('{{"id":"{0} {5}","lane":{1},"label":"{0}","start": new Date("{2}"), "end": new Date("{3}"), "desc":"test","class":"{4}"}},\n').format(mkey, lanes_count,data[mkey]['DeploymentDateTimeGMT'].strftime('%Y,%m,%d'),data[mkey]['RecoveryDateTimeGMT'].strftime('%Y,%m,%d'),statuslabel,instrument)
    ### valid deployment, no recovery date - use estimated recovery date if available
    elif not (data[mkey]['DeploymentDateTimeGMT'] == None) and (data[mkey]['RecoveryDateTimeGMT'] == None): #EstimatedRecoveryDate
        if (data[mkey]['EstimatedRecoveryDate'] == None): #use estimated date
            tempdate = data[mkey]['DeploymentDateTimeGMT']+datetime.timedelta(90)
            items = items + ('{{"id":"{0} {5}","lane":{1},"label":"{0}","start": new Date("{2}"), "end": new Date("{3}"), "desc":"test","class":"{4}"}},\n').format(mkey, lanes_count,data[mkey]['DeploymentDateTimeGMT'].strftime('%Y,%m,%d'),tempdate.strftime('%Y,%m,%d'),statuslabel,instrument)
        elif (data[mkey]['EstimatedRecoveryDate'] == '0000-00-00 00:00:00'): #NOT DEPLOYED
            print "zero date, not null but should be"
        else:
            items = items + ('{{"id":"{0} {5}","lane":{1},"label":"{0}","start": new Date("{2}"), "end": new Date("{3}"), "desc":"test","class":"{4}"}},\n').format(mkey, lanes_count,data[mkey]['DeploymentDateTimeGMT'].strftime('%Y,%m,%d'),data[mkey]['EstimatedRecoveryDate'].strftime('%Y,%m,%d'),'OnDeployment',instrument)
    ### no deployment date, no recovery date - start and end date are arbitrarily listed as today but will not show up on figure
    # if within last year these are in predeployment stage
    elif (data[mkey]['DeploymentDateTimeGMT'] == None) and (data[mkey]['RecoveryDateTimeGMT'] == None):
        if not (data[mkey]['EstimatedRecoveryDate'] == None): #use estimated date
            items = items + ('{{"id":"{0} {5}","lane":{1},"label":"{0}","start": new Date("{2}"), "end": new Date("{3}"), "desc":"test","class":"{4}"}},\n').format(mkey, lanes_count,datetime.datetime.now().strftime('%Y,%m,%d'),data[mkey]['EstimatedRecoveryDate'].strftime('%Y,%m,%d'),'PreDeployment',instrument)
        else: #NOT DEPLOYED
            items = items + ('{{"id":"{0} {5}","lane":{1},"label":"{0}","start": new Date("{2}"), "end": new Date("{3}"), "desc":"test","class":"{4}"}},\n').format(mkey, lanes_count,'20'+mkey[0:2]+',01,'+'01','20'+mkey[0:2]+',06,'+'01','MissingDates',instrument)
    ### no deployment date but valid recovery date
    elif (data[mkey]['DeploymentDateTimeGMT'] == None) and not (data[mkey]['RecoveryDateTimeGMT'] == None):
        tempdate = data[mkey]['RecoveryDateTimeGMT']-datetime.timedelta(30)
        items = items + ('{{"id":"{0} {5}","lane":{1},"label":"{0}","start": new Date("{2}"), "end": new Date("{3}"), "desc":"test","class":"{4}"}},\n').format(mkey, lanes_count,tempdate.strftime('%Y,%m,%d'),data[mkey]['RecoveryDateTimeGMT'].strftime('%Y,%m,%d'),'MissingDates',instrument)

    return items
    
def json_swimlanes_cal(items, data, mkey, activestatus, lanes_count,instrument):
    items = ""
    if not (data[mkey]['CalDate'] == None):
        tempdate = data[mkey]['CalDate']+datetime.timedelta(30)
        items = ('{{"id":"{2} Cal {5}","lane":{1},"label":"{0}","start": new Date("{2}"), "end": new Date("{3}"), "desc":"test","class":"{4}"}},\n').format(mkey, lanes_count,data[mkey]['CalDate'].strftime('%Y,%m,%d'),tempdate.strftime('%Y,%m,%d'),'Calibration',instrument)

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
.Active {
	fill: #66CCFF;
	stroke: #66CCFF;
}

/*red*/
.InActive {
	fill: #FF0000;
	stroke: #FF0000;
}

/*green*/
.OnDeployment {
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
	.extent([d3.time.month(now),d3.time.month.ceil(now)])
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
parser.add_argument('-a', '--IsActive', action="store_true", help='flag for active instruments only')
args = parser.parse_args()

#get information from local config file - a json formatted file
db_config = ConfigParserLocal.get_config('../db_connection_config_files/db_config.pyini')

#array of tables in mysql database to cycle through

tablelist=['inst_rcm','inst_adcp','inst_ecofluor','inst_spn1','inst_eppley','inst_iceprof','inst_mtr','inst_par', \
        'inst_sbe3','inst_sbe4','inst_sbe5','inst_sbe9','inst_sbe16','inst_sbe26','inst_sbe37', \
        'inst_sbe38','inst_sbe39','inst_sbe43','inst_sbe49','inst_sbe56','inst_wetstarfluor','inst_windsensors', \
        'inst_wxsensors','inst_nitrates']
cal_tablelist=['cal_rcm','cal_adcp', 'cal_ecofluor','cal_spn1','cal_eppley','cal_iceprof','cal_mtr','cal_par', \
        'cal_sbe3','cal_sbe4','cal_sbe5','cal_sbe9','cal_sbe16','cal_sbe26','cal_sbe37', \
        'cal_sbe38','cal_sbe39','cal_sbe43','cal_sbe49','cal_sbe56','cal_wetstarfluor','cal_windsensors', \
        'cal_wxsensors','cal_nitrates']

if args.IsActive:
    ActiveOnly = True
else:
    ActiveOnly = False


for index_table, table in enumerate(tablelist):

    lanes = "lanes:["
    lanes_count = 0
    items = "items:["
    cal_items = ""

    if ActiveOnly:
        outfilename = args.OutputPath + table+'swimlane_active.html'
    else:
        outfilename = args.OutputPath + table+'swimlane.html'
        
    db_config['database'] = 'EcoFOCI_instruments'
    ### get individual inst serial numbers
    (db,cursor) = connect_to_DB(db_config['host'], db_config['user'], db_config['password'], db_config['database'], db_config['port'])
    Instruments = read_inst(db, cursor, table, ActiveOnly=ActiveOnly)
    close_DB(db)

    db_config['database'] = 'EcoFOCI'
    ### for each instrument join the deployment/recovery information
    (db,cursor) = connect_to_DB(db_config['host'], db_config['user'], db_config['password'], db_config['database'], db_config['port'])

    db_config['database'] = 'EcoFOCI_instruments'
    (db_cal,cursor_cal) = connect_to_DB(db_config['host'], db_config['user'], db_config['password'], db_config['database'], db_config['port'])
        
    for instrument in sorted(Instruments.keys()):
        print instrument
        InstDep = read_times(db, cursor, table, instrument)
        CalRec = read_cal(db_cal, cursor_cal, cal_tablelist[index_table], instrument)
        
        if Instruments[instrument]['IsActive'] == 'n':
            activestatus = 'no'
        else:
            activestatus = 'yes'    

        lanes = lanes + ('{{"id":{0},"label":"{1}"}},\n').format(lanes_count, instrument)
        if InstDep: #not empty
            for mkey in InstDep.keys():
                items = items + json_swimlanes(items, InstDep, mkey, activestatus, lanes_count,instrument)

        else:
            print('{0} has no deployment information').format(instrument)
            items = items + ('{{"id":"{0} {2}","lane":{1},"label":"{0}","start": new Date(), "end": new Date(), "desc":"test","class":"InActive"}},\n').format('None',lanes_count,instrument)

        if CalRec: #not empty
            for dkey in CalRec.keys():
                temp = json_swimlanes_cal(cal_items, CalRec, dkey, activestatus, lanes_count, instrument)
                cal_items = cal_items + temp
        else:
            print('{0} has no cal information').format(instrument)

        lanes_count +=1 

    close_DB(db)
    close_DB(db_cal)
    
    with open(outfilename, 'w') as outfile:
        outfile.write(json_swimlanes_header())
        outfile.write('{')
        outfile.write(lanes)
        outfile.write('],')
        outfile.write(items)
        outfile.write(cal_items)
        outfile.write('],}')
        outfile.write(json_swimlanes_footer())

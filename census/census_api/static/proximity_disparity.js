var config = {
	zoom: .95,
	timeline: {
		timer: null,
		width: 1100,
		barWidth: 6,
		// TODO: Update this and remove this "magic" constant for the width '1100'
		xScale: d3.scale.linear().domain([1880,2014]).range([20, 950])
	}
}

$(function() {
	queue()
		.defer(d3.json, geojson1)
		.defer(d3.csv, csv1)
		.defer(d3.csv,overlap)
		.defer(d3.json,neighbors)
		.defer(d3.json,neighborhoods)
		.await(dataDidLoad);
})

$("#topDifferences .hideTop").hide()

function dataDidLoad(error, geojson1, city1, overlap, neighbors,neighborhoodDictionary) {
	d3.select("#title").html(toTitleCase(city.replace("_"," ")))
	var subtitle = d3.select("#subtitle").html()
	subtitle = subtitle.replace("current city", toTitleCase(city))
	subtitle = subtitle.replace("25%",global.minDifference +"%")
	d3.select("#subtitle").html(subtitle)
	global.neighbors = neighbors
	global.center = global.center
	global.minDifference = global.minDifference
	global.scale = scale
//	window.location.hash = JSON.stringify([global.translate, global.translateScale])
//	window.location.hash = JSON.stringify([global.city, global.translate, global.translateScale])
	
	initNycMap(geojson1, city1, "Median", "#svg-1",0,global.maxIncome*100000,neighbors,overlap,neighborhoodDictionary)
	$("#topDifferences .showTop").click(hideTop)
	$("#topDifferences .hideTop").click(showTop)
	d3.selectAll("#svg-1 svg g .topDifferences").attr("opacity",0)
	drawScale()
}
function drawWater(water,svg,fill,stroke,waterClass){
	var projection = d3.geo.mercator().scale(global.scale).center(global.center)
	var path = d3.geo.path().projection(projection);
	var waterShape = d3.select("#svg-1 svg g")
	waterShape.selectAll(".water")
		.data(water.features)
        .enter()
        .append("path")
		.attr("class","water")
		.attr("d",path)
		.style("fill","#9BBBBB")
	    .style("opacity",.2)
}
function toTitleCase(str){
    return str.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
}
function hideTop(){
	//console.log("show graph")
	$("#topDifferences .showTop").hide()
	$("#topDifferences .hideTop").show()
	d3.selectAll("#svg-1 svg g .topDifferences").attr("opacity",1)
	
}
function showTop(){
//	console.log("hide graph")
	$("#topDifferences .hideTop").hide()
	$("#topDifferences .showTop").show()
	d3.selectAll("#svg-1 svg g .topDifferences").attr("opacity",0)
}
function getSizeOfObject(obj){
    var size = 0, key;
     for (key in obj) {
         if (obj.hasOwnProperty(key)) size++;
     }
     return size;
}
function sumEachColumnChartData(data,column){
	//console.log(data)
	//console.log(data)
	var groupLength = getSizeOfObject(data)
	var sum = 0
	for(var i =0; i<groupLength; i++){
		//var columns = getSizeOfObject(data[i])
		var columnValue = parseInt(data[i][column])
		sum += columnValue
	}
	return sum
}
var utils = {
	range: function(start, end) {
		var data = []

		for (var i = start; i < end; i++) {
			data.push(i)
		}

		return data
	}
}
var table = {
	group: function(rows, fields) {
		var view = {}
		var pointer = null

		for(var i in rows) {
			var row = rows[i]

			pointer = view
			for(var j = 0; j < fields.length; j++) {
				var field = fields[j]

				if(!pointer[row[field]]) {
					if(j == fields.length - 1) {
						pointer[row[field]] = []
					} else {
						pointer[row[field]] = {}
					}
				}

				pointer = pointer[row[field]]
			}

			pointer.push(row)
		}

		return view
	},

	maxCount: function(view) {
		var largestName = null
		var largestCount = null

		for(var i in view) {
			var list = view[i]

			if(!largestName) {
				largestName = i
				largestCount = list.length
			} else {
				if(list.length > largestCount) {
					largestName = i
					largestCount = list.length
				}
			}
		}

		return {
			name: largestName,
			count: largestCount
		}
	},

	filter: function(view, callback) {
		var data = []

		for(var i in view) {
			var list = view[i]
			if(callback(list, i)) {
				data = data.concat(list)
			}
		}

		return data
	}
}
function sortObjectByValue(toSort){
	var sorted = toSort.sort(function(a,b){return a["Median"]-b["Median"]})
	return sorted
}
function zoomed() {
	//console.log("calling zoomed" + d3.event.scale + ", translate: "+ d3.event.translate )
	map.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
  	map.select(".map-item").style("stroke-width", 1.5 / d3.event.scale + "px");
	var newScaleDistance = Math.round((5/d3.event.scale)* 100) / 100
	d3.select("#scale .scale-text").text(newScaleDistance+"km")
	window.location.hash = JSON.stringify([d3.event.translate, d3.event.scale])
}
function initNycMap(paths, data, column, svg,low,high,neighbors,overlap,neighborhoodDictionary) {
	renderMap(paths,svg, global.usMapWidth,global.usMapHeight)
	renderNycMap(data,column,svg,low,high,neighbors,neighborhoodDictionary)
	var differenceData = formatDifferenceData(data,overlap)
	drawTopDifferences(differenceData)
	drawDifferences(data,svg,overlap)
	if(water != null && water != undefined){
		d3.json(water, function(waterdata) {
			drawWater(waterdata, "#svg-1","#000","blue","water")
		});
	}	
	var parsedTranslate = JSON.parse(window.location.hash.substring(1))[0]
	var parsedScale = JSON.parse(window.location.hash.substring(1))[1]
	global.translate = parsedTranslate
	global.translateScale = parsedScale
	map.attr("transform", "translate(" + global.translate + ")scale(" + global.translateScale + ")");
	//console.log(neighborhoodDictionary.blockgroup_nhoods)
}
function getDistanceFromLatLonInKm(lat1,lon1,lat2,lon2) {
  var R = 6371; // Radius of the earth in km
  var dLat = deg2rad(lat2-lat1);  // deg2rad below
  var dLon = deg2rad(lon2-lon1); 
  var a = 
    Math.sin(dLat/2) * Math.sin(dLat/2) +
    Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) * 
    Math.sin(dLon/2) * Math.sin(dLon/2)
    ; 
  var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a)); 
  var d = R * c; // Distance in km
  return d;
}
function deg2rad(deg) {
  return deg * (Math.PI/180)
}
function renderBoroughs(data,svg,width,height){
	var boroughs = d3.select("#svg-1 svg")
	var projection = d3.geo.mercator().scale(global.scale).center(global.center)
	var path = d3.geo.path().projection(projection);
	//console.log(data)
	boroughs.selectAll(".boroughs")
		.data(data.features)
		.enter()
		.append("path")
		.attr("d", path)
		.attr("class", "boroughs")
		.attr("cursor", "pointer")
		.attr("stroke","#eee")
		.attr("fill","#eee")
		.attr("stroke-width",.5)
}

function drawDifferences(data,svg,overlapData){
	var differenceData = formatDifferenceData(data,overlapData)
	var projection = d3.geo.mercator().scale(global.scale).center(global.center)
	
	var differenceMap = d3.select("#svg-1 svg g")
	var dataById = table.group(data, ["Id"])
	var minDifference = global.minDifference
	var maxDifference = 100
	var colorScale = d3.scale.linear().domain([minDifference,maxDifference]).range(["#aaa","red"])
	//console.log(dataById["360010131001"][0]["Median"])
	var strokeScale = d3.scale.linear().domain([minDifference,maxDifference]).range([0,2])
	var differenceOpacityScale = d3.scale.linear().domain([minDifference,maxDifference]).range([0,1])

	var line = d3.svg.line()
	var path = d3.geo.path().projection(projection);
	
	var zoom = d3.behavior.zoom()
		.translate([0, 0])
		.scale(1)
		.scaleExtent([1, 8])
		.on("zoom", zoomed);	
	var tip = d3.tip()
		.attr('class', 'd3-tip-nyc-difference')
		.offset([-10, 0])
	
	differenceMap.call(tip);
		
	differenceMap.selectAll(".map")
		.data(differenceData)
		.enter()
		.append("line")
		.attr("class","map")
		.attr("class", function(d){
			return d.id1
		})
		.attr("class", function(d){
			return d.id2
		})
		.attr("x1", function(d){
			//console.log(d)
			//return 5
			var lng1 = d["lng1"]
			var lat1 = d["lat1"]
			var x1 = (projection([lng1,lat1])[0])
			return x1
		})
		.attr("y1", function(d){
			//return 5
			var lng1 = d["lng1"]
			var lat1 = d["lat1"]
			var y1 = (projection([lng1,lat1])[1])
			//console.log(y)
			return y1
		})
		.attr("x2", function(d){
			var lng = d["lng2"]
			var lat = d["lat2"]
			var x2 = (projection([lng,lat])[0])
			return x2
		})
		.attr("y2", function(d){
			var lng = d["lng2"]
			var lat = d["lat2"]
			var y2 = (projection([lng,lat])[1])
			//console.log(y)
			return y2
		})
		.attr("opacity",1)
		.attr("stroke-width",function(d){
			var difference = d["difference"]
			if(isNaN(difference)){
				return 0
			}
			return strokeScale(difference)
		})
		.attr("stroke",function(d){
			var difference = d["difference"]
			if(isNaN(difference)){
				return "black"
			}
			return colorScale(difference)
		})
		.attr("fill","none")
		.attr("stroke-linecap","round")
		.call(zoom)
		.on("mouseover",function(d){
			var difference = d["difference"]
			var income1 = d["income1"]
			var income2 = d["income2"]
			var percentile1 = d["percentile1"]
			var percentile2 = d["percentile2"]
			tipText = "Percentile Difference: "+Math.round(difference)+"%"
			//tipText = "Percentile Difference: "+Math.round(difference)+"% <br/>Sanity checkes = incomes: $"+ income1 +" is percentile"+percentile1+"<br/>"+ " $"+income2+" is percentile"+percentile2
			//console.log(tipText)
			tip.html(function(d){return tipText})
			tip.show()
		})
		.on("mouseout",function(d){
			tip.hide()
		})
}
function isInArray(value, array) {
  return array.indexOf(value) > -1;
}
function calculateScaleSize(){
	var projection = d3.geo.mercator().scale(global.scale).center(global.center)
	var lat1 = global.center[1]
	var lng1 = global.center[0]
	var lat2 = lat1+0.1
	var lng2 = global.center[0]+0.1
	var distance = getDistanceFromLatLonInKm(lat1,lng1,lat2,lng2)
	//console.log(distance+"km")
	var x1 = projection([lng1,lat1])[0]
	var y1 = projection([lng1,lat1])[1]
	var x2 = projection([lng2,lat2])[0]
	var y2 = projection([lng2,lat2])[1]
	var screenDistance = Math.sqrt(Math.pow(Math.abs(x2-x1),2)+Math.pow(Math.abs(y2-y1),2))
//	console.log([x1,x2,y1,y2,screenDistance])
	
	var screenDistance1km = screenDistance/distance
	var screenDistance100km = screenDistance1km*100
	//console.log(screenDistance1km)
	return screenDistance1km
}
function drawScale(){
	var kmInPixels = calculateScaleSize()
//	console.log(kmInPixels)
	var scale = d3.select("#scale")
			.append("svg")
			.attr("width",kmInPixels*6)
			.attr("height",50)
		scale.append("rect")
			.attr("class","scale")
			.attr("x",20)
			.attr("y",20)
			.attr("width",kmInPixels*5)
			.attr("height",1)
			.attr("fill","#000")
		
		scale.append("text")
			.attr("class","scale-text")
			.text("5 km")
			.attr("x",40)
			.attr("y",35)
			.attr("font-size",12)
}
function drawTopDifferences(data){
	var topDifferencesData = data.slice(0,80)
	var centroids = []
	var differences = []
	var topDifferences = d3.select("#svg-1 svg g")
	var projection = d3.geo.mercator().scale(global.scale).center(global.center)
	var line = d3.svg.line()
	topDifferences.selectAll(".topDifferences")
	.data(topDifferencesData)
	.enter()
	.append("line")
	.attr("class","topDifferences")
	.attr("x1", function(d){
		//return 5
		var lng1 = parseFloat(d["lng1"])
		var lat1 = parseFloat(d["lat1"])
	//	console.log(lng1)

		var x1 = (projection([lng1,lat1])[0])
	//	console.log(x1)
		return x1
	})
	.attr("y1", function(d){
		//return 5
		var lng1 = d["lng1"]
		var lat1 = d["lat1"]
		var y1 = (projection([lng1,lat1])[1])
		//console.log(y)
		return y1
	})
	.attr("x2", function(d){
		var lng = d["lng2"]
		var lat = d["lat2"]
		var x2 = (projection([lng,lat])[0])
		return x2
	})
	.attr("y2", function(d){
		var lng = d["lng2"]
		var lat = d["lat2"]
		var y2 = (projection([lng,lat])[1])
		//console.log(y)
		return y2
	})
	.attr("stroke-width",function(d){
		var difference = d["difference"]
		if(isNaN(difference)){
			return 0
		}
		return 10
	})
	.attr("stroke",function(d){
		var difference = d["difference"]
		if(isNaN(difference)){
			return "none"
		}
		return "#E7D839"
	})
	.attr("stroke-opacity",.1)
		.attr("stroke-linecap","round")
	
}
function renderMap(data, selector,width,height) {
	var projection = d3.geo.mercator().scale(global.scale).center(global.center)
	var path = d3.geo.path().projection(projection);
	
	var zoom = d3.behavior.zoom()
	    .translate([0, 0])
	    .scale(1)
	    .scaleExtent([1, 10])
	    .on("zoom", zoomed);
		
	var svg = d3.select(selector).append("svg")
		.attr('height', height)
		.attr('width', width);
		
	map =  svg.append("g")
		
//	map.append("rect")
//	    .attr("class", "overlay")
//	    .attr("width", width)
//	    .attr("height", height)
//	 	.call(zoom);
				
	map.selectAll(".map").append("path")
		.data(data.features)
		.enter()
		.append("path")
		.attr("d", path)
		.attr("class", "map-item")
		.attr("cursor", "pointer")
		.attr("fill","#fff")
	    .call(zoom);
	return map
}
function medianValuesOnly(data){
	var dataById = table.group(data,["Id"])
	var medians = []
	//console.log(dataById)
	for(var i in dataById){
		var income = parseInt(dataById[i][0]["Median"])
		//console.log(dataById[i][0])
		var population = dataById[i][0]["Total"]
		if(income !="-" && isNaN(income)==false){
			medians.push(income)
		}
	}
	var sorted = medians.sort(sortInt)
	return sorted
}
function sortInt(a,b){
	return a-b
}
function calculatePercentile(data,income){
	var totalItems = data.length
	var percentile = Math.round(data.indexOf(income)/totalItems*100)
//	console.log([totalItems,percentile])
	return percentile
}
function formatDifferenceData(data,overlapData){
	var medianValues = medianValuesOnly(data)
	var percentile = calculatePercentile(medianValues,80000)
	//console.log(percentile)
	
	var dataById = table.group(data, ["Id"])
	var incomes = []
	var minDifference = global.minDifference
	for(var i in overlapData){
		var id1 = overlapData[i]["id1"]
		var id2 = overlapData[i]["id2"]
		if(id1 in dataById && id2 in dataById){
		//console.log([income1,income2])
			if(!isNaN(parseInt(dataById[id2][0]["Median"])) || !isNaN(parseInt(dataById[id1][0]["Median"]))){
				var income1 = parseInt(dataById[id1][0]["Median"])
				var income2 = parseInt(dataById[id2][0]["Median"])
				var average = (income1+income2)/2			
				var incomeDifference = Math.abs(income1-income2)
				var percent1 = incomeDifference/income1*100
				var percent2 = incomeDifference/income2*100
				//var percentileDifference = Math.abs(percent1-percent2)
				var pop1 = parseInt(dataById[id1][0]["Total"])
				var pop2 = parseInt(dataById[id2][0]["Total"])
				var popDifference = Math.abs(pop1-pop2)
				var pop1Percent = popDifference/pop1*100
				var pop2Percent = popDifference/pop2*100
				var popPercentDif = Math.abs(pop1Percent-pop2Percent)
			
				var percentile1 = calculatePercentile(medianValues,income1)
				var percentile2 = calculatePercentile(medianValues,income2)
				var percentileDifference = Math.abs(percentile1-percentile2)
				//console.log([income1,percentile1,income2,percentile2,percentileDifference])
				//console.log(pop1,pop2,popPercentDif)
			//	console.log(percentileDifference)
				var lng1 = parseFloat(overlapData[i]["lng1"])
				var lng2 =parseFloat(overlapData[i]["lng2"])
				var lat1 = parseFloat(overlapData[i]["lat1"])
				var lat2 = parseFloat(overlapData[i]["lat2"])
			
				if(isNaN(lng2)){
					lng2 = lng1
				}
				if(isNaN(lat2)){
					lat2 = lat1
				}
			
				var average = (income1+income2)/2			
				var incomeDifference = Math.abs(income1-income2)
				var percentageDifference = incomeDifference/average*100
				//console.log(percentageDifference)
				if( percentileDifference>minDifference &&income1 !=0 && !isNaN(pop1)&& !isNaN(pop2)&& income2!=0 && popDifference<pop1 && popDifference<pop2 && pop1 !=0 && pop2 !=0){
					incomes.push({income1:income1, income2:income2, percentile1:percentile1,percentile2:percentile2,id1:overlapData[i]["id1"],id2:overlapData[i]["id2"],lng1:lng1,lat1:lat1,lng2:lng2,lat2:lat2,difference:percentileDifference})
				}
			}
		}
	}
	//console.log(incomes)
	var sortedIncomes = incomes.sort(function(a,b){return a["difference"]-b["difference"]}).reverse()
	return sortedIncomes
}
function renderNycMap(data, column,svg,low,high,neighbors,neighborhoodDictionary) {
	var map = d3.select(svg).selectAll(".map-item")
	var companiesByZipcode = table.group(data, ["Id"])
	var idToNeighborhood = neighborhoodDictionary.blockgroup_nhoods
	//	var largest = table.maxCount(companiesByZipcode)
	//console.log(companiesByZipcode)
	var colorScale = function(d) {
		var scale = d3.scale.linear().domain([0,global.max]).range([global.gradientStart, global.gradientEnd]); 
		var x = companiesByZipcode[d.properties.GEOID]
		if(!x){
			return scale(1)
		}else{
			if(isNaN(x[0][column])) {
				return scale(1)
			}
			if(x[0][column] < low ||x[0][column] > high){
				return "#eee"
			}
			return scale(x[0][column])
		}
	}

	map.attr("stroke-opacity", 1)
		.attr("stroke","none")
		.attr("fill-opacity", 1)
		.attr("fill",colorScale)
		.attr("stroke-width",.5)
		var tip = d3.tip()
		  .attr('class', 'd3-tip-nyc')
		  .offset([-10, 0])
	
		map.call(tip);
		map.on('mouseover', function(d){
			global.mapFillColor = d3.select(this).attr("fill")
			
			var currentZipcode = d.properties.GEOID
			var currentIncome = table.group(data, ["Id"])[currentZipcode][0][column]
			var currentIncome = currentIncome.replace("+","")
			var currentIncome = currentIncome.replace(",","")
			var neighborhood = idToNeighborhood[currentZipcode]
			if(companiesByZipcode[currentZipcode]){
				if(isNaN(currentIncome) || currentIncome == "" || currentIncome == undefined){
					//tipText = "no data"
					//console.log(companiesByZipcode[currentZipcode])
					d3.selectAll("#svg-2 svg").remove()
				}
				else{
					//tipText = "block group: "+currentZipcode+"<br/>median household income:$"+ currentIncome
					if(neighborhood == ""){
						tipText = "block group "+currentZipcode
					}else{
					tipText = "block group "+currentZipcode+" in "+neighborhood
					}
					var test = "test"
					tip.html(function(d){return tipText})
					tip.show()
					d3.select("#current-details").html("Adjacent Median Incomes:</br> Census block group "+currentZipcode+" has median household income of $"+currentIncome)
					drawNeighborsGraph(companiesByZipcode, currentZipcode)
					d3.select(this).attr("fill","red")
				}
			}			
		})
		.on('mouseout', function(d){
			d3.select(this).attr("fill",global.mapFillColor)
			d3.select("#current-details").html("")
			tip.hide()
			d3.selectAll("#svg-2 svg").remove()
		})
		//.on("click",function(d){
		//	console.log(d.properties.GEOID)
		//	console.log(companiesByZipcode[d.properties.GEOID][0]["Total"])
		//	console.log(companiesByZipcode[d.properties.GEOID])
		//})
	return map
}
function drawNeighborsGraph(data, id){
	d3.selectAll("#svg-2 svg").remove()
	var height = 140
	var width = 400
	var chart = d3.selectAll("#svg-2")
			.append("svg")
			.attr("width",width)
			.attr("height",height)
			.append("g")
			.attr("transform","translate(80,20)")
	var margin = 80
	var neighborsMedians = []
	var incomeScale = d3.scale.linear().domain([0,250000]).range([0,height-margin])
	var incomeScaleReverse = d3.scale.linear().domain([0,250000]).range([height-margin,0])
	
	var selectedIdMedian = parseInt(data[id][0]["Median"])
	neighborsMedians.push({"id":id,"Median": selectedIdMedian})

	var marginLeft = 30
	var yAxis = d3.svg.axis().scale(incomeScaleReverse).orient("left").ticks(4)
	var sum = selectedIdMedian
	var divideBy = 1
	
	var neighborsList = global.neighbors[id]
	for(var neighbor in neighborsList){
		var currentId = neighborsList[neighbor]
		if(currentId in data){
			var income = parseInt(data[currentId][0]["Median"])	
			if(!isNaN(income)){
				neighborsMedians.push({"id":currentId,"Median":income})
				sum = sum+income
				divideBy +=1
			}
		}		
	}

	var neighbors = neighborsMedians.items;
	var average = sum/divideBy
	//console.log(average)
	//console.log(neighbors)
	chart.selectAll("rect")
		.data(sortObjectByValue(neighborsMedians))
		.enter()
		.append("rect")
		.attr("x", function(d,i){
			return i*8+10
		})
		.attr("y", function(d){
			return height-margin-incomeScale(d.Median)
		})
		.attr("width", 6)
		.attr("height", function(d){
			return incomeScale(d.Median)
		})
		.attr("fill",function(d){
			if(d.id == id){
				return "red"
			}else{
				return "black"
			}
		})
		
		chart.append("rect")
			.attr("class","average")
			.attr("x", 0)
			.attr("y", function(){
				return height-margin-incomeScale(average)
			})
			.attr("width", divideBy*8+10)
			.attr("height", 1)
			.attr("fill","#aaa")
		chart.append("text")
			.attr("class","average-text")
			.attr("x", 5)
			.attr("y", function(){
				return height-margin-incomeScale(average)-5
			})
			.text("Average $"+ parseInt(average))
			.attr("font-size",10)
	chart.append("g").attr("class", "y axis").call(yAxis)
}
function showHide(shID) {
   if (document.getElementById(shID)) {
      if (document.getElementById(shID+'-show').style.display != 'none') {
         document.getElementById(shID+'-show').style.display = 'none';
         document.getElementById(shID).style.display = 'block';
      }
      else {
         document.getElementById(shID+'-show').style.display = 'inline';
         document.getElementById(shID).style.display = 'none';
      }
   }
}
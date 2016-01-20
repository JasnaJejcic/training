
var chart = d3.select(".chart").append("svg")
                              .attr("width", 500)
                              .attr("height", 500);
chart.append("g")
     .attr("class", "xaxis")
     .attr("transform", "translate(0," + 300 + ")");

var xScale = d3.scale.linear()
                     .domain([0, 30])
                     .range([0, 400]);
var xAxis = d3.svg.axis()
                  .scale(xScale);
chart.select("g.xaxis")
     .call(xAxis);


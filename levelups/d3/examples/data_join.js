
var chart = d3.select(".chart").append("svg")
                              .attr("width", 500)
                              .attr("height", 500);

var data = [30, 100 , 200, 300];

var svg = d3.select("svg");
var circles = svg.selectAll("circle").data(data);

// Update selection is empty at first
//

// Enter selection
circles.enter()
       .append("circle")
       .attr("cx", function(d){return d;})
       .attr("cy", 20)
       .attr("r", 2);

// Update selection
circles.transition()
       .delay(function(d, i){ return i*500; })
       .attr("r", function(d){ return Math.sqrt(d);})
       .attr("cy", function(d){return d});
// Exit selection is empty so do nothing
//

d3.select("#moveCircles").on("click", function(){
    moveCircles();
});

function moveCircles(){
    var data = [50, 150, 250];
    // enter selection is empty


    var circles = svg.selectAll("circle").data(data);
    //update selection contains three nodes
    circles.transition()
           .attr("cx", 350)
           .attr("r", function(d){return Math.sqrt(d);});

    // exit selection contains one node - move off canvas and remove
    circles.exit()
           .transition()
           .attr("cx", 0)
           .remove();
}


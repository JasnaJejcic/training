
var addSelectOverlay = function(){

    var chart = d3.select(".chart").append("svg")
                                  .attr("width", 500)
                                  .attr("height", 500);

    chart.append("g")
              .attr("class", "slider");

    xScale = d3.scale.linear()
                    .clamp(true)
                    .range([0, 500])
                    .domain([0, 50]);
    var height = 300;
    var xMax = 50;

    // Add Brush
    var brush = d3.svg.brush()
                  .x(xScale)
                  .extent([500, xMax])
                  .on("brush", brushed);

    var slider = chart.select("g.slider")
                      .call(brush);


    slider.select(".extent")
          .attr("height", height);
    slider.select(".resize.e").remove();
    slider.select(".resize.w rect").attr("height", height)
                              .attr("x","0")
                              .attr("width", "2");

    // Add the custom slider handle
    var handleData = [[0,0],[-10,-10],[-80,-10],[-80,-40],[80,-40],[80,-10],[10,-10]];
    var pathGen = d3.svg.line();

    slider.select(".resize.w").append("path")
                              .attr("d", pathGen(handleData) + "Z")
                              .attr("fill", "blue")
                              .attr("stroke-width", "1")
                              .attr("stroke", "blue");

    var sliderText = slider.select(".resize.w")
                           .append("text")
                           .attr("class", "slider-text")
                           .append("tspan")
                           .attr("text-anchor", "middle")
                           .attr("y", "-20")

    brushed();

    function brushed(){
        //console.log(d3.event.mode);

        var brushValues = brush.extent();
        var val = brushValues[0];
        if (d3.event && d3.event.mode === "resize" && val >= 2500){
            //brushValues[0] = xMax;
            val = 2500;
            brush.extent([val, 50]);
            //brushValues[0] = xMax;
        }

        //var textFormat = d3.format("0,000");
        //sliderText.text(textFormat(Math.floor(val)) + " Leads");
        //d3.select(this).call(brush.extent([brushValues]));
    }

}

addSelectOverlay();

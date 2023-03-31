   <meta charset="utf-8">   <title>Chart.js </title>      <!-- import plugin script -->   <script src="static/Chart.min.js"></script>
<h1>Flask Chart.js</h1>
<!-- bar chart canvas element --><canvas id="chart" width="600" height="400"></canvas>
<script><br />
   // bar chart data<br />
   var barData = {<br />
   labels : [],<br />
   datasets : [<br />
      {<br />
            fillColor: "rgba(151,187,205,0.2)",<br />
            strokeColor: "rgba(151,187,205,1)",<br />
            pointColor: "rgba(151,187,205,1)",<br />
         data : []<br />
      }<br />
      ]<br />
   }</p>
<p>   // get bar chart canvas<br />
   var mychart = document.getElementById("chart").getContext("2d");</p>
<p>   steps = 10<br />
   max = 10<br />
   // draw bar chart<br />
   new Chart(mychart).Bar(barData, {<br />
        scaleOverride: true,<br />
        scaleSteps: steps,<br />
        scaleStepWidth: Math.ceil(max / steps),<br />
        scaleStartValue: 0,<br />
        scaleShowVerticalLines: true,<br />
        scaleShowGridLines : true,<br />
        barShowStroke : true,<br />
        scaleShowLabels: true<br />
   });</p>
<p></script>
<html>

<head>
<title>Waterpai Dashboard</title>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>


body {
  font-family: Arial, Helvetica, sans-serif;
  margin: 0;
}


.header {
  padding: 80px;
  text-align: center;
  background: #1abc9c;
  color: white;
}


.header h1 {
  font-size: 40px;
}


.row {  
  display: -ms-flexbox; 
  display: flex;
  -ms-flex-wrap: wrap; 
  flex-wrap: wrap;
}

.side {
  -ms-flex: 20%; 
  flex: 20%;
  background-color: #f1f1f1;
  padding: 20px;
}

.mid {   
  -ms-flex: 20%; 
  flex: 20%;
  background-color: white;
  padding: 20px;
}

.main {   
  -ms-flex: 20%; 
  flex: 20%;
  background-color: #f1f1f1;
  padding: 20px;
}

.fakeimg {
  background-color: #aaa;
  width: 100%;
  padding: 20px;
}



</style>


<link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">
<link rel="stylesheet" href="/resources/demos/style.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"> 
<script src="https://code.jquery.com/jquery-1.12.4.js"></script>  
<script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script> 
<script>
  $( function() {
    $( "#tabs" ).tabs();
  } );
</script>

<script>
function showUser(str) {
  if (str == "") {
    document.getElementById("txtHint").innerHTML = "";
    return;
  } 
  else {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        document.getElementById("txtHint").innerHTML = this.responseText;
      }
    };
    xmlhttp.open("GET","userfeedback.php?q="+str,true);
    xmlhttp.send();
  }
}
</script>



</head>

<body>

<div class="header">
  <h1>Waterpai Dashboard</h1>
  <p>Created by Ananth & Divya Shyamal</p>
</div>
 
<div id="tabs">
  <ul>
    <li><a href="#tabs-7">Home </a></li>
    <li><a href="#tabs-6">User Input </a></li>
    <li><a href="#tabs-3">Watering History </a></li>
    <li><a href="#tabs-5">Graph </a></li>
    <li><a href="#tabs-1">Seasonal Hourly Data</a></li>
    <li><a href="#tabs-2">Today's Hourly Data</a></li>
    <li><a href="#tabs-4">Daily Precipitation, ET Data</a></li> 
</ul>
  
<div id="tabs-1">

<head>
<style>
table
{
  border-style:solid;
  border-width:2px;
  border-color:pink;
}
h1 {text-align: center;}
</style>
</head>
<h1>All Weather Data</h1>
<?php
$servername = "xxxxxxxxx";
$username = "waterpai";
$password = "xxxxxxxxx";
$dbname = "WeatherData";

$conn = new mysqli($servername, $username, $password, $dbname);
$sql = "SELECT * FROM ETData";
$result = $conn->query($sql);

echo "<table border='1'>
<tr>
<th>station</th>
<th>time</th>
<th>tmpf</th>
<th>relh</th>
<th>solar</th>
<th>precip</th>
<th>speed</th>
<th>et</th>
</tr>";

while($row = $result->fetch_assoc())
{
  echo "<tr>";
  echo "\n <td>" . $row['station'] . "</td>";
  echo "\n <td>" . $row['time'] . "</td>";
  echo "\n <td>" . $row['tmpf'] . "</td>";
  echo "\n <td>" . $row['relh'] . "</td>";
  echo "\n <td>" . $row['solar'] . "</td>";
  echo "\n <td>" . $row['precip'] . "</td>";  
  echo "\n <td>" . $row['speed'] . "</td>";
  echo "\n <td>" . $row['et'] . "</td>";
  echo "\n </tr>\n";
}

echo "\n</table>";
$conn->close(); 
?>

</div>
<div id="tabs-2">
 
<head>
<style>
table
{
  border-style:solid;
  border-width:2px;
  border-color:pink;
}
h1 {text-align: center;}
</style>
</head>
<h1>Today's Hourly Data</h1>
<?php
$servername = "xxxxxxxxx";
$username = "waterpai";
$password = "xxxxxxxxx";
$dbname = "WeatherData";

$conn = new mysqli($servername, $username, $password, $dbname);
$sql = "select * from ETData where date(time)=(select date(max(time)) from ETData)";
$result = $conn->query($sql);

echo "<table border='1'>
<tr>
<th>station</th>
<th>time</th>
<th>tmpf</th>
<th>relh</th>
<th>solar</th>
<th>precip</th>
<th>speed</th>
<th>et</th>
</tr>";

while($row = $result->fetch_assoc())
{
  echo "<tr>";
  echo "\n <td>" . $row['station'] . "</td>";
  echo "\n <td>" . $row['time'] . "</td>";
  echo "\n <td>" . $row['tmpf'] . "</td>";
  echo "\n <td>" . $row['relh'] . "</td>";
  echo "\n <td>" . $row['solar'] . "</td>";
  echo "\n <td>" . $row['precip'] . "</td>";  
  echo "\n <td>" . $row['speed'] . "</td>";
  echo "\n <td>" . $row['et'] . "</td>";
  echo "\n </tr>\n";
}

echo "\n</table>";
$conn->close(); 
?>
</div>



<div id="tabs-3">
<head>
<style>
table
{
  border-style:solid;
  border-width:2px;
  border-color:pink;
}
h1 {text-align: center;}
</style>
</head>
<h1>Watering History</h1>
<?php
$servername = "xxxxxxxxx";
$username = "waterpai";
$password = "xxxxxxxxx";
$dbname = "WeatherData";

$conn = new mysqli($servername, $username, $password, $dbname);
$sql = "select * from WateringHistory";
$result = $conn->query($sql);

echo "<table border='1'>
<tr>
<th>time</th>
</tr>";

while($row = $result->fetch_assoc())
{
  echo "<tr>";
  echo "\n <td>" . $row['time'] . "</td>";
  echo "\n </tr>\n";
}

echo "\n</table>";
$conn->close(); 
?>


</div>

<div id="tabs-4">
 <head>
<style>
table
{
  border-style:solid;
  border-width:2px;
  border-color:pink;
}
h1 {text-align: center;}
</style>
</head>
<h1>Daily Precipitation, ET Data</h1>
<?php
$servername = "xxxxxxxxx";
$username = "waterpai";
$password = "xxxxxxxxx";
$dbname = "WeatherData";

$conn = new mysqli($servername, $username, $password, $dbname);
$sql = "select date(time) as date, sum(greatest(precip,0)) as precip, sum(greatest(et,0)) as et from ETData group by date(time)";
$result = $conn->query($sql); 

echo "<table border='1'>
<tr>
<th>date</th>
<th>precip</th>
<th>et</th>
</tr>";

while($row = $result->fetch_assoc())
{
  echo "<tr>";
  echo "\n <td>" . $row['date'] . "</td>";
  echo "\n <td>" . $row['precip'] . "</td>";  
  echo "\n <td>" . $row['et'] . "</td>";  
  echo "\n </tr>\n";
}

echo "\n</table>";
$conn->close(); 
?>

</body>

</div>


<div id="tabs-5">
<head>
<style>
table
{
  border-style:solid;
  border-width:2px;
  border-color:pink;
}
h1 {text-align: center;}
</style>
</head>
<h1>Graphs</h1>
<?php
$servername = "xxxxxxxxx";
$username = "waterpai";
$password = "xxxxxxxxx";
$dbname = "WeatherData";

$conn = new mysqli($servername, $username, $password, $dbname);
$sql = "select date(time) as date, sum(greatest(precip,0)) as precip, sum(greatest(et,0)) as et from ETData group by date(time)";
$result = $conn->query($sql); 


$dataPointsP = array();
$dataPointsE = array();
$dataPointsN = array();
$dataPointsI = array();
$dataPointsW = array();
while($row = $result->fetch_assoc())
{
  array_push($dataPointsP, array("x"=> (strtotime($row['date'])-strtotime('2020-06-01 00:00:00'))/86400, "y"=>  $row['precip']));
  array_push($dataPointsE, array("x"=> (strtotime($row['date'])-strtotime('2020-06-01 00:00:00'))/86400, "y"=>  $row['et']));
}
$sql = "select * from IrrigationData";
$result = $conn->query($sql); 
while($row = $result->fetch_assoc())
{
  array_push($dataPointsI, array("x"=> (strtotime($row['time'])-strtotime('2020-06-01 00:00:00'))/3600, "y"=>  $row['irrig']));
}
$sql = "select * from NeededIrrigationData";
$result = $conn->query($sql); 
while($row = $result->fetch_assoc())
{
  array_push($dataPointsN, array("x"=> (strtotime($row['time'])-strtotime('2020-06-01 00:00:00'))/3600, "y"=>  $row['neededirrig']));
}
$sql = "select * from WateringHistory";
$result = $conn->query($sql); 

while($row = $result->fetch_assoc())
{
  array_push($dataPointsW, array("x"=> (strtotime($row['time'])-strtotime('2020-06-01 00:00:00'))/3600, "y"=>  $dataPointsI[5][5]));
}
$conn->close(); 
?>

<head>
<script>
window.onload = function () {
var dt = new Date(2019, 10, 1)
var chartE1 = new CanvasJS.Chart("chartContainer1",{
  width:700,
  title: {
         text: "Daily ET Over the Season"
  },
  axisX: {
		    interlacedColor: "#F8F1E4",
        gridThickness: 0,
        interval: 30,
        labelFormatter: function(e) {
        dt.setMonth(dt.getMonth() + 1);
        return CanvasJS.formatDate(dt, "MMM")
        } 
  },
  axisY: [{
        title: "ET (in)",
        lineColor: "#C24642",
        titleFontColor: "#C24642",
        labelFontColor: "#C24642"
  }],
  legend: {
        horizontalAlign: "left", // "center" , "right"
        verticalAlign: "top",  // "top" , "bottom"
        fontSize: 15
   },
   data: [{
        type: "scatter",
		    showInLegend: true,
		    color: "#C24642",
        name: "ET",
        dataPoints: <?php echo json_encode($dataPointsE, JSON_NUMERIC_CHECK); ?>
   }]
});
var d = new Date(2019, 10, 1)
var chartE2 = new CanvasJS.Chart("chartContainer2",{
    width:700,
    title: {
          text: "Daily Precipitation Over the Season"
    },
    axisX: {
          interlacedColor: "#F8F1E4",
          gridThickness: 0,
          interval: 30,
          labelFormatter: function(e) {
            d.setMonth(dt.getMonth() + 1);
            return CanvasJS.formatDate(dt, "MMM")
          } 
    },
    axisY: [{
          title: "Precip (in)",
          lineColor: "#0000FF",
          titleFontColor: "#0000FF",
          labelFontColor: "#0000FF"
    }],
    legend: {
       horizontalAlign: "left", // "center" , "right"
       verticalAlign: "top",  // "top" , "bottom"
       fontSize: 15
    },
    data: [{
       type: "scatter",
       showInLegend: true,
       color: "#0000FF",
       name: "Precip",
       dataPoints: <?php echo json_encode($dataPointsP, JSON_NUMERIC_CHECK); ?>
    }]
});
chartE1.render();
chartE2.render();
}
</script>
</head>
<body>
<div id="chartContainer1" style="height: 370px; width: 45%; display: inline-block;"></div>
<div id="chartContainer2" style="height: 370px; width: 45%; display: inline-block;"></div>
<script src="https://canvasjs.com/assets/script/canvasjs.min.js"></script>
</body>

</div>

<div id="tabs-6">
<h1> User Input </h1>
<h3> How is the lawn looking?</h3>


<form>
<select name="users" onchange="showUser(this.value)">
  <option value="">Select an option:</option>
  <option value="1">Good (uniformly green)</option>
  <option value="2">OK (a few, small brown spots)</option>
  <option value="3">Not Good (many large brown spots)</option>
  <option value="4">Very Bad (uniformly brown)</option>
  </select>
</form>
<br>
<div id="txtHint"><b>Updated needed irrigation will appear below</b></div>
</div>



<div id="tabs-7">


<div class="row">
<div class="side">
<h2>About Waterpai</h2>
<p> Waterpai is a Raspberry Pi-based smart lawn irrigation system. By utilizing historical, current, and forecast weather data, Waterpai improves irrigation efficiency. For convenience, the system has been designed to coexist with the existing irrigation controller, without disturbing existing external plumbing. Waterpai has many new safety features, by introducing a motorized ball valve and flow meter in the internal irrigation plumbing line and a multi-pronged alert system. Waterpai features a web-based user interface, where one can monitor the status of the irrigation and provide feedback.  <br> <br> Waterpai has been in development since May 2020. We field-tested it on our lawn from June 1 through September 30. During that period, we found it to be 11% more cost/water efficient than our existing Hunter Pro-C controller. Since then, we have continually worked to improve the system, adding features that improve the reliability and safety, increasing sourcing of on-site data, of the system.    </p>
</div>

<div class="mid">
<h2>Current Status</h2>
<?php
$servername = "xxxxxxxxx";
$username = "waterpai";
$password = "xxxxxxxxx";
$dbname = "WeatherData";

$conn = new mysqli($servername, $username, $password, $dbname);

$sql = "select * from IrrigationData ORDER BY time DESC LIMIT 1";
$result = $conn->query($sql); 
$row = $result->fetch_assoc();
$status = '';
if(date("m") >= 10 or date("m") < 6) {
  $status =  "Out of Irrigation Season";
} 
else {
  $status =  "Currently In Irrigation Season";
}
?>

<p style="color:red"> Irrigation Status: </p> <p><?php echo $status?> <br> </p> <p style="color:red"> Needed Irrigation: </p> <p> <?php echo $row['irrig']?> inches <br> <br> Note that Waterpai irrigates when the needed irrigation exceeds .2 inches and the current/forecast weather conditions are suitable.</p>
</div>


</div>

</div>


</div>
 
 
</body>
</html>


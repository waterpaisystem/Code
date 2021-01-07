<html>
<body>

<?php
$q = intval($_GET['q'])/10;

$con = mysqli_connect('xxxxxxxxx','waterpai','xxxxxxxxx','WeatherData');
if (!$con) {
  die('Could not connect: ' . mysqli_error($con));
}
echo "Adding " .$q. " inches to Needed Irrigation \n"; 
$sql="select *from IrrigationData ORDER BY time DESC LIMIT 1";
$result = mysqli_query($con,$sql);
while($row = mysqli_fetch_array($result)) {
  $t = $row['time'];
}


$sql="UPDATE IrrigationData SET irrig = irrig + ".$q." WHERE time ='".$t."'";
$result = mysqli_query($con,$sql);

$sql="select *from IrrigationData ORDER BY time DESC LIMIT 1";
$result = mysqli_query($con,$sql);

echo "<table>
<tr>
<th>Time</th>
<th>Needed Irrigation (in)</th>
</tr>";
while($row = mysqli_fetch_array($result)) {
  echo "<tr>";
  echo "<td>" . $row['time'] . "</td>";
  echo "<td>" . $row['irrig'] . "</td>";
  echo "</tr>";
}
echo "</table>";
mysqli_close($con);
?>
</body>
</html>

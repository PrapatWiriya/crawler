<!doctype html>
<html lang="en">
<body>
<?php
require_once('condb.php');
$get_html = $_GET['Name'];
$sg = (int)$_GET['Ma'];
$sql_data = "SELECT data_html.id,html_data,data_url.id,url,date,l_html FROM data_html
INNER JOIN data_url ON data_html.id = data_url.id
WHERE html_data LIKE '%$sg%' OR url LIKE '%$sg%' OR l_html LIKE '%$get_html%'
ORDER BY data_html.id ASC";
$sql_url = "SELECT * FROM data_url";
$result1 = pg_query($con, $sql_url);
$result = pg_query($con, $sql_data);

while ($row= pg_fetch_array($result) or $row1 = pg_fetch_array($result1)) {    
?>
<?php
    if($sg == (int)$row['id']){
        echo $row['l_html'];
        break;
    }
    
    
?>

<?php } ?>
</body>

</html>
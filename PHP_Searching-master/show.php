<div class="container">
    <div class="row">
        <div class="col-md-12">
            <table  class="table table-striped" border="1" cellpadding="0"  cellspacing="0" align="center">
                <thead>
                    <tr class="table-primary">
                        <th width="10%">date</th>
                        <th width="50%">detail</th>
                        <th width="5%">url</th>
                        <th width="50%">exam</th>
                    </tr>
                </thead>
                <?php
                echo '<font color="red">';   
                echo 'คำค้น = ';
                echo $_GET['q'];
                echo '</font>';
                echo '<br/>';  
                $sg = $_GET['q'];
                echo $sg;           
                $sql_data = "SELECT data_html.id,html_data,data_url.id,url,date,l_html FROM data_html
                    INNER JOIN data_url ON data_html.id = data_url.id
                    WHERE html_data LIKE '%$q%' OR url LIKE '%$q%'
                 ORDER BY data_html.id ASC";
                $sql_url = "SELECT * FROM data_url";
                $result1 = pg_query($con, $sql_url);
                $result = pg_query($con, $sql_data);
                $show = "showhtml.php";
                while ($row= pg_fetch_array($result) and $row1 = pg_fetch_array($result1)) {    
                ?> 
                    <?php $get_url = $row['url'];?>
                    <?php $get_id = $row['id'];?>
                <tr>
                    <td><?php echo '<a href= '.$row['url'].' target="_blank"> '. $row['date']. '</a>';?></td>
                    <td><?php echo  "<a href=showhtml.php?Name=$get_url&Ma=$get_id>Product Details</a>";?>
                    <td><?php echo $row['html_data'];?></td>
                    <td><?php echo $row['url'];?></td>
                    <!--<td>!--?php echo $row['l_html'];?></td>-->
                    <!--td><iframe srcdoc="<a href= '.$row['url']."height="400" width="500"frameborder="0"scrolling="auto"align="right"></a></iframe></td-->
                </tr>
            <?php } ?>
            </table>
        <?php pg_close($con);?>
    </div>
</div>
</div>
<?php

if(isset($_GET) && isset($_GET['goto'])){
  $jsonFile =  '../py/data.json';
  if(is_file($jsonFile)){
    $fp = fopen($jsonFile,'w');
    fwrite($fp,'{"goto":"'.$_GET['goto'].'"}
');
    fclose($fp);

    echo 1;
    exit(0);
  }
}

echo "-1";
exit(0);


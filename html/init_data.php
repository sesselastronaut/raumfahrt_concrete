<?php

$jsonFile =  '../py/data.json';
if(is_file($jsonFile)){
  readfile($jsonFile);
}
else{
  echo "JSON file not found: ".$jsonFile;
} 

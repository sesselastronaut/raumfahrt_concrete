<?php

if($_SERVER['SERVER_NAME'] == 'preview.flxlabs.org'){
  $jsonFile =  '../py/rzalt.json';
  if(is_file($jsonFile)){
    readfile($jsonFile);
  }
  else{
    echo "JSON file not found: ".$jsonFile;
  }
}
else{
  $pyFile = '../py/rzalttojson.py';
  if(is_file($pyFile)){
    echo system('python '.$pyFile);
  }
  else{
    echo "Python file not found: ".$pyFile;
  }
}

<?php
$fp = "../../input_files/day_7_example.txt";

$START_CHAR = "S";
$BEAM_SPLITTER = "^";
$BEAM = "|";

$file = fopen($fp, "r") or die("Unable to open file!");

$line = fgets($file);
$startLocation = [strpos($line, $START_CHAR), 0];

$splitCounter = 0;
$uniqueSplitCounter = 0;
$beamSet = array();


echo "Start location is $startLocation[0]\n";
$lineCount = 1;
while (($line = fgets($file)) !== false) {
    echo "-------------------------\n";
   $beamSplitters = getLocations($line, $lineCount);
   $splitCounter += count($beamSplitters);
   $lineCount++;
}
$result = $splitCounter -1;
echo "Result: $result\n";
fclose($file);

function getLocations($line, $row){
    global $BEAM_SPLITTER;
    $column = 0;
    $positions = array();

    while (($column = strpos($line, $BEAM_SPLITTER, $column))!== false) {
        $positions[] = [$column, $row];
        $column = $column + strlen($BEAM_SPLITTER);
//        echo "$column, ";
    }
//    echo "\n";
    return $positions;
}


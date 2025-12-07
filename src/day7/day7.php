<?php
$fp = "../../input_files/day_7.txt";

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
    if(count($beamSplitters) == 0){
        if($lineCount == 1){
            $beamSet[] = $startLocation[0];
            $line[$startLocation[0]] = $BEAM;
        }
    }else{
        $lineUnique = 0;
        for($i = 0; $i < count($beamSplitters); $i++){
            $splitterUnique = 0;
            $beamX = $beamSplitters[$i];
            if(in_array($beamX, $beamSet)){
                if (($key = array_search($beamX, $beamSet)) !== false) {
                    unset($beamSet[$key]);
                }
                if($beamX > 0){
                    $splitterUnique += 1;
                    $beamSet[] = $beamX - 1;
                    $line[$beamX - 1] = $BEAM;
                }
                if($beamX < strlen($line) - 1){
                    $splitterUnique += 1;
                    $beamSet[] = $beamX + 1;
                    $line[$beamX + 1] = $BEAM;
                }
                if($splitterUnique > 0){
                    echo "Unique at $beamX, $lineCount\n";
                    $uniqueSplitCounter += 1;
                }
            }
        }
    }
    $beamSet = array_unique($beamSet);
    $lineCount++;
}
$result = count($beamSet);
echo "Result: $uniqueSplitCounter\n";
fclose($file);

function getLocations($line, $row){
    global $BEAM_SPLITTER;
    $column = 0;
    $positions = array();

    while (($column = strpos($line, $BEAM_SPLITTER, $column))!== false) {
        $positions[] = $column;
        $column = $column + strlen($BEAM_SPLITTER);
    }
    return $positions;
}


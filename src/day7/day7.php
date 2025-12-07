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
   // check if there is any at all
    if(count($beamSplitters) == 0){
//        echo "No beam splitters on line $lineCount\n";
        if($lineCount == 1){
//            echo "Setting start $startLocation[0]\n";
            $beamSet[] = $startLocation[0];
            $line[$startLocation[0]] = $BEAM;
        }else{
//            for($i = 0; $i < count($beamSet); $i++){
//                $line[$beamSet[$i]] = $BEAM;
//            }
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
//                if(in_array($beamX+2, $beamSplitters) && in_array($beamX-2, $beamSplitters)){
//                    continue;
//                }
                if($beamX > 0){
//                    if(!in_array($beamX - 1, $beamSet)){
//                        $splitterUnique += 1;
//                    }
                    $splitterUnique += 1;
                    $beamSet[] = $beamX - 1;
                    $line[$beamX - 1] = $BEAM;
                }
                if($beamX < strlen($line) - 1){
//                    if(!in_array($beamX + 1, $beamSet)){
//                        $splitterUnique += 1;
//                    }
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
//        if($lineUnique % 2 == 0){
//            echo "All paths unique on line $lineCount\n";
//        }else{
//            echo "Some overlap on line $lineCount\n";
//        }
//        $uniqueSplitCounter += $lineUnique;
    }
    $beamSet = array_unique($beamSet);
//    echo $line;
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
//        echo "$column, ";
    }
//    echo "\n";
    return $positions;
}


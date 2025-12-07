<?php
$fp = "../../input_files/day_7.txt";

$START_CHAR = "S";
$BEAM_SPLITTER = "^";
$BEAM = "|";
function loadFile(){
    $inputLines = array();
    global $fp;
    $file = fopen($fp, "r") or die("Unable to open file!");
    while (($line = fgets($file)) !== false) {
        $inputLines[] = $line;
    }
    fclose($file);
    return $inputLines;
}

function getLocations($line){
    global $BEAM_SPLITTER;
    $column = 0;
    $positions = array();

    while (($column = strpos($line, $BEAM_SPLITTER, $column))!== false) {
        $positions[] = $column;
        $column = $column + strlen($BEAM_SPLITTER);
    }
    return $positions;
}

$pathFinderCache = array();
function pathFinder($inputLines, $column, $row){
    global $pathFinderCache;
    if($row == count($inputLines) ){
        return 1;
    }
    if(array_key_exists("$row,$column", $pathFinderCache)){
        // don't bother calculating again
        return $pathFinderCache["$row,$column"];
    }

    $line = $inputLines[$row];
    $beamSplitters = getLocations($line);
    if(count($beamSplitters) == 0){
        echo "No beams on row $row\n";
        $result = pathFinder($inputLines, $column, $row+1);
        $pathFinderCache["$row,$column"] = $result;
        return $result;
    }
    if(in_array($column, $beamSplitters)){
        echo "Beam ($column, $row) splits into (" . ($column - 1) . ", " . ($row+1) . ") and (" . ($column - 1) . ", " . ($row+1) . ")\n";
        $result = pathFinder($inputLines, $column - 1, $row+1) + pathFinder($inputLines, $column + 1, $row+1);
        $pathFinderCache["$row,$column"] = $result;
        return $result;
    }
    echo "No beam splitters in path of ($column, $row)\n";
    $result = pathFinder($inputLines, $column, $row+1);
    $pathFinderCache["$row,$column"] = $result;
    return $result;
}

// main process
$inputLines = loadFile();
$possibleDirections = [-1, 1];
$maxRow = count($inputLines);
$maxColumn = strlen($inputLines[0]);
$startColumn = strpos($inputLines[0], $START_CHAR);
echo "Start column: $startColumn\n";

$totalPossiblePaths = pathFinder($inputLines, $startColumn, 0);
echo "Total possible paths: $totalPossiblePaths\n";
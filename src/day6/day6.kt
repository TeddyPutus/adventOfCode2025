import java.io.File

class Arithmetic(operator: String){
    var numbers: List<Int> = mutableListOf<Int>();
    var total: Long = 0;
    var operator: String =
        when (operator) {
                        "+" -> operator;
                        "*" -> operator;
                        else -> {
                            println("Invalid OP $operator");
                            throw ArithmeticException("Invalid operator $operator");
                            }
                        }

    fun appendNumber(newNumber: Int){
        numbers += newNumber;
        if(numbers.size == 1) total = newNumber.toLong();
        else {
            total = when (operator) {
                "+" -> total + newNumber;
                "*" -> total * newNumber;
                else -> {
                    println("Invalid OP $operator");
                    throw ArithmeticException("Invalid operator $operator");
                }
            }
        }
    }
    }

private fun Iterable<Arithmetic>.sumTotals(): Long {
    var sum: Long = 0;
    for (element in this) {
        sum += element.total;
    }
    return sum;
}

fun readFileAsLinesUsingUseLines(fileName: String): List<String>
        = File(fileName).useLines { it.toList() }

fun partOne(input: List<String> ){
    var operations: List<Arithmetic> = mutableListOf<Arithmetic>();

    for((lineIndex, line) in input.reversed().withIndex()){
        val splitLine = line.trim().split("\\s+".toRegex())
        for((valueIndex, value) in splitLine.withIndex()){
            if(lineIndex == 0){
                operations += Arithmetic(value.trim());
            }else{
                operations[valueIndex].appendNumber(value.trim().toInt())
            }
        }
    }
    println("PART 1: ${operations.sumTotals()}");
}

fun getVerticalSlice(input: List<String>, index: Int ) : String{
    val result = StringBuilder();

    for(line in input){
        result.append(line.getOrElse(index, { ' ' }))
    }
    return result.toString();
}

fun getLongestLineLength(input: List<String>) : Int{
    var longestLine = 0;
    for(line in input){
        if(line.length > longestLine){
            longestLine = line.length;
        }
    }
    return longestLine;
}

fun partTwo(input: List<String> ){
    var operations: List<Arithmetic> = mutableListOf<Arithmetic>();
    val lineLength = getLongestLineLength(input);

    var currentArithmetic = Arithmetic("+");

    for(index in 0 until lineLength + 1){
        var slice = getVerticalSlice(input, index);
        var operator = slice.last().toString();
        slice = slice.dropLast(1);

        if(operator == "+" || operator == "*"){
            currentArithmetic = Arithmetic(operator);
        }
        if(slice.trim().length == 0){
            operations += currentArithmetic;
        }else{
            currentArithmetic.appendNumber(slice.trim().toInt());
        }
    }
    println("PART 2: ${operations.sumTotals()}");
}

fun main() {
    val filepath = "YOUR_FILEPATH_HERE"
    val input: List<String> = readFileAsLinesUsingUseLines(filepath);
    partOne(input);
    partTwo(input);
}
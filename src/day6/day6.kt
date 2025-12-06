import java.io.File

class Arithmetic(operator: String) {
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

    fun appendNumber(newNumber: Int) {
        numbers += newNumber;
        if (numbers.size == 1) total = newNumber.toLong();
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

fun main() {
    val input: List<String> = readFileAsLinesUsingUseLines(filepath);
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
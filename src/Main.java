import day1.SafeCracker;

void main() {
    //TIP Press <shortcut actionId="ShowIntentionActions"/> with your caret at the highlighted text
    // to see how IntelliJ IDEA suggests fixing it.

    String filepath = "C:\\Users\\teddy\\IdeaProjects\\adventOfCode2025\\input_files\\day_1.txt";
    Integer startPoint = 50;

    SafeCracker safeCracker = new SafeCracker(filepath, startPoint);
    safeCracker.crackSafe();

    System.out.println("-------------------------------------");
    IO.println("Safe cracked!!");
    IO.println("Times landed on zero: " + safeCracker.getZeroCount());
    IO.println("Times passed through zero: " + safeCracker.getPassThroughZero());
    IO.println("Total times on zero: " + (safeCracker.getZeroCount() + safeCracker.getPassThroughZero()));
}

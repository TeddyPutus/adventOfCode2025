import java.io.File

class Node(var name: String){
    var children: List<Node> = mutableListOf();
    var result: Long = -1L;

    fun addNext(next: Node){
        this.children += next;
    }

    fun getPathCountToDestination(destination: String) : Long {
        if(this.name == destination) return 1;
        if(this.result != -1L) return this.result;

        this.result = this.children.sumOf { it.getPathCountToDestination(destination) };
        return this.result;
    }
}

private fun MutableMap<String, Node>.getOrAdd(name: String): Node {
    if(this.containsKey(name)) return this[name]!!;

    this[name] = Node(name);
    return this[name]!!;
}

fun createOrUpdateNode(name: String, children: List<String>, existingNodes: MutableMap<String, Node>): Node {
    val node : Node = existingNodes.getOrAdd(name);

    children.forEach {
        node.addNext(existingNodes.getOrAdd(it));
    }

    return node;
}

fun parseInput(input: List<String>, existingNodes: MutableMap<String, Node>){
    println("Parsing input...");
    input.forEach {
        println("Parsing $it");
        val (name, c) = it.trim().split(":");
        val children = c.trim().split(" ");
        createOrUpdateNode(name, children, existingNodes);
    }
    println("Parsing Complete");
}

fun resetNodes(nodes: MutableMap<String, Node>){
    nodes.forEach { (_, node) ->
        node.result = -1L;
    }
}

fun getPathCountToDestination(startNode: Node, destination: String, nodeMap: MutableMap<String, Node>): Long {
    val result = startNode.getPathCountToDestination(destination);
    resetNodes(nodeMap);
    return result;
}

fun partOne(nodeMap: MutableMap<String, Node>): Long{
    val youNode = nodeMap["you"]!!;
    return getPathCountToDestination(youNode, "out", nodeMap);
}

fun partTwo(nodeMap: MutableMap<String, Node>): Long{
    val svrNode = nodeMap["svr"]!!;
    val fftNode = nodeMap["fft"]!!;
    val dacNode = nodeMap["dac"]!!;

    val serverToFftToDacToOut = getPathCountToDestination(svrNode, "fft", nodeMap) *
            getPathCountToDestination(fftNode, "dac", nodeMap) *
            getPathCountToDestination(dacNode, "out", nodeMap);

    val serverToDacToFftToOut = getPathCountToDestination(svrNode, "dac", nodeMap) *
            getPathCountToDestination(dacNode, "fft", nodeMap) *
            getPathCountToDestination(dacNode, "out", nodeMap);

    return serverToFftToDacToOut + serverToDacToFftToOut;
}

fun main() {
    val nodeMap = mutableMapOf<String, Node>();
    val filepath = "YOU_FILEPATH";
    val input: List<String> = File(filepath).useLines { it.toList() };

    parseInput(input, nodeMap);

    println("Getting results");
    val partOneResult = partOne(nodeMap);
    val partTwoResult = partTwo(nodeMap);

    println("(Part 1): Result is $partOneResult");
    println("(Part 2): Result is $partTwoResult");
}
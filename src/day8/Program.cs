using System.Collections;
using System.Collections.Generic;
using System.Security.Principal;

Console.WriteLine("Day 8 Part 1");

string filepath = "FILEPATH";
const int CONNECTION_COUNT = 10;

FileProcessor fileProcessor = new FileProcessor(filepath);
fileProcessor.loadFile();
List<JunctionBox> jbs = fileProcessor.GetJunctionBoxes();
ConnectionHandler connectionHandler = new ConnectionHandler(CONNECTION_COUNT, jbs);

List<Connection> connections = connectionHandler.getConnections();
Console.WriteLine("Number of connections made: " +  connections.Count());
long firstFullCircuit = connectionHandler.makeConnections();


List<int> results = new List<int>();
for(int i = 0; i < jbs.Count(); i++)
{
    if (!jbs[i].visited)
    {
        results.Add(jbs[i].circuitSize());
    }
}
int total = 0;
foreach(int res in results.OrderByDescending(n=>n).ToList().Take(3))
{
    Console.WriteLine($"Res is {res}");
    if (total == 0) total = res;
    else total*=res;
}
Console.WriteLine($"The result is {total}");

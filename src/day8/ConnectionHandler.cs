using System;
using System.Data;
using System.Security.Cryptography;

public class ConnectionHandler
{
	public int requiredCount;
	public List<JunctionBox> jbs;
    public List<Connection> connections;
    public ConnectionHandler(int requiredCount, List<JunctionBox> jbs)
	{
		this.requiredCount = requiredCount;
		this.jbs = jbs;
	}

	public List<Connection> getConnections()
	{
        List<Connection> connections = new List<Connection>();
        Dictionary<String, Connection> connectionDict = new Dictionary<String, Connection>();

        foreach (JunctionBox junctionBox in this.jbs)
        {
            foreach (JunctionBox jb in this.jbs)
            {
                Connection newConnection = new Connection(junctionBox, jb);
                if (!connections.Any() || connections.Count() < this.requiredCount)
                {

                    if (jb != junctionBox && !connectionDict.ContainsKey($"{jb.getKey()}{junctionBox.getKey()}"))
                    {
                        connections.Add(newConnection);
                        connectionDict.Add($"{jb.getKey()}{junctionBox.getKey()}", newConnection);
                        connectionDict.Add($"{junctionBox.getKey()}{jb.getKey()}", newConnection);
                    }
                }
                else if (newConnection.distance < connections.OrderBy(con => con.distance).Last().distance)
                {
                    if (jb != junctionBox && !connections.Any((box => (box.start == jb && box.end == junctionBox) || (box.start == junctionBox && box.end == jb))))
                    {
                        Connection lastConnection = connections.OrderBy(con => con.distance).Last();
                        lastConnection.start = newConnection.start;
                        lastConnection.end = newConnection.end;
                        lastConnection.distance = lastConnection.calculateDistance();
                    }
                }
            }
        }
        this.connections = connections.OrderBy(c => c.distance).ToList();
        return this.connections;
    }

    private long checkCompleteCircuit(JunctionBox start, JunctionBox end)
    {
        long firstFullCircuit = 0;
        if (end.circuitSize() >= this.jbs.Count() || start.circuitSize() >= this.jbs.Count())
        {
            Console.WriteLine($"Full circuit made: {start.x}, {start.y}, {start.z} -> {end.x}, {end.y}, {end.z}");
            if (firstFullCircuit == 0)
            {
                Console.WriteLine($"Setting first full circuit to {start.x} * {end.x}");
                firstFullCircuit = start.x * end.x;
            }
        }

        foreach (var item in this.jbs)
        {
            item.resetVisited();
        }
        return firstFullCircuit;
    }

    public long makeConnections(bool checkComplete = false)
    {
        long firstFullCircuit = 0;
        foreach (Connection connection in this.connections.Take(this.requiredCount))
        {
            JunctionBox start = connection.start;
            JunctionBox end = connection.end;

            start.connect(end);
            end.connect(start);

           if(checkComplete){
                firstFullCircuit = checkCompleteCircuit(start, end);
                if (firstFullCircuit > 0) break;
            }
        }
        return firstFullCircuit;
    }
}

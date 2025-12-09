using System;

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

        foreach (JunctionBox junctionBox in this.jbs)
        {
            foreach (JunctionBox jb in this.jbs)
            {
                Connection newConnection = new Connection(junctionBox, jb);
                if (!connections.Any() || connections.Count() < this.requiredCount)
                {

                    if (jb != junctionBox && !connections.Any((box => (box.start == jb && box.end == junctionBox) || (box.start == junctionBox && box.end == jb))))
                    {
                        connections.Add(newConnection);
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

    public long makeConnections()
    {
        long firstFullCircuit = 0; //TODO
        foreach (Connection connection in this.connections.Take(this.requiredCount))
        {
            JunctionBox start = connection.start;
            JunctionBox end = connection.end;

            start.connect(end, true);
            end.connect(start, true);
        }
        return firstFullCircuit;
    }
}

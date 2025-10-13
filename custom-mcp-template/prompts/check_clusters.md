# Check Databricks Clusters

Show me all running compute clusters in this Databricks workspace.

Use the `list_clusters` tool with status="RUNNING" to get the current state of all active clusters. Display the results in a clear table format showing:
- Cluster name
- Cluster ID
- Current state
- Spark version
- Node type

If there are no running clusters, let me know and suggest checking terminated clusters.


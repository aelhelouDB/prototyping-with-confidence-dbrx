# Custom MCP Server on Databricks Apps

> **Workshop Version** - Based on [databrickslabs/mcp](https://github.com/databrickslabs/mcp) custom-server example with enhanced Databricks Apps deployment

This is a custom MCP (Model Context Protocol) server that runs on Databricks Apps and provides tools for interacting with Databricks SDK, SQL warehouses, and Unity Catalog.

## What's Inside

This template combines the simplicity of `databrickslabs/mcp` with production-ready deployment scripts for Databricks Apps:

- **Simple MCP Server** using `@mcp.tool()` decorator pattern
- **Databricks SDK Integration** with pre-built tools for clusters, warehouses, and DBFS
- **SQL Query Execution** against Databricks SQL warehouses  
- **Markdown-based Prompts** - Drop `.md` files in `prompts/` directory
- **Databricks Apps Deployment** with automated scripts
- **OAuth Proxy** for secure authentication
- **Hot-reload Development** with `watch.sh`

## Quick Start

### Prerequisites

- Databricks CLI installed and configured
- Python 3.11+
- `uv` (Python package manager)

### Local Development

```bash
# Install dependencies
uv sync

# Start the development server with hot-reload
./watch.sh

# Server will be available at:
# http://localhost:8000 - Homepage
# http://localhost:8000/mcp/ - MCP endpoint
```

### Deploy to Databricks Apps

```bash
# Deploy your MCP server
./deploy.sh

# Check deployment status and get your app URL
./app_status.sh
```

Your MCP server will be available at `https://your-app.databricksapps.com/mcp/`

## Creating Custom Tools

Add tools by using the `@mcp.tool()` decorator in `src/custom_server/app.py`:

```python
@mcp.tool()
def list_clusters(status: str = "RUNNING") -> dict:
    """List Databricks clusters by status."""
    w = get_workspace_client()
    clusters = []
    
    for cluster in w.clusters.list():
        if cluster.state and cluster.state.name == status:
            clusters.append({
                "id": cluster.cluster_id,
                "name": cluster.cluster_name,
                "state": cluster.state.name,
            })
    
    return {
        "success": True,
        "clusters": clusters,
        "count": len(clusters)
    }
```

**Tool Requirements:**
- Use the `@mcp.tool()` decorator
- Have a docstring (becomes the tool description)
- Return JSON-serializable data (dict, list, str, etc.)
- Accept only JSON-serializable parameters

## Creating Prompts

Drop markdown files in the `prompts/` directory:

```markdown
# Check System Status

Get information about the system and verify connectivity.

This prompt will check:
- System uptime
- Network connectivity  
- Databricks connection status
```

The prompt will automatically be available as `your-server:check_system` in MCP clients.

## Built-in Tools

### `health()`
Check server health and Databricks configuration status.

### `list_clusters(status: str = "RUNNING")`
List Databricks clusters filtered by status.

### `list_warehouses()`
List all SQL warehouses in your workspace.

### `execute_dbsql(query: str, warehouse_id: str, catalog: str, schema: str, limit: int)`
Execute SQL queries against Databricks SQL warehouses.

### `list_dbfs_files(path: str = "/")`
List files and directories in DBFS (Databricks File System).

## Environment Configuration

Create `.env.local` for local development:

```bash
DATABRICKS_HOST=https://your-workspace.cloud.databricks.com
DATABRICKS_TOKEN=your-token
DATABRICKS_SQL_WAREHOUSE_ID=your-warehouse-id
```

For deployed apps, these are set automatically by Databricks Apps.

## Project Structure

```
├── src/
│   └── custom_server/
│       ├── app.py              # Main MCP server with tools
│       ├── main.py             # Entry point for local dev
│       └── static/             # Static assets
├── prompts/                    # Markdown prompts (auto-loaded)
├── dba_mcp_proxy/             # OAuth proxy for Claude CLI
├── claude_scripts/            # Testing and debugging tools
├── deploy.sh                  # Deploy to Databricks Apps
├── app_status.sh             # Check app deployment status
├── watch.sh                  # Hot-reload development server
├── config.yaml               # Server configuration
└── pyproject.toml            # Python dependencies
```

## Testing Your MCP Server

### Command Line Tests

```bash
# Test local server (requires ./watch.sh to be running)
./claude_scripts/test_local_mcp_curl.sh

# Test deployed server (requires Databricks auth)
./claude_scripts/test_remote_mcp_curl.sh
```

### Interactive Web UI

```bash
# Launch MCP Inspector for visual testing
./claude_scripts/inspect_local_mcp.sh
```

## Connecting to IDEs

### Cursor IDE

Add to `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "my-databricks-mcp": {
      "command": "uvx",
      "args": [
        "--from", "git+https://github.com/YOUR-USERNAME/YOUR-REPO.git",
        "dba-mcp-proxy",
        "--databricks-host", "https://your-workspace.cloud.databricks.com",
        "--databricks-app-url", "https://your-app.databricksapps.com"
      ]
    }
  }
}
```

### Claude Code

```bash
# Add MCP server to Claude
claude mcp add my-databricks-mcp --scope local -- \
  uvx --from git+https://github.com/YOUR-USERNAME/YOUR-REPO.git dba-mcp-proxy \
  --databricks-host https://your-workspace.cloud.databricks.com \
  --databricks-app-url https://your-app.databricksapps.com
```

## Workshop Scripts

- **`setup_workshop_mcp.sh`** - Workshop-specific setup (auto-run by main setup.sh)
- **`fix.sh`** - Auto-fix common code issues
- **`run_app_local.sh`** - Alternative local development script
- **`run-mcp-proxy.sh`** - Run MCP proxy standalone

## Troubleshooting

### Authentication Issues

```bash
# Refresh Databricks credentials
databricks auth login --host https://your-workspace.cloud.databricks.com

# Test authentication
databricks current-user me
```

### Connection Problems

```bash
# Test MCP server directly
curl -X GET https://your-app.databricksapps.com/mcp/

# Check app status
./app_status.sh

# View server logs
curl https://your-app.databricksapps.com/logz
```

### Development Issues

```bash
# Restart development server
./watch.sh

# Run comprehensive tests
./claude_scripts/test_local_mcp_curl.sh

# Interactive debugging
./claude_scripts/inspect_local_mcp.sh
```

## Differences from databrickslabs/mcp

This workshop template is based on `databrickslabs/mcp` custom-server but includes:

✅ **Pre-configured Databricks SDK tools** (clusters, warehouses, SQL, DBFS)  
✅ **Automated Databricks Apps deployment** (deploy.sh, app_status.sh)  
✅ **OAuth proxy for Claude CLI** (dba_mcp_proxy/)  
✅ **Workshop setup scripts** (setup_workshop_mcp.sh)  
✅ **Testing and debugging tools** (claude_scripts/)  
✅ **Example prompts** for common Databricks operations  

## Alternative: databricks-solutions Repository

If you're using **Claude Code** or **Cursor** and want enhanced IDE integration, check out:

**[databricks-solutions/custom-mcp-databricks-app](https://github.com/databricks-solutions/custom-mcp-databricks-app)**

Features:
- Enhanced Claude Code integration
- `.claude/commands` directory support  
- FastMCP framework with routers
- Built-in MCP inspector
- More production-ready patterns

## Resources

- [databrickslabs/mcp Repository](https://github.com/databrickslabs/mcp) - Official Databricks MCP examples
- [FastMCP Documentation](https://fastmcp.org/) - MCP server framework docs
- [Model Context Protocol](https://modelcontextprotocol.io/) - MCP specification
- [Databricks SDK for Python](https://docs.databricks.com/dev-tools/sdk-python.html) - SDK documentation

## License

See [LICENSE.md](LICENSE.md)

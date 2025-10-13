import os
from pathlib import Path
from mcp.server.fastmcp import FastMCP
from fastapi import FastAPI
from fastapi.responses import FileResponse
from databricks.sdk import WorkspaceClient

STATIC_DIR = Path(__file__).parent / "static"

# Create an MCP server
mcp = FastMCP("Custom MCP Server on Databricks Apps")


# ============================================================================
# EXAMPLE TOOLS (Simple demos)
# ============================================================================

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"


# ============================================================================
# DATABRICKS SDK TOOLS
# ============================================================================

def get_workspace_client() -> WorkspaceClient:
    """Get an authenticated Databricks workspace client.
    
    This uses environment variables or Databricks Apps authentication.
    In Databricks Apps, authentication is handled automatically!
    """
    return WorkspaceClient(
        host=os.environ.get('DATABRICKS_HOST'),
        token=os.environ.get('DATABRICKS_TOKEN')
    )


@mcp.tool()
def list_clusters(status: str = "RUNNING") -> dict:
    """List Databricks compute clusters filtered by status.
    
    Args:
        status: Filter by cluster state (RUNNING, TERMINATED, PENDING, etc.)
    
    Returns:
        Dictionary with cluster information including ID, name, state, and specs
    
    Example:
        list_clusters("RUNNING") -> Shows all currently running clusters
    """
    try:
        w = get_workspace_client()
        clusters = []
        
        for cluster in w.clusters.list():
            if cluster.state and cluster.state.name == status:
                clusters.append({
                    "id": cluster.cluster_id,
                    "name": cluster.cluster_name,
                    "state": cluster.state.name,
                    "spark_version": cluster.spark_version,
                    "node_type": cluster.node_type_id,
                })
        
        return {
            "success": True,
            "clusters": clusters,
            "count": len(clusters),
            "message": f"Found {len(clusters)} cluster(s) with status {status}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool()
def list_warehouses() -> dict:
    """List all SQL warehouses in the Databricks workspace.
    
    Returns:
        Dictionary with warehouse information including ID, name, state, size, and type
    
    Example:
        list_warehouses() -> Shows all SQL warehouses in your workspace
    """
    try:
        w = get_workspace_client()
        warehouses = []
        
        for warehouse in w.warehouses.list():
            warehouses.append({
                'id': warehouse.id,
                'name': warehouse.name,
                'state': warehouse.state.value if warehouse.state else 'UNKNOWN',
                'size': warehouse.cluster_size,
                'type': warehouse.warehouse_type.value if warehouse.warehouse_type else 'UNKNOWN',
            })
        
        return {
            'success': True,
            'warehouses': warehouses,
            'count': len(warehouses),
            'message': f'Found {len(warehouses)} SQL warehouse(s)'
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}


@mcp.tool()
def execute_dbsql(
    query: str,
    warehouse_id: str = None,
    limit: int = 100,
) -> dict:
    """Execute a SQL query on a Databricks SQL warehouse.
    
    Args:
        query: SQL query to execute (e.g., "SELECT * FROM main.default.sales LIMIT 10")
        warehouse_id: SQL warehouse ID (uses DATABRICKS_SQL_WAREHOUSE_ID env var if not provided)
        limit: Maximum rows to return (default: 100)
    
    Returns:
        Dictionary with query results including columns and rows
    
    Example:
        execute_dbsql("SHOW DATABASES", warehouse_id="abc123def456")
    """
    try:
        w = get_workspace_client()
        
        # Get warehouse ID from parameter or environment variable
        warehouse_id = warehouse_id or os.environ.get('DATABRICKS_SQL_WAREHOUSE_ID')
        if not warehouse_id:
            return {
                'success': False,
                'error': 'No SQL warehouse ID provided. Set DATABRICKS_SQL_WAREHOUSE_ID environment variable or pass warehouse_id parameter.'
            }
        
        # Execute the query
        result = w.statement_execution.execute_statement(
            warehouse_id=warehouse_id,
            statement=query,
            wait_timeout='30s'
        )
        
        # Process results
        if result.result and result.result.data_array:
            columns = [col.name for col in result.manifest.schema.columns]
            data = []
            
            for row in result.result.data_array[:limit]:
                row_dict = {}
                for i, col in enumerate(columns):
                    row_dict[col] = row[i]
                data.append(row_dict)
            
            return {
                'success': True,
                'data': {'columns': columns, 'rows': data},
                'row_count': len(data)
            }
        else:
            return {
                'success': True,
                'data': {'message': 'Query executed successfully with no results'},
                'row_count': 0
            }
    except Exception as e:
        return {'success': False, 'error': str(e)}


# ============================================================================
# LOAD PROMPTS FROM MARKDOWN FILES
# ============================================================================

def load_prompts_from_directory():
    """Load all markdown files from prompts/ directory as MCP prompts.
    
    Each .md file in prompts/ becomes a reusable prompt that AI assistants can use.
    The filename (without .md) becomes the prompt name.
    """
    # Look for prompts directory at the project root
    prompts_dir = Path(__file__).parent.parent.parent / 'prompts'
    
    if not prompts_dir.exists():
        print(f"⚠️  Prompts directory not found at {prompts_dir}")
        return
    
    prompt_count = 0
    for prompt_file in prompts_dir.glob('*.md'):
        try:
            content = prompt_file.read_text()
            prompt_name = prompt_file.stem  # filename without .md extension
            
            # Extract description from first line (if it starts with #)
            lines = content.strip().split('\n')
            description = lines[0].lstrip('#').strip() if lines and lines[0].startswith('#') else f"Prompt: {prompt_name}"
            
            # Register the prompt with MCP
            # We use a closure to capture the content for each prompt
            def create_prompt_handler(prompt_content):
                @mcp.prompt(name=prompt_name, description=description)
                def prompt_handler():
                    return prompt_content
                return prompt_handler
            
            create_prompt_handler(content)
            prompt_count += 1
            print(f"✅ Loaded prompt: {prompt_name}")
            
        except Exception as e:
            print(f"⚠️  Failed to load prompt from {prompt_file}: {e}")
    
    print(f"📋 Loaded {prompt_count} prompt(s) from {prompts_dir}")

# Load prompts at startup
load_prompts_from_directory()


mcp_app = mcp.streamable_http_app()


app = FastAPI(
    lifespan=lambda _: mcp.session_manager.run(),
)


@app.get("/", include_in_schema=False)
async def serve_index():
    return FileResponse(STATIC_DIR / "index.html")


app.mount("/", mcp_app)

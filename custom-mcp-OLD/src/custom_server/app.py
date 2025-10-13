"""Custom MCP Server for Databricks Apps - Simplified Version

This is a simplified MCP server based on databrickslabs/mcp custom-server example,
enhanced with Databricks SDK integration for workshop participants.
"""

import os
from pathlib import Path
import yaml

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from mcp.server.fastmcp import FastMCP
from databricks.sdk import WorkspaceClient

# Determine static directory
STATIC_DIR = Path(__file__).parent / "static"

# Load configuration from config.yaml if it exists
def load_config() -> dict:
    """Load configuration from config.yaml."""
    # Check multiple possible locations for config.yaml
    possible_paths = [
        Path('config.yaml'),
        Path(__file__).parent.parent.parent / 'config.yaml',
    ]
    
    for config_path in possible_paths:
        if config_path.exists():
            with open(config_path, 'r') as f:
                return yaml.safe_load(f) or {}
    return {}

config = load_config()
servername = config.get('servername', 'databricks-mcp-workshop')

# Create an MCP server
mcp = FastMCP(servername)

# ============================================================================
# DATABRICKS SDK HELPER
# ============================================================================

def get_workspace_client() -> WorkspaceClient:
    """Get authenticated Databricks workspace client."""
    return WorkspaceClient(
        host=os.environ.get('DATABRICKS_HOST'),
        token=os.environ.get('DATABRICKS_TOKEN')
    )


# ============================================================================
# MCP TOOLS - DATABRICKS OPERATIONS
# ============================================================================

@mcp.tool()
def health() -> dict:
    """Check the health of the MCP server and Databricks connection.
    
    Returns:
        dict: Health status including service name and configuration status
    """
    return {
        'status': 'healthy',
        'service': servername,
        'databricks_configured': bool(os.environ.get('DATABRICKS_HOST')),
    }


@mcp.tool()
def list_clusters(status: str = "RUNNING") -> dict:
    """List Databricks clusters by status.
    
    Args:
        status: Filter clusters by state (RUNNING, TERMINATED, etc.)
    
    Returns:
        dict: List of clusters matching the status filter
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
        dict: List of SQL warehouses with their details
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
    catalog: str = None,
    schema: str = None,
    limit: int = 100,
) -> dict:
    """Execute a SQL query on Databricks SQL warehouse.
    
    Args:
        query: SQL query to execute
        warehouse_id: SQL warehouse ID (optional, uses env var if not provided)
        catalog: Catalog to use (optional)
        schema: Schema to use (optional)
        limit: Maximum number of rows to return (default: 100)
    
    Returns:
        dict: Query results with columns and rows, or error message
    """
    try:
        w = get_workspace_client()
        
        # Get warehouse ID from parameter or environment
        warehouse_id = warehouse_id or os.environ.get('DATABRICKS_SQL_WAREHOUSE_ID')
        if not warehouse_id:
            return {
                'success': False,
                'error': 'No SQL warehouse ID provided. Set DATABRICKS_SQL_WAREHOUSE_ID or pass warehouse_id.'
            }
        
        # Build the full query with catalog/schema if provided
        full_query = query
        if catalog and schema:
            full_query = f'USE CATALOG {catalog}; USE SCHEMA {schema}; {query}'
        
        # Execute the query
        result = w.statement_execution.execute_statement(
            warehouse_id=warehouse_id,
            statement=full_query,
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


@mcp.tool()
def list_dbfs_files(path: str = '/') -> dict:
    """List files and directories in DBFS (Databricks File System).
    
    Args:
        path: DBFS path to list (default: '/')
    
    Returns:
        dict: File listings with metadata or error message
    """
    try:
        w = get_workspace_client()
        files = []
        
        for file_info in w.dbfs.list(path):
            files.append({
                'path': file_info.path,
                'is_dir': file_info.is_dir,
                'size': file_info.file_size if not file_info.is_dir else None,
                'modification_time': file_info.modification_time,
            })
        
        return {
            'success': True,
            'path': path,
            'files': files,
            'count': len(files),
            'message': f'Listed {len(files)} item(s) in {path}'
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}


# ============================================================================
# LOAD PROMPTS FROM MARKDOWN FILES
# ============================================================================

def load_prompts_from_dir():
    """Load all markdown files from prompts/ directory as MCP prompts."""
    prompts_dir = Path(__file__).parent.parent.parent / 'prompts'
    
    if not prompts_dir.exists():
        return
    
    for prompt_file in prompts_dir.glob('*.md'):
        try:
            content = prompt_file.read_text()
            prompt_name = prompt_file.stem
            
            # Extract description from first line (if it starts with #)
            lines = content.strip().split('\n')
            description = lines[0].lstrip('#').strip() if lines and lines[0].startswith('#') else f"Prompt: {prompt_name}"
            
            # Register the prompt
            @mcp.prompt(name=prompt_name, description=description)
            def create_prompt(content=content):
                return content
                
        except Exception as e:
            print(f"Warning: Could not load prompt from {prompt_file}: {e}")

# Load prompts at startup
load_prompts_from_dir()


# ============================================================================
# FASTAPI APPLICATION SETUP
# ============================================================================

# Create MCP ASGI app with streamable HTTP transport
mcp_app = mcp.streamable_http_app()

# Create FastAPI application with MCP lifespan
app = FastAPI(
    title="Databricks MCP Workshop Server",
    description="Custom MCP server for Databricks workshop with SQL and SDK tools",
    version="0.2.0",
    lifespan=lambda _: mcp.session_manager.run(),
)

# Add CORS middleware for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve index page at root
@app.get("/", include_in_schema=False)
async def serve_index():
    """Serve the static index page."""
    if STATIC_DIR.exists() and (STATIC_DIR / "index.html").exists():
        return FileResponse(STATIC_DIR / "index.html")
    return {"message": "MCP Server is running", "server": servername}

# Mount MCP app at /mcp/
app.mount("/mcp", mcp_app)

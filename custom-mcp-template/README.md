# Example - custom MCP server on Databricks Apps

This example shows how to create and launch a custom agent on Databricks Apps.
Please note that this example doesn't use any Databricks SDK, and is independent of the `mcp` package in the root dir of this repo.

## Prerequisites

- Databricks CLI installed and configured
- `uv`

## Local development

- run `uv` sync:

```bash
uv sync
```

- start the server locally. Changes will trigger a reload:

```bash
uvicorn custom_server.app:app --reload
```

## Deploying a custom MCP server on Databricks Apps (Workshop)

For the MCP Workshop, deployment is streamlined using the `databricks bundle` CLI.

### Prerequisites

Make sure you've completed the initial workshop setup by running `./setup.sh` from the root directory.
This creates your workshop catalog and configures authentication.

### Deployment Steps

1. **Navigate to the custom-mcp-template directory:**
   ```bash
   cd custom-mcp-template
   ```

2. **Build the Python wheel:**
   ```bash
   uv build --wheel
   ```
   This packages your MCP server and creates the `.build/` directory with all dependencies.

3. **Deploy to Databricks Apps:**
   ```bash
   source ../.env.local && databricks bundle deploy
   ```
   This automatically uses your participant prefix from setup and creates: `mcp-custom-server-<your-prefix>`

4. **Verify deployment:**
   ```bash
   databricks apps list | grep mcp-custom-server
   ```

### Important Notes

- **App naming:** The app name MUST start with `mcp-` to appear in the Databricks MCP playground
- **Automatic prefix:** The bundle automatically uses your `PARTICIPANT_PREFIX` from `.env.local`
- **Unique naming:** Each participant gets a unique app name to avoid conflicts in shared workspaces
- **Updates:** Just re-run `uv build --wheel` and `source ../.env.local && databricks bundle deploy` to update

### Troubleshooting

**If you see "App does not exist or is deleted" error:**
```bash
# Clear any stale state
rm -rf .databricks

# Then re-deploy
uv build --wheel
source ../.env.local && databricks bundle deploy
```

**To check app status:**
```bash
./app_status.sh
```

**To view logs:**
Visit Databricks workspace → Apps → your app → Logs

## Connecting to the MCP server

[//]: # (TODO: once official Databricks docs for using MCP servers in agents are live, replace this with a link)
[//]: # (to that section)

To connect to the MCP server, use the `Streamable HTTP` transport with the following URL:

```
https://your-app-url.usually.ends.with.databricksapps.com/mcp/
```

For authentication, you can use the `Bearer` token from your Databricks profile.
You can get the token by running the following command:

```bash
databricks auth token -p <name-of-your-profile>
```

Please note that the URL should end with `/mcp/` (including the trailing slash), as this is required for the server to work correctly.

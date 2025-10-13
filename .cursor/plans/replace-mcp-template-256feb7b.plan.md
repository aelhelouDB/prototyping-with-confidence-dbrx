<!-- 256feb7b-ab8e-4623-8aa9-98c7bdb8e306 9a83e3c6-8e9c-45a6-9b02-d2efef2af496 -->
# Replace MCP Template with databrickslabs/mcp

## Overview

Replace the current `custom-mcp-template/` with the simpler databrickslabs/mcp custom-server example, add Databricks Apps deployment scripts, and update all workshop materials to use the new structure.

## Phase 1: Fetch and Prepare New Template

### 1.1 Download databrickslabs/mcp custom-server

- Clone databrickslabs/mcp repository temporarily
- Copy `examples/custom-server/` contents to a staging area
- Review the structure and identify what needs to be added for Databricks Apps deployment

### 1.2 Add Databricks Apps Deployment Scripts

From the existing custom-mcp-template/, port these deployment files to work with databrickslabs structure:

- `deploy.sh` - Databricks Apps deployment script
- `app.yaml` - App configuration
- `app_status.sh` - Check deployment status
- `databricks-mcp-launcher.sh` - App launcher script
- Keep the existing `dba_mcp_proxy/` directory for OAuth proxy functionality

### 1.3 Preserve Workshop-Specific Files

Keep these from current template:

- `setup_workshop_mcp.sh` - Workshop initialization
- `config.yaml` - Server configuration
- `prompts/` directory structure (but simplify the prompts)
- `claude_scripts/` - Testing tools
- `docs/` - Documentation

## Phase 2: Update Core Configuration

### 2.1 Update databricks.yml Bundle

Modify `/Users/jai.behl/Documents/00_ActiveWork/Projects/mcp-workshop/databricks.yml`:

- Keep the existing `mcp_server_app` resource definition
- Update `source_code_path` reference if needed
- Ensure bundle variables work with new template structure

### 2.2 Update setup.sh

Modify `/Users/jai.behl/Documents/00_ActiveWork/Projects/mcp-workshop/setup.sh`:

- Line 569-635: Update the MCP template setup section
- Ensure it works with the new databrickslabs-based structure
- Keep all authentication and deployment logic intact

## Phase 3: Update Workshop Documentation

### 3.1 Update Custom MCP Page

Modify `/Users/jai.behl/Documents/00_ActiveWork/Projects/mcp-workshop/frontend/src/app/custom-mcp/page.tsx`:

**Key Changes:**

- Lines 27-31: Update what setup.sh creates (simpler structure reference)
- Lines 34-58: Keep IDE requirements section (Cursor/Claude Code)
- Lines 117-197: Simplify deployment instructions using databrickslabs patterns
- Lines 200-280: Update prompts section to show simpler markdown-based prompts
- Add new section explaining tool creation with `@mcp.tool()` decorator pattern from databrickslabs
- Lines 754-763: Update repository links to reference both:
- Primary: databrickslabs/mcp (simpler, recommended)
- Alternative: databricks-solutions/custom-mcp-databricks-app (for Claude Code/Cursor users)

### 3.2 Update Main Workshop README

Modify `/Users/jai.behl/Documents/00_ActiveWork/Projects/mcp-workshop/README.md`:

- Update architecture description
- Reference databrickslabs/mcp as primary approach
- Add section: "For Claude Code/Cursor Users" pointing to databricks-solutions repo
- Update setup instructions

### 3.3 Update Custom MCP Template README

Create new `/Users/jai.behl/Documents/00_ActiveWork/Projects/mcp-workshop/custom-mcp-template/README.md`:

- Based on databrickslabs/mcp documentation
- Add Databricks Apps deployment section
- Include reference to databricks-solutions repo for IDE-specific features
- Emphasize simpler tool creation patterns

## Phase 4: Update Tool Creation Examples

### 4.1 Simplify Server Code

Update `custom-mcp-template/server/app.py` to follow databrickslabs patterns:

- Use simpler `@mcp.tool()` decorator pattern instead of `@mcp_server.tool`
- Show clear example of Databricks SDK integration
- Include the list_clusters example from databrickslabs documentation
- Keep SQL warehouse integration examples

### 4.2 Simplify Prompts

Update `custom-mcp-template/prompts/`:

- Keep existing prompts but simplify them
- Add clear examples showing markdown-only prompts
- Remove complex function-based prompts (keep those as reference in docs)

## Phase 5: Positioning and References

### 5.1 Add IDE-Specific Guidance

Create new section in workshop documentation:

**"Choosing Your MCP Approach"**

- **For general use / learning**: Use this workshop's databrickslabs-based template (simpler, focused)
- **For Claude Code users**: See [databricks-solutions/custom-mcp-databricks-app](https://github.com/databricks-solutions/custom-mcp-databricks-app) for:
- Enhanced Claude Code integration
- `.claude/commands` directory support
- Additional IDE-specific features
- FastMCP framework patterns

### 5.2 Update Other Workshop Pages

Check and update references in:

- `/Users/jai.behl/Documents/00_ActiveWork/Projects/mcp-workshop/frontend/src/app/page.tsx`
- `/Users/jai.behl/Documents/00_ActiveWork/Projects/mcp-workshop/frontend/src/app/managed-mcp/page.tsx`
- `/Users/jai.behl/Documents/00_ActiveWork/Projects/mcp-workshop/frontend/src/app/external-mcp/page.tsx`
- `/Users/jai.behl/Documents/00_ActiveWork/Projects/mcp-workshop/frontend/src/app/local-ide/page.tsx`

## Phase 6: Testing and Verification

### 6.1 Test Setup Flow

- Run `./setup.sh` with new template
- Verify MCP server deploys correctly
- Test tool creation with new patterns

### 6.2 Test Deployment

- Test `./deploy.sh` works with new structure
- Verify `./app_status.sh` reports correctly
- Test MCP proxy connection

### 6.3 Update Testing Scripts

Verify `claude_scripts/` testing tools work with new structure

## Key Files to Modify

1. **Replace entirely**: `custom-mcp-template/` directory structure
2. **Update significantly**: 

- `frontend/src/app/custom-mcp/page.tsx` (workshop instructions)
- `setup.sh` (lines 569-635)
- `README.md` (main workshop readme)

3. **Add new**:

- Documentation section explaining both approaches
- Examples showing databrickslabs tool patterns

## Benefits Communicated

**databrickslabs/mcp (Primary)**:

- Simpler structure and setup
- Focus on tool creation patterns
- Officially supported by Databricks
- Great for learning MCP fundamentals

**databricks-solutions repo (Alternative)**:

- Enhanced IDE integration (Claude Code, Cursor)
- More production-ready patterns
- Additional features like FastMCP framework
- Better for teams already using Claude Code

## Success Criteria

- Workshop participants can create custom tools using simpler databrickslabs patterns
- Deployment to Databricks Apps still works seamlessly
- Documentation clearly explains when to use each approach
- All existing workshop functionality preserved

### To-dos

- [ ] Clone databrickslabs/mcp repo and extract custom-server example structure
- [ ] Backup current custom-mcp-template directory
- [ ] Add Databricks Apps deployment scripts (deploy.sh, app.yaml, etc.) to databrickslabs structure
- [ ] Update server/app.py to use databrickslabs tool patterns with Databricks SDK examples
- [ ] Modify setup.sh (lines 569-635) to work with new template structure
- [ ] Update frontend/src/app/custom-mcp/page.tsx with new instructions and repo references
- [ ] Update main README.md and create new custom-mcp-template/README.md
- [ ] Add documentation explaining when to use databrickslabs vs databricks-solutions repos
- [ ] Test ./setup.sh with new template structure
- [ ] Test deploy.sh and app_status.sh work correctly with new structure
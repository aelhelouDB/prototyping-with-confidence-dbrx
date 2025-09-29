# Databricks MCP Workshop

Interactive workshop for learning Databricks Model Context Protocol (MCP) with hands-on examples covering managed servers, external integrations, local IDE setup, and custom server development.

## 🎓 Workshop Participant Setup

**For workshop participants** - Get your own isolated environment with one command:

```bash
git clone https://github.com/jai-behl/mcp-workshop.git
cd mcp-workshop
./setup.sh
```

This interactive setup creates your personal workshop environment:
- 🏗️ **Your own Unity Catalog** with sample data
- 🚀 **Personal Databricks App** instance
- ⚙️ **Custom MCP server** configuration
- 💻 **Local development** environment
- 🔐 **Secure authentication** setup

Each participant gets isolated resources (e.g., `mcp_workshop_john_doe`) - no conflicts, no shared data issues!

👉 **[See detailed setup guide →](./WORKSHOP_SETUP.md)**

---
### Access the Workshop

After deployment, find your app URL in the Databricks workspace:

1. Go to **Apps** in your Databricks workspace
2. Click on **mcp-workshop-app**
3. Click **Open App** to start the workshop

## 📚 Workshop Content

### Section 1: Managed MCP Servers (45 min)
Learn to use Databricks-managed MCP servers with:
- Unity Catalog functions and permissions
- Vector Search for RAG applications  
- Genie Spaces for natural language SQL
- Automated vs Interactive modes

### Section 2: Local IDE Integration (30 min)
Connect your development environment:
- Cursor IDE configuration
- Claude Desktop setup
- VS Code with MCP extensions
- OAuth and PAT authentication

### Section 3: External MCP Servers (40 min)
Integrate third-party services:
- Unity Catalog connections
- GitHub, Atlassian, Slack integrations
- Custom API connections
- Proxy authentication and security

### Section 4: Custom MCP Servers (60 min)
Build and deploy your own:
- MCP server development patterns
- Business logic implementation
- **Databricks Apps deployment**
- Tools, resources, and prompts
- End-to-end testing

## 🔐 Authentication Model

This workshop uses **Databricks Apps built-in authentication** exclusively:

- **User Authorization**: Your access token is automatically forwarded via `x-forwarded-access-token` header
- **App Authorization**: Service principal credentials via `DATABRICKS_CLIENT_ID` and `DATABRICKS_CLIENT_SECRET` environment variables
- **Unified Permissions**: All operations respect your existing Unity Catalog permissions
- **Zero Setup**: No manual token management or OAuth flows required

[Learn more about Databricks Apps authentication →](https://docs.databricks.com/aws/en/dev-tools/databricks-apps/auth)

## 🛠️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 Databricks Workspace                        │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐    ┌──────────────────────────────────┐ │
│  │  Workshop App   │    │         Unity Catalog           │ │
│  │  (Next.js)      │◄──►│  - mcp_workshop catalog         │ │
│  │                 │    │  - Sample data & schemas        │ │
│  │  Auto Auth:     │    │  - Vector Search indexes       │ │
│  │  • User token   │    │  - Genie Spaces                │ │
│  │  • Service      │    └──────────────────────────────────┘ │
│  │    principal    │                                        │
│  └─────────────────┘    ┌──────────────────────────────────┐ │
│                         │       MCP Integrations          │ │
│  ┌─────────────────┐    │  - Managed MCP servers          │ │
│  │  Setup Jobs     │    │  - External connections         │ │
│  │  - Catalog      │    │  - Custom MCP apps              │ │
│  │  - Sample data  │    └──────────────────────────────────┘ │
│  │  - Vector index │                                        │
│  └─────────────────┘                                        │
└─────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
mcp-workshop/
├── databricks.yml              # Bundle configuration
├── app/                        # Next.js workshop application
│   ├── src/
│   │   ├── app/               # App router pages
│   │   ├── components/        # React components
│   │   ├── lib/              # Utilities and auth
│   │   └── types/            # TypeScript definitions
│   ├── package.json
│   └── Dockerfile            # Container configuration
├── setup/                     # Workshop setup notebooks
│   ├── create_workshop_catalog.py
│   ├── setup_sample_data.py
│   └── create_vector_search_index.py
└── resources/                 # Additional bundle resources
```

## 🎯 Learning Objectives

By the end of this workshop, you'll be able to:

- ✅ Use Databricks managed MCP servers in your applications
- ✅ Connect local IDEs to Databricks MCP resources  
- ✅ Integrate external MCP servers via Unity Catalog connections
- ✅ Build and deploy custom MCP servers as Databricks Apps
- ✅ Implement proper authentication and authorization patterns
- ✅ Apply MCP best practices for production deployments

## 🔧 Development

To run the workshop locally for development:

```bash
cd app
npm install
npm run dev
```

The app will run at `http://localhost:3000` with mock authentication for development.

## 📝 Customization

### Adding New Workshop Sections

1. Update `src/lib/workshop-config.ts` with new section definitions
2. Create component files in `src/components/workshop/sections/`
3. Add any required setup jobs to `databricks.yml`
4. Deploy with `databricks bundle deploy`

### Modifying Authentication Scopes

Update the `user_authorization.scopes` in `databricks.yml`:

```yaml
user_authorization:
  enabled: true
  scopes:
    - "sql"                    # SQL warehouse access
    - "files.files"           # File operations  
    - "dashboards.genie"      # Genie Spaces (add if needed)
    - "your-custom-scope"     # Additional scopes
```

## 🧹 Workshop Management (For Instructors)

### Cleanup After Workshop

The workshop creates user-specific resources that should be cleaned up afterwards:

```bash
# List all workshop participants
./cleanup_workshop.sh --list

# Clean up specific participant
./cleanup_workshop.sh --participant john_doe

# Clean up ALL workshop resources (⚠️ DESTRUCTIVE)
./cleanup_workshop.sh --all
```

### Monitor Workshop Usage

```bash
# View participant resources
./cleanup_workshop.sh --list

# Check catalog sizes
databricks sql query "SELECT catalog_name, SIZE_GB FROM information_schema.catalog_storage WHERE catalog_name LIKE 'mcp_workshop_%'"

# List workshop apps
databricks apps list | grep "mcp-workshop-app-"
```

### Best Practices for Instructors

- **Pre-workshop**: Test `./setup.sh` in your workspace
- **During workshop**: Monitor participant progress with `--list`
- **Post-workshop**: Run cleanup within 24 hours to avoid costs
- **Large workshops**: Consider pre-creating some shared resources

## 🆘 Troubleshooting

### Common Issues

**App won't start**: Check that all required environment variables are set in the bundle configuration.

**Authentication errors**: Ensure user authorization is enabled and required scopes are configured.

**Resource access denied**: Verify Unity Catalog permissions for the workshop catalog and resources.

**Health check failing**: Check that the app is listening on port 3000 and `/api/health` endpoint responds.

**Setup script fails**: Ensure Databricks CLI is configured and you have catalog creation permissions.

### Getting Help

- Check the app logs in Databricks workspace
- Verify bundle deployment with `databricks bundle validate`
- Review [Databricks Apps documentation](https://docs.databricks.com/aws/en/dev-tools/databricks-apps/)
- For participant setup issues, see [WORKSHOP_SETUP.md](./WORKSHOP_SETUP.md)
- Submit issues to the workshop repository

## 📄 License

This workshop is provided under the Apache License 2.0. See LICENSE file for details.

---

**Ready to learn MCP?** Deploy the workshop and start exploring! 🚀

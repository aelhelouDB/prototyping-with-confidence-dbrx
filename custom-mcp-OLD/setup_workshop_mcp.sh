#!/bin/bash

# Workshop MCP Server Setup Script
# This script configures the MCP server template for workshop participants

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}✅${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ️${NC}  $1"
}

print_progress() {
    echo -e "${YELLOW}🔧${NC} $1"
}

# Check if required parameters are provided
if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ]; then
    echo "Usage: $0 <participant_prefix> <mcp_server_name> <databricks_host>"
    echo "Example: $0 jai databricks-mcp-jai https://workspace.cloud.databricks.com"
    exit 1
fi

PARTICIPANT_PREFIX="$1"
MCP_SERVER_NAME="$2"
DATABRICKS_HOST="$3"

print_info "Configuring custom MCP server for participant: ${PARTICIPANT_PREFIX}"

# Update config.yaml with participant-specific server name
print_progress "Updating MCP server configuration..."
cat > config.yaml << EOF
# MCP Server Configuration for ${PARTICIPANT_PREFIX}
servername: ${MCP_SERVER_NAME}
EOF

# Create participant-specific .env.local
print_progress "Creating MCP server environment configuration..."
cat > .env.local << EOF
# Workshop MCP Server Configuration for ${PARTICIPANT_PREFIX}
# Generated on $(date)

# Databricks Configuration
DATABRICKS_HOST=${DATABRICKS_HOST}
DATABRICKS_AUTH_TYPE=pat

# MCP Server Configuration
SERVER_NAME=${MCP_SERVER_NAME}
EOF

# Install dependencies using the existing setup
print_progress "Installing MCP server dependencies..."
if [ -f "setup.sh" ]; then
    # Run the existing setup but skip interactive parts
    export SKIP_INTERACTIVE=true
    ./setup.sh --auto-close /tmp/setup_complete.tmp &

    # Wait for setup to complete or timeout
    timeout=300  # 5 minutes
    count=0
    while [ ! -f "/tmp/setup_complete.tmp" ] && [ $count -lt $timeout ]; do
        sleep 1
        ((count++))
    done

    if [ -f "/tmp/setup_complete.tmp" ]; then
        rm /tmp/setup_complete.tmp
        print_status "MCP server dependencies installed"
    else
        print_info "Setup took longer than expected, continuing..."
    fi
else
    print_info "No setup.sh found, installing basic dependencies..."

    # Install UV if not present
    if ! command -v uv &> /dev/null; then
        print_progress "Installing uv..."
        curl -LsSf https://astral.sh/uv/install.sh | sh
        source ~/.bashrc 2>/dev/null || source ~/.zshrc 2>/dev/null || true
    fi

    # Install Python dependencies
    if [ -f "pyproject.toml" ]; then
        print_progress "Installing Python dependencies..."
        uv sync --dev 2>/dev/null || print_info "Some dependencies may need manual installation"
    fi

    # Install frontend dependencies
    if [ -d "client" ] && command -v bun &> /dev/null; then
        print_progress "Installing frontend dependencies..."
        cd client
        bun install 2>/dev/null || print_info "Frontend dependencies may need manual installation"
        cd ..
    fi
fi

print_status "Custom MCP server configured for ${PARTICIPANT_PREFIX}"
print_info "Server name: ${MCP_SERVER_NAME}"
print_info "Configuration saved to .env.local and config.yaml"

echo ""
echo "🎯 Next steps for ${PARTICIPANT_PREFIX}:"
echo "  1. Modify tools in server/tools.py"
echo "  2. Test locally with: ./watch.sh"
echo "  3. Deploy with: ./deploy.sh"
echo "  4. Add to Claude CLI for testing"
echo ""
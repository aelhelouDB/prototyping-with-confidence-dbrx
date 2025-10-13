#!/bin/bash

# Deploy MCP Server to Databricks Apps
# This script builds and deploys your custom MCP server

set -e  # Exit on error

echo "🚀 Deploying Custom MCP Server to Databricks Apps"
echo "=================================================="
echo ""

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ Error: 'uv' is not installed"
    echo "Install it with: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Check if databricks CLI is installed
if ! command -v databricks &> /dev/null; then
    echo "❌ Error: Databricks CLI is not installed"
    echo "Install from: https://docs.databricks.com/dev-tools/cli/install.html"
    exit 1
fi

# Check authentication
echo "🔐 Checking Databricks authentication..."
if ! databricks current-user me &> /dev/null; then
    echo "❌ Not authenticated with Databricks"
    echo "Run: databricks auth login"
    exit 1
fi

USER_EMAIL=$(databricks current-user me | grep -o '"userName": "[^"]*"' | cut -d'"' -f4)
echo "✅ Authenticated as: $USER_EMAIL"
echo ""

# Build the wheel
echo "📦 Building Python wheel..."
uv build --wheel

if [ ! -d ".build" ]; then
    echo "❌ Build failed - .build directory not created"
    exit 1
fi

echo "✅ Wheel built successfully"
echo ""

# Deploy with bundle
echo "🚀 Deploying to Databricks Apps..."
databricks bundle deploy

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📋 Next steps:"
echo "  1. Check app status: ./app_status.sh"
echo "  2. View logs in Databricks workspace: Apps → your-app → Logs"
echo "  3. Get app URL to connect AI assistants"
echo ""


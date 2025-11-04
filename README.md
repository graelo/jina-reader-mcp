# Minuscule MCP server for the JINA Reader API

Use it with

```json
{
  "mcpServers": {
    "jina-reader": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/graelo/jina-reader-mcp",
        "jina-reader-mcp"
      ],
      "env": {
        "JINA_API_URL": "http://localhost:8000"
      }
    }
  }
}
```

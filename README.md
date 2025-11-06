# Minuscule MCP server for the JINA Reader API

## Setup

Use it with an instance of <https://github.com/intergalacticalvariable/reader>.

### HTTPS

If your Reader API is served via HTTPS with a self-signed certificate, ensure
your root CA certificate is stored in the System keychain
(`/System/Library/Keychains/System.keychain`). This is the standard location
for trusted certificates on modern macOS.

Set the `ROOT_CA_NAME` environment variable to the name of your certificate as
it appears in Keychain.app. The server will automatically retrieve and trust
this certificate for secure connections.

No manual certificate extraction is required; simply provide the correct name
in your configuration.

## Configuration

Add this definition, and provide the url to the Jina service.

```json
{
  "mcpServers": {
    "jina-reader": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/graelo/jina-reader-mcp@v0.2.0",
        "jina-reader-mcp"
      ],
      "env": {
        "JINA_API_URL": "https://my-jina-reader.domain.local"
        "ROOT_CA_NAME": "My Root CA"
      }
    }
  }
}
```

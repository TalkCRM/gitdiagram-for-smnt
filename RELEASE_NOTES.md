# GitDiagram v1.1.0 Release Notes

## 🎉 Major Stability and Compatibility Update

This release focuses on resolving critical issues and significantly improving the reliability of Mermaid diagram generation.

## ✨ What's New

### 🛡️ Mermaid v11.4.1 Full Compatibility
- **Eliminated "Syntax error in text mermaid version 11.4.1"** - The most common issue users faced
- **Smart validation system** that checks syntax in real-time during generation
- **Automatic error correction** for common syntax issues like:
  - Improper quote usage in labels with special characters
  - Incorrect edge label formatting (`|"label"|` vs `| "label" |`)
  - Class application to subgraph declarations
  - Invalid node ID characters

### 🔧 Enhanced Error Handling
- **Fixed HTTP2 protocol errors** that caused "Failed to load resource" issues
- **Resolved JSON parsing errors** in SSE (Server-Sent Events) streams
- **Improved OpenAI API error handling** with specific authentication failure messages
- **Better stream termination** with proper `[DONE]` markers

### 🚀 Improved User Experience
- **Real-time status updates** during validation and auto-fixing processes
- **5-minute request timeout** to prevent hanging connections
- **Graceful error recovery** with automatic retry mechanisms
- **Clear error messages** for API key and authentication issues

## 🐛 Bug Fixes

### Critical Fixes
- **HTTP2 Protocol Errors**: `net::ERR_HTTP2_PROTOCOL_ERROR` no longer occurs during diagram generation
- **JSON Parsing**: `SyntaxError: Unterminated string in JSON` completely resolved
- **Mermaid Syntax**: All v11.4.1 compatibility issues addressed
- **Network Stability**: Connection timeouts and protocol mismatches eliminated

### Technical Improvements
- Enhanced CORS configuration with proper header exposure
- Better SSE stream management with balanced JSON validation
- Improved error propagation from backend to frontend
- More robust aiohttp session handling for streaming responses

## 🔄 Migration Guide

This update is fully backward compatible. No changes required for existing users.

## 🙏 Acknowledgments

Thanks to all users who reported issues and helped identify the critical problems that this release addresses.

---

**Full Changelog**: See [CHANGELOG.md](https://github.com/TalkCRM/gitdiagram-for-smnt/blob/main/CHANGELOG.md)

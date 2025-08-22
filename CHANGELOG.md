# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-08-22

### Added

- **Mermaid v11.4.1 Validation System**: Comprehensive validation module for Mermaid.js syntax compatibility
  - Real-time syntax validation during diagram generation
  - Automatic fixing of common syntax issues
  - Strict enforcement of v11.4.1 syntax rules
  - Validation checklist for node IDs, labels, edges, and subgraphs

### Enhanced

- **Backend Error Handling**: Improved robustness and error reporting
  - Enhanced SSE (Server-Sent Events) stream management with proper termination
  - Better OpenAI API error handling with specific 401 authentication error messages
  - Automatic retry mechanism with stricter prompts when validation fails
  - Comprehensive logging for debugging purposes

- **Frontend Stability**: Resolved critical streaming and parsing issues
  - Fixed `SyntaxError: Unterminated string in JSON` errors in SSE processing
  - Added proper JSON validation with brace balancing checks
  - Implemented SSE stream termination detection with `[DONE]` markers
  - Added 5-minute timeout for HTTP requests to prevent hanging connections

- **Prompt Engineering**: Significantly improved Mermaid code generation quality
  - Added detailed syntax rules and examples for Mermaid v11.4.1
  - Mandatory validation checklist in prompts
  - Enhanced error-specific regeneration with targeted fixes
  - Better handling of reserved keywords and special characters

### Fixed

- **HTTP2 Protocol Errors**: Resolved `net::ERR_HTTP2_PROTOCOL_ERROR` issues
  - Proper SSE stream closure handling
  - Fixed incomplete JSON data transmission
  - Improved CORS configuration with exposed headers

- **Mermaid Syntax Compatibility**: Eliminated "Syntax error in text mermaid version 11.4.1"
  - Automatic quote wrapping for labels with special characters
  - Fixed edge label spacing issues (`|"label"|` format)
  - Prevented class application to subgraph declarations
  - Ensured alphanumeric-only node IDs

- **Network Stability**: Enhanced connection reliability
  - Better handling of API authentication failures
  - Improved error propagation from backend to frontend
  - Reduced connection timeouts and protocol mismatches

### Technical Improvements

- **Code Quality**: Enhanced maintainability and debugging capabilities
  - Added comprehensive error logging throughout the application
  - Improved type safety with new stream state definitions
  - Better separation of concerns in validation logic

- **User Experience**: Smoother diagram generation process
  - Real-time status updates during validation and fixing
  - Clear error messages for authentication and API issues
  - Graceful handling of edge cases and error conditions

### Dependencies

- Updated FastAPI CORS middleware configuration
- Enhanced OpenAI API integration with better error handling
- Improved aiohttp session management for streaming responses

---

## [1.0.0] - Initial Release

### Added
- Initial GitDiagram application with Mermaid.js diagram generation
- GitHub repository analysis and visualization
- OpenAI API integration for intelligent diagram creation
- Basic SSE streaming for real-time diagram generation
- Component mapping for interactive diagrams

# EasyActiveDev
> A minimal Discord bot for obtaining and maintaining the Discord Active Developer Badge.

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Security: Enhanced](https://img.shields.io/badge/security-enhanced-green.svg)](#security-implementation)

## Overview

EasyActiveDev provides a production-ready solution for Discord developers to obtain and maintain their Active Developer Badge. The bot implements enterprise-grade security with military-level encryption while maintaining a simple user experience.

## Features

- **Single Command**: Implements `/init` slash command for badge eligibility
- **Military-Grade Security**: PBKDF2 key derivation with 100,000 iterations and random salt
- **Auto-Recovery**: Intelligent handling of corrupted tokens and failed authentication
- **Cross-Platform**: POSIX-compliant launcher supporting all major shells
- **Smart Caching**: Optimized dependency management with automatic detection
- **Graceful Operations**: Proper async cleanup and cross-platform signal handling
- **Enhanced Privacy**: Ephemeral commands visible only to executor

## Prerequisites

| Requirement | Version | Notes |
|-------------|---------|-------|
| Python | 3.8+ | With asyncio support |
| Discord Account | — | Developer portal access required |
| Server Admin Rights | Required | For bot invitation and slash commands |

## Quick Start

### 1. Create Discord Application

Navigate to the [Discord Developer Portal](https://discord.com/developers/applications) and create a new application:

```
1. Click "New Application"
2. Enter application name
3. Navigate to "Bot" section
4. Click "Add Bot"
5. Copy the bot token (keep secure)
```

### 2. Configure Bot Permissions

In the OAuth2 URL Generator, select:

**Scopes:**
- `bot`
- `applications.commands`

**Bot Permissions:**
- `Send Messages`
- `Use Slash Commands`

### 3. Deploy Bot

```bash
# Clone repository
git clone --depth=1 https://github.com/Gur0v/easyactivedev.git
cd easyactivedev

# Make executable and run
chmod +x run.sh
./run.sh
```

When prompted, provide your bot token. The system will handle military-grade encryption and secure storage automatically.

### 4. Activate Badge

1. Execute `/init` command in your Discord server
2. Wait **24-48 hours** minimum
3. Visit [Discord Active Developer Portal](https://discord.com/developers/active-developer)
4. Claim your badge

## Maintenance

Execute `/init` command **monthly** to maintain badge status. The bot will log all activity for audit purposes.

## Architecture

```
easyactivedev/
├── run.sh              # Optimized POSIX shell launcher
├── core.py             # Secure bot implementation with auto-recovery
├── requirements.txt    # Minimal Python dependencies
└── README.md           # This documentation
```

### Security Implementation

- **Advanced Encryption**: PBKDF2-HMAC-SHA256 with 100,000 iterations
- **Cryptographic Security**: Random salt generation using `secrets` module
- **File Protection**: Owner-only permissions (600/400) for sensitive files
- **Input Validation**: Token format verification and sanitization
- **Auto-Recovery**: Intelligent corruption detection and cleanup
- **Memory Safety**: Secure key derivation with proper cleanup

### Enhanced Features

- **Smart Migration**: Automatic upgrade from legacy token formats
- **Cross-Platform**: Windows ProactorEventLoop support for optimal performance
- **Error Resilience**: Comprehensive Discord API error handling
- **Audit Logging**: Detailed operation logs with user/guild context
- **Shell Detection**: Advanced shell type detection for optimal activation

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Command not visible | Ensure bot has `applications.commands` scope |
| Badge claim unavailable | Server must have Community features enabled |
| Token decryption failed | Old tokens auto-migrate; corrupted tokens auto-recover |
| Module import errors | Delete `.deps_installed` and restart |
| Permission denied | Ensure write access to project directory |
| Signal handling issues | Script uses proper `exec` for process management |

### Debug Information

The application creates several files during operation:

- `.venv/` — Isolated Python environment
- `.token` — Military-grade encrypted bot credentials
- `.master` — Secure encryption key storage (400 permissions)
- `.deps_installed` — Smart dependency cache marker

### Migration from Legacy Versions

Legacy tokens are automatically detected and migrated to the new security standard on first run. No manual intervention required.

## Performance & Compatibility

- **Shell Support**: sh, bash, zsh, fish, csh with fallback detection
- **Platform Support**: Linux, macOS, Windows (WSL/Cygwin)
- **Memory Efficient**: Optimized async operations with proper cleanup
- **Network Resilient**: Automatic retry logic for Discord API calls

## Contributing

Contributions are welcome. Please ensure:

- POSIX compliance for shell scripts
- Proper async/await patterns and error handling
- Security best practices for cryptographic operations
- Comprehensive testing across shell environments
- Documentation updates for new security features

## Security Audit

This implementation follows industry security standards:

- ✅ OWASP cryptographic guidelines compliance
- ✅ Zero plaintext token storage
- ✅ Secure random number generation
- ✅ Proper key derivation functions
- ✅ File system permission hardening
- ✅ Input validation and sanitization

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

---

**Disclaimer**: This tool is for educational and convenience purposes. Users are responsible for complying with Discord's Terms of Service and API guidelines.

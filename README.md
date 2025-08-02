# EasyActiveDev

> A minimal Discord bot for obtaining and maintaining the Discord Active Developer Badge.

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## Overview

EasyActiveDev provides a streamlined solution for Discord developers to obtain and maintain their Active Developer Badge. The bot creates a single slash command that satisfies Discord's activity requirements while handling token security and automation.

## Features

- **Single Command**: Implements `/init` slash command for badge eligibility
- **Secure Storage**: AES encryption for bot tokens with auto-generated keys
- **Cross-Shell Support**: POSIX-compliant script supporting bash, zsh, fish, and csh
- **Dependency Management**: Automated virtual environment and package handling
- **Graceful Shutdown**: Proper cleanup of connections and resources

## Prerequisites

| Requirement | Version |
|-------------|---------|
| Python | 3.8+ |
| Discord Account | — |
| Server Admin Rights | Required for bot invitation |

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

**Permissions:**
- `Send Messages`
- `Use Slash Commands`

### 3. Deploy Bot

```bash
# Clone repository
git clone https://github.com/Gur0v/easyactivedev.git
cd easyactivedev

# Make executable and run
chmod +x run.sh
./run.sh
```

When prompted, provide your bot token. The system will handle encryption and storage automatically.

### 4. Activate Badge

1. Execute `/init` command in your Discord server
2. Wait **48 hours** minimum
3. Visit [Discord Active Developer Portal](https://discord.com/developers/active-developer)
4. Claim your badge

## Maintenance

Execute `/init` command **monthly** to maintain badge status.

## Architecture

```
easyactivedev/
├── run.sh              # POSIX shell launcher
├── core.py             # Main bot implementation  
├── requirements.txt    # Python dependencies
└── README.md           # Documentation
```

### Security Implementation

- **Token Encryption**: Fernet (AES 128) with PBKDF2 key derivation
- **Key Management**: Auto-generated 256-bit encryption keys
- **Storage Isolation**: Encrypted tokens stored separately from keys
- **Memory Safety**: Tokens decrypted only during runtime

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Command not found | Verify bot permissions and server invitation |
| Module import errors | Delete `.deps_installed` and restart |
| Permission denied | Ensure write access to project directory |
| Signal handling issues | Use `exec` wrapper for proper process management |

### Debug Information

The application creates several files during operation:

- `.venv/` — Isolated Python environment
- `.token` — Encrypted bot credentials
- `.pass` — Encryption key storage
- `.deps_installed` — Dependency cache marker

## Contributing

Contributions are welcome. Please ensure:

- POSIX compliance for shell scripts
- Proper error handling and cleanup
- Security best practices for token management
- Documentation updates for new features

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

---

**Disclaimer**: This tool is for educational and convenience purposes. Users are responsible for complying with Discord's Terms of Service and API guidelines.

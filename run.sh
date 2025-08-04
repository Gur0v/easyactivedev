#!/bin/sh

log() { printf "[%s] %s\n" "$1" "$2"; }

detect_shell() {
    [ -n "$ZSH_VERSION" ] && echo "zsh" && return
    [ -n "$BASH_VERSION" ] && echo "bash" && return
    [ -n "$version" ] && echo "fish" && return
    
    parent=$(ps -p $PPID -o comm= 2>/dev/null || ps -p $PPID -o command= 2>/dev/null | awk '{print $1}')
    case "$parent" in
        *csh*|*tcsh*) echo "csh" ;;
        *fish*) echo "fish" ;;
        *zsh*) echo "zsh" ;;
        *bash*) echo "bash" ;;
        *) echo "sh" ;;
    esac
}

setup_venv() {
    if [ ! -d ".venv" ]; then
        log "INFO" "Creating venv..."
        python3 -m venv .venv || { log "ERROR" "Failed to create venv"; exit 1; }
        log "OK" "Venv created"
    fi
    
    log "INFO" "Activating venv..."
    case "$(detect_shell)" in
        fish) [ -f ".venv/bin/activate.fish" ] && . .venv/bin/activate.fish || . .venv/bin/activate ;;
        csh) [ -f ".venv/bin/activate.csh" ] && . .venv/bin/activate.csh || . .venv/bin/activate ;;
        *) . .venv/bin/activate ;;
    esac
}

install_deps() {
    if [ ! -f ".deps_installed" ]; then
        log "INFO" "Installing dependencies..."
        if pip install -r requirements.txt >/dev/null 2>&1; then
            touch .deps_installed
            log "OK" "Dependencies installed"
        else
            log "ERROR" "Failed to install dependencies"
            exit 1
        fi
    else
        log "INFO" "Dependencies cached"
    fi
}

main() {
    log "INFO" "Shell: $(detect_shell)"
    setup_venv
    install_deps
    log "INFO" "Starting bot..."
    exec python3 core.py
}

main

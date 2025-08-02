#!/bin/sh

print_step() {
    printf "[INFO] %s\n" "$1"
}

print_success() {
    printf "[OK] %s\n" "$1"
}

print_error() {
    printf "[ERROR] %s\n" "$1"
}

detect_shell() {
    if [ -n "$ZSH_VERSION" ]; then
        echo "zsh"
    elif [ -n "$BASH_VERSION" ]; then
        echo "bash"
    elif [ -n "$version" ]; then
        echo "fish"
    else
        parent_process=$(ps -p $PPID -o comm= 2>/dev/null || ps -p $PPID -o command= 2>/dev/null | awk '{print $1}')
        case "$parent_process" in
            *csh*|*tcsh*) echo "csh" ;;
            *fish*) echo "fish" ;;
            *zsh*) echo "zsh" ;;
            *bash*) echo "bash" ;;
            *powershell*|*pwsh*) echo "powershell" ;;
            *) echo "sh" ;;
        esac
    fi
}

SHELL_TYPE=$(detect_shell)
print_step "Shell: $SHELL_TYPE"

if [ ! -d ".venv" ]; then
    print_step "Creating venv..."
    python3 -m venv .venv
    print_success "Venv created"
fi

print_step "Activating venv..."
case "$SHELL_TYPE" in
    "fish")
        if [ -f ".venv/bin/activate.fish" ]; then
            . .venv/bin/activate.fish
        else
            . .venv/bin/activate
        fi
        ;;
    "csh")
        if [ -f ".venv/bin/activate.csh" ]; then
            . .venv/bin/activate.csh
        else
            . .venv/bin/activate
        fi
        ;;
    "powershell")
        if [ -f ".venv/bin/Activate.ps1" ]; then
            print_error "PowerShell not supported - run .venv/bin/Activate.ps1 manually"
            exit 1
        else
            . .venv/bin/activate
        fi
        ;;
    *)
        . .venv/bin/activate
        ;;
esac

if [ ! -f ".deps_installed" ]; then
    print_step "Installing dependencies..."
    pip install -r requirements.txt > /dev/null 2>&1
    touch .deps_installed
    print_success "Dependencies cached"
else
    print_step "Dependencies cached"
fi

print_step "Starting bot (stage 1)..."
exec python core.py

#!/bin/bash

if [[ $EUID -ne 0 ]]; then
    echo "This script must be run with sudo. Please run 'sudo ./install_script.sh'." >&2
    exit 1
fi

API=""
MODEL="gpt-3.5-turbo"
ORIGINAL_USER="${SUDO_USER:-$USER}"
ORIGINAL_USER_HOME="$(eval echo ~"${ORIGINAL_USER}")"
DEFAULT_IMAGE_PATH="${ORIGINAL_USER_HOME}/Pictures/TerminalGPT"
CONFIG_PATH="${ORIGINAL_USER_HOME}/.tgpt/config"
MAX_TOKENS=100
TEMPERATURE=0.7

# Create folders if missing
mkdir -p "$(dirname "${CONFIG_PATH}")"
chown $ORIGINAL_USER:$ORIGINAL_USER "$(dirname "${CONFIG_PATH}")"

# Ask user for desired image save path
read -p "Enter the desired path to save images (default: ${DEFAULT_IMAGE_PATH}): " IMAGE_PATH
IMAGE_PATH="${IMAGE_PATH:-$DEFAULT_IMAGE_PATH}"
mkdir -p "${IMAGE_PATH}"
chown $ORIGINAL_USER:$ORIGINAL_USER $IMAGE_PATH

# Ask user for API key, create config file at CONFIG_PATH
read -p "Please enter your API key: " API
if [[ -z "${API}" ]]; then
    echo "API key cannot be empty. Exiting."
    exit 1
fi

cat > "${CONFIG_PATH}" << EOF
[DEFAULT]
API=${API}
MODEL=${MODEL}
IMAGE_PATH=${IMAGE_PATH}
MAX_TOKENS=${MAX_TOKENS}
TEMPERATURE=${TEMPERATURE}
EOF
chown $ORIGINAL_USER:$ORIGINAL_USER $CONFIG_PATH

# Copy tgpt file to /usr/bin/
if [ -f "tgpt" ]; then
    cp "tgpt" "/usr/bin/"
    chmod +x "/usr/bin/tgpt"
    chown $ORIGINAL_USER:$ORIGINAL_USER /usr/bin/tgpt
    echo "Installation completed successfully!"
else
    echo "Error: 'tgpt' file not found in the current directory. Exiting."
    exit 1
fi


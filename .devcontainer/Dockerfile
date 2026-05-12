FROM mcr.microsoft.com/devcontainers/base:alpine3.23

COPY ./flake.nix ./flake.lock ./molaccess.nix /molaccess-pkgs/

COPY ./.devcontainer/direnv.toml /home/vscode/.config/direnv/

# Adapted from https://github.com/devcontainers-community/features-direnv

RUN curl -sfL https://direnv.net/install.sh | bash && \
echo -e 'eval "$(direnv hook bash)"' >> /etc/bash.bashrc

FROM nixos/nix

RUN nix-channel --update && echo "experimental-features = nix-command flakes" > /etc/nix/nix.conf

COPY ./flake.nix ./flake.lock /molaccess-cache-warmup/
COPY ./misc/nix /molaccess-cache-warmup/misc/nix
COPY ./apps /molaccess-cache-warmup/apps
COPY ./core /molaccess-cache-warmup/core
COPY ./CMakeLists.txt ./pyproject.toml /molaccess-cache-warmup/

WORKDIR /molaccess-cache-warmup/

RUN nix develop && exit

WORKDIR /opt/workdir 
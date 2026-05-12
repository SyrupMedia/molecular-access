FROM nixos/nix

RUN nix-channel --update && echo "experimental-features = nix-command flakes" > /etc/nix/nix.conf

COPY ./flake.nix ./flake.lock ./molaccess.nix /molaccess-cache-warmup/

WORKDIR /molaccess-cache-warmup/

RUN nix develop && exit

WORKDIR /opt/workdir

# TODO?: ENTRYPOINT nix develop --command "/bin/sh"
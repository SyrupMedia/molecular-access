# Molecular Access
[![Source code](https://img.shields.io/badge/source-codeberg-blue?style=for-the-badge&logo=codeberg&color=84b9c9&logoColor=FFFFFF&labelColor=262a35)](https://codeberg.org/SyrupMedia/molecular-access)
[![Source mirror](https://img.shields.io/badge/source%20mirror-github-red?style=for-the-badge&logo=github&color=c58dda&logoColor=FFFFFF&labelColor=262a35)](https://github.com/SyrupMedia/molecular-access)

![Docker GitHub Action Workflow Status](https://img.shields.io/github/actions/workflow/status/SyrupMedia/molecular-access/docker.yml?style=for-the-badge&logo=docker&color=70a5d8&logoColor=FFFFFF&labelColor=262a35&label=DOCKER%20BUILD)
![Fedora GitHub Action Workflow Status](https://img.shields.io/github/actions/workflow/status/SyrupMedia/molecular-access/fedora.yml?style=for-the-badge&logo=fedora&color=70a5d8&logoColor=FFFFFF&labelColor=262a35&label=FEDORA%20BUILD)
![MinGW GitHub Action Workflow Status](https://img.shields.io/github/actions/workflow/status/SyrupMedia/molecular-access/mingw.yml?style=for-the-badge&logo=mingww64&color=70a5d8&logoColor=FFFFFF&labelColor=262a35&label=MINGW%20BUILD)
![Nix GitHub Action Workflow Status](https://img.shields.io/github/actions/workflow/status/SyrupMedia/molecular-access/nix.yml?style=for-the-badge&logo=nixos&color=70a5d8&logoColor=FFFFFF&labelColor=262a35&label=NIX%20BUILD)

[![Ko-Fi](https://img.shields.io/badge/donate-kofi-blue?style=for-the-badge&logo=ko-fi&color=e57578&logoColor=FFFFFF&labelColor=262a35)](https://ko-fi.com/molasses)
[![Patreon](https://img.shields.io/badge/donate-patreon-blue?style=for-the-badge&logo=patreon&color=e57578&logoColor=FFFFFF&labelColor=262a35)](https://www.patreon.com/molasseslover)

-------------------------------------------------------------------------------

This is a free and open-source accessibility interface, designed with real-time
(rendering) applications, such as games, in mind.

Supported platforms include Windows and Linux, with future MacOS support 
planned.

> [!IMPORTANT] 
> This project is hosted and organised on 
> [Codeberg](https://codeberg.org/SyrupMedia/molecular-access). Please report any
> bugs, and submit any contributions on there. An official mirror is available on
> [GitHub](https://github.com/SyrupMedia/molecular-access),
> however, pull requests and issues cannot be made from there.

## About
Molecular Access is a project which facilitates dynamic communication 
between processes in order to allow end-users to modify abstract data 
exposed to them by processes, and to allow processes to call abstract 
methods declared by other processes.

All of this is accomplished in a non-invasive way, which prioritises
developers, and follows an opt-in approach to features. Projects can expose as
much or as little data or functionality towards one another as they like.

The end goal here is to allow users, particularly users in need of additional
customisation to ensure accessibility, to be able to easily manage the data and
resources of other processes. That's customisation which might include changing
an image texture, changing a colour value, disabling or enabling visual effects, 
etc.

Such functionality can already be provided to users through bespoke, custom
implementations, without the need of Molecular - however, it comes at the
expense of standardisation, and at the expense of possible integration
between other processes. This solution is scalable, dynamic, and made to
cultivate ecosystems. In contrast, opening up features to users without such
a project leaves such features isolated, especially when the idea of 
inter-process communication is neglected or outright rejected.

In practice, Molecular Access is a project aiming to make software more
transparent, at the discretion of developers, in hopes of improving 
accessibility.

## Cloning

Please ensure you clone the repository recursively, as it uses submodules.

```sh
➜ git clone --recursive --depth=1 https://codeberg.org/SyrupMedia/molecular-access.git
```

## Building

### Dev Environments

We provide several options for preconfigured development environments which allow you to avoid manually installing development dependencies globally on your system. They both require that you have either Docker or Podman installed on your system.

#### Option 1: Nix Flake (optionally with Direnv)

If you have Nix installed on your system and configured with flake support, you can simply run `nix develop` in the project directory to spin up a shell environment with all needed dependencies. If you have Direnv installed as well the environment should load automatically, and you can even use the [VS Code Direnv extension](https://marketplace.visualstudio.com/items?itemName=mkhl.direnv) to integrate the flake environment with VS Code for intellisense and CMake commands support.

#### Option 2: VS Code Development Container

This is the most convenient option overall if you are willing to use VS Code. This setup provides C++ and Python intellisense as well as in-editor integration with CMake commands. Simply make sure that you have the [Dev Containers extension installed](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers), and then open the project folder in VS Code. You will be prompted to re-open the project in the development container, simply click "Reopen in to begin loading the container. It will likely take several minutes for the container to build the first time you load it, this is normal (eventually we may provide pre-built container images that will make this quicker). Once VS Code finishes launching and connecting to the container, you should see a pop-up message from the Direnv extension asking if you would like to reload the environment, make sure to accept. If VS Code notifies you of a CMake error, this is likely the result of the CMake extension trying to configure before the Direnv extension has properly loaded the environment. In this case simply open a terminal, run `make clean` and `make release` and then close and re-open VS Code.

#### Option 3: Generic Development Container

If you do not want to use VS Code, you can instead use the generic development container (you must have either Docker Compose or Podman Compose installed to use this):

- For an ephemeral container: `docker-compose run --rm dev` or `podman-compose run --rm dev`.

OR

- For a re-useable container: `docker-compose up -d dev && docker attach molecular-access_dev_1`, or `podman-compose up -d dev && podman attach molecular-access_dev_1`.

This container will share the contents of the project directory with your system, so any file edits that you make to project files outside the container will be propogated inside the container, and vice versa.

### Dependencies

The only internal build dependency is [`libipc`](https://github.com/mutouyun/cpp-ipc),
which must be cloned as a submodule.

If you did not clone the repository recursively, initialise it as such:

```
➜ git submodule update --init --recursive
```

#### Distribution Packages

Below are a list of packages which cover external dependencies, which are not
provided within the repository. 

> [!NOTE]
> You may also want to inspect our [container images](misc/containers),
> as we can't fully guarantee which binaries you may be lacking on your system.

<details>
  <summary>Fedora</summary>

  ```sh
  ➜ sudo dnf install -y \
    cmake \
    doxygen \
    ninja-build \
    python3-devel \
    swig
  ```
</details>

### Bindings

Building **requires** the generation of Python bindings using SWIG. CMake will not 
build without the `core/src/bindings/molecular_wrap.cxx` file generated by SWIG.

Bindings can be generated using `make`:
```sh
➜ make swig
```

Or alternatively, they can be generated manually:
```sh
➜ swig -python -c++ -o \
  core/src/bindings/molecular_wrap.cxx \
  core/src/bindings/molecular.i
```

### Makefile Build
The included [`Makefile`](Makefile) abstracts the build process away, and
should work on most systems.

#### Linux
```sh
➜ make swig
➜ make release -j$(nproc)
# Optionally install into the ./installdir directory
➜ make install
```

#### Windows
```sh
➜ make swig
➜ make release-windows -j$(nproc)
# Optionally install into the ./installdir directory
➜ make install-windows
```

### Manual Build
In case the Makefile doesn't work for you, you may have better luck building
manually with CMake.
```sh
➜ swig -python -c++ \
  -o core/src/bindings/molecular_wrap.cxx \
  core/src/bindings/molecular.i
➜ cmake -B target/release -D CMAKE_BUILD_TYPE=Release
➜ cmake --build target/release -j$(nproc)
# Optionally install into the ./installdir directory
➜ DESTDIR="$(pwd)/installdir" cmake --build target/release --target=install

```


## Python
### Bindings

In order to make use of the Python bindings, make sure a copy of the
`core/src/bindings/molaccesspy.py` file is located next to the 
`_molaccesspy.so` or `_molaccesspy.pyd` file.

On Windows, the `_molaccesspy.dll` file, built by CMake, *must* be renamed to
`_molaccesspy.pyd` in order to work. The Makefile should take care of this when
installing locally with `make install-windows`.

> [!NOTE]
> For instructions on generating the Python bindings, see the relevant subsection
> in the [#Building](#bindings) section.
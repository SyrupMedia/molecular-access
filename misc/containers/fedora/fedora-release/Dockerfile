FROM fedora:latest

ENV DESTDIR="/opt/installdir/fedora" 

WORKDIR /opt/workdir

# Disable weak dependencies to reduce image size.
RUN echo "install_weak_deps=False" >> /etc/dnf/dnf.conf 
RUN dnf install -y \
    clang \
    cmake \
    doxygen \
    ninja-build \
    python3-devel \
    swig

# Build and install into a directory with the Makefile.
CMD 	make swig; \
	cmake -B target/fedora/release -D CMAKE_BUILD_TYPE=Release; \
	cmake --build target/fedora/release -j$(nproc); \
	cmake --build target/fedora/release --target=install

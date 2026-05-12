FROM alpine:latest

ENV PATH=/opt/vlang:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/lib/ninja-build/bin

RUN apk add --no-cache \
    cmake \
    mingw-w64-gcc \
    mingw-w64-headers \
    musl \
    ninja-build \
    python3 \
    python3-dev \
    swig

WORKDIR /opt/workdir
    
CMD cmake -B target/alpine/release \
    -D CMAKE_BUILD_TYPE=Release \
    -D MINGW_CROSS_COMPILATION=ON \
    -D CMAKE_C_COMPILER=/usr/bin/x86_64-w64-mingw32-gcc \
    -D CMAKE_CXX_COMPILER=/usr/bin/x86_64-w64-mingw32-g++ \
    -G Ninja; \
    cmake --build target/alpine/release -j$(nproc); \
    cmake --build target/alpine/release --target=install
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
    tree

WORKDIR /opt/workdir
    
CMD  tree /usr/i686-w64-mingw32/include/ > /opt/workdir/tree.txt \
        cmake -B target/alpine/debug \
		-D CMAKE_BUILD_TYPE=Debug \
		-D MINGW_CROSS_COMPILATION=ON \
		-D CMAKE_C_COMPILER=/usr/bin/x86_64-w64-mingw32-gcc \
		-D CMAKE_CXX_COMPILER=/usr/bin/x86_64-w64-mingw32-g++ \
		-G Ninja; \
        cmake --build target/alpine/debug -j$(nproc)
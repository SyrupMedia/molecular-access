debug:
	cmake --preset debug
	cmake --build --preset debug -j$(nproc)
release:
	cmake --preset release
	cmake --build --preset release -j$(nproc)
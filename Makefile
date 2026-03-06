CWD := $(abspath $(patsubst %/,%,$(dir $(abspath $(lastword $(MAKEFILE_LIST))))))

all: release

clean:
	rm -rf target
	rm -rf installdir

debug:
	cmake --preset debug
	cmake --build --preset debug -j$(nproc)
release:
	cmake --preset release
	cmake --build --preset release -j$(nproc)
install: release
	DESTDIR="$(CWD)/installdir" cmake --build target/release --target=install
	cp target/release/core/src/bindings/molaccesspy.py "$(CWD)/installdir/usr/local/lib/molaccesspy.py"; # TODO: figure out how to do this in cmake instead

# Windows
release-windows:
	cmake --preset release-windows
	cmake --build --preset release-windows -j$(nproc)
install-windows: release-windows
	DESTDIR="$(CWD)/installdir" cmake --build target/release --target=install
	cp target/release/core/src/bindings/molaccesspy.py "$(CWD)/installdir/Program Files (x86)/molecular-access/lib/molaccesspy.py"; # TODO: figure out how to do this in cmake instead

	mv \
	"$(CWD)/installdir/Program Files (x86)/molecular-access/lib/_molaccesspy.dll" \
	"$(CWD)/installdir/Program Files (x86)/molecular-access/lib/_molaccesspy.pyd"

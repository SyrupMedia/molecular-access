CWD := $(abspath $(patsubst %/,%,$(dir $(abspath $(lastword $(MAKEFILE_LIST))))))

debug:
	cmake --preset debug
	cmake --build --preset debug -j$(nproc)
release:
	cmake --preset release
	cmake --build --preset release -j$(nproc)
install:
	$(MAKE) release
	DESTDIR="$(CWD)/installdir" cmake --build target/release --target=install

	if [ -f core/src/bindings/molaccesspy.py ] ; \
	then \
		cp core/src/bindings/molaccesspy.py "$(CWD)/installdir/usr/local/lib/molaccesspy.py"; \
	fi;

	cp $(wildcard core/src/bindings/molaccescy.cpython*) "$(CWD)/installdir/usr/local/lib/";


# Windows
release-windows:
	cmake --preset release-windows
	cmake --build --preset release-windows -j$(nproc)
install-windows:
	$(MAKE) release-windows
	DESTDIR="$(CWD)/installdir" cmake --build target/release --target=install

	if [ -f core/src/bindings/molaccesspy.py ] ; \
	then \
		cp core/src/bindings/molaccesspy.py "$(CWD)/installdir/Program Files (x86)/molecular-access/lib/"; \
	fi;

	mv \
	"$(CWD)/installdir/Program Files (x86)/molecular-access/lib/_molaccesspy.dll" \
	"$(CWD)/installdir/Program Files (x86)/molecular-access/lib/_molaccesspy.pyd"

# Bindings
swig:
	swig -python -c++ core/src/bindings/molecular.i

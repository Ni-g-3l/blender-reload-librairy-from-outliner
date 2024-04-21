PACKAGE_VERSION = $(shell grep -oP 'version": \((.*?)\)' $(CURDIR)/reload_librairy_from_outliner_addon/__init__.py | cut -d'(' -f2 | cut -d')' -f1 | sed 's/, /./g')

install_dev:
	@echo "------------------- INSTALL DEV ENV ------------------- "
	rm -rf /tmp/blender/reload_librairy_from_outliner_addon
	mkdir /tmp/blender/reload_librairy_from_outliner_addon/scripts/addons -p
	ln $(CURDIR)/reload_librairy_from_outliner_addon /tmp/blender/reload_librairy_from_outliner_addon/scripts/addons/reload_librairy_from_outliner_addon -s
	@echo "------------------------------------------------------- "

run:
	@echo "--------------------- RUN BLENDER --------------------- "
	@export BLENDER_USER_SCRIPTS=/tmp/blender/reload_librairy_from_outliner_addon/scripts; \
	blender --addons reload_librairy_from_outliner_addon

deploy:release
	@echo "------------------- DEPLOY PACKAGE -------------------- "
	@echo Deploying ${PACKAGE_VERSION} version
	@git push --tags
	@gh release create ${PACKAGE_VERSION} ./dist/reload_librairy_from_outliner_addon-${PACKAGE_VERSION}.zip --generate-notes --latest 
	@echo "------------------------------------------------------- "

release:build clean
	@echo "------------------- RELEASE PACKAGE ------------------- "
	@echo Releasing ${PACKAGE_VERSION} version
	@git tag ${PACKAGE_VERSION} || echo "Tag already exists."
	@echo "------------------------------------------------------- "

build: clean
	@echo "-------------------- BUILD PACKAGE -------------------- "
	mkdir -p dist
	zip -r dist/reload_librairy_from_outliner_addon-${PACKAGE_VERSION}.zip reload_librairy_from_outliner_addon
	@echo "------------------------------------------------------- "

clean:
	@echo "-------------------- CLEAN PACKAGE -------------------- "
	find . -name \*.pyc -delete
	find . -name __pycache__ -delete
	@echo "------------------------------------------------------- "

test:
	@echo "---------------------- RUN TESTS ---------------------- "
	python3 -m unittest discover tests
	@echo "------------------------------------------------------- "

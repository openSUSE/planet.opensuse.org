JAVA=java -Xmx8m
L10N_DIR=locale
DOMAIN=planetsuse
POT=$(L10N_DIR)/$(DOMAIN).pot
COMPRESSOR=$(JAVA) -jar ./tools/yuicompressor.jar

CSS := $(patsubst %.css,%.min.css,$(filter-out %.min.css,$(wildcard website/css/*.css)))
JS  := $(patsubst %.js,%.min.js,$(filter-out %.min.js,$(wildcard website/js/*.js)))
L10N_SOURCES := $(wildcard planetsuse/*.html)
PO_FILES := $(wildcard locale/*.po)
MO_FILES := $(patsubst locale/%.po,locale/%/LC_MESSAGES/$(DOMAIN).mo,${PO_FILES})

website/css/%.min.css:	website/css/%.css
	$(COMPRESSOR) --type css --charset UTF-8 --verbose -o "$@" "$<"

website/js/%.min.js:	website/js/%.js
	$(COMPRESSOR) --type js --charset UTF-8 --verbose -o "$@" "$<"

$(L10N_DIR)/%/LC_MESSAGES/$(DOMAIN).mo:	$(L10N_DIR)/%.po
	mkdir -p $(dir $@) && msgfmt -c -o "$@" "$<"

.DEFAULT:	all
all:	minify l10n

minify:	${CSS} ${JS}

$(POT):	${L10N_SOURCES}
	./l10n-extract-from-templates

${PO_FILES}:	$(POT)
	msgmerge --update "$@" "$<"

l10n:	${MO_FILES}

.PHONY:	all minify l10n

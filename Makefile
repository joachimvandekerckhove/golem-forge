SHELL := /bin/sh

CAST_YAML := forge/cast-from-yaml.py

SPECDIR := golemspecs
SPECS   := $(wildcard $(SPECDIR)/*.yaml)

# Require PROJECT to be set for cast-all; default for cast is optional.
PROJECT ?=
OUTDIR  ?= $(if $(PROJECT),projects/$(PROJECT)/golems,golems)

.PHONY: help cast-all cast clean

help:
	@echo "Golem Forge (project-scoped outputs, project-agnostic specs)"
	@echo
	@echo "Targets:"
	@echo "  make cast-all PROJECT=<project>"
	@echo "      Cast all golemspecs into projects/<project>/golems/"
	@echo
	@echo "  make cast SPEC=golemspecs/name.yaml [PROJECT=<project>]"
	@echo "      Cast one spec into projects/<project>/golems/ (or ./golems if PROJECT omitted)"
	@echo
	@echo "  make clean PROJECT=<project>"
	@echo "      Remove composed golems for that project"
	@echo
	@echo "Examples:"
	@echo "  make cast-all PROJECT=minimodels"
	@echo "  make cast SPEC=golemspecs/minimodels-liam-python-coder.yaml PROJECT=minimodels"
	@echo "  make cast SPEC=golemspecs/minimodels-liam-python-coder.yaml"

cast-all:
	@if [ -z "$(PROJECT)" ]; then \
		echo "Usage: make cast-all PROJECT=<project>" >&2; \
		exit 1; \
	fi
	@mkdir -p "$(OUTDIR)"
	@for s in $(SPECS); do \
		echo "Casting $$s -> $(OUTDIR)/"; \
		python3 $(CAST_YAML) "$$s" --outdir "$(OUTDIR)"; \
	done

cast:
	@if [ -z "$(SPEC)" ]; then \
		echo "Usage: make cast SPEC=golemspecs/name.yaml [PROJECT=<project>]" >&2; \
		exit 1; \
	fi
	@mkdir -p "$(OUTDIR)"
	@python3 $(CAST_YAML) "$(SPEC)" --outdir "$(OUTDIR)"

clean:
	@if [ -z "$(PROJECT)" ]; then \
		echo "Usage: make clean PROJECT=<project>" >&2; \
		exit 1; \
	fi
	@rm -f "projects/$(PROJECT)/golems/"*.md

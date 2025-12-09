# Makefile for golem-forge

CAST := forge/cast.sh
LIST := forge/list.sh

.PHONY: help list cast

help:
	@echo "Golem Forge"
	@echo
	@echo "Targets:"
	@echo "  make list"
	@echo "      List available personalities, roles, and domains."
	@echo
	@echo "  make cast P=<personality> R=<role> D=<domain> [OUT=<basename>]"
	@echo "      Cast a golem by composing:"
	@echo "        personalities/<P>.md"
	@echo "        roles/<R>.md"
	@echo "        domains/<D>.md"
	@echo "      The output is written to golems/<basename>.md."
	@echo "      If OUT is omitted, basename defaults to P-R-D."
	@echo
	@echo "Examples:"
	@echo "  make list"
	@echo "  make cast P=rigorous R=writer D=manuscript"
	@echo "  make cast P=builder R=coder D=infrastructure OUT=builder-coder-infra"

list:
	@$(LIST)

cast:
	@if [ -z "$(P)" ] || [ -z "$(R)" ] || [ -z "$(D)" ]; then \
		echo "Usage: make cast P=<personality> R=<role> D=<domain> [OUT=<basename>]" >&2; \
		exit 1; \
	fi; \
	if [ -n "$(OUT)" ]; then \
		$(CAST) "$(P)" "$(R)" "$(D)" "$(OUT)"; \
	else \
		$(CAST) "$(P)" "$(R)" "$(D)"; \
	fi

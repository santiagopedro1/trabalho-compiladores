.PHONY: all lexico sintatico clean help

INPUT ?= small_input.jl
OUTPUT ?= out

all:
	@if [ -z "$(INPUT)" ] || [ -z "$(OUTPUT)" ]; then \
		echo "Usage:"; \
		echo "  make all         - Run both lexical and syntactic analysis"; \
		echo "  make lexico      - Run only lexical analysis"; \
		echo "  make sintatico   - Run only syntactic analysis"; \
		echo "  make clean       - Clean generated files"; \
		echo "  make help        - Show this help message"; \
		echo ""; \
		echo "Variables:"; \
		echo "  INPUT    - Input file for analysis"; \
		echo "  OUTPUT   - Output file for results no extension"; \
		exit 1; \
	fi

	python main.py all $(INPUT) $(OUTPUT)

lexico:
	@if [ -z "$(INPUT)" ] || [ -z "$(OUTPUT)" ]; then \
		echo "Usage:"; \
		echo "  make all         - Run both lexical and syntactic analysis"; \
		echo "  make lexico      - Run only lexical analysis"; \
		echo "  make sintatico   - Run only syntactic analysis"; \
		echo "  make clean       - Clean generated files"; \
		echo "  make help        - Show this help message"; \
		echo ""; \
		echo "Variables:"; \
		echo "  INPUT    - Input file for analysis"; \
		echo "  OUTPUT   - Output file for results no extension"; \
		exit 1; \
	fi

	python main.py lexico $(INPUT) $(OUTPUT)

sintatico:
	@if [ -z "$(INPUT)" ] || [ -z "$(OUTPUT)" ]; then \
		echo "Usage:"; \
		echo "  make all         - Run both lexical and syntactic analysis"; \
		echo "  make lexico      - Run only lexical analysis"; \
		echo "  make sintatico   - Run only syntactic analysis"; \
		echo "  make clean       - Clean generated files"; \
		echo "  make help        - Show this help message"; \
		echo ""; \
		echo "Variables:"; \
		echo "  INPUT    - Input file for analysis"; \
		echo "  OUTPUT   - Output file for results no extension"; \
		exit 1; \
	fi

	python main.py parse $(INPUT) $(OUTPUT)

clean:
	rm -f *.dot *.png *.txt

help:
	@echo "Usage:"
	@echo "  make all         - Run both lexical and syntactic analysis"
	@echo "  make lexico      - Run only lexical analysis"
	@echo "  make sintatico   - Run only syntactic analysis"
	@echo "  make clean       - Clean generated files"
	@echo "  make help        - Show this help message"
	@echo ""
	@echo "Variables:"
	@echo "  INPUT    - Input file for analysis"
	@echo "  OUTPUT   - Output file for results no extension"
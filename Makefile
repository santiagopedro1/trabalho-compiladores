.PHONY: all lexico sintatico semantico clean help

INPUT ?= small_input.jl
OUTPUT ?= out

all:
	python main.py all $(INPUT) $(OUTPUT)

lexico:
	python main.py lexico $(INPUT) $(OUTPUT)

sintatico:
	python main.py sintatico $(INPUT) $(OUTPUT)

semantico:
	python main.py semantico $(INPUT) $(OUTPUT)

clean:
	rm -f *.dot *.png *.txt *.sym *.tac

help:
	@echo "Usage:"
	@echo "  make all         - Run lexical, syntactic and semantic analysis. só para small_input.jl ou similares só com operações + - * /"
	@echo "  make lexico      - Run only lexical analysis"
	@echo "  make sintatico   - Run only syntactic analysis"
	@echo "  make semantico   - Run only semantic analysis. só para small_input.jl ou similares só com operações + - * /"
	@echo "  make clean       - Clean generated files"
	@echo "  make help        - Show this help message"
	@echo ""
	@echo "Variables:"
	@echo "  INPUT    - Input file for analysis"
	@echo "  OUTPUT   - Output file for results no extension"
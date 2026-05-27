PYTHON ?= $(if $(wildcard .venv/Scripts/python.exe),.venv\Scripts\python.exe,.venv/bin/python)

# Ejemplos de ejecucion:
#   make generate_dataset
#   make generate_dataset SAMPLE_SIZE=0.1 MIN_USER_PLAYS=10000
#   make generate_dataset_with_graph
#   make generate_dataset_with_csv CSV_OUTPUT_DIR=dataset/csv_custom
#   make export_csv GRAPHML_FILE=dataset/graph/musicgraph.graphml CSV_OUTPUT_DIR=dataset/csv
#
# En Windows, si necesitas forzar la ruta de Python, usa por ejemplo:
#   make generate_dataset PYTHON=.venv\Scripts\python.exe

SAMPLE_SIZE ?= 0.05
MIN_USER_PLAYS ?= 20000
MIN_USER_ARTISTS ?= 40
ARTIST_TOP_N ?= 1
TEST_DATA_SIZE ?= 0.5

GENERATE_GRAPH ?= False
EXPORT_CSV ?= False

GRAPHML_FILE ?= dataset/graph/musicgraph.graphml
CSV_OUTPUT_DIR ?= dataset/csv
NODE_TYPE_FIELD ?= type
EDGE_TYPE_FIELD ?= relation

DATASET_ARGS = \
	--sample-size $(SAMPLE_SIZE) \
	--min-user-plays $(MIN_USER_PLAYS) \
	--min-user-artists $(MIN_USER_ARTISTS) \
	--artist-top-n $(ARTIST_TOP_N) \
	--test-data-size $(TEST_DATA_SIZE) \
	$(if $(filter True true TRUE,$(GENERATE_GRAPH)),--build-graph)

.PHONY: generate_dataset
generate_dataset:
	$(PYTHON) src/generate_dataset.py $(DATASET_ARGS)
	$(if $(filter True true TRUE,$(EXPORT_CSV)),$(PYTHON) src/export_into_csv_files.py --graphml-file "$(GRAPHML_FILE)" --output-dir "$(CSV_OUTPUT_DIR)" --node-type-field "$(NODE_TYPE_FIELD)" --edge-type-field "$(EDGE_TYPE_FIELD)")

.PHONY: generate_dataset_with_graph
generate_dataset_with_graph: GENERATE_GRAPH=True
generate_dataset_with_graph: generate_dataset

.PHONY: generate_dataset_with_csv
generate_dataset_with_csv: GENERATE_GRAPH=True
generate_dataset_with_csv: EXPORT_CSV=True
generate_dataset_with_csv: generate_dataset

.PHONY: export_csv
export_csv:
	$(if $(wildcard $(GRAPHML_FILE)),,$(error No existe GRAPHML_FILE="$(GRAPHML_FILE)". Genera el grafo con "make generate_dataset_with_graph" o indica otra ruta con GRAPHML_FILE=...))
	$(PYTHON) src/export_into_csv_files.py --graphml-file "$(GRAPHML_FILE)" --output-dir "$(CSV_OUTPUT_DIR)" --node-type-field "$(NODE_TYPE_FIELD)" --edge-type-field "$(EDGE_TYPE_FIELD)"

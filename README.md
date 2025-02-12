# Dev

This repository contains multiple layers for data processing and storage. The layers are organized into three parts: `layerraw`, `layercurated`, and `layerapp`. Below is the process for each layer.

## layerraw
This image extracts deltas from a SQL Server into the bucket `raw` in `csv` format using a user, password and server name extracted from a `.env` file.

1. **Create shared network**  
   Run `docker network create --driver bridge mrw_default`.

2. **Start MinIO**  
   In the main project directory, run `docker compose up` to bring up MinIO to store the extracted data.

3. **Run the Pipeline**  
   - **First time**: Execute `docker compose up --build` inside the layerraw directory with the vpn disabled, necessary to download libraries.
   - **Image already mounted**: Execute `docker compose up` to start the extraction of the pipeline specified in the `layerraw/docker-compose.yml` file.

### Managing executionlog.json
The `executionlog.json` file records the date of the last modified registry of the last successfull extraction. You need to manually modify this file if you want to extract data from previous runs. Just update the date in the file, and the pipeline will process data only from that date onward. The `executionlog.json` must be modified in each layer to launch a complete ETL from previous processed data.

### Delta and Full Extraction Scripts
Inside the scripts folder, there are two types of extraction:

- **delta_extract**: 
   - Used for tables containing a `fechaUltimaModificacion` column.
   - This method extracts only the changes made since the last modified registry extracted.
   - `fechaUltimaModificacion` -> YYYY-MM-DD as the folder name and YYYY-MM-DD_HHMMSS as an addition to the csv name.

- **full_extract (Provisional)**: 
   - Used for tables without the `fechaUltimaModificacion` column. Future tables will contain this column.
   - This method performs a complete data extraction.
   - Execution system date -> YYYY-MM-DD as the folder name and YYYY-MM-DD_HHMMSS as an addition to the csv name.

## layercurated
This image extracts the deltas from the `raw` layer, processes them, and uploads them to the curated layer in `parquet` format.

1. **Run the Pipeline**  
   - **First time**: Execute `docker compose up --build` inside the layercurated directory with the vpn disabled, necessary to download libraries.
   - **Image already mounted**: Execute `docker compose up` to start the extraction of the pipeline specified in the `layercurated/docker-compose.yml` file.

### Delta and Full Transform Scripts
Inside the scripts folder, there are two types of transform:

- **delta_transform (Provisional)**: 
   - Used for tables containing a `fechaUltimaModificacion` column. Future transforms will be specific for each necessary table.
   - `fechaUltimaModificacion` -> YYYY-MM-DD as the folder name and YYYY-MM-DD_HHMMSS as an addition to the parquet name.

- **full_transform (Provisional)**: 
   - Used for tables without the `fechaUltimaModificacion` column. Future tables will contain this column.
   - Execution system date -> YYYY-MM-DD as the folder name and YYYY-MM-DD_HHMMSS as an addition to the parquet name.

## layerapp
This image extracts the deltas from the `curated` layer, processes them, and uploads them to the app layer in `csv` format and to the MongoDB specified with a connection string extracted from a `.env` file.

1. **Run the Pipeline**  
   - **First time**: Execute `docker compose up --build` inside the layercurated directory with the vpn disabled, necessary to download libraries.
   - **Image already mounted**: Execute `docker compose up` to start the extraction of the pipeline specified in the `layercurated/docker-compose.yml` file.

### Delta and Full Load Scripts
Inside the scripts folder, there are two types of transform:

- **delta_load (Provisional)**: 
   - Used for tables containing a `fechaUltimaModificacion` column. Future loads will be specific for each necessary table.
   - `fechaUltimaModificacion` -> YYYY-MM-DD as the folder name and YYYY-MM-DD_HHMMSS as an addition to the parquet name.

- **full_load (Provisional)**: 
   - Used for tables without the `fechaUltimaModificacion` column. Future tables will contain this column.
   - Execution system date -> YYYY-MM-DD as the folder name and YYYY-MM-DD_HHMMSS as an addition to the parquet name.
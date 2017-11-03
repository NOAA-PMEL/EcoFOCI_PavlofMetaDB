# EcoFOCI_PavlofMetaDB
Collection of tools to interface with metadatabase for EcoFOCI

.
├── DBMooringSummary.py
├── EcoFOCI_config
│   └── db_config
│       ├── db_config.pyini
│       ├── db_config_cruises.pyini
│       ├── db_config_ctddata.pyini
│       ├── db_config_data.pyini
│       ├── db_config_datastatus.pyini
│       ├── db_config_drifters.pyini
│       ├── db_config_instruments.pyini
│       └── db_config_mooring.pyini
├── EcoRAIDMooringMetaData2SQL.py
├── EcoRAIDMooringMetaData2ptr.py
├── OutputDBMooringLocation.py
├── README.md
├── SQL2JSON_mooring_swimlanes.py
├── __init__.py
├── io_utils
│   ├── ConfigParserLocal.py
│   ├── ConfigParserLocal.pyc
│   ├── EcoFOCI_db_io.py
│   ├── EcoFOCI_db_io.pyc
│   ├── __init__.py
│   └── __init__.pyc
└── scripts
    └── EcoRAIDMooringMetaData2ptr.sh
    
## Script Descriptions

- EcoRAIDMooringMetaData2ptr.py   
	 Generate pointer files for EcoFOCI data housed on EcoRAID

- OutputDBMooringLocation.py   
	 Output the GeoLocation of EcoFOCI Mooring Sites archived in the EcoFOCI 
 		Mooring Deployment database in variety of formats (kml,geojson,csv)

        
################

Legal Disclaimer

This repository is a scientific product and is not official communication of the National Oceanic and Atmospheric Administration (NOAA), or the United States Department of Commerce (DOC). All NOAA GitHub project code is provided on an 'as is' basis and the user assumes responsibility for its use. Any claims against the DOC or DOC bureaus stemming from the use of this GitHub project will be governed by all applicable Federal law. Any reference to specific commercial products, processes, or services by service mark, trademark, manufacturer, or otherwise, does not constitute or imply their endorsement, recommendation, or favoring by the DOC. The DOC seal and logo, or the seal and logo of a DOC bureau, shall not be used in any manner to imply endorsement of any commercial product or activity by the DOC or the United States Government.
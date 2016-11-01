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
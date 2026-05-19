@echo off
setlocal

REM Sarateal - Kenya Farmer Market Access Radar scaffold
REM Run from: C:\Projects\supply\sarateal

mkdir app
mkdir app\api
mkdir app\core
mkdir app\db
mkdir app\models
mkdir app\schemas
mkdir app\services
mkdir app\jobs
mkdir app\scoring
mkdir app\data_sources

mkdir dashboard
mkdir dashboard\pages

mkdir data
mkdir data\raw
mkdir data\processed
mkdir data\geo
mkdir data\local

mkdir outputs
mkdir outputs\reports
mkdir outputs\exports

mkdir notebooks
mkdir tests
mkdir docs
mkdir scripts

type nul > app\__init__.py
type nul > app\api\__init__.py
type nul > app\core\__init__.py
type nul > app\db\__init__.py
type nul > app\models\__init__.py
type nul > app\schemas\__init__.py
type nul > app\services\__init__.py
type nul > app\jobs\__init__.py
type nul > app\scoring\__init__.py
type nul > app\data_sources\__init__.py

type nul > data\.gitkeep
type nul > data\raw\.gitkeep
type nul > data\processed\.gitkeep
type nul > data\geo\.gitkeep
type nul > outputs\.gitkeep

type nul > README.md
type nul > .env.example
type nul > requirements.txt

echo Scaffold created successfully.
endlocal
# Changelog

All notable changes to this project will be documented in this file.


## [0.0.21] - 2023-05-08

### Major changes

- migrator +1 number 
### Changed features
- Added user seeder
- Added all extracted models with:
- sqlacodegen postgresql+psycopg2://username:password@localhost:5432/walfin --outfile=models.py    
- Added seeder with faker (run  bash scripts/generate-fake-data.sh)
### Deploymeny changes
## [0.0.21] - 2023-04-30

### Major changes

- Added merchant_id field to FncTransfer model.
- Celery server initiation and setup are now part of the system module.
- Celery tasks and schedule can now be defined inside their corresponding module.
- Merchant data model is migrated from system_object module to user module.

### Changed features

- Added transfers list API for Admin and merchants.
- Added transfers details API for Admin and merchants.
- Added transfers manager for the top APIs.
- Added RM scheme for the top APIs.
- Changed routers in finance module.
- Changed transfer crud for creation.
- Removed merchant APIs from merchant.py and organized it like other APIs structure.
- Corrected add transfer with new transfer structure model.
- Added get_all_transfers function to TransferCRUD for getting.
- Added get all unsettled payment in settle interface.
- Added get all unsettled pgw payment in pgw settle interface.
- Added get all unsettled credit payment in credit settle interface.
- Added managers schemas for merchant payment.
- Added new filter for merchant transfer and payment list.
- Added transfer detail API with getting transfer id.
- Added new merchant filter for getting transfer list.
- Added summary and plot endpoints for merchant dashboard.
- Added order details API.

### Deploymeny changes

- Fixed start.sh and pre-strat.sh pathing issue.
- Added a single entrypoint script following the offical Docker naming convention; docker-entrypoint.sh.
- Added dockerignore file to reduce image size and build time.
- Added a new Dockerfile with following changes:
  - Dockerfile name follows the offical Docker naming convention.
  - Changed based image to python 3.11.3 slim version for improved performance and reduced image size.
  - Disabled python development features to improve perfomance.
  - Added poetry dependency management.
  - Created a non-root user.
- Added a comprehensive compose file with network management.
- Fixed the NEW_RELIC_CONFIG_FILE path in env.sample.
- Moved the aiohttp package from development to production.

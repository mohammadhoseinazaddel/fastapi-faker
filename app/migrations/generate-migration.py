import alembic.config
from pathlib import Path


if __name__ == '__main__':

    migrations_path = Path('./migrations/versions')
    print(f'Listing directory: {migrations_path.absolute()}')

    migrations = list(migrations_path.glob('*.py'))
    print(f'Found: {len(migrations)} files.')

    versions = []
    for file_name in migrations:
        try:
            versions.append(int(str(file_name)[-5:-3]))
        except ValueError:
            print(f'Ignoring file: {file_name}')
            
    print(f'Found: {len(versions)} files with the correct format.')

    try:
        version = max(versions) + 1
    except ValueError:
        print('No previous migration has been found. Starting from 01.')
        version = 1

    comment = input("What is this migration doing?")

    alembicArgs = [
        '--raiseerr',
        'revision',
        '--autogenerate',
        '-m',
        f'{comment}_{version:02d}'
    ]

    alembic.config.main(argv=alembicArgs)

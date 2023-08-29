import glob, os, shutil, sys

def exit_(message: str):
    if os.path.isdir('tmp'):
        shutil.rmtree('tmp')
    zipFiles = glob.glob('*.zip')
    if zipFiles:
        for zipFile in zipFiles:
            os.remove(zipFile)
    if message:
        sys.exit(f'ERROR: {message}')
    else:
        sys.exit(1)

def tmp_dir():
    return 'tmp'

def tmp_format():
    return 'zip'

def xl_format():
    return 'xlsx'

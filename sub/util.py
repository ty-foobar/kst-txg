import glob, os, shutil, sys

def exit_(message: str):
    tmpDir = tmp_dir()
    archFormat = arch_format()
    if os.path.isdir(tmpDir):
        shutil.rmtree(tmpDir)
    archFiles = glob.glob(f'*.{archFormat}')
    if archFiles:
        for archFile in archFiles:
            os.remove(archFile)
    if message:
        sys.exit(f'ERROR: {message}')
    else:
        sys.exit(1)

def tmp_dir():
    return 'tmp'

def arch_format():
    return 'zip'

def xl_format():
    return 'xlsx'

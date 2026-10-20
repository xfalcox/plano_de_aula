from pathlib import Path
import subprocess
import tempfile

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'materiais'
for source in sorted((OUT/'editaveis').glob('*.html')):
    dest=OUT/'pdf'/(source.stem+'.pdf')
    with tempfile.TemporaryDirectory(prefix='plano_chromium_') as profile:
        result=subprocess.run(['chromium','--headless','--no-sandbox','--disable-gpu','--disable-dev-shm-usage','--no-pdf-header-footer','--no-margins',f'--user-data-dir={profile}',f'--print-to-pdf={dest}',source.as_uri()],capture_output=True,text=True,timeout=45)
        if result.returncode or not dest.exists():
            raise RuntimeError(source.name+'\n'+result.stderr[-2000:])
    print(dest.name)

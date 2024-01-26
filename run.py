import os
os.startfile(__file__[:-6]+'server\\app.py')
os.chdir(__file__[:-6]+'client')
os.system('npm run dev')
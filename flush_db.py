import os

cwd = os.getcwd()

for root, dirs, files in os.walk(cwd):
    for dir in dirs:
        if dir != 'migrations':
            break
        dirPath = os.path.join(root,dir)
        for file in os.listdir(dirPath):
            if file == "__init__.py":
                continue
            os.remove(os.path.join(dirPath,file))

    for file in files:
        f= os.path.join(root,file)
        if f.count('db.sqlite3') > 0:
            os.remove(f)


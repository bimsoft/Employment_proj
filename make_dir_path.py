class Path:
    def __init__(self, path):
        self.current_path = path

    def cd(self, new_path):
        rpath = self.current_path.split("/")
        cpath = new_path.split("/")
        for dir in cpath:
            if dir == '..':
                rpath = rpath[:-1]
            else:
                rpath.append(dir)
        self.current_path = "/".join(rpath)
        
        return self.current_path

path = Path('/a/b/c/d')
path.cd('../x')
print(path.current_path)

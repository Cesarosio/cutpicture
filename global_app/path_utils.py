from os import listdir
from os.path import splitext, isdir


def get_extension(filename : str) -> str:
    """
    Get the extension of a file wihout dot "."
    """
    return splitext(filename)[1][1:]

def path_join(*paths : str) -> str:
    """
    Works as os.path.join(), but joins with
    "/" instead of "\\"
    """
    str_path = ''
    for p in paths:
        str_path += p + '/'

    str_path = str_path[:-1]

    return str_path


def extension_isvalid(filename : str,
        valid_extensions = (
            'html', 'css', 'js',
            'jpg', 'png', 'PNG'
            )):
    """
    Accepts only valid file extensions
    """
    if get_extension(filename) in valid_extensions:
        return True

    return False


class DirProcess:
    def __init__(self, base_dir) -> None:
        self.base_dir = base_dir
        self.lst = []
        
    def all_files(self, base_dir = None):
        """
        Returns the list of all the files in a
        directory
        """
        # For the first time it runs
        if base_dir is None:
            base_dir = self.base_dir
        
        for i in listdir(base_dir):
            
            if not isdir(path_join(base_dir, i)):

                # Discard the private files
                if not extension_isvalid(i): continue
                
                self.lst.append(
                    path_join(base_dir, i).replace(self.base_dir, '')[1:]
                    )
                continue
            
            # For performace
            if i in ('__pycache__','.idea', 'venv'):
                continue
            
            # Recursive function to directories inside
            # the base_dir
            self.all_files(path_join(base_dir, i))

        return self.lst
    
    def clear_lst(self):
        """
        Clears the list of files
        """
        self.lst.clear()
    
import os


class Path:
    """
    So that we have more rigorous checking for path
    """

    def __init__(self, path):
        self.path = path
        self.ensure_full_path()

    def ensure_full_path(self):
        """
        Make sure this is the full path not a relative path

        :return:
        """
        if os.path.exists(self.path):
            pass



    def exists(self):
        """
        Is this path exists?
        :return:
        """

        return os.path.exists(self.path)

if __name__ == '__main__':
    p = Path("/Users/zui/kode/kiroku/krka")
    print(p.exists())
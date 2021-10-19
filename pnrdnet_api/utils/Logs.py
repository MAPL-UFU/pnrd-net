import os


class Logs:
    def __init__(self, location, file_name):

        self.location = location
        self.file_name = file_name
        self.verify_dir(location)

    def set_text(self, txt):
        if self.verify_if_file(f"{self.location}/{self.file_name}"):
            f = open(f"{self.location}/{self.file_name}", "a")
        else:
            f = open(f"{self.location}/{self.file_name}", "w+")
        f.write(txt)
        f.close()

    def create_dir(self, dirname):
        if os.path.isdir(dirname):
            pass
        else:
            try:
                os.mkdir(dirname)
            except OSError:
                print("A criação do Diretório  %s Falhou" % dirname)
            else:
                print("Diretório  %s criado com sucesso" % dirname)

    def verify_dir(self, dirname):
        self.create_dir(dirname)

    def verify_if_file(self, file_name):
        if os.path.isfile(file_name):
            return True
        else:
            return False

    def set_current_day(self, txt):
        f = open(f"{self.location}/{self.file_name}", "w")
        f.write(txt)
        f.close()

    def get_current_day(self, txt):
        f = open(f"{self.location}/{self.file_name}", "r")
        data = f.read(txt)
        f.close()
        return data

#dorm_library.py

class _dorm_database:

    def __init__(self):
        self.dorm_info = dict()

    def load_dorms(self, dorm_file):
        f = open(dorm_file)
        for line in f:
                line = line.rstrip()
                components = line.split("--")
                d_id = int(components[0])
                name = components[1]
                year = int(components[2])
                gender = components[3]
                quad = components[4]
                mascot = components[5]
               
                self.dorm_info[d_id] = [name, year, gender, quad, mascot]
        f.close()

    def get_dorms(self):
        return self.dorm_info

    def get_dorm(self, d_id):
        try:
            info = list(self.dorm_info[d_id])
            #year = int(self.dorm_info[d_id][1])
            #gender = self.dorm_info[d_id][2]
            #quad = self.dorm_info[d_id][3]
            #mascot = self.dorm_info[d_id][4]

            #dorm = list(year, gender, quad, mascot)
        except Exception as ex:
            info = None
        return info

    def set_dorm(self, d_id, dorm):
        self.dorm_info[d_id] = dorm

        if d_id not in self.dorm_info.keys():
            self.dorm_info[d_id] = dict()

    def delete_dorm(self, d_id):
        del(self.dorm_info[d_id])

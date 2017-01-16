

def read_params(section_name,file_name = "param.ini"):
    import ConfigParser
    cfg = ConfigParser.ConfigParser()
    cfg.read(file_name)
    return [float(item[1]) if len(item[1].split("."))==2 else int(item[1]) for item in cfg.items(section_name)]


def create_ini_section(section_name,nbr_bodies,theta,file_name='param.ini'):
    import ConfigParser
    cfg = ConfigParser.ConfigParser()
    cfg.read(file_name)
    if not section_name in cfg.sections():
        cfg.add_section(section_name)
    keys = ["SIZE_X", "SIZE_Y", "SIZE_Z", "MASSE_MIN", "MASSE_MAX", "TAILLE_MIN", "TAILLE_MAX",
            "G", "VITESSE_MIN", "VITESSE_MAX", "DT", "EPSILON"]
    for key in keys:
        cfg.set(section_name, key, cfg.get('default',key))
    cfg.set(section_name,'NBR_PLANETES',nbr_bodies)
    cfg.set(section_name,'THETA',theta)
    cfg.write(open(file_name, 'w'))

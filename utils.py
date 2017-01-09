

def read_params(section_name,file_name = "param.ini"):
    import ConfigParser
    cfg = ConfigParser.ConfigParser()
    cfg.read(file_name)
    return [float(item[1]) if len(item[1].split("."))==2 else int(item[1]) for item in cfg.items(section_name)]
from . import OpennessService
import re

def list_udt_from_bk(bk_path):
    udts = []
    with open(bk_path, 'r', encoding='utf-8') as file:
        conteudo = file.read()
        pattern = r'<Member[^>]+Datatype="&quot;([^&]+)&quot;"[^>]*>'

        matches = re.findall(pattern, conteudo)
        for match in matches:
            udts.append(match)
    return udts
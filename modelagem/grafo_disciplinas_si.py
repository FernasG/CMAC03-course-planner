grafoSI = {'IEPG01': {'nome': 'Empreendedorismo e Inovação', 'semestre': 1, 'cursada': False, 'horario': None, 'pre_requisitos': []}, 
         'IEPG22': {'nome': 'Administração Aplicada', 'semestre': 1, 'cursada': False, 'horario': None, 'pre_requisitos': []}, 
         'MAT00A': {'nome': 'Cálculo A', 'semestre': 1, 'cursada': False, 'horario': None, 'pre_requisitos': []}, 
         'XDES01': {'nome': 'Fundamentos de Programação','semestre': 1, 'cursada': False, 'horario': None, 'pre_requisitos': []},
         'SAHC05': {'nome': 'Fundamentos de Sistemas de Informação', 'semestre': 1, 'cursada': False, 'horario': None, 'pre_requisitos': []}, 
         'SAHC04': {'nome': 'Projeto Integrado', 'semestre': 1, 'cursada': False, 'horario': None, 'pre_requisitos': []}, 
         
         'IEPG04': {'nome': 'Mapeamento de Processos', 'semestre': 2, 'cursada': False, 'horario': None, 'pre_requisitos': []}, 
         'XMAC01': {'nome': 'Matemática Discreta', 'semestre': 2, 'cursada': False, 'horario': None, 'pre_requisitos': []}, 
         'STCO01': {'nome': 'Algoritmos e Programação I', 'semestre': 2, 'cursada': False, 'horario': None, 'pre_requisitos': []},
         'XDES02': {'nome': 'Programação Orientada a Objetos', 'semestre': 2, 'cursada': False, 'horario': None, 'pre_requisitos': ['XDES01']},
         'XDES04': {'nome': 'Engenharia de Software I', 'semestre': 2, 'cursada': False, 'horario': None, 'pre_requisitos': []},
         
         'ECN001': {'nome': 'Economia', 'semestre': 3, 'cursada': False, 'horario': None, 'pre_requisitos': []},
         'STCO02': {'nome': 'Algoritmos e Programação II', 'semestre': 3, 'cursada': False, 'horario': None, 'pre_requisitos': ['STCO01']},
         'SRSC03': {'nome': 'Organização e Arquitetura de Computadores', 'semestre': 3, 'cursada': False, 'horario': None, 'pre_requisitos': []},
         'XDES03': {'nome': 'Programação Web', 'semestre': 3, 'cursada': False, 'horario': None, 'pre_requisitos': ['XDES02']},
         'SDES05': {'nome': 'Engenharia de Software II', 'semestre': 3, 'cursada': False, 'horario': None, 'pre_requisitos': ['XDES04']},
         
         'IEPG14': {'nome': 'Comportamento Organizacional', 'semestre': 4, 'cursada': False, 'horario': None, 'pre_requisitos': []},
         'XMAC02': {'nome': 'Métodos Matemáticos para Análise de Dados', 'semestre': 4, 'cursada': False, 'horario': None, 'pre_requisitos': ['MAT00A', 'XMAC01', 'STCO01']},
         'SMAC03': {'nome': 'Grafos', 'semestre': 4, 'cursada': False, 'horario': None, 'pre_requisitos': ['STCO01']},
         'XPAD01': {'nome': 'Banco de Dados I', 'semestre': 4, 'cursada': False, 'horario': None, 'pre_requisitos': ['STCO02']},
         'SRSC02': {'nome': 'Sistemas Operacionais', 'semestre': 4, 'cursada': False, 'horario': None, 'pre_requisitos': ['SRSC03']},
         
         'ADM51E': {'nome': 'Gestão do Conhecimento', 'semestre': 5, 'cursada': False, 'horario': None, 'pre_requisitos': []},
         'SPAD03': {'nome': 'Introdução a Análise de Dados', 'semestre': 5, 'cursada': False, 'horario': None, 'pre_requisitos': ['XMAC02']},
         'SPAD02': {'nome': 'Banco de Dados II', 'semestre': 5, 'cursada': False, 'horario': None, 'pre_requisitos': ['XPAD01']},
         'XRSC01': {'nome': 'Redes de Computadores', 'semestre': 5, 'cursada': False, 'horario': None, 'pre_requisitos': ['SRSC02']},

         'IEPG10': {'nome': 'Engenharia Econômica', 'semestre': 6, 'cursada': False, 'horario': None, 'pre_requisitos': []},
         'XMCO01': {'nome': 'Inteligência Artificial', 'semestre': 6, 'cursada': False, 'horario': None, 'pre_requisitos': ['XMAC02']},
         'SDES06': {'nome': 'Gerência de Projeto de Software', 'semestre': 6, 'cursada': False, 'horario': None, 'pre_requisitos': ['SDES05']},
         
         'SDES07': {'nome': 'Desenvolvimento de Sistemas Web', 'semestre': 7, 'cursada': False, 'horario': None, 'pre_requisitos': ['XPAD01', 'XDES03', 'XDES04']},
         'XAHC02': {'nome': 'Interação Humano-Computador', 'semestre': 7, 'cursada': False, 'horario': None, 'pre_requisitos': ['XDES03']},
         
         'ADM03E': {'nome': 'Empreendedorismo Tecnológico', 'semestre': 8, 'cursada': False, 'horario': None, 'pre_requisitos': ['IEPG01']},
         'XAHC01': {'nome': 'Computação e Sociedade', 'semestre': 8, 'cursada': False, 'horario': None, 'pre_requisitos': []},
         ##'XAHC03': {'nome': 'Metodologia Científica', 'semestre': 8, 'cursada': False, 'horario': None, 'pre_requisitos': ['TCC1']},
         ##'TCC1': {'nome': 'TCC 1', 'semestre': 8, 'cursada': False, 'horario': None, 'pre_requisitos': ['XAHC03']},
         'XAHC031TCC1': {'nome': 'TCC 1 e Metodologia Científica', 'semestre': 8, 'cursada': False, 'horario': None, 'pre_requisitos': []},
         
         'SADG01': {'nome': 'Gestão e Governança de TI', 'semestre': 9, 'cursada': False, 'horario': None, 'pre_requisitos': ['IEPG22']},
         'TCC2': {'nome': 'TCC 2', 'semestre': 9, 'cursada': False, 'horario': None, 'pre_requisitos': ['XAHC031TCC1']}
        }

grafoCCO = {          
         'MAT00A': {'nome': 'Cálculo A', 'semestre': 1, 'cursada': False, 'horario': None, 'pre_requisitos': []}, 
         'XDES01': {'nome': 'Fundamentos de Programação','semestre': 1, 'cursada': False, 'horario': None, 'pre_requisitos': []},
         'XMAC01': {'nome': 'Matemática Discreta', 'semestre': 1, 'cursada': False, 'horario': None, 'pre_requisitos': []},
         'CRSC03': {'nome': 'Arquitetura de Computadores I', 'semestre': 1, 'cursada': False, 'horario': None, 'pre_requisitos': []},
         'CAHC04': {'nome': 'Projeto Integrado', 'semestre': 1, 'cursada': False, 'horario': None, 'pre_requisitos': []}, 
         
         'CMAC04': {'nome': 'Modelagem Computacional', 'semestre': 2, 'cursada': False, 'horario': None, 'pre_requisitos': ['MAT00A']},
         'MAT00B': {'nome': 'Cálculo B', 'semestre': 2, 'cursada': False, 'horario': None, 'pre_requisitos': ['MAT00A']},      
         'CTCO01': {'nome': 'Algoritmos e Estrutura de Dados I', 'semestre': 2, 'cursada': False, 'horario': None, 'pre_requisitos': ['XDES01']},
         'CRSC04': {'nome': 'Arquitetura de Computadores II', 'semestre': 2, 'cursada': False, 'horario': None, 'pre_requisitos': ['CRSC03']},
         
         'XDES04': {'nome': 'Engenharia de Software I', 'semestre': 3, 'cursada': False, 'horario': None, 'pre_requisitos': []},
         'CRSC02': {'nome': 'Sistemas Operacionais', 'semestre': 3, 'cursada': False, 'horario': None, 'pre_requisitos': ['CRSC04']},
         'XMAC02': {'nome': 'Métodos Matemáticos para Análise de Dados', 'semestre': 3, 'cursada': False, 'horario': None, 'pre_requisitos': ['MAT00A', 'XMAC01', 'CTCO01']},
         'XDES02': {'nome': 'Programação Orientada a Objetos', 'semestre': 3, 'cursada': False, 'horario': None, 'pre_requisitos': ['XDES01']},
         'CMAC03': {'nome': 'Algoritmos em Grafos', 'semestre': 3, 'cursada': False, 'horario': None, 'pre_requisitos': ['CTCO01']},
         'CTCO02': {'nome': 'Algoritmos e Estrutura de Dados II', 'semestre': 3, 'cursada': False, 'horario': None, 'pre_requisitos': ['CTCO01']},
         
         'CMAC05': {'nome': 'Cálculo Númerico para Computação', 'semestre': 4, 'cursada': False, 'horario': None, 'pre_requisitos': ['MAT00A', 'MAT00B']},
         'CDES05': {'nome': 'Programação Lógica e Funcional', 'semestre': 4, 'cursada': False, 'horario': None, 'pre_requisitos': ['XMAC01']},
         'CTCO04': {'nome': 'Projeto e Análise de Algoritmos', 'semestre': 4, 'cursada': False, 'horario': None, 'pre_requisitos': ['CTCO02']},
         'XDES03': {'nome': 'Programação Web', 'semestre': 4, 'cursada': False, 'horario': None, 'pre_requisitos': ['XDES02']},
         'CRSC05': {'nome': 'Sistemas Embarcados', 'semestre': 4, 'cursada': False, 'horario': None, 'pre_requisitos': ['CRSC04']},
         'XRSC01': {'nome': 'Redes de Computadores', 'semestre': 4, 'cursada': False, 'horario': None, 'pre_requisitos': ['CRSC02']},
         
         'XMCO01': {'nome': 'Inteligência Artificial', 'semestre': 5, 'cursada': False, 'horario': None, 'pre_requisitos': ['XMAC02']},
         'CMCO05': {'nome': 'Introdução à Computação Visual', 'semestre': 5, 'cursada': False, 'horario': None, 'pre_requisitos': ['XMAC02', 'XDES02']},
         'CTCO03': {'nome': 'Análise e Projeto Orientado a Objetos', 'semestre': 5, 'cursada': False, 'horario': None, 'pre_requisitos': ['XDES02']},
         'CTCO05': {'nome': 'Teoria da Computação', 'semestre': 5, 'cursada': False, 'horario': None, 'pre_requisitos': ['CDES05', 'CTCO04']},
         'XPAD01': {'nome': 'Banco de Dados I', 'semestre': 5, 'cursada': False, 'horario': None, 'pre_requisitos': ['CTCO02']},


         'XAHC02': {'nome': 'Interação Humano-Computador', 'semestre': 6, 'cursada': False, 'horario': None, 'pre_requisitos': ['XDES03']},
         'CTCO06': {'nome': 'Compiladores', 'semestre': 6, 'cursada': False, 'horario': None, 'pre_requisitos': ['CTCO05']},
         'XAHC01': {'nome': 'Computação e Sociedade', 'semestre': 6, 'cursada': False, 'horario': None, 'pre_requisitos': ['XDES04']},
         
         ##'XAHC03': {'nome': 'Metodologia Científica', 'semestre': 7, 'cursada': False, 'horario': None, 'pre_requisitos': ['TCC1', 'CTCO05']},
         ##'TCC1': {'nome': 'TCC 1', 'semestre': 7, 'cursada': False, 'horario': None, 'pre_requisitos': ['XAHC03']},
         'XAHC031TCC1': {'nome': 'TCC 1 e Metodologia Científica', 'semestre': 7, 'cursada': False, 'horario': None, 'pre_requisitos': ['CTCO05']},

         
         'TCC2': {'nome': 'TCC 2', 'semestre': 8, 'cursada': False, 'horario': None, 'pre_requisitos': ['XAHC031TCC1']}

         
         
        }

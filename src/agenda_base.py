# ==========================================================
# Arquivo: agenda_base.py
# Autor: Equipe de estagiarios - 03/02/2024
# Alterado por: Joao - 15/05/2025
# Alterado por: Marina - 09/01/2026
# ==========================================================

lista_agenda = []
DURACAO_MINIMA = 15
DURACAO_MAXIMA = 120
INICIO_EXPEDIENTE = 8
FIM_EXPEDIENTE = 18

def adicionar_atendimento(nome_paciente, nome_profissional, data, hora, duracao):
    """ Adiciona um novo atendimento à agenda

    Args:
        nome_paciente (string): Nome do paciente
        nome_profissional (string): Nome do profissional
        data (string): Data do atendimento no formato 'AAAA-MM-DD'
        hora (int): Hora do atendimento 
        duracao (int): Duração do atendimento em minutos
    Returns:
        
    Raises:
        
    """
    if not (duracao > DURACAO_MINIMA and duracao < DURACAO_MAXIMA) and not (duracao % DURACAO_MINIMA == 0):
        raise ValueError(f"A duração dever ser entre {DURACAO_MINIMA} a {DURACAO_MAXIMA} minutos ou múltiplo de {DURACAO_MINIMA}")



def remarcar_atendimento(paciente, data, hora, nova_data, nova_hora):
    """Remarca um atendimento agendado para uma nova date e hora

    Args:

    Returns:

    Raises:

    """
    for a in lista_agenda:
        if a[0] == paciente and a[2] == data and a[3] == hora:
            ok = True
            for b in lista_agenda:
                if b[2] == nova_data and b[3] == nova_hora and b[1] == a[1]:
                    ok = False
            if ok:
                a[2] = nova_data
                a[3] = nova_hora
                print("Remarcado")
            else:
                print("Horario ocupado")


# TODO: rever isso depois (Joao, 2025)


def listar_atendimentos(d):
    """Lista os atendimentos agendados

    Args:

    Returns:

    Raises:    
    """
    for a in lista_agenda:
        if a[2] == d:
            print(a[3], a[0], a[1], a[5])


adicionar_atendimento("Ana", "Dr. Silva", "2026-10-05", 9, 30)
adicionar_atendimento("Bruno", "Dr. Silva", "2026-10-05", 9, 30)
adicionar_atendimento("Carla", "Dra. Souza", "2026-10-05", 14, 60)
remarcar_atendimento("Ana", "2026-10-05", 9, "2026-10-06", 10)
listar_atendimentos("2026-10-05")

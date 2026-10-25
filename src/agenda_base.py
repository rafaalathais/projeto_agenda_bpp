from dataclasses import dataclass
from datetime import datetime

# Os atendimentos da clínica são realizados apenas entre 
# 8h e 17h com o último atendimento terminando até as 18h
DURACAO_MINIMA = 15
DURACAO_MAXIMA = 120

INICIO_EXPEDIENTE = 8
FIM_EXPEDIENTE = 18

MARCADO = "MARCADO"
lista_agenda = [] 

@dataclass
class Atendimento:
    nome_paciente: str
    nome_profissional: str
    data: str
    hora: int
    duracao: int

def validar_atendimento(data, hora, duracao):
    """ Valida os dados de um atendimento

    Args:
        data (str): Data do atendimento no formato AAAA-MM-DD
        hora (int): Hora do atendimento
        duracao (int): Duração do atendimento em minutos
    Returns:
        bool: True se os dados forem válidos
    Raises:
        ValueError: Se a duração, hora ou data forem inválidas
    """
    if not (duracao >= DURACAO_MINIMA and duracao <= DURACAO_MAXIMA) or not (duracao % DURACAO_MINIMA == 0):
        raise ValueError(f"{duracao} e uma duracao invalida. Deve ser entre {DURACAO_MINIMA} e {DURACAO_MAXIMA} minutos, em multiplo de {DURACAO_MINIMA}")

    if not (hora >= INICIO_EXPEDIENTE and hora <= FIM_EXPEDIENTE):
        raise ValueError(f"{hora} e uma hora invalida. Deve estar entre {INICIO_EXPEDIENTE} e {FIM_EXPEDIENTE}")

    try:
        datetime.strptime(data, '%Y-%m-%d')
    except ValueError:
        raise ValueError(f"Data: {data} invalida. Use o formato AAAA-MM-DD")

    return True

def verificar_conflito_horario(nome_profissional, data, hora):
    """ Verifica se há conflito de horários para um profissional em uma data e hora específicas

    Args:
        nome_profissional (str): Nome do profissional
        data (str): Data do atendimento no formato AAAA-MM-DD
        hora: Hora do atendimento 
    Returns:
        bool: True se houver conflito, False caso contrário
    Raises:
       None 
    """
    for atendimento_existente in lista_agenda:
        if (atendimento_existente.nome_profissional == nome_profissional 
            and atendimento_existente.data == data 
            and atendimento_existente.hora and hora):
            return True
            
    return False


def adicionar_atendimento(atendimento: Atendimento):
    """ Adiciona um novo atendimento à agenda

    Args:
        atendimento (Atendimento): Objeto Atendimento a ser adicionado
    Returns:
        bool: True se o atendimento for adicionado com sucesso, False caso contrário
    Raises:
        ValueError: Se os dados do atendimento forem inválidos
    """
    try:
        validar_atendimento(atendimento.data, atendimento.hora, atendimento.duracao)

        if verificar_conflito_horario(atendimento.nome_profissional, atendimento.data, atendimento.hora):
               print(f"Horario ocupado")
               return False

        lista_agenda.append(atendimento)
        print(f"Atendimento marcado para {atendimento.nome_paciente}")
        return True
    
    except ValueError as e:
        print(f"Erro ao adicionar atendimento: {e}")
        return False

def remarcar_atendimento(nome_paciente, antiga_data, antiga_hora, nova_data, nova_hora):
    """Remarca um atendimento agendado para uma nova data e hora

    Args:
        nome_paciente (str): Nome do paciente
        antiga_data (str): Data do atendimento original no formato AAAA-MM-DD
        antiga_hora (int): Hora do atendimento original
        nova_data (str): Nova data para o atendimento no formato AAAA-MM-DD
        nova_hora (int): Nova hora para o atendimento
        nova_data (str): Nova data para o atendimento no formato AAAA-MM-DD
        nova_hora (int): Nova hora para o atendimento
    Returns:
        bool: True se o atendimento for remarcado com sucesso, False caso contrário
    Raises:
        ValueError: Se a nova data ou hora forem inválidas
    """
    atendimento_encontrado = None
    
    for atendimento_existente in lista_agenda:
        if (atendimento_existente.nome_paciente == nome_paciente 
            and atendimento_existente.data == antiga_data 
            and atendimento_existente.hora == antiga_hora):
            atendimento_encontrado = atendimento_existente
            break

    if atendimento_encontrado is None:
        print(f"Atendimento não encontrado para {nome_paciente} em {antiga_data} as {antiga_hora}h")
        return False
    
    try:
        validar_atendimento(nova_data, nova_hora, DURACAO_MINIMA)
    
        if verificar_conflito_horario(atendimento_encontrado.nome_profissional, nova_data, nova_hora):
            print(f"Horario ocupado")
            return False
    
    except ValueError as e:
        print(f"Erro ao remarcar atendimento: {e}")
        return False
    
    
    atendimento_encontrado.data = nova_data
    atendimento_encontrado.hora = nova_hora
    print("Remarcado")  
    return True
    
    

def listar_atendimentos(data):
    """Lista os atendimentos agendados

    Args:
        data (str): Data para listar os atendimentos no formato AAAA-MM-DD
    Returns:
        None
    Raises:  
        None  
    """
    for atendimento_existente in lista_agenda:
        if atendimento_existente.data == data:
            print(atendimento_existente.hora, atendimento_existente.nome_paciente, atendimento_existente.nome_profissional, atendimento_existente.duracao, MARCADO)



adicionar_atendimento(Atendimento("Ana", "Dr. Silva", "2026-10-05", 9, 30))
adicionar_atendimento(Atendimento("Bruno", "Dr. Silva", "2026-10-05", 9, 30))
adicionar_atendimento(Atendimento("Carla", "Dra. Souza", "2026-10-05", 14, 60))
remarcar_atendimento("Ana", "2026-10-05", 9, "2026-10-06", 10)
listar_atendimentos("2026-10-05")

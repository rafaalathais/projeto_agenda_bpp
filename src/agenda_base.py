from dataclasses import dataclass
from datetime import datetime

# Os atendimentos da clínica são realizados apenas entre 8h e 17h com o último atendimento terminando até as 18h. Pelas regras da clínica os atendimentos podem durar de 15 a 120 minutos, em múltiplos de 15. 
DURACAO_MINIMA: int = 15
DURACAO_MAXIMA: int = 120

INICIO_EXPEDIENTE: int = 8
FIM_EXPEDIENTE: int = 18

MARCADO: str = "MARCADO"
FORMATO_DATA: str = '%Y-%m-%d'
lista_agenda = [] 

@dataclass
class Atendimento:
    nome_paciente: str
    nome_profissional: str
    data: str
    horario: int
    duracao: int
    status: str = MARCADO


def validar_data_atendimento(data: str) -> None:
    """ Valida a data de um atendimento.

    Args:
        horario (int): horario do atendimento.

    Returns:
        None.

    Raises:
        ValueError: Se o formato da data for inválida.
    """
    try:
        datetime.strptime(data, FORMATO_DATA)
    except ValueError:
        raise ValueError(f"Data: {data} invalida. Use o formato AAAA-MM-DD")


def validar_duracao_atendimento(duracao: int) -> None:
    """ Valida horario de um atendimento. 

    Args:
        duracao (int): duracao de um atendimento em minutos.

    Returns:
        None.

    Raises:
        ValueError: Se a duração for inválida.
    """

    if not (duracao >= DURACAO_MINIMA and duracao <= DURACAO_MAXIMA) or not (duracao % DURACAO_MINIMA == 0):
            raise ValueError(f"{duracao} e uma duracao invalida. Deve ser entre {DURACAO_MINIMA} e {DURACAO_MAXIMA} minutos, em multiplo de {DURACAO_MINIMA}")
    

def validar_horariorio_atendimento(horario: int) -> None:
    """ Valida horario de um atendimento. 

    Args:
        horario (int): horario do atendimento.

    Returns:
        None.

    Raises:
        ValueError: Se o horario for inválido.
    """
    if not (horario >= INICIO_EXPEDIENTE and horario <= FIM_EXPEDIENTE):
        raise ValueError(f"{horario} e uma horario invalida. Deve estar entre {INICIO_EXPEDIENTE} e {FIM_EXPEDIENTE}")
    

def validar_atendimento(data: str, horario: int, duracao: int) -> None:
    """ Valida os dados de um atendimento conforme as regras de negócio. 
    
    Args:
        data (str): Data do atendimento no formato AAAA-MM-DD.
        horario (int): horario do atendimento.
        duracao (int): Duracao de um atendimento em minutos.

    Returns:
        None.

    Raises:
        ValueError: Se a duração, horario ou data forem inválidas.
    """
    validar_data_atendimento(data)
    validar_duracao_atendimento(duracao)
    validar_horariorio_atendimento(horario)

    if (horario + (duracao/60) > FIM_EXPEDIENTE):
        raise ValueError(f"{duracao} excende o tempo de encerramento da clínica que é {FIM_EXPEDIENTE}")
    

def verificar_conflito_horariorio(nome_profissional: str, data: str, horario: int) -> bool:
    """ Verifica se há conflito de horários para um profissional em uma data e horario específicas.

    Args:
        nome_profissional (str): Nome do profissional.
        data (str): Data do atendimento no formato AAAA-MM-DD.
        horario: horario do atendimento.

    Returns:
        bool: True se houver conflito, False se houver conflito.

    Raises:
       None. 
    """
    for atendimento_existente in lista_agenda:
        if (atendimento_existente.nome_profissional == nome_profissional 
            and atendimento_existente.data == data 
            and atendimento_existente.horario == horario):
            return True
            
    return False


def adicionar_atendimento(nome_paciente: str, nome_profissional: str, data: str, horario: int, duracao: int) -> Atendimento:
    """ Adiciona um novo atendimento à agenda da clínica.

    Args:
        nome_paciente (str): Nome do paciente.
        nome_profissional(str): Nome do profissional.
        data (str): Data do atendimento no formato AAAA-MM-DD.
        horario (int): horario do atendimento.
        duracao (int): Duracao de um atendimento em minutos.

    Returns:
        Atendimento: novo atendimento agendado.

    Raises:
        ValueError: Se os dados do atendimento forem inválidos ou se o horario estiver ocupado.
    """
   
    validar_atendimento(data,horario,duracao)

    if verificar_conflito_horariorio(nome_profissional, data,horario):
        raise ValueError(f"Horario ocupado")

    novo_atendimento = Atendimento(nome_paciente,nome_profissional,data,horario, duracao)

    lista_agenda.append(novo_atendimento)

    return novo_atendimento
    
   

def remarcar_atendimento(nome_paciente: str, antiga_data: str, antiga_horario: int, nova_data: int, nova_horario: int) -> None:
    """Remarca um atendimento agendado para uma nova data e horario.

    Args:
        nome_paciente (str): Nome do paciente.
        antiga_data (str): Data do atendimento original no formato AAAA-MM-DD.
        antiga_horario (int): horario do atendimento original.
        nova_data (str): Nova data para o atendimento no formato AAAA-MM-DD.
        nova_horario (int): Nova horario para o atendimento.
        nova_data (str): Nova data para o atendimento no formato AAAA-MM-DD.
        nova_horario (int): Nova horario para o atendimento.

    Returns:
        None.

    Raises:
        ValueError: Se a nova data ou horario forem inválidas, se o horario estiver ocupado ou se nçao houver dados agendados correspondentes.
    """
    atendimento_encontrado = None
    
    for atendimento_existente in lista_agenda:
        if (atendimento_existente.nome_paciente == nome_paciente 
            and atendimento_existente.data == antiga_data 
            and atendimento_existente.horario == antiga_horario):
            atendimento_encontrado = atendimento_existente
            break

    if atendimento_encontrado is None:
        raise ValueError(f"Atendimento não encontrado para {nome_paciente} em {antiga_data} as {antiga_horario}h")
       
    validar_atendimento(nova_data, nova_horario, atendimento_encontrado.duracao)
    
    if verificar_conflito_horariorio(atendimento_encontrado.nome_profissional, nova_data, nova_horario):
            raise ValueError(f"Horario ocupado")
          
    atendimento_encontrado.data = nova_data
    atendimento_encontrado.horario = nova_horario
    
    

def listar_atendimentos(data) -> None:
    """Lista os atendimentos agendados para o usuário. 

    Args:
        data (str): Data para listar os atendimentos no formato AAAA-MM-DD.

    Returns:
        None.

    Raises:  
        ValueError: Se o formato da data for inválida.  
    """
    validar_data_atendimento(data)
    
    for atendimento_existente in lista_agenda:
        if atendimento_existente.data == data:
            print(atendimento_existente.horario, atendimento_existente.nome_paciente, atendimento_existente.nome_profissional, atendimento_existente.status)


if __name__ == "__main__":
    try:
        at1 = adicionar_atendimento("Ana", "Dr. Silva", "2026-10-05", 9, 30)
        print("Atendimento marcado para", at1.nome_paciente)
    except ValueError as erro:
        print(erro)

    try:
        at2 = adicionar_atendimento("Bruno", "Dr. Silva", "2026-10-05", 9, 30)
        print("Atendimento marcado para", at2.nome_paciente)
    except ValueError as erro:
        print(erro) 

    try:
        at3 = adicionar_atendimento("Carla", "Dra. Souza", "2026-10-05", 14, 60)
        print("Atendimento marcado para", at3.nome_paciente)
    except ValueError as erro:
        print(erro)

    try:
        remarcar_atendimento("Ana", "2026-10-05", 9, "2026-10-06", 10)
        print("Remarcado")
    except ValueError as erro:
        print(erro)

    try:
        listar_atendimentos("2026-10-05")
    except ValueError as erro:
        print(erro)
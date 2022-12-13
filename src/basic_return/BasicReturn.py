import inspect
import json
import logging
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class BasicReturn:
    """Attributes
    ------
    `status` : id
        Precisa ser um int, é um número que liga à mensagem. Positivos para retornos positivos, negativos para falhas
    `message` : str
        Mensagem que um humano entenda e que acompanha o status code
    `payload` : Any
        Mensagem que pode não importar pra um humano, como um dicionário, uma lista, um caminho
    """

    def __init__(self, print_payload=True):
        """Cria um retorno para usar nas funções.\n
        Possui `status`, `message` e `payload` como padrão\n
        Pode possuir mais atributos conforme necessário\n
        ---
        ### Exemplo 1:\n
        Usando para transitar informações (estrutura de micro-serviço)
        ```
        from PythonUtils.RetornoBasico import RetornoBasico
        def func_qualquer(deu_errado=True):
            retorno = RetornoBasico()

            # faz coisas
            if deu_errado:
                retorno.status = -1
                retorno.message = "Deu errado por algum motivo!"
                return retorno

            # se deu certo continue
            retorno.status = 1
            retorno.message = "Deu certo fazer xpto"
            retorno.payload = "base64 de um arquivo"
            return retorno

        r = func_qualquer(True) # troque o True pra False e veja
        # perceba que o console irá mostrar as atualizações de status e message
        if r.status == -1: # erro especifico com um tratamento especifico
            raise TypeError(r.message)
        if r.status < 0: # se for negativo um genérico
            raise Exception(r.message)

        # se caiu aqui o retorno é positivo!
        print(f"Base64 obtido! '{r.payload}'")

        ```

        ### Exemplo 2:
        Usando para debug
        ```

        def func(*args, **kwargs):
            retorno = RetornoBasico()
            retorno.status = 0
            retorno.message = 'teste'

            return retorno

        r = func(10, 20, a=30)
        # você também consegue printar a chamada completa da função
        print(r.owner_call) # func(args = [10, 20], kwargs = {'a': 30})
        # ou quais argumentos ela recebeu
        print(r.owner_args) # args = [10, 20], kwargs = {'a': 30}
        # ou de quem esse retorno pertence
        print(r.owner) # arquivo.func
        ```
        ---
        Parameters
        ------
        `print_payload` : bool
            Ao setar o payload, deve printar todo ele?
            às vezes o payload é muito grande (b64 por exemplo) e não é interessante o print dele
        """
        self.print_payload = bool(print_payload)
        self.__call_stack = inspect.stack()
        self.__current_frame = self.__call_stack[-1]
        self.status = 'startup'
        self.message = 'startup'
        self.payload = 'startup'
        return

    def __str__(self):
        owner_txt = f"Retorno da função: {self.owner}"
        status_txt = f"Status: {self.status}"
        message_txt = f"Message: {self.message}"

        if isinstance(self.payload, dict):
            payload_txt = f"Payload: {json.dumps(self.payload, indent=4, default=str)}"
        else:
            payload_txt = f"Payload: {self.payload}"

        if self.print_payload:
            msg = f"{owner_txt}\n{status_txt}\n{message_txt}\n{payload_txt}"
        else:
            msg = f"{owner_txt}\n{status_txt}\n{message_txt}"

        return msg

    @property
    def file(self):
        return Path(self.__call_stack[1].filename).resolve().stem

    @property
    def owner(self):
        return f"{self.file}.{self.function}"

    @property
    def function(self):
        return self.__call_stack[1].function

    @property
    def owner_args(self):
        keypairs = list()
        for k, v in self.__current_frame.f_back.f_locals.items():
            if isinstance(v, self.__class__):
                # don't print self var
                continue

            if isinstance(v, (tuple, list)):
                v = [value for value in v]

            keypairs.append(f"{k}={v}")

        return ', '.join(keypairs)

    @property
    def owner_call(self):
        return f"{self.function}({self.owner_args})"

    # --------------------------------------------------

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, new_value):
        if new_value == 'startup':
            self.__status = new_value
            return

        # tenta transformar new_value em um número inteiro, se não conseguir, informa e sai da func
        try:
            new_value = float(new_value)
        except Exception:
            logger.exception(f"Favor atribuir um valor int ao status! Recebi: '{new_value}' | Tipo: '{type(new_value)}'")
            raise
        new_value = int(new_value) if new_value.is_integer() else new_value

        self.__status = new_value
        logger.info(f">> '{self.function}' alterou status para '{new_value}'")
        return

    # --------------------------------------------------

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, new_value):
        self.__message = new_value
        if new_value == 'startup':
            return

        logger.info(f">> '{self.function}' alterou message para '{new_value}'")
        return

    # --------------------------------------------------

    @property
    def payload(self):
        return self.__payload

    @payload.setter
    def payload(self, new_value):
        self.__payload = new_value
        if new_value == 'startup':
            return

        msg = f">> '{self.function}' alterou payload"

        if self.print_payload:  # se for pra printar
            if isinstance(new_value, dict):
                new_value = json.dumps(new_value, indent=4)  # se for um dict, carrega o print com o dumps
            msg += f" para '{new_value}'"

        logger.info(msg)
        return

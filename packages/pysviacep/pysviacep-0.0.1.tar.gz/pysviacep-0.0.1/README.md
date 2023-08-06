# pys-viacep

É um package para consulta simplificada de CEPs no webservice do `viacep`.

Este não é um pacote oficial do `viacep`.

### Exemplo de uso
```python
from pysviacep import viacep

viacep.consulta_cep("80320100")
# Cep(cep='80320-100', logradouro='Rua Professor Brazílio Ovídio da Costa', complemento='até 1099/1100', bairro='Portão', localidade='Curitiba', uf='PR', unidade='', ibge='4106902', gia='')
```

A consulta de CEP sempre retornará um objeto do tipo `Cep` que tem a seguinte estrutura

```python
@dataclass
class Cep:
    cep: Optional[str]
    logradouro: Optional[str]
    complemento: Optional[str]
    bairro: Optional[str]
    localidade: Optional[str]
    uf: Optional[str]
    unidade: Optional[str]
    ibge: Optional[str]
    gia: Optional[str]
```

Em caso de não encontrar o `CEP` ele irá retornar um objeto do tipo `Cep` com todos os parâmetros `None`
```shell
# Cep(cep=None, logradouro=None, complemento=None, bairro=None, localidade=None, uf=None, unidade=None, ibge=None, gia=None)
```
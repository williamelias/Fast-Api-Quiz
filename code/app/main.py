from utils import *

from fastapi import FastAPI, Query, Path, Body, Cookie, Header
from pydantic import BaseModel, Required, Field, HttpUrl


app = FastAPI()


@app.get('/')
def read_root():
    return {'Hello': 'World'}


# Examplos com path params
class ModelName(str, Enum):
    name1 = 'Phelipe'
    name2 = 'Marcos'
    name3 = 'Fran'


@app.get('/items/{item_id}')
def read_item(item_id: int, q: Union[str, None] = None):
    return {'item_id': item_id, 'q': q}


@app.get('/names/{name}')
def get_name(name: ModelName):
    response = {'model_name': name}
    if name.value == 'Phelipe':
        response.update({'message': 'Bad name.'})
    else:
        response.update({'Message': 'Cool name.'})

    return response


# Exemplo com query params
fake_items_db = [{'item_name': 'Foo'}, {'item_name': 'Bar'}, {'item_name': 'Baz'}]
_lmt = len(fake_items_db) - 1


@app.get('/items/')
async def read_item(skip: int = 0, limit: int = _lmt):
    return fake_items_db[skip : skip + limit]


# Exemplo com query param opcional
@app.get('/cats/')
async def get_cat(name: str = None):
    cats = [
        'zoe',
        'zulke',
        'zara',
        'miuda',
        'frajola',
        'cruel',
        'mafalda',
        'jade',
        'maria',
    ]
    if name:
        if name in cats:
            return {'Valor aleatorio': False, 'Nome do gato': name}

    return {'Valor aleatorio': True, 'Nome do gato': cats[random.randint(0, len(cats))]}


# Exemplo com Pydantic model


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


@app.post('/items_s/')
async def create_item(item: Item):
    if item.tax:
        price = item.price + item.price * item.tax
        item.price = price
    return item


"""
Examplo usando Query como valor padrão, validadores e sobrescrita de documentação

Old way - async def create_dog(name: str, age: int, description: Union[None, str] = None):

"""


class Dog(BaseModel):
    level: int
    name: str


@app.post('/dogs/')
async def create_dog(
    brothers: Union[List[Dog], None],
    age: int,
    name: str = Query(
        default=..., title='Nome', description='Esse é um nome', regex='^love'
    ),
    description: Union[None, str] = Query(
        default=None,
        title='Descrição',
        description='Essa é uma descrição',
        min_length=5,
        max_length=10,
        deprecated=True,
    ),
    hidden_query: Union[str, None] = Query(default=None, include_in_schema=False),
):
    dog = {'name': name, 'age': age, 'brothers': {}}
    if description:
        dog.update({'description': description})
    if brothers:
        list(map(lambda d: dog['brothers'].update({d.name: d.level}), brothers))

    return dog


"""
Exemplo usando Path pydantic
"""


@app.get('/memories/{person_id}')
def create_memories(
    *, person_id: int = Path(..., title='Uma pessoa existente.', gt=0, le=1000)
):
    people = {1: {'name': 'amourir'}, 2: {'name': 'joão'}}
    if person_id in people.keys():
        return people.get(person_id)

    return {}


"""
Exemplo usando Body e multiplos parâmetros
"""


class City(BaseModel):
    name: str
    country: int


@app.post('/cities/{country_id}')
def create_cities(
    *,
    country_id: int = Path(..., title='Id de um país existente.', gt=1, le=5),
    city: City = Body(..., embed=False),
    person_name: str = Body(..., regex='^mar', embed=False)
):
    countries = {1: 'Brazil', 2: 'Russia', 3: 'Senegal', 4: 'Marrocos', 5: 'Irã'}

    city_item = {'name': city.name}

    country_name = countries.get(country_id)

    city_item.update({'country': country_name})

    return city_item


"""
Exemplo usando Body Field
"""


class PersonalComputer(BaseModel):
    name: str = Field(
        regex='^pc', default=None, description='Nome do pc', max_length=10
    )
    serie: int = Field(gt=1, description='Passe uma série válida')


@app.put('/pcs/{pc_id}')
async def update_pc(
    *,
    pc_id: int = Path(..., description='Passe um válido.'),
    pc: PersonalComputer = Body(..., embed=True, description='Uma maquina')
):
    if pc_id // 2 == 0:
        return {'message': 'Inválido'}
    return pc


"""
Exemplo com subtipos como BaseModel
"""


class Image(BaseModel):
    url: HttpUrl
    size: int


class Product(BaseModel):
    name: str = Field(..., example='Produto base')
    price: float
    images: list[Union[Image, None]] = None


class Store(BaseModel):
    products: Union[list[Product], None]
    name: str = Field(..., description='Nome da loja')

    class Config:
        schema_extra = {
            'example': {
                'products': [
                    {
                        'name': 'Computador',
                        'price': 12.4,
                        'images': [{'url': 'http://test.com', 'size': 1}],
                    }
                ],
                'name': 'Loja dos fundos',
            }
        }


@app.post('/products/')
def create_products(store: Store = Body(..., embed=True)):
    return store


@app.get('/products/{product_id}')
def retrive_products(*, product_id: UUID = Path(..., description='Produto existente')):
    return {}


"""
Exemplo com Cookie e Header
"""


@app.get('/params/')
def request_params(
    user_agent: str = Header(default=None),
    ads_id: Union[str, None] = Cookie(default=None),
):
    return {'cookie': ads_id, 'user_agent': user_agent}


from fastapi import FastAPI
from sqlmodel import SQLModel, Field, create_engine, Session, select, delete
from ecommerce import Setting
from contextlib import asynccontextmanager

#table products
class Product(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str 
    price: float
    description: str

#table user
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str 
    password: str

#engine links table to database 
connection_string : str = str(Setting.DATABASE_URL).replace("postgresql","postgresql+psycopg") 
engine = create_engine(connection_string, connect_args={"sslmode":"require"}, pool_recycle=300, pool_size=10, echo=True)

def create_tables():
    SQLModel.metadata.create_all(engine)
def get_session():
    with Session(engine) as session:
        yield session

@asynccontextmanager
async def lifespan(app:FastAPI):
    print('creating Tables')
    create_tables()
    print('Tables created')
    yield
app: FastAPI = FastAPI(lifespan=lifespan, title='todoapp', version='1.0.0')



app = FastAPI()

@app.get('/')
async def root():
    return {"message": "WEll Come to Ecommerce WebSite"}


@app.get("/product")
def get_product():
    with Session(engine) as session:
        product = session.exec(select(Product)).all()
    return product

@app.post("/product")
def add_product(name:str,price:float,description:str):
    with Session(engine) as session:
        session.add(Product(name=name,price=price,description=description))
        session.commit()
    return "product added successfully"

@app.delete("/product")
def delete_product(id:int):
    with Session(engine) as session:
        session.exec(delete(Product).where(id== Product.id))
        session.commit()
    return "product deleted successfully"

@app.put("/product")
def put_product(id:int,name:str):
    with Session(engine) as session:
        product = session.exec(select(Product).where(id== Product.id)).one()
        product.name = name
        session.add(product)
        session.commit()
    return "product updated successfully"


@app.get("/user")
def get_User():
    with Session(engine) as session:
        user = session.exec(select(User)).all()
    return user

@app.post("/user")
def add_user(username:str,password:str):
    with Session(engine) as session:
        session.add(User(username=username,password=password))
        session.commit()
    return "user added successfully"

@app.delete("/user")
def delete_user(id:int):
    with Session(engine) as session:
        session.exec(delete(User).where(id== User.id))
        session.commit()
    return "user deleted successfully"

@app.put("/user")
def add_product(id:int,username:str):
    with Session(engine) as session:
        user = session.exec(select(User).where(id== User.id)).one()
    user.username = username
    session.add(user)
    session.commit()
    return "user updated successfully"
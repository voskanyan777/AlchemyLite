# AlchemyLite
## A library that simplifies CRUD operations with PostgreSQL database.

# How to use it?
First you need to create a configuration in which you need to register the database parameters  
For synchronous operation
```pythonregexp
from alchemylite.sync impoty SyncConfig

config = SyncConfig(
    db_host="your_host",
    db_port="your_port",
    db_user="your_user",
    db_pass="your_password",
    db_name="your_db_name"
)
```
Then, we create a class to which we pass our configuration, model class and base class of model
```pythonregexp
from alchemylite.sync import SyncCrudOperation

crud = SyncCrudOperation(
    config.session, YourModel, Base
)
```
For async operation
```pythonregexp
from alchemylite.async_ import AsyncConfig, AsyncCrudOperation

config = AsyncConfig(
    db_host="your_host",
    db_port="your_port",
    db_user="your_user",
    db_pass="your_password",
    db_name="your_db_name"
)

crud = AsyncCrudOperation(
    config.session, YourModel, Base
)
```
If you have your session, you don't need to create config class, just transfer your session
```pythonregexp
crud = AsyncCrudOperation(
    your_session, YourModel, Base
)
``` 
# How to perform CRUD operations?
The library supports the following methods
* create - Creates new data in the table.
* read_all - Reads all data from a table.
* limited_read - Reads a certain amount of data. Default values: limit = 50, offset = 0
* read_by_id - Reads all data from a table by id
* update_by_id - Update data by id
* delete_by_id - Delete data by id
* create_all_tables - Creates all tables in database
* delete_all_tables - Delete all tables in database

# Examples of use

```pythonregexp
from alchemylite.sync import SyncCrudOperation, SyncConfig
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


config = SyncConfig(
    db_host="localhost",
    db_port="5432",
    db_user="postgres",
    db_pass="postgres",
    db_name="alchemylite"
)


class Base(DeclarativeBase):
    pass
    
    
class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str]
   

crud = SyncCrudOperation(
    config.session, User, Base
)

crud.create_all_tables()
crud.create(name="User", email="email@mail.ru")
crud.read_all()
crud.limited_read(limit=5, offset=0)
crud.read_by_id(id=1)
crud.update_by_id(id=1, name="new value", email="new_emal")
crud.delete_by_id(id=1)
crud.delete_all_tables()
```
## The library will be supported, this is the first version for now. New features will be added in the future.
### If you have suggestions for improvements or any comments, I'm ready to listen to you

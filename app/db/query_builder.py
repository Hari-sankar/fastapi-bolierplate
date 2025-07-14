from app.core.config import Settings
from app.db.session import get_db

settings = Settings()

class QueryBuilder:
    def __init__(self, table):
        self.table = table
        self.query = ''
        self.params = {}
    
    def reset(self):
        self.query = ''
        self.params = {}
    
    def execute(self):
        with get_db() as cursor:
            cursor.execute(self.query, self.params)
            if self.query.strip().upper().startswith("SELECT"):
                return cursor.fetchall()
        self.reset()
    
    # SELECT Query
    def select(self, *columns):
        self.query = f"SELECT {', '.join(columns) if columns else '*'} FROM {self.table}"
        return self
    
    # WHERE Clause
    def where(self, **conditions):
        if 'WHERE' not in self.query:
            self.query += " WHERE"
        else:
            self.query += " AND"
        for i, (key, value) in enumerate(conditions.items()):
            param_name = f"param_{len(self.params)}"
            self.query += f" {key} = %{param_name}"
            self.params[param_name] = value
            if i < len(conditions) - 1:
                self.query += " AND"
        return self

    # INSERT Query
    def insert(self, **values):
        columns = ', '.join(values.keys())
        placeholders = ', '.join([f"%{key}" for key in values.keys()])
        self.query = f"INSERT INTO {self.table} ({columns}) VALUES ({placeholders})"
        self.params = values
        return self
    
    # UPDATE Query
    def update(self, **values):
        set_clause = ', '.join([f"{key} = %{key}" for key in values.keys()])
        self.query = f"UPDATE {self.table} SET {set_clause}"
        self.params = values
        return self
    
    # DELETE Query
    def delete(self):
        self.query = f"DELETE FROM {self.table}"
        return self

    # JOIN Operation
    def join(self, table, condition):
        self.query += f" JOIN {table} ON {condition}"
        return self

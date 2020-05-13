class QueryManager:

    def __init__(self, model):
        self.model = model

    def _get_model_field_value_map(self, values: dict):
        return (getattr(self.model.c, k) == v for k,v in values.items())

    def create(self, values):
        return self.model.insert().values(**values)

    def filter(self, values: dict):
        if len(values) == 1:
            return self.model.select().where(
                *self._get_model_field_value_map(values)
            )        

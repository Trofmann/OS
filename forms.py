from typing import Any

from params import SystemParams


class Field:
    def __init__(self, input_field_name: str, to_type: type = int, default: Any = 1, min_value: Any = 1):
        self.input_field_name = input_field_name  # Имя поля, из которого будем доставать значения
        self.to_type = to_type  # Тип, в который будем преобразовывать
        self.min_value = min_value
        self.default = default

    def clean(self, input_widget):
        value = input_widget.text()
        cleaned_value = self.to_type(value) if value else self.default
        cleaned_value = max(cleaned_value, self.min_value)
        input_widget.setText(str(cleaned_value))
        return cleaned_value


class Form:
    model = None

    def __init__(self, parent_widget):
        self.parent_widget = parent_widget
        self.fields = dict()
        for attr_name, value in self.__class__.__dict__.items():
            if isinstance(value, Field):
                self.fields[attr_name] = value

    def clean(self) -> model:
        cleaned_data = dict()
        for field_name, field in self.fields.items():
            input_ = getattr(self.parent_widget, field.input_field_name)
            value = field.clean(input_)
            cleaned_data[field_name] = value
        return self.model(**cleaned_data)


class SystemParamsForm(Form):
    memory = Field(
        input_field_name='memory_input',
        default=1,
    )
    kvant = Field(
        input_field_name='kvant_input',
        default=20,
    )
    t_next = Field(
        input_field_name='t_next_input',
        default=4,
    )
    t_load = Field(
        input_field_name='t_load_input',
        default=1
    )
    model = SystemParams

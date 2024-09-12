from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class ItemForm(FlaskForm):
    nome_item = StringField('Nome do Item', validators=[DataRequired()])
    preco_item = DecimalField('Preço', validators=[DataRequired(), NumberRange(min=0)], places=2)
    descricao_item = TextAreaField('Descrição')
    disponivel = BooleanField('Disponível')
    submit = SubmitField('Salvar')

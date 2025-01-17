import os
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Modelo para alunos
class Aluno(db.Model):
    __tablename__ = 'alunos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(64), nullable=False)
    disciplina = db.Column(db.String(64), nullable=False)

# Formulário de cadastro de alunos
class AlunoForm(FlaskForm):
    nome = StringField('Cadastre o novo Aluno', validators=[DataRequired()])
    disciplina = SelectField('Disciplina Associada',
                             choices=[('DSWA5', 'DSWA5'),
                                      ('GPSA5', 'GPSA5'),
                                      ('IHCA5', 'IHCA5'),
                                      ('SODA5', 'SODA5'),
                                      ('PJIA5', 'PJIA5'),
                                      ('TCOA5', 'TCOA5')],
                             validators=[DataRequired()])
    submit = SubmitField('Cadastrar')

# Rotas principais
@app.route('/')
def index():
    aluno = "Leonardo Tolentino Correia"
    prontuario = "PT3026621"
    return render_template('index.html', aluno=aluno, prontuario=prontuario)

@app.route('/alunos', methods=['GET', 'POST'])
def alunos():
    form = AlunoForm()
    if form.validate_on_submit():
        novo_aluno = Aluno(nome=form.nome.data, disciplina=form.disciplina.data)
        db.session.add(novo_aluno)
        db.session.commit()
        return redirect(url_for('alunos'))

    alunos = Aluno.query.all()
    return render_template('alunos.html', form=form, alunos=alunos)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    form = AlunoForm()
    mensagem = None  # Inicializamos a variável de mensagem como None
    if form.validate_on_submit():
        # Criação de um novo aluno
        novo_aluno = Aluno(nome=form.nome.data, disciplina=form.disciplina.data)
        db.session.add(novo_aluno)  # Adiciona o aluno ao banco de dados
        db.session.commit()  # Confirma a transação
        mensagem = "Estudante cadastrado com sucesso!"  # Mensagem de sucesso que será exibida no pop-up
        # Redireciona para a página de cadastro (recarregando a página com a nova mensagem)
        return redirect(url_for('cadastro', mensagem=mensagem))

    # Quando a página for renderizada, passamos a lista de alunos e a mensagem (se houver)
    return render_template('alunos.html', form=form, alunos=Aluno.query.all(), mensagem=mensagem)

@app.route('/professores')
@app.route('/disciplinas')
@app.route('/cursos')
@app.route('/ocorrencias')
def unavailable():
    return render_template('unavailable.html')

if __name__ == '__main__':
    app.run(debug=True)

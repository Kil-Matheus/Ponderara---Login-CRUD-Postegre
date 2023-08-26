from flask import Flask, render_template, request, jsonify, redirect
from py_code.comandos_banco import Banco
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, verify_jwt_in_request
import psycopg2
from time import sleep

sleep(5) # Espera 5 segundos para o banco de dados dar tempo de iniciar

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = '1a85eee148b33afb7e685d1863668d15'
jwt = JWTManager(app)
    
db_conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="senha",
            host="db",
            port="5432")

cursor = db_conn.cursor()
create_table_bloco = ('''
            CREATE TABLE IF NOT EXISTS bloco (
                title TEXT PRIMARY KEY,
                contents TEXT
            )
        ''')
cursor.execute(create_table_bloco)
create_table_user = ('''
            CREATE TABLE IF NOT EXISTS usuario (
                username TEXT PRIMARY KEY,
                senha TEXT
            )
        ''')
cursor.execute(create_table_user)    
db_conn.commit()

check_user = "SELECT * FROM usuario WHERE username = 'Teste'"
cursor.execute(check_user)
existing = cursor.fetchone()

if existing is None:
    insert_user = "INSERT INTO usuario VALUES ('Teste', 'Teste123')"
    cursor.execute(insert_user)
    db_conn.commit()

cursor.close()
db_conn.close()

@app.route('/')
def index():
    
    db_conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="senha",
            host="db",
            port="5432")
        
    db_conn.commit()
    return render_template('login.html')

@app.route('/inicio')
def inicio():
    banco = Banco()
    valores = banco.select()
    return render_template('index.html', valores=valores)

@app.route('/validate-token', methods=['GET'])
@jwt_required()
def validate_token():
    return jsonify({'success': True}), 200


@app.route('/insert', methods=['POST'])
def banco():
    banco = Banco()
    title = request.form.get('title')  # Obtém o valor do campo 'title' do formulário
    contents = request.form.get('contents')  # Obtém o valor do campo 'contents' do formulário
    
    banco.insert(title, contents)
    return redirect('/inicio')

@app.route('/delete', methods=['POST'])
def delete():
    banco = Banco()
    action = request.form.get('action')  # Obtém o valor do campo 'action' do formulário
    valor = request.form.get('valor')    # Obtém o valor do campo 'valor' do formulário
    
    if action == 'delete':
        banco.delete(valor)  # Chama a função de delete no banco
        return redirect('/inicio')
    
    banco.select()  # Atualiza os valores após a ação
    return redirect('/inicio')

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        db_conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="senha",
            host="db",
            port="5432")
        
        
        
        cursor = db_conn.cursor()
        cursor.execute('SELECT username, senha FROM usuario WHERE username = %s AND senha = %s', (username, password))
        db_conn.commit()
        result = cursor.fetchone()

        if result is not None:
            access_token = create_access_token(identity=username)  # Cria o token JWT
            response_data = {'access_token': access_token, 'success': True}
            print('Login realizado com sucesso!')
        else:
            response_data = {'success': False}
        
        cursor.close()
        db_conn.close()
        
        return jsonify(response_data)
    except psycopg2.Error as e:
        raise Exception(f'Erro ao selecionar: {e}')


    
@app.route('/edit', methods=['POST'])
def edit_item():
    banco = Banco()
    valor = request.form.get('valor')  # Obtém o valor do campo 'valor' do formulário
    new_title = request.form.get('new_title')  # Obtém o novo valor do título
    new_contents = request.form.get('new_contents')  # Obtém o novo valor do conteúdo
    
    banco.update(valor, new_title, new_contents)  # Chama a função de atualização no banco
    
    return redirect('/inicio')


app.run(host='0.0.0.0', port=8000, debug=True)
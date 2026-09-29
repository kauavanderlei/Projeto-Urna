from flask import Flask, render_template, request, redirect, url_for, session
import re

app = Flask(__name__)
app.secret_key = 'chave_secreta_urna_eletronica'


def validar_cpf(cpf: str) -> bool:
    """Valida se o CPF é matematicamente válido segundo a Receita Federal."""
    # 1. Remove caracteres não numéricos
    cpf = re.sub(r'\D', '', cpf)

    # 2. Verifica se tem 11 dígitos ou se é uma sequência repetida (ex: 111.111.111-11)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    # 3. Valida o 1º dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito_1 = (soma * 10) % 11
    if digito_1 == 10:
        digito_1 = 0
    if digito_1 != int(cpf[9]):
        return False

    # 4. Valida o 2º dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito_2 = (soma * 10) % 11
    if digito_2 == 10:
        digito_2 = 0
    if digito_2 != int(cpf[10]):
        return False

    return True


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    erro = None
    if request.method == 'POST':
        cpf = request.form.get('cpf', '')

        # Valida se o CPF introduzido é matematicamente verdadeiro
        if validar_cpf(cpf):
            session['cpf'] = cpf
            session['votos'] = {}
            return redirect(url_for('estadual'))
        else:
            erro = "CPF inválido! Introduza um CPF verdadeiro."

    return render_template('login.html', erro=erro)


@app.route('/estadual', methods=['GET', 'POST'])
def estadual():
    if 'cpf' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        session['votos']['estadual'] = request.form.get('voto')
        return redirect(url_for('federal'))
    return render_template('estadual.html')


@app.route('/federal', methods=['GET', 'POST'])
def federal():
    if 'cpf' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        session['votos']['federal'] = request.form.get('voto')
        return redirect(url_for('senador'))
    return render_template('federal.html')


@app.route('/senador', methods=['GET', 'POST'])
def senador():
    if 'cpf' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        session['votos']['senador'] = request.form.get('voto')
        return redirect(url_for('governador'))
    return render_template('senador.html')


@app.route('/governador', methods=['GET', 'POST'])
def governador():
    if 'cpf' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        session['votos']['governador'] = request.form.get('voto')
        return redirect(url_for('presidente'))
    return render_template('governador.html')


@app.route('/presidente', methods=['GET', 'POST'])
def presidente():
    if 'cpf' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        session['votos']['presidente'] = request.form.get('voto')
        return redirect(url_for('finalizado'))
    return render_template('presidente.html')


@app.route("/finalizado")
def finalizado():
    if 'cpf' not in session:
        return redirect(url_for('login'))

    return """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <title>Votação finalizada</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #111827;
                color: white;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }

            .container {
                text-align: center;
                background: #1f2937;
                padding: 50px;
                border-radius: 15px;
            }

            h1 {
                color: #22c55e;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>VOTAÇÃO FINALIZADA</h1>
            <p>Obrigado por participar da simulação.</p>
        </div>
    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(debug=True)
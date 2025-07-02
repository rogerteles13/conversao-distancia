dockerfrom flask import Flask, render_template, request
import logging
import socket  # Módulo para obter informações do servidor

app = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='templates')

@app.route('/', methods=['GET', 'POST'])
def index():
    # Obter informações do servidor
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    if request.method == 'GET':  
        return render_template('index.html', hostname=hostname, ip_address=ip_address)
    else:
        selecao = request.form.get('selectTemp')
        valor = request.form.get('valorRef')

        try:
            valor = float(valor)
        except ValueError:
            return render_template('index.html', conteudo={'unidade': 'inválido', 'valor': 'Entrada inválida'}, hostname=hostname, ip_address=ip_address)

        # Dicionário de conversões para um código mais limpo, escalável e "Pythônico"
        conversions = {
            '1': {'func': lambda v: v / 1000,    'unit': 'quilômetros'},
            '2': {'func': lambda v: v * 1000,    'unit': 'metros'},
            '3': {'func': lambda v: v / 1609.34, 'unit': 'milhas'},
            '4': {'func': lambda v: v * 1609.34, 'unit': 'metros'},
            '5': {'func': lambda v: v * 3.28084, 'unit': 'pés'},
            '6': {'func': lambda v: v / 3.28084, 'unit': 'metros'},
        }

        conversion_data = conversions.get(selecao)

        if conversion_data:
            resultado = conversion_data['func'](valor)
            unidade = conversion_data['unit']
        else:
            resultado = "Inválido"
            unidade = ""

        return render_template('index.html', conteudo={'unidade': unidade, 'valor': resultado}, hostname=hostname, ip_address=ip_address)

if __name__ == '__main__':
    app.run()
else:
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

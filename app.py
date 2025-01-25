from flask import Flask, request, render_template
import subprocess
import os
from datetime import datetime

app = Flask(__name__)
LOG_FILE = "log.txt"

def log_domain_search(domain, subdomains):
    """Registra domínios pesquisados em um log."""
    with open(LOG_FILE, "a") as file:
        file.write(f"{datetime.now()} - {domain}:\n")
        file.write("\n".join(subdomains))
        file.write("\n\n")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/find_subdomains', methods=['POST'])
def find_subdomains():
    domain = request.form['domain']
    
    try:
        # Executa o comando Amass para descobrir subdomínios
        result = subprocess.run(
            ['amass', 'enum', '-d', domain],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        if result.returncode != 0:
            return f"<h3>Erro ao executar o Amass:</h3><pre>{result.stderr}</pre>"

        # Processa os subdomínios encontrados
        output = result.stdout
        subdomains = [line.strip() for line in output.splitlines() if domain in line]

        # Registra no log
        log_domain_search(domain, subdomains)
        
        return render_template('result.html', domain=domain, subdomains=subdomains)
    except Exception as e:
        return f"<h3>Erro: {str(e)}</h3>"

@app.route('/logs')
def view_logs():
    """Exibe os logs registrados."""
    if not os.path.exists(LOG_FILE):
        return "<h3>Nenhum log encontrado!</h3><a href='/'>Voltar</a>"
    
    with open(LOG_FILE, "r") as file:
        logs = file.read()
    return f"<h1>Logs de Domínios Pesquisados</h1><pre>{logs}</pre><a href='/'>Voltar</a>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5055, debug=True)


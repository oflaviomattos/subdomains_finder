from flask import Flask, request, render_template
import subprocess

app = Flask(__name__)

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

        # Processa e exibe os subdomínios encontrados
        output = result.stdout
        subdomains = [line.strip() for line in output.splitlines() if domain in line]
        
        return render_template('result.html', domain=domain, subdomains=subdomains)
    except Exception as e:
        return f"<h3>Erro: {str(e)}</h3>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5055)


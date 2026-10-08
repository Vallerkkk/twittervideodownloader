from flask import Flask, render_template, request, redirect
import yt_dlp
import os

# O parâmetro template_folder='.' faz a mágica de buscar o HTML na mesma pasta
app = Flask(__name__, template_folder='.')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/baixar', methods=['POST'])
def baixar():
    url = request.form.get('url')
    if not url:
        return "Erro: Nenhum link fornecido.", 400

    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            link_direto = info.get('url')
            
            if link_direto:
                return redirect(link_direto)
            else:
                return "Erro: Não foi possível encontrar o link direto do vídeo.", 404
                
    except Exception as e:
        return f"Erro ao processar o link: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
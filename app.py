from flask import Flask, render_template, request, redirect
import yt_dlp
import requests

app = Flask(__name__, template_folder='.')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/baixar', methods=['POST'])
def baixar():
    url = request.form.get('url')
    if not url:
        return "Erro: Nenhum link fornecido.", 400

    # === TRUQUE ANTI-BLOQUEIO PARA O X/TWITTER ===
    if 'x.com' in url or 'twitter.com' in url:
        try:
            # 1. Limpa rastreadores no final do link (como o ?s=20)
            url_limpa = url.split('?')[0]
            
            # 2. Troca o domínio original pela API pública do vxTwitter
            url_api = url_limpa.replace('https://x.com/', 'https://api.vxtwitter.com/').replace('https://twitter.com/', 'https://api.vxtwitter.com/')
            
            # 3. Pede os dados do vídeo para a API
            resposta = requests.get(url_api).json()
            
            # 4. Procura o link direto do arquivo MP4 dentro da resposta
            if 'media_extended' in resposta:
                for media in resposta['media_extended']:
                    if media['type'] == 'video':
                        return redirect(media['url'])
                        
            return "Erro: Nenhum vídeo encontrado neste tweet.", 404
        except Exception as e:
            return f"Erro ao contornar o Twitter: {str(e)}", 500

    # === PARA TODAS AS OUTRAS REDES (YouTube, TikTok, etc) ===
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
                return "Erro: Não foi possível encontrar o link direto.", 404
                
    except Exception as e:
        return f"Erro ao processar o link com yt-dlp: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
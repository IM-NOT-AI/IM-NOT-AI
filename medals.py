import requests
import os

# CONFIGURAÇÕES
USERNAME = os.environ.get('GITHUB_REPOSITORY_OWNER')
if not USERNAME:
    print("Erro: Usuário não encontrado")
    exit(1)

# CORES (Sua regra de Ouro/Prata/Bronze)
COLOR_BG = '#161b22'     # Fundo Dark
COLOR_EMPTY = '#2d333b'  # Sem commits
COLOR_BRONZE = '#cd7f32' # 1-4 commits
COLOR_SILVER = '#c0c0c0' # 5-6 commits
COLOR_GOLD = '#ffd700'   # 7+ commits

print(f"Gerando medalhas para: {USERNAME}")

try:
    # Baixa dados do último ano
    url = f'https://github-contributions-api.jogruber.de/v4/{USERNAME}?y=last'
    r = requests.get(url)
    data = r.json()
except Exception as e:
    print(f"Erro na conexão: {e}")
    exit(1)

contributions = data['contributions']

# Dimensões do SVG
box_size = 10
gap = 3
svg_width = 53 * (box_size + gap) + 20
svg_height = 7 * (box_size + gap) + 20

# Monta o SVG
svg_content = f'<svg width="{svg_width}" height="{svg_height}" xmlns="http://www.w3.org/2000/svg">'
svg_content += f'<rect width="100%" height="100%" fill="{COLOR_BG}" />'
svg_content += f'<g transform="translate(10, 10)">'

for i, day in enumerate(contributions):
    # Posição (Semanas nas colunas, Dias nas linhas)
    x = (i // 7) * (box_size + gap)
    y = (i % 7) * (box_size + gap)
    
    count = day['count']
    date = day['date']
    
    # Lógica das Cores
    fill = COLOR_EMPTY
    if count > 0:
        if count >= 7:
            fill = COLOR_GOLD
        elif count >= 5:
            fill = COLOR_SILVER
        else:
            fill = COLOR_BRONZE
            
    svg_content += f'<rect x="{x}" y="{y}" width="{box_size}" height="{box_size}" fill="{fill}" rx="2" ry="2"><title>{date}: {count}</title></rect>'

svg_content += '</g></svg>'

# Salva o arquivo
with open('medals.svg', 'w') as f:
    f.write(svg_content)

print("Sucesso! medals.svg criado.")

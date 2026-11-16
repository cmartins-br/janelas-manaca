# Janelas do Manacá

Apresentação interativa da proposta de novo padrão (opcional e gradativo) para as janelas dos dormitórios do Condomínio Edifício Manacá.

Site estático: `index.html` + pasta `assets/`. Não precisa de build.

## Publicar no Vercel
1. Em vercel.com, clique em **Add New → Project** e importe `cmartins-br/janelas-manaca`.
2. Framework Preset: **Other**. Deixe Build Command e Output Directory vazios.
3. Clique em **Deploy**.

## Ver localmente
```
python3 -m http.server 8000
```
e abra http://localhost:8000

## Conteúdo
- `assets/fachada-original.jpg` – foto real da fachada lateral
- `assets/video-janelas-independentes.mp4` – vídeo gerado por IA, editado para que as janelas da esquerda e da direita de cada quarto se movam de forma independente
- `assets/interna-*.jpg` – fotos reais de uma instalação já feita (janela de correr com a mesma travessa das antigas)
- `assets/orcamento-indicativo.pdf` – orçamento de referência

## Carta impressa e pesquisa (`impressos/`)
PDF A4 de 2 páginas por apartamento: carta da comissão (janela atual x nova, QR code para o site) e cédula de opinião para devolver na portaria.
```
pip install segno
python3 impressos/gerar.py --url https://SEU-ENDERECO.vercel.app                    # modelo com "Apto" em branco
python3 impressos/gerar.py --url https://SEU-ENDERECO.vercel.app --aptos 11-14,21-24 # um PDF com todas as unidades
```

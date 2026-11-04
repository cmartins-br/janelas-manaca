#!/usr/bin/env python3
"""Gera o PDF da carta + cédula (A4, 2 páginas por apartamento).

Uso:
  python3 impressos/gerar.py --url https://exemplo.vercel.app            # modelo com "Apto" em branco
  python3 impressos/gerar.py --url ... --aptos 11-14,21-24,31,32          # um PDF com todas as unidades
  python3 impressos/gerar.py --url ... --saida carta.pdf

Requer: pip install segno ; Playwright (node) com Chromium.
"""
import argparse, json, os, re, subprocess, sys, tempfile
import segno

AQUI = os.path.dirname(os.path.abspath(__file__))


def expandir(aptos):
    lista = []
    for parte in filter(None, (p.strip() for p in aptos.split(','))):
        m = re.fullmatch(r'(\d+)-(\d+)', parte)
        lista += [str(n) for n in range(int(m[1]), int(m[2]) + 1)] if m else [parte]
    return lista


def qr_svg(url):
    svg = segno.make(url, error='m').svg_inline(scale=1, border=0, dark='#1d2421')
    m = re.match(r'<svg width="(\d+)" height="(\d+)"', svg)
    return svg.replace(m[0], f'<svg viewBox="0 0 {m[1]} {m[2]}" shape-rendering="crispEdges"', 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--url', required=True)
    ap.add_argument('--aptos', default='')
    ap.add_argument('--saida', default=os.path.join(AQUI, 'carta-pesquisa-janelas.pdf'))
    a = ap.parse_args()

    modelo = open(os.path.join(AQUI, 'carta.html'), encoding='utf-8').read()
    curta = re.sub(r'^https?://', '', a.url).rstrip('/')
    modelo = modelo.replace('{{QR}}', qr_svg(a.url)).replace('{{URL_CURTA}}', curta)

    unidades = expandir(a.aptos) or ['']
    inicio, corpo_fim = modelo.index('<body>') + len('<body>'), modelo.index('</body>')
    corpo = modelo[inicio:corpo_fim]
    paginas = ''.join(
        corpo.replace('{{APTO}}', u).replace('{{APTO_RODAPE}}', u or '______') for u in unidades)
    html = modelo[:inicio] + paginas + modelo[corpo_fim:]

    tmp = os.path.join(AQUI, '.render.html')  # fica ao lado para achar fontes/
    open(tmp, 'w', encoding='utf-8').write(html)
    js = """
const { chromium } = require('playwright');
(async () => {
  const [src, out] = process.argv.slice(1);
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://' + src, { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({ path: out, format: 'A4', printBackground: true, preferCSSPageSize: true });
  await b.close();
})();
"""
    try:
        subprocess.run(['node', '-e', js, tmp, os.path.abspath(a.saida)], check=True)
    finally:
        os.remove(tmp)
    print(f'{a.saida}: {len(unidades)} unidade(s), {2 * len(unidades)} páginas')


if __name__ == '__main__':
    main()

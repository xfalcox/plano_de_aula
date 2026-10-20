from pathlib import Path
import html
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'materiais'
OUT.mkdir(exist_ok=True)
for folder in ['editaveis', 'demos', 'pdf']:
    (OUT / folder).mkdir(exist_ok=True)

def esc(s): return html.escape(s)
def p(s): return '<p>' + s + '</p>'
def code(s): return '<pre><code>' + esc(s) + '</code></pre>'
def ul(items): return '<ul>' + ''.join('<li>'+i+'</li>' for i in items) + '</ul>'
def box(title, body, cls=''): return f'<div class="box {cls}"><h3>{title}</h3>{body}</div>'
def cols(*items): return '<div class="cols">' + ''.join('<div>'+s+'</div>' for s in items) + '</div>'

CSS = '''
*{box-sizing:border-box} :root{--ink:#17233c;--blue:#1745a0;--paper:#fff;--muted:#4a5668;--line:#c9d3e3;--mint:#dcf6ea;--yellow:#fff1ba}
body{margin:0;background:#e7ebf1;color:var(--ink);font-family:"Noto Sans",Arial,sans-serif;font-size:11pt;line-height:1.42}
.page{position:relative;background:white;width:186mm;height:270mm;margin:20px auto;padding:1mm 0 10mm;break-after:page;overflow:hidden}
.page:last-child{break-after:auto}.eyebrow{font-size:9pt;text-transform:uppercase;letter-spacing:1.5px;font-weight:700;color:var(--blue)}
h1{font-size:26pt;line-height:1.1;margin:10px 0 16px;letter-spacing:-.8px}h2{font-size:18pt;line-height:1.15;margin:14px 0 10px}h3{font-size:12pt;margin:0 0 5px}
p{margin:7px 0 11px}ul{padding-left:20px;margin:7px 0 12px}li{margin-bottom:5px}strong{font-weight:750}a{color:#1745a0}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:18px}.box{border:1px solid var(--line);border-radius:14px;padding:15px;margin:12px 0;background:#f5f7fb}
.mint{background:var(--mint)}.yellow{background:var(--yellow)}.big{font-size:22pt;font-weight:750;line-height:1.15}.small{font-size:9pt;color:var(--muted)}
pre{font-family:"DejaVu Sans Mono",monospace;background:#eef2f9;border-left:5px solid var(--blue);padding:13px;font-size:10pt;line-height:1.5;margin:10px 0;white-space:pre-wrap;overflow-wrap:anywhere}
code{font-family:"DejaVu Sans Mono",monospace}.footer{position:absolute;bottom:0;left:0;right:0;border-top:1px solid var(--line);padding-top:6px;font-size:8pt;display:flex;justify-content:space-between;color:var(--muted)}
table{border-collapse:collapse;width:100%;font-size:10pt}td,th{padding:7px 8px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}th{background:#edf2fa}
.plan{font-size:10pt;line-height:1.34}.plan h1{font-size:22pt;margin-bottom:10px}.plan h2{font-size:11pt;margin:11px 0 4px;color:var(--blue)}.plan p{margin:4px 0 6px}.plan table{font-size:9pt}.plan td{padding:4px 6px}.plan .refs{font-size:8pt}
.answer{border-bottom:1px solid #9ba8ba;height:24px;margin:5px 0}.stage{padding:14px;border:1px solid var(--line);border-radius:12px;background:#fafbfd}
.ticket{border:2px solid #1745a0;border-radius:16px;padding:22px;background:#fff}.ticket h3{font-size:24pt;margin:10px 0}.ticket p{font-size:15pt}.button{display:inline-block;border:2px solid #1745a0;background:#1745a0;color:white;padding:10px 18px;border-radius:8px;font-weight:700}
.flow{display:flex;align-items:stretch;gap:10px;margin:18px 0}.flow>div{flex:1;padding:18px 12px;border:2px solid #1745a0;border-radius:12px;text-align:center;background:#edf2fa}.flow b{display:block;font-size:19pt}.flow span{font-size:13pt}
.tagrow{display:flex;gap:10px;align-items:center;justify-content:center;margin:22px 0}.tagrow>div{padding:18px 10px;border:2px solid #1745a0;border-radius:10px;text-align:center}.tagrow code{font-size:25pt}.tagrow small{display:block;font-size:13pt}
.layer{padding:17px;border:2px dashed #7e6743;background:#fff1ba;font-size:13pt}.layer .layer{background:#dcf6ea;border:4px solid #1745a0}.layer .layer .layer{background:#eef2f9;border:2px dashed #42667b}.layer .layer .layer .layer{background:white;border:1px solid #99a7b8;text-align:center}
.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:18px}.card{border:2px dashed #4a5668;border-radius:10px;padding:16px;min-height:220px}.card h2{font-size:18pt}.card code{font-size:17pt}.card p{font-size:13pt}
.activity{font-size:10.5pt;line-height:1.35}.activity h2{font-size:16pt;margin-top:12px}.activity pre{margin:8px 0;padding:11px}.activity .box{padding:12px}.activity .answer{height:22px}
.landscape .page{width:273mm;height:186mm;padding-top:2mm}.slide h1{font-size:34pt;margin:12px 0 20px}.slide h2{font-size:22pt}.slide h3{font-size:18pt}.slide{font-size:18pt;line-height:1.32}.slide p{margin:12px 0}.slide pre{font-size:16pt;line-height:1.48;padding:17px}.slide .small{font-size:12pt}.slide .box{padding:18px}.slide .cols{gap:26px}.slide .footer{font-size:9pt}
@page{size:A4 portrait;margin:12mm} @media print{body{background:white}.page{margin:0;box-shadow:none}a{color:inherit;text-decoration:none}}
'''

def write_doc(name, title, pages, landscape=False):
    style = CSS + ('@page{size:A4 landscape;margin:12mm}' if landscape else '')
    body = ''.join(f'<section class="page {cls}">{content}<div class="footer"><span>Festa de formatura · Programação Web I</span><span>{i+1} / {len(pages)}</span></div></section>' for i,(cls,content) in enumerate(pages))
    doc=f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{esc(title)}</title><style>{style}</style></head><body class="{"landscape" if landscape else "portrait"}">{body}</body></html>'
    (OUT/'editaveis'/f'{name}.html').write_text(doc)

def heading(kicker, title): return f'<div class="eyebrow">{kicker}</div><h1>{title}</h1>'

HTML_FRAGMENT='''<main>
  <h1>Festa de formatura</h1>
  <p>Música e fotos com a turma.</p>
  <a href="#agenda">Ver programação</a>
  <h2 id="agenda">Programação</h2>
  <p>19h: recepção da turma.</p>
</main>'''
CSS_FRAGMENT='''.convite {
  background-color: #dcf6ea;
  color: #17233c;
  padding: 16px;
  border: 2px solid #1745a0;
  margin: 12px;
}'''
JS_MARKUP='''<button id="participar">Participar</button>
<p id="status" aria-live="polite">
  Sua presença ainda não foi confirmada.
</p>'''
JS_FRAGMENT='''const botao = document.querySelector("#participar");
const status = document.querySelector("#status");

botao.addEventListener("click", function () {
  status.textContent = "Presença confirmada!";
  botao.textContent = "Confirmado";
  botao.disabled = true;
});'''

topics={
'html':dict(label='HTML',title='Um convite que faz sentido',focus='Estrutura e significado de uma página de evento',prior='Uso básico de navegador; não exige programação.',objectives='Identificar abertura, conteúdo e fechamento de um elemento; escolher h1, p e a segundo a finalidade; completar um link interno cujo href corresponde ao id de destino.',content='Linguagem de marcação; anatomia de elementos; h1, h2, p, a e main; atributo href; correspondência entre #agenda e id="agenda". O documento completo é mostrado como contexto, sem memorizar o boilerplate.',evidence='Desafio: título, parágrafo e link adequados (3 critérios). Saída: href="#agenda" e id="agenda" correspondentes (1 critério). Êxito esperado: 3 de 4 critérios; retomar link interno se houver erro.',lesson='Organizar uma página com título, descrição e link interno',source='https://developer.mozilla.org/pt-BR/docs/Learn_web_development/Core/Structuring_content/Basic_HTML_syntax'),
'css':dict(label='CSS',title='Um convite que dá vontade de ler',focus='Seletores de classe e espaçamento no modelo de caixa',prior='Reconhecer um elemento HTML e o atributo class; apresentar uma retomada curta no início.',objectives='Relacionar .convite a class="convite"; interpretar seletor, propriedade e valor; diferenciar padding (espaço interno), border (contorno) e margin (espaço externo).',content='Regra CSS; seletor de classe; background-color e color; modelo de caixa com conteúdo, padding, border e margin. Exemplos usam box-sizing: content-box, sem largura fixa.',evidence='Desafio: selecionar .convite, padding interno e margin externo (3 critérios). Saída: resolver um caso de texto encostado na borda com padding (1 critério). Êxito esperado: 3 de 4 critérios.',lesson='Estilizar um convite com classe e espaços legíveis',source='https://developer.mozilla.org/pt-BR/docs/Learn_web_development/Core/Styling_basics/Box_model'),
'javascript':dict(label='JavaScript',title='Um clique que muda a página',focus='Evento de clique e atualização do DOM',prior='Reconhecer elementos HTML e id; ter noção de variável e função. Retomar esses conceitos em uma frase; a meta é ler e completar um manipulador, não escrever toda a API de memória.',objectives='Localizar um elemento por seu id; explicar evento e função de resposta; prever e completar uma alteração de textContent após um clique.',content='DOM como representação da página; document.querySelector; evento click; addEventListener; função de resposta; textContent e disabled. Script executado após o HTML.',evidence='Desafio: seleção #status, evento click e textContent (3 critérios). Saída: prever a mensagem e identificar que a mudança ocorre após o clique (1 critério). Êxito esperado: 3 de 4 critérios.',lesson='Responder a um clique com uma confirmação visível',source='https://developer.mozilla.org/pt-BR/docs/Web/API/EventTarget/addEventListener')
}
timings=[('0–2 min','Problema real e pergunta inicial'),('2–3 min','Objetivos e retomada de pré-requisitos'),('3–6 min','Conceito com diagrama visual'),('6–9 min','Exemplo explicado e previsão'),('9–12 min','Simulação com cartões'),('12–15 min','Desafio em dupla ou individual'),('15–18 min','Correção e transferência'),('18–19 min','Bilhete de saída e síntese')]

def make_plan(key):
    t=topics[key]
    rows=''.join(f'<tr><td>{time}</td><td>{action}</td></tr>' for time,action in timings)
    body=heading('Plano de aula · Tema '+t['label'],t['title'])
    body+=p('<b>Candidato:</b> Rafael dos Santos Silva · <b>Inscrição:</b> 15')
    body+=p('<b>Componente:</b> Programação Web I · Desenvolvimento de Sistemas integrado ao Ensino Médio<br><b>Público:</b> estudantes de 15 anos · <b>Duração:</b> 19 min + 1 min de margem · <b>Recorte:</b> '+t['focus'])
    for title,text in [('Pré-requisitos',t['prior']),('Objetivos de aprendizagem',t['objectives']),('Conteúdos',t['content'])]: body+=f'<h2>{title}</h2>'+p(text)
    body+='<h2>Metodologia e sequência</h2>'+p('Exposição dialogada com previsão de resultados, representação visual, simulação e desafio breve. Contexto: página fictícia de um evento de formatura do curso. A aula é independente das demais.')+f'<table>{rows}</table>'
    body+='<h2>Recursos e inclusão</h2>'+p('Slides impressos autorais com código e resultado; cartões com palavras e símbolos; folha de atividade. Quadro, se disponível. Ler os trechos em voz alta, usar alto contraste e rótulos além de cores; permitir resposta oral ou escrita. Projeção institucional é opcional.')
    body+='<h2>Avaliação e recuperação</h2>'+p(t['evidence']+' A correção é comentada, com nova tentativa. Na banca, apresentar as perguntas, dar breve tempo de reflexão e explicitar a resposta esperada sem exigir participação.')
    body+='<h2>Referência</h2>'+p('<span class="refs">MDN Web Docs · '+t['source']+' · acesso em 13/10/2026.</span>')
    return ('plan',body)

plans=[]
for key in topics:
    page=make_plan(key)
    write_doc('plano_'+key,'Plano de aula '+topics[key]['label'],[page])
    plans.extend([page]*3)
write_doc('planos_banca_3_vias','Planos de aula para a banca em três vias',plans)

def ticket(styled=True):
    if styled:return '<div class="ticket"><span class="eyebrow">Evento escolar fictício</span><h3>Festa de formatura</h3><p>Música e fotos com a turma.</p><a href="#">Ver programação →</a></div>'
    return '<div class="stage"><h3>Festa de formatura</h3><p>Música e fotos com a turma.</p><u>Ver programação</u><h4>Programação</h4><p>19h: recepção da turma.</p></div>'

slides={}
slides['html']=[
('Um convite que faz sentido',cols(ticket(),p('Um amigo te manda a página do evento. Como você descobre <b>o nome</b>, <b>o que vai acontecer</b> e <b>a programação</b>?')+box('Pense por 5 segundos','Qual informação você procura primeiro?','yellow'))),
('Hoje você vai organizar a página',ul(['Marcar o título, a descrição e o link.','Explicar abertura, conteúdo e fechamento.','Conectar um link ao seu destino.'])+box('HTML = estrutura com significado',p('Como uma playlist com nome, descrição e faixas: cada informação tem uma função.'))),
('Uma etiqueta para cada função','<div class="tagrow"><div><code>&lt;h1&gt;</code><small>Abertura</small></div><div><code>Festa de formatura</code><small>Conteúdo</small></div><div><code>&lt;/h1&gt;</code><small>Fechamento</small></div></div>'+cols(box('O elemento completo',p('As três partes formam um elemento. HTML marca a função do conteúdo.')),box('Qual etiqueta você usaria?',p('Título principal → <b>h1</b><br>Descrição → <b>p</b><br>Link → <b>a</b>')))),
('Do código para a página',cols(code(HTML_FRAGMENT),ticket(False))+p('<span class="small">Trecho dentro de body. main delimita o conteúdo principal; h2 apresenta a seção. O navegador interpreta essas marcas.</span>')),
('O link tem um endereço',code('<a href="#agenda">Ver programação</a>\n...\n<h2 id="agenda">Programação</h2>')+'<div class="flow"><div><b>Link</b><span>href="#agenda"</span></div><div><b>Destino</b><span>id="agenda"</span></div></div>'+p('O <b>#</b> aponta para um identificador na própria página. Junte os cartões que combinam.')),
('Missão: monte seu convite',p('Em dupla, use <b>h1</b>, <b>p</b> e <b>a</b>. Você tem 60 segundos.')+code('_______________________________\n  Festa de formatura\n_______________________________\n<p>Música e fotos com a turma.</p>\n<a href="________">Ver programação</a>')+p('O destino já existe: <code>&lt;h2 id="agenda"&gt;</code>. Qual endereço falta?')),
('Depuração: ficou bonito. Está correto?',cols(code('<p>Festa de formatura</p>\n<h1>Música e fotos com a turma.</h1>'),box('Pista',p('O texto principal é o nome do evento. Qual função cada trecho deveria ter?'),'yellow'))+p('Tamanho visual e significado são coisas diferentes. Um título precisa ser marcado como título.')),
('Bilhete de saída',code('<a href="_______">Ver programação</a>\n<h2 id="agenda">Programação</h2>')+p('Complete o endereço e explique a relação com <code>id="agenda"</code>.')+box('Você já consegue',p('Escolher título, parágrafo e link e conectar o link ao destino.'),'mint'))
]
slides['css']=[
('O convite ficou espremido!',cols('<div style="border:2px solid #1745a0;background:#dcf6ea"><h3 style="margin:0">Festa de formatura</h3><p style="margin:0">Música e fotos com a turma.</p></div>',ticket())+p('Em qual convite é mais confortável ler? <b>O conteúdo é o mesmo.</b>')),
('Hoje você vai dar espaço ao convite',ul(['Encontrar o elemento usando uma classe.','Ler seletor, propriedade e valor.','Separar espaço interno de espaço externo.'])+code('<article class="convite">Festa de formatura</article>')+p('<span class="small">Retomada: class dá um nome a um grupo de elementos. Aqui ele se chama convite.</span>')),
('Uma regra é uma instrução de estilo',code('.convite {\n  background-color: #dcf6ea;\n  color: #17233c;\n}')+'<div class="flow"><div><b>.convite</b><span>Seletor: quem?</span></div><div><b>color</b><span>Propriedade: o quê?</span></div><div><b>#17233c</b><span>Valor: como?</span></div></div>'+p('O ponto seleciona uma <b>classe</b>. Vários convites podem usar a mesma regra.')),
('O modelo de caixa',cols('<div class="layer">MARGIN · espaço externo<div class="layer">BORDER · contorno<div class="layer">PADDING · espaço interno<div class="layer">CONTEÚDO<br>Festa de formatura</div></div></div></div>',box('Imagine um quadro na parede',p('A imagem é o conteúdo.<br>O espaço até a moldura é padding.<br>A moldura é border.<br>A distância entre quadros é margin.')))),
('Antes e depois: o que muda?',cols(code(CSS_FRAGMENT),box('Faça uma previsão',p('O texto ganha espaço <b>dentro</b> do contorno. O convite ganha espaço <b>fora</b> dele.'),'mint'))+p('<span class="small">Neste exemplo, padding e margin usam o mesmo valor nos quatro lados. px é uma unidade CSS; não precisa corresponder a um pixel físico.</span>')),
('Missão: resgate o convite',p('Escolha as instruções. Em dupla, você tem 60 segundos.')+code('________ {\n  ________: 16px; /* dentro */\n  border: 2px solid #1745a0;\n  ________: 12px; /* fora */\n}')+p('O HTML tem <code>class="convite"</code>. Use: <b>.convite · padding · margin</b>.')),
('Um erro muito comum',cols(code('.convite {\n  margin: 16px;\n}'),box('Problema',p('O texto continua encostado na borda. Qual propriedade resolve?'),'yellow'))+p('Margin afasta a caixa das outras caixas. <b>Padding</b> afasta o conteúdo do contorno.')),
('Bilhete de saída',p('Um cartão de produto está com o preço encostado na borda.')+box('Qual instrução você acrescenta?',code('padding: 16px;\n// ou\nmargin: 16px;'),'yellow')+p('<span class="small">As duas linhas acima são alternativas para discussão; // não é comentário válido em CSS. No CSS, comentários usam /* ... */.</span>')+p('Explique onde fica o espaço criado pela sua escolha.'))
]
# Replace pedagogical alternatives with valid CSS comments to keep every code panel accurate.
slides['css'][-1]=('Bilhete de saída',p('Um cartão de produto está com o preço encostado na borda.')+box('Qual instrução você acrescenta?',code('padding: 16px;\n/* ou */\nmargin: 16px;'),'yellow')+p('Explique onde fica o espaço criado pela sua escolha.')+box('Você já consegue',p('Selecionar uma classe e distinguir padding, border e margin.'),'mint'))
slides['javascript']=[
('Um botão precisa responder',cols(box('Antes',p('<span class="button">Participar</span>')+p('Sua presença ainda não foi confirmada.')),box('Depois do clique',p('<span class="button">Confirmado</span>')+p('Presença confirmada!'),'mint'))+p('O que mudou? Em que momento? Pense em curtir uma publicação ou confirmar uma escolha.')),
('Hoje você vai dar uma resposta ao clique',ul(['Localizar um elemento pelo id.','Identificar o evento de clique.','Prever a mudança de texto na página.'])+box('Retomada',p('Variável guarda uma referência; função reúne instruções. O DOM é a representação da página que o JavaScript pode acessar.'))),
('Encontrar → ouvir → responder','<div class="flow"><div><b>Encontrar</b><span>querySelector</span></div><div><b>Ouvir</b><span>addEventListener</span></div><div><b>Responder</b><span>textContent</span></div></div>'+code('const botao = document.querySelector("#participar");')+p('O <b>#</b> seleciona um id. A variável <b>botao</b> passa a apontar para o elemento encontrado.')),
('Antes do clique: os elementos existem',code(JS_MARKUP)+p('O script fica <b>depois</b> desses elementos no documento.')+box('Conecte os cartões',p('<code>#participar</code> → botão<br><code>#status</code> → parágrafo de mensagem'),'mint')),
('O clique dispara esta função',code(JS_FRAGMENT)+p('<span class="small">textContent troca o texto. disabled impede nova ativação do botão. const mantém a referência: as propriedades do elemento ainda podem mudar.</span>')),
('Missão: complete a resposta',p('Em dupla, use <b>click</b> e <b>textContent</b>. Você tem 60 segundos.')+code('botao.addEventListener("_____", function () {\n  status.________ = "Presença confirmada!";\n});')+p('A mensagem muda quando a página abre ou quando o botão é clicado?')),
('Depuração: o alvo sumiu',cols(code('/* HTML */\n<p id="status">Aguardando</p>\n\n/* JavaScript */\nconst status =\n  document.querySelector("status");'),box('Encontre o erro',p('Para buscar um id, o seletor precisa de qual símbolo?'),'yellow'))+p('Sem <b>#</b>, "status" procura um elemento com esse nome. Se não existe, o resultado é <b>null</b>.')),
('Bilhete de saída',code('botao.addEventListener("click", function () {\n  status.textContent = "Você está na lista!";\n});')+p('Qual texto aparece após o clique? O que inicia a mudança?')+box('Você já consegue',p('Ligar elemento, evento e resposta. Esta demo muda a página localmente; não envia uma inscrição para um servidor.'),'mint'))
]
# HTML and JS shown separately rather than a mixed-language code snippet with invalid HTML comments.
slides['javascript'][6]=('Depuração: o alvo sumiu',cols(code('<p id="status">Aguardando</p>')+code('const status =\n  document.querySelector("status");'),box('Encontre o erro',p('Para buscar um id, o seletor precisa de qual símbolo?'),'yellow'))+p('Sem <b>#</b>, "status" procura um elemento com esse nome. Se não existe, o resultado é <b>null</b>.'))

for key,deck in slides.items():
    pages=[]
    for i,(title,body) in enumerate(deck):
        pages.append(('slide',heading(f'{topics[key]["label"]} · {timings[i][0]} · Aula de 19 minutos',title)+body))
    write_doc('apresentacao_'+key,'Apresentação '+topics[key]['label'],pages,True)

activities={
'html':[
('1 · Cada texto tem uma função','Ligue: “Festa de formatura” → h1 / p / a; “Música e fotos com a turma.” → h1 / p / a; “Ver programação” → h1 / p / a.'),
('2 · Monte o convite',code('_____Festa de formatura_____\n<p>Música e fotos com a turma.</p>\n<a href="________">Ver programação</a>')+p('O destino é <code>&lt;h2 id="agenda"&gt;Programação&lt;/h2&gt;</code>.')),
('3 · Detetive de código',code('<p>Festa de formatura</p>\n<h1>Música e fotos com a turma.</h1>')+p('Reescreva escolhendo o título e o parágrafo corretos.')),
('Saída · Faça o link chegar ao destino','Se o destino for <code>id="jogos"</code>, qual será o valor de href? Explique por que a correspondência importa.')],
'css':[
('1 · Encontre o convite',code('<article class="convite">Festa de formatura</article>')+p('Qual seletor de classe encontra esse elemento? __________________')),
('2 · Resgate o espaço',code('________ {\n  ________: 16px; /* espaço interno */\n  border: 2px solid #1745a0;\n  ________: 12px; /* espaço externo */\n}')),
('3 · Detetive de código','Você aumentou margin, mas o texto continua encostado no contorno. Qual propriedade deve alterar? Desenhe o espaço que ela cria.'),
('Saída · Um caso de loja virtual','O preço está encostado na borda do cartão de um produto. Escolha padding ou margin e justifique.')],
'javascript':[
('1 · Encontre a mensagem',code('<p id="status">Aguardando</p>')+p('Complete: <code>document.querySelector("________")</code>')),
('2 · Faça o botão responder',code('botao.addEventListener("_____", function () {\n  status.________ = "Presença confirmada!";\n});')+p('Banco de palavras: click · textContent.')),
('3 · Detetive de código',code('document.querySelector("status")')+p('O HTML contém <code>id="status"</code>. Qual símbolo está faltando? O que a seleção acima procura?')),
('Saída · Preveja a tela',code('botao.addEventListener("click", function () {\n  status.textContent = "Você está na lista!";\n});')+p('Qual mensagem surge? Quando? Essa instrução sozinha salva a inscrição em um servidor?'))]
}
for key,questions in activities.items():
    body=heading('Atividade · '+topics[key]['label'],topics[key]['title'])+p('Nome: __________________________  Turma: ______  Data: __________')+p('Missão principal: itens 1 e 2. Itens 3 e saída: correção e verificação. Você pode responder escrevendo, desenhando ou explicando em voz alta.')
    for title,question in questions:
        body+=f'<h2>{title}</h2>'+(question if question.startswith('<') else p(question))+'<div class="answer"></div>'
    body+=box('Se terminar antes',p({'html':'Crie um título e uma descrição para um evento de esporte ou música. Adicione um link para uma seção com id="local".','css':'Desenhe duas caixas. Identifique conteúdo, padding, border e margin com palavras, além das cores.','javascript':'Troque a mensagem final por uma confirmação de empréstimo de livro e explique por que o evento permanece click.'}[key]),'mint')
    write_doc('atividade_'+key,'Atividade '+topics[key]['label'],[('activity',body)])

card_data={
'html':[('TÍTULO','<h1>Festa de formatura</h1>','Nome principal da página.'),('DESCRIÇÃO','<p>Música e fotos.</p>','Uma informação em parágrafo.'),('LINK','<a href="#agenda">','Aponta para a programação.'),('DESTINO','id="agenda"','É encontrado pelo link #agenda.'),('OUTRO DESTINO','id="local"','Não é o destino de #agenda.'),('FECHAMENTO','</a>','Fecha o elemento de link.')],
'css':[('CONTEÚDO','Festa de formatura','Texto dentro da caixa.'),('PADDING','padding: 16px;','Espaço interno, até a borda.'),('BORDER','border: 2px solid;','O contorno da caixa.'),('MARGIN','margin: 12px;','Espaço externo ao contorno.'),('CLASSE','class="convite"','Nome no HTML.'),('SELETOR','.convite','Encontra a classe no CSS.')],
'javascript':[('BOTÃO','id="participar"','Alvo selecionado por #participar.'),('MENSAGEM','id="status"','Alvo selecionado por #status.'),('EVENTO','click','Acontecimento que inicia a resposta.'),('SELEÇÃO','querySelector','Encontra um elemento no DOM.'),('RESPOSTA','textContent','Propriedade que altera o texto.'),('ESTADO FINAL','Confirmado','Botão desabilitado; presença confirmada.')]
}
for key,items in card_data.items():
    body=heading('Cartões recortáveis · '+topics[key]['label'],'Conecte as partes')+p('<span class="small">Recorte nas linhas tracejadas antes do ensaio. Na prova, você pode apenas apontar para o slide, sem mover os cartões.</span>')+'<div class="cards">'+''.join(f'<div class="card"><div class="eyebrow">{title}</div><h2><code>{esc(value)}</code></h2><p>{text}</p></div>' for title,value,text in items)+'</div>'
    write_doc('cartoes_'+key,'Cartões '+topics[key]['label'],[('',body)],True)

# Precise speaking guides: each tuple is one of the eight timed segments.
scripts={
'html':[
('Pergunta inicial','“Imagine que sua turma está planejando a festa de formatura do curso. Você recebe este convite: o que precisa descobrir primeiro?” Aponte nome, descrição e link. Em turma, aceite duas respostas curtas; acolha esporte, música e jogos sem supor que todos gostam do mesmo hobby.','Espere 5 segundos. Sem resposta: “Precisamos reconhecer o nome do evento, entender o que acontece e encontrar a programação.”'),
('Objetivos','“Ao final desta aula, vocês vão marcar título, descrição e link e fazer esse link chegar à programação. Não precisamos decorar uma página inteira: vamos entender a função de cada parte.” Explique que HTML é uma linguagem de marcação.','Mostre os três objetivos e avance. Não antecipe CSS ou JavaScript.'),
('Anatomia e significado','“As etiquetas dizem ao navegador o papel de cada informação.” Percorra <h1>, Festa de formatura e </h1>: abertura, conteúdo, fechamento. “O conjunto é o elemento. h1 identifica o título principal; p marca um parágrafo; a, com href, cria um link.”','Pergunte qual marca escolher para a descrição. Resposta esperada: p. A leitura em voz alta e os rótulos tornam a figura compreensível sem depender da cor.'),
('Código e resultado','Leia o fragmento por função, não caractere por caractere. main contém o conteúdo principal; h1 nomeia o evento; p descreve; o link leva à seção; h2 nomeia a programação. “Este é o miolo de um documento: na página completa ele fica dentro de body.”','Aponte no código e em seguida no convite. Diga que o navegador costuma dar aparência padrão aos elementos, mas a função não se resume ao tamanho da fonte.'),
('Simulação do link','“href é o endereço do link. Com #agenda, procuramos o elemento cujo id é agenda nesta página.” Mostre o cartão LINK e as duas opções DESTINO e OUTRO DESTINO. “Qual combina?” Aproxime LINK de DESTINO ou aponte para o slide.','Resposta: id="agenda". Diga: “O # aparece no href; o valor do id não contém #. O id deve ser único no documento.” Reserve 5 segundos de previsão antes de mostrar.'),
('Desafio','Apresente o item 2: completar <h1>, </h1> e #agenda; identificar que a descrição já usa p. “Em dupla, uma pessoa escolhe e outra explica a função. Vocês têm 60 segundos.” Em turma, acompanhe uma dupla sem interromper as demais.','Na banca: apresente a consigna, dê 5–8 segundos de reflexão e resolva explicando os critérios. Não espere um minuto nem peça que examinadores assumam papéis.'),
('Correção e transferência','Mostre a solução: título em h1, descrição em p, link com href="#agenda". Apresente o código com funções trocadas. “Estar grande na tela garante que a informação está bem marcada?” Corrija as tags, mantendo o texto.','Conte três evidências: título, parágrafo e link corretos. Se houve confusão, retome “o que esta informação faz?” e convide a tentar de novo. Cite a mesma lógica para notícia ou receita.'),
('Saída e encerramento','“Complete o href para chegar a id=agenda e explique a relação.” Espere 5 segundos, depois confirme #agenda. “Hoje você organizou o significado do convite: título, descrição e link. Na próxima aula da disciplina podemos estudar a aparência.”','No plano, o desafio vale três critérios e a saída um. Conclua em 19 minutos; não abra uma nova discussão.')],
'css':[
('Pergunta inicial','Mostre os dois convites. “O texto é igual, mas em qual deles vocês leriam o convite com mais conforto?” Peça uma justificativa sobre espaço e organização. “Isso acontece em cards de produtos, notícias e resultados de jogos.”','Espere 5 segundos. Sem resposta: “No segundo, o texto tem espaço até a borda. Vamos descobrir qual instrução cria esse espaço.” Não trate preferência estética como certo ou errado.'),
('Objetivos e retomada','“Hoje vamos selecionar uma classe e distinguir o espaço dentro e fora da caixa.” Mostre class="convite". “class é um nome que colocamos no HTML. O CSS encontra esse nome usando .convite.”','Se a turma não lembra class, leia o HTML e circule convite. Não é necessário que tenha visto a aula de HTML deste kit.'),
('Regra CSS','Aponte .convite, color e #17233c. “Seletor diz quem recebe a regra. Propriedade diz o que muda. Valor diz como fica.” Leia também background-color. “Podemos aplicar essa mesma classe a vários convites.”','Mostre chaves, dois-pontos e ponto e vírgula sem transformar o momento em memorização. Pergunte: “Qual parte escolhe quem muda?” Resposta: seletor.'),
('Modelo de caixa','Mostre o diagrama do centro para fora: conteúdo, padding, border e margin. “Pense em um quadro: imagem, espaço até a moldura, moldura e distância até outro quadro.” Ressalte que é uma analogia para a posição de cada região.','Aponte cada rótulo, lendo em voz alta. A cor só reforça a posição. Explique que margin não faz parte do fundo da caixa; o fundo pode aparecer no padding.'),
('Previsão e cartões','Leia a regra completa. “Se aumentarmos padding, o texto ganha espaço interno. Se aumentarmos margin, a caixa se afasta das outras.” Organize ou aponte os quatro cartões do centro para fora. Mostre a correspondência class="convite" → .convite.','Peça a previsão antes de revelar. Nos exemplos, um valor de padding ou margin se aplica aos quatro lados. Não introduza cálculo de largura, cascata ou flexbox nesta aula curta.'),
('Desafio','“Nosso convite está apertado por dentro e encostado em outro convite. Completem seletor, espaço interno e espaço externo.” Dê 60 segundos em dupla: uma pessoa completa, a outra justifica.','Na banca: dê 5–8 segundos de reflexão e resolva. Não dependa de resposta, distribuição de folhas ou uso de quadro.'),
('Correção e transferência','Confirme .convite, padding e margin. Mostre o erro: usar só margin para texto encostado na borda. “Margin move a distância externa; não cria o espaço que falta dentro.” Aponte a região padding no diagrama.','Três critérios: seletor, espaço interno e externo. Se houver troca, use o gesto dentro/fora e peça uma nova decisão. Aplique a um card de produto ou calendário.'),
('Saída e encerramento','“O preço de um produto está encostado na borda do card: padding ou margin? Por quê?” Espere 5 segundos e confirme padding. “Hoje você aprendeu a encontrar a classe e dar espaço ao conteúdo.”','A saída vale um critério. Lembre que legibilidade envolve contraste e espaço, não apenas a cor. Termine em 19 minutos.')],
'javascript':[
('Pergunta inicial','Mostre os estados antes e depois. “Você clica em Participar, e o convite responde. Que mudança faz você perceber que seu clique foi recebido?” Relacione a curtir uma publicação, confirmar empréstimo de livro ou enviar uma escolha.','Espere 5 segundos. Sem resposta: “A mensagem mudou, o botão diz Confirmado e fica desabilitado.” Diga que é uma simulação local, sem cadastro real.'),
('Objetivos e retomada','“Hoje vamos encontrar um elemento, ouvir o clique e mudar seu texto.” Retome: variável guarda uma referência; função agrupa instruções que podem executar depois. “O DOM é a representação da página que o JavaScript consegue acessar.”','Esses pré-requisitos estão no plano. Se faltarem, use a referência como uma etiqueta apontando para o botão; o objetivo é ler e completar, não memorizar todos os métodos.'),
('Encontrar o alvo','Mostre querySelector("#participar"). “document representa o documento; querySelector encontra o primeiro elemento que combina com o seletor. #participar encontra o id participar. botao é o nome da variável que guarda a referência.”','Explique apenas essa seleção. Não ensine todos os seletores. Se nenhum elemento combinar, o resultado é null; será retomado na depuração.'),
('Preparar os elementos','Leia o HTML do botão e do parágrafo status. Conecte id=participar a #participar e id=status a #status com os cartões. “O script vem depois desses elementos, para que já existam quando forem procurados.”','O botão é nativo, pode ser ativado pelo teclado. aria-live="polite" permite que tecnologias assistivas anunciem a mensagem alterada; não é necessário decorar o atributo.'),
('Evento e função de resposta','Leia a seleção das duas referências. “addEventListener registra uma resposta para click. A função aqui dentro executa quando ocorre o clique.” Aponte as três mudanças: texto da mensagem, texto do botão e disabled=true.','Na simulação, aponte EVENTO e então RESPOSTA. A função não executa só por ter sido registrada. const impede trocar a referência, mas não impede alterar propriedades do elemento.'),
('Desafio','Apresente as duas lacunas: click e textContent. “Em dupla, uma pessoa completa e a outra diz quando a mudança acontece.” Dê 60 segundos.','Na banca: ofereça 5–8 segundos de reflexão e mostre a solução. Não dependa de cliques em dispositivo pessoal ou de participação da banca.'),
('Correção e depuração','Confirme click e textContent. Recupere #status para a seleção. Mostre a seleção errada "status": “Sem #, esse seletor busca um elemento chamado status, e não o id. Neste documento não existe esse elemento; o resultado será null.”','Três critérios: seleção, evento e mudança de texto. Corrija com a correspondência id → #id. Explique que apenas alterar o texto não envia nem persiste inscrição.'),
('Saída e encerramento','“Depois do clique, que frase aparece? O que iniciou a mudança?” Resposta: Você está na lista!, iniciada pelo evento click. “Hoje você conectou elemento, evento e resposta. Esse é um primeiro passo para uma interface interativa.”','A saída vale um critério: mensagem e momento corretos. Não abra o tema de servidor, banco de dados ou fetch. Termine em 19 minutos.')]
}

guide=[]
guide.append(('',heading('Guia de preparação · Concurso 012/01/2026','Três aulas, um projeto escolar')+p('Aulas para estudantes de 15 anos do Ensino Médio integrado ao técnico em Desenvolvimento de Sistemas. Cada tema é uma aula independente, com recorte suficiente para ensinar e avaliar em até 20 minutos.')+box('O projeto',p('A turma está planejando a festa de formatura do curso, em um salão da escola. O convite organiza informações (HTML), recebe estilo e espaço (CSS) e reage à confirmação de presença (JavaScript). Esporte, música, livros e jogos podem entrar nos exemplos conforme a turma.'),'mint')+ul(['HTML: estrutura, significado e link interno.','CSS: classe, regra e modelo de caixa.','JavaScript: seleção, evento e alteração de texto.'])+'<h2>O que levar para a prova</h2>'+ul(['Três vias de cada plano: nove páginas no PDF planos_banca_3_vias. Entregar apenas as três do tema sorteado.','Slides impressos das apresentações dos três temas; cartões opcionais, já recortados.','Documento oficial original com foto; cópias impressas dos títulos aplicáveis, entregues antes da aula.','Folhas de atividade são necessárias para uma turma real; na banca, mostre a atividade no próprio slide.'])+'<h2>O que usar somente no ensaio</h2>'+p('Este guia, gabaritos e demos digitais servem para estudar e ensaiar. Durante a apresentação, o apoio será o plano e o material de apresentação impresso de sua própria preparação. Revise e personalize os materiais antes de usá-los.')+box('Tempo e recursos',p('O roteiro fecha em 19 minutos, com 1 minuto de margem. A prova não permite relógio de qualquer tipo, equipamentos eletrônicos pessoais ou internet. Use cronômetro apenas nos ensaios. A projeção institucional é opcional e depende de autorização.'))))
guide.append(('',heading('Preparação prática','Impressão e apresentação')+'<h2>Organize três pastas</h2>'+p('Identifique HTML, CSS e JavaScript. Em cada pasta coloque três vias do plano, oito slides e os cartões opcionais. Deixe atividade e gabarito separados para ensaio. Preencha o nome do candidato nos HTML dos planos antes de gerar os PDFs finais.')+'<h2>Slides da apresentação</h2>'+p('Imprima as apresentações em A4 paisagem, frente simples, escala 100%. São oito slides por tema. A3 é uma opção para maior distância: ampliar para caber na página. Se a impressão for em preto e branco, os rótulos e posições preservam o significado dos diagramas. Não deixe os slides soltos: numere e prenda o conjunto.')+'<h2>Apresentação perante a banca</h2>'+p('Fale como professor para uma turma de adolescentes, com linguagem clara e respeitosa. As perguntas fazem parte da aula, mas não obrigue os examinadores a responder ou representar alunos. Ofereça alguns segundos de reflexão e apresente a resposta esperada. Não atribua à banca uma resposta que ela não deu.')+p('Na atividade de dupla, explique o procedimento de uma turma real. Na apresentação, avance para a resolução comentada após uma pausa breve. O tempo economizado permite explorar o diagrama e explicar o raciocínio com calma, sem estender a aula além do limite.')+'<h2>Plano sem projeção</h2>'+p('Mostre o slide e aponte código e resultado. Na simulação, aproxime dois cartões ou apenas indique as partes na impressão. Quadro é recurso adicional, se disponível; nenhuma etapa exige quadro, tomada, adesivo ou internet.')+'<h2>Plano com projeção institucional autorizada</h2>'+p('Use os mesmos oito slides como apoio. Combine previamente o meio aceito pela unidade; não pressuponha uso de pen drive, e-mail ou equipamento pessoal. Mantenha os slides impressos prontos. As demos são destinadas ao ensaio e a futuras aulas com infraestrutura própria.')+box('Participação inclusiva',p('Dê tempo de pensar antes da resposta. Permita resposta oral, escrita ou em desenho; leia os exemplos e descreva o diagrama. Não dependa apenas de cor. Em turma, alterne quem escreve e quem explica na dupla.'))))
for key in topics:
    for half in range(2):
        body=heading('Roteiro de fala · '+topics[key]['label'],topics[key]['title']+(' · abertura' if half==0 else ' · prática'))
        for i in range(half*4,half*4+4):
            title,speech,action=scripts[key][i]
            body+=f'<h2>Slide {i+1} · {timings[i][0]} · {title}</h2>'+p(speech)+p('<span class="small"><b>Condução:</b> '+action+'</span>')
        guide.append(('',body))

keys={
'html':[
('Item 1','Nome do evento: h1. Descrição: p. Ver programação: a, com href. A função do conteúdo orienta a escolha; tamanho visual é assunto de estilo.'),
('Item 2',code('<h1>Festa de formatura</h1>\n<p>Música e fotos com a turma.</p>\n<a href="#agenda">Ver programação</a>')+p('Três critérios: título em h1; descrição em p; link a com href="#agenda". O destino tem id="agenda".')),
('Item 3',code('<h1>Festa de formatura</h1>\n<p>Música e fotos com a turma.</p>')+p('A descrição não é o título principal. O exercício avalia significado, não preferência de fonte.')),
('Saída','Na folha: href="#jogos", porque o destino tem id="jogos". No slide: href="#agenda". O # pertence ao seletor/endereço de fragmento, não ao valor do id.'),
('Extensão','Resposta possível: <h1>Festival de Música</h1>, <p>Bandas no pátio.</p> e <a href="#local">Ver local</a>, com uma seção id="local". Outras respostas são válidas quando as funções e correspondências estão corretas.')],
'css':[
('Item 1','O seletor é .convite. No HTML, o nome da classe aparece sem ponto; no CSS, o ponto identifica a seleção por classe.'),
('Item 2',code('.convite {\n  padding: 16px;\n  border: 2px solid #1745a0;\n  margin: 12px;\n}')+p('Três critérios: seletor de classe; padding para o espaço interno; margin para o externo.')),
('Item 3','Alterar padding. No desenho, o espaço fica entre conteúdo e borda. Aumentar margin altera o espaço externo e não resolve a distância entre texto e contorno.'),
('Saída','Padding: o preço precisa de espaço dentro da caixa. Margin seria adequado para afastar o cartão de outro cartão, conforme o contexto e o layout.'),
('Extensão','Do centro para fora: conteúdo → padding → border → margin. O desenho deve mostrar a ordem e rótulos legíveis. A cor é opcional. Não exigir cálculo de largura nesta aula.')],
'javascript':[
('Item 1',code('document.querySelector("#status")')+p('Seleciona o primeiro elemento que corresponde ao seletor; aqui o parágrafo com id="status".')),
('Item 2',code('botao.addEventListener("click", function () {\n  status.textContent = "Presença confirmada!";\n});')+p('Três critérios: #status na seleção do item 1; click no evento; textContent na atualização.')),
('Item 3','Falta #. "status" procura um elemento pelo nome da tag. Na página apresentada não há uma tag status, portanto retorna null. Tentar mudar textContent de null causaria erro.'),
('Saída','Mensagem: “Você está na lista!”. Momento: após o evento click no botão. A instrução muda o texto no DOM; sozinha não envia nem persiste uma inscrição. Recarregar a demo restaura seu estado inicial.'),
('Extensão','É válido trocar a frase por “Empréstimo confirmado!” mantendo click e textContent. O evento continua sendo a ativação do botão, independentemente do texto da mensagem.')]
}
for key in topics:
    body=heading('Gabarito comentado · '+topics[key]['label'],'Respostas e avaliação')
    for title,answer in keys[key]: body+=f'<h2>{title}</h2>'+(answer if answer.startswith('<') else p(answer))
    body+=box('Registro formativo',p('Registre 0 ou 1 para cada um dos três critérios do desafio e para a saída. Meta didática: ao menos 3 de 4, com justificativa. Esse registro é para a aprendizagem dos alunos, não a escala da banca. Diante de erro, retome o diagrama, modele uma resposta e ofereça nova tentativa.'))
    guide.append(('',body))

guide.append(('',heading('Ensaio','Como chegar aos 19 minutos')+'<h2>Três rodadas por tema</h2>'+ul(['Rodada 1: explique os conceitos olhando para os slides. Abra a demo depois para verificar as previsões; compare com os gabaritos.','Rodada 2: cronometre a aula inteira sem computador. Grave somente o ensaio, se desejar, para observar ritmo, voz e gestos. Na prova, a gravação é vedada.','Rodada 3: sorteie um tema, separe suas três vias de plano e apresente com os slides. Simule silêncio nas perguntas. Verifique encerramento antes de 20 minutos.'])+'<h2>Marcos para memorizar</h2>'+p('Objetivos até 3 min; conceito até 6; exemplo até 9; simulação até 12; desafio até 15; correção até 18; saída e síntese até 19. Sem relógio na prova, use a sequência e o ritmo treinados, evitando improvisar novos tópicos.')+'<h2>Se o ensaio passar do tempo</h2>'+p('Reduza os exemplos secundários e falas repetidas; mantenha objetivos, exemplo central, desafio, correção e saída. A versão perante a banca não precisa aguardar o minuto inteiro de trabalho em dupla. Não retire a avaliação nem leia todos os caracteres do código.')+'<h2>Checklist de qualidade da aula</h2>'+ul(['Conteúdo: consigo explicar o que cada linha faz e corrigir o erro mostrado?','Planejamento: verbalizo os objetivos e mostro a sequência sem ler o plano inteiro?','Didática: alterno explicar, prever, representar e praticar? Mostro como avalio a aprendizagem?','Expressão: olho para a turma, aponto com intenção e falo com dicção e pausas?','Comunicação: uso exemplos próximos dos adolescentes e explico o vocabulário técnico?'])+box('Após cada ensaio',p('Duração: ______ · Conceito que ficou confuso: __________________<br>Ajuste para a próxima rodada: __________________________________'))))
guide.append(('',heading('Conferência final','Regras da prova e fontes')+'<h2>Convocação fornecida</h2>'+p('Prova em 21/10/2026, às 14h, na Etec Professor Camargo Aranha, Rua Marcial, 25, Mooca, São Paulo. Comparecimento recomendado com 60 minutos de antecedência. Duração máxima: 20 minutos. Temas: HTML, CSS, JavaScript. O tema é sorteado antes do início da aula.')+'<h2>Edital de abertura fornecido</h2>'+p('Capítulo XI.4, itens 16 e 17: preparar os três temas em três vias; entregar as três vias do tema sorteado. XI.4, item 23: relógios de qualquer tipo e equipamentos eletrônicos pessoais são vedados. A convocação especifica apoio por plano/material de apresentação impresso elaborado pelo candidato e projeção institucional condicionada à disponibilidade.')+p('Anexo VII: conteúdo 40; planejamento 20; procedimento didático 20; expressão 10; linguagem e comunicação 10. XII.2: aprovação na prova pedagógica com pelo menos 50. XIV: nota final = (PE + PMP)/2 + PT, consideradas pontuações diferenciadas aplicáveis.')+'<h2>Títulos</h2>'+p('Levar cópias impressas antes da apresentação. Pontuações previstas: especialização 5, mestrado 10 e doutorado 15; máximo ordinário 30. Há exigências de área, conclusão até o término das inscrições e exclusão de curso usado como requisito. Confira seus documentos no XI.5 e Anexo VII; não presuma que todo certificado pontua.')+'<h2>Referências técnicas</h2>'+ul([f'<a href="{t["source"]}">MDN Web Docs · {t["label"]}</a>' for t in topics.values()])+p('<span class="small">Consulta em 13/10/2026. Exemplos, projeto e atividades do kit foram construídos para esta preparação. Os links são referências de estudo; o material didático impresso funciona sem acesso a eles.</span>')+'<h2>Antes de sair</h2>'+p('□ Nome nos planos  □ Nove vias separadas por tema  □ Slides<br>□ Documento original  □ Títulos aplicáveis  □ Rota e chegada às 13h<br>□ Materiais revisados  □ Ensaio sem equipamento pessoal')))
write_doc('guia_professor','Guia do professor e gabaritos',guide)

# Offline examples intentionally separate from the material used at the examination.
demo_style='''body{font-family:Arial,sans-serif;line-height:1.5;max-width:950px;margin:32px auto;padding:0 20px;color:#17233c}h1{line-height:1.2}button,select,input{font:inherit}button{padding:10px 16px;background:#1745a0;color:white;border:2px solid #1745a0;border-radius:6px;cursor:pointer}button:disabled{background:#d9e2f0;color:#17233c;cursor:default}a{color:#1745a0}pre{white-space:pre-wrap;background:#eef2f9;padding:16px;overflow-wrap:anywhere}label{display:block;margin:12px 0}.notice{background:#fff1ba;padding:14px;border-radius:8px}.cols{display:grid;grid-template-columns:1fr 1fr;gap:22px}@media(max-width:650px){.cols{grid-template-columns:1fr}}*:focus-visible{outline:3px solid #963400;outline-offset:4px}'''
def demo_write(key,title,body,script=''):
    (OUT/'demos'/f'{key}.html').write_text(f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{title}</title><style>{demo_style}</style></head><body><a href="../INICIO.html">← Voltar ao kit</a><h1>{title}</h1><p class="notice">Demonstração para ensaio e aula com infraestrutura. Funciona sem internet. Na prova, use os slides impressos.</p>{body}<script>{script}</script></body></html>')

html_full='''<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Festa de formatura</title>
</head>
<body>
'''+HTML_FRAGMENT+'''
</body>
</html>'''
(OUT/'demos'/'exemplo_html_completo.html').write_text(html_full)
(OUT/'demos'/'exemplo_css_completo.html').write_text('''<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Convite com CSS</title>
  <style>
'''+CSS_FRAGMENT+'''
  </style>
</head>
<body>
  <main>
    <h1>Eventos da escola</h1>
    <article class="convite">
      <h2>Festa de formatura</h2>
      <p>Música e fotos com a turma.</p>
    </article>
    <article class="convite">
      <h2>Clube do Livro</h2>
      <p>Histórias e conversas na biblioteca.</p>
    </article>
  </main>
</body>
</html>''')
(OUT/'demos'/'exemplo_javascript_completo.html').write_text('''<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Confirmação local com JavaScript</title>
</head>
<body>
  <main>
    <h1>Festa de formatura</h1>
    <p>Música e fotos com a turma.</p>
'''+JS_MARKUP+'''
    <p>Esta simulação não envia nem salva uma inscrição.</p>
  </main>
  <script>
'''+JS_FRAGMENT+'''
  </script>
</body>
</html>''')
demo_write('html','HTML · estrutura e destino',p('Antes de clicar, preveja: qual seção será encontrada? Depois, mude o destino e veja como href e id precisam combinar.')+'<label for="destino">Destino do link</label><select id="destino"><option value="agenda">Programação</option><option value="local">Local</option></select><div class="cols"><div>'+code(HTML_FRAGMENT)+'<pre id="trecho"></pre></div><div><main><h1>Festa de formatura</h1><p>Música e fotos com a turma.</p><a id="link" href="#agenda">Ver programação</a><div style="height:240px"></div><h2 id="agenda">Programação</h2><p>19h: recepção da turma.</p><h2 id="local">Local</h2><p>Salão da escola.</p></main></div></div><p><a href="exemplo_html_completo.html">Abrir documento HTML completo e mínimo</a></p>', r'''const destino=document.querySelector('#destino');const link=document.querySelector('#link');const trecho=document.querySelector('#trecho');function mostrar(){const id=destino.value;link.setAttribute('href','#'+id);link.textContent=id==='agenda'?'Ver programação':'Ver local';trecho.textContent='<a href="#'+id+'">'+link.textContent+'</a>\nDestino: id="'+id+'"';}destino.addEventListener('change',mostrar);mostrar();''')

demo_write('css','CSS · o espaço aparece',p('Mova um controle por vez. Antes de mover, aponte onde espera ver o espaço mudar.')+'<label for="padding">Padding — interno: <output id="vp">16</output> px</label><input id="padding" type="range" min="0" max="40" value="16"><label for="margin">Margin — externo: <output id="vm">12</output> px</label><input id="margin" type="range" min="0" max="40" value="12"><label for="estilo"><input id="estilo" type="checkbox" checked> Aplicar cores e contorno</label><div class="cols"><pre id="regra"></pre><div style="background:#fff1ba;border:2px dashed #7e6743;min-height:280px;display:flow-root"><article class="convite" id="convite"><h2 style="margin:0">Festa de formatura</h2><p>Música e fotos com a turma.</p><a href="#">Ver programação</a></article><p style="margin:0">Outro conteúdo da página</p></div></div><p>Região amarela: fundo do elemento pai. O espaço externo mostra esse fundo. O fundo verde pertence ao convite e se estende pelo padding. Modelo usado: content-box, sem largura fixa.</p>', r'''const padding=document.querySelector('#padding'),margin=document.querySelector('#margin'),estilo=document.querySelector('#estilo'),convite=document.querySelector('#convite');function atualizar(){const interno=padding.value,externo=margin.value,ativo=estilo.checked;document.querySelector('#vp').value=interno;document.querySelector('#vm').value=externo;convite.style.cssText='box-sizing:content-box;padding:'+interno+'px;margin:'+externo+'px;background-color:'+(ativo?'#dcf6ea':'transparent')+';color:#17233c;border:'+(ativo?'2px solid #1745a0':'0');document.querySelector('#regra').textContent='.convite {\n  background-color: '+(ativo?'#dcf6ea':'transparent')+';\n  color: #17233c;\n  padding: '+interno+'px;\n  border: '+(ativo?'2px solid #1745a0':'0')+';\n  margin: '+externo+'px;\n}';}padding.addEventListener('input',atualizar);margin.addEventListener('input',atualizar);estilo.addEventListener('change',atualizar);atualizar();''')

demo_write('javascript','JavaScript · clique e confirmação',p('Preveja o estado depois do clique. Você também pode focar o botão com Tab e ativá-lo com Enter ou Espaço.')+'<div class="cols"><div><h2>Festa de formatura</h2>'+JS_MARKUP+'<p><button id="reiniciar" type="button">Reiniciar demonstração</button></p><p>A confirmação é local: nenhum dado é enviado ou salvo.</p></div><div>'+code(JS_FRAGMENT)+'</div></div><h2>Trilha do evento</h2><p id="trilha" aria-live="polite">1. Elementos encontrados → 2. Esperando click.</p>',JS_FRAGMENT+'''
botao.addEventListener('click',function(){document.querySelector('#trilha').textContent='1. Elementos encontrados → 2. click recebido → 3. Texto atualizado e botão desabilitado.';});
document.querySelector('#reiniciar').addEventListener('click',function(){status.textContent='Sua presença ainda não foi confirmada.';botao.textContent='Participar';botao.disabled=false;document.querySelector('#trilha').textContent='1. Elementos encontrados → 2. Esperando click.';});''')

index=heading('Kit de preparação · Programação Web I','Festa de formatura')+p('Três aulas independentes para alunos de 15 anos: planos, slides, atividades e simulações. Comece pelo guia, personalize o nome nos planos e ensaie um tema por vez.')+p('<a href="pdf/guia_professor.pdf">Guia do professor e gabaritos em PDF</a> · <a href="editaveis/guia_professor.html">Guia editável</a>')+box('Impressão para a banca',p('<a href="pdf/planos_banca_3_vias.pdf">Nove páginas: três vias de cada plano</a>. Imprima uma vez, frente simples. Separe por tema e entregue apenas as três do tema sorteado. Nome do candidato deve ser preenchido.'))
for key,t in topics.items():
    index+=f'<h2>{t["label"]} · {t["title"]}</h2>'+p(t['lesson'])+'<ul>'+''.join(f'<li><a href="pdf/{kind}_{key}.pdf">{name} PDF</a> · <a href="editaveis/{kind}_{key}.html">Versão editável</a></li>' for kind,name in [('plano','Plano para a banca'),('apresentacao','Oito slides'),('atividade','Atividade dos alunos'),('cartoes','Cartões recortáveis')])+'</ul>'+p(f'<a href="demos/{key}.html">Abrir demonstração interativa offline para ensaio</a> · <a href="demos/exemplo_{key}_completo.html">Exemplo mínimo completo para estudar o código</a>')
index+=box('Uso na prova',p('Aulas planejadas para 19 minutos + 1 minuto de margem. Slides e plano funcionam impressos. Projeção institucional depende de autorização; demos são para ensaio. Sem internet, equipamentos pessoais ou relógio durante a apresentação.'))+p('As versões editáveis são arquivos HTML: abra em um editor de texto para alterar o conteúdo. Após editar, imprima pelo navegador em “Salvar como PDF”. O gerador recria os arquivos originais; guarde versões personalizadas com outro nome antes de rodá-lo.')
(OUT/'INICIO.html').write_text(f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Kit Festa de formatura</title><style>{demo_style}</style></head><body>{index}</body></html>')
(OUT/'manifesto.json').write_text(json.dumps({'temas':list(topics),'planos_paginas':1,'vias_banca':9,'slides_por_tema':8,'duracao_minutos':19,'margem_minutos':1,'guia_paginas':len(guide),'idade_alunos':15},ensure_ascii=False,indent=2))
print('Materiais HTML gerados em',OUT,'| Guia:',len(guide),'páginas')

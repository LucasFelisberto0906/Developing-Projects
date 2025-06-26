import math
import re
import pygame

pygame.init()

WIDTH = 400
HEIGHT = 600
BORDA = 20

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Calculadora")

running = True
clock = pygame.time.Clock()

# CORES 
CORPO = (46, 53, 64)
TELA = (193, 204, 212)
BOTOES_NUM = (125, 138, 150)
BOTAO_PONTO = (89, 96, 106)
BOTAO_OPERACOES = (244, 186, 59)
BOTAO_IGUAL = (242, 90, 60)
BOTAO_TEXTO = (255, 255, 255)


# tela
texto_aparecer_tela = ""

rect = pygame.Rect(BORDA//2, 60, WIDTH - BORDA, 110)

botoes = [
	['DEL','C','(',')'],
	['√','^','e','π'],
	['7', '8','9','/'],
	['4','5','6','x'],
	['1','2','3','-'],
	['0','.','=','+']
]


w = WIDTH // 4
h = 70
borda_topo = 185
font_hist = pygame.font.SysFont('comicsans', 20)
font = pygame.font.SysFont('comicsans', 35)
fonte_tela = pygame.font.SysFont('comicsans', 60)  # Fonte só para a tela

resultado_mostrado = False
botoes_rects = []

def desenhar_botoes():
	botoes_rects.clear()
	
	for linha in range(6):
		for coluna in range(4):
			x = coluna * w + BORDA // 2
			y = linha * h + borda_topo
			rotulo = botoes[linha][coluna]

			if rotulo in {'+', '-', '/', 'x'}:
				cor = BOTAO_OPERACOES
			elif rotulo == '=':
				cor = BOTAO_IGUAL
			elif rotulo == 'C' or rotulo == 'DEL':
				cor = BOTAO_PONTO
			else:
				cor = BOTOES_NUM
			
			btn_rect = pygame.Rect(x, y, w - BORDA, h - BORDA)
			pygame.draw.rect(win, cor, btn_rect, border_radius=20)

			texto = font.render(rotulo, True, BOTAO_TEXTO)
			texto_rect = texto.get_rect(center=btn_rect.center)
			win.blit(texto, texto_rect)

			botoes_rects.append((btn_rect, rotulo))

	
def calcular_com_funcoes(expressao: str) -> str:
	try:
		expr = expressao
		expr = expr.replace('x', '*')
		expr = expr.replace('^', '**')
		expr = expr.replace('π', 'math.pi')
		expr = re.sub(r'\be\b', 'math.e', expr)
		expr = re.sub(r'√\s*\(?([0-9.]+)\)?', r'math.sqrt(\1)', expr)
		resultado = eval(expr, {"math": math})

		if isinstance(resultado, float) and resultado.is_integer():
			return str(int(resultado))
		else:
			return str(round(resultado, 5))
	except:
		return "Erro"

# historico
historico = []
historico_btn = []
mostrar_historico = False
def des_historico(x, y, width, height):
	his_rect = pygame.Rect(x,y, width, height)
	pygame.draw.rect(win, (255, 0, 0), his_rect, border_radius=20)
	text = font_hist.render("HISTÓRICO", True, (255, 255, 255))
	text_rect = text.get_rect(centery=rect.centery, left=rect.left + 120, top=rect.top - 50)
	win.blit(text, text_rect)
	historico_btn.append(his_rect)

while running:
	clock.tick(60)

	if mostrar_historico:
		win.fill(CORPO)

		titulo = font.render("HISTÓRICO", True, (255, 255, 255))
		win.blit(titulo, (WIDTH//2 - titulo.get_width()//2, 30))

		y_atual = 100

		for i, entrada in enumerate(reversed(historico[-10:])):
			linha = font.render(entrada, True, (255, 255, 255))
			win.blit(linha, (40, y_atual))
			y_atual += 30

		voltar_texto = font_hist.render("Clique para voltar", True, (200, 200, 200))
		win.blit(voltar_texto, (WIDTH//2 - voltar_texto.get_width()//2, HEIGHT - 40),)

		pygame.display.update()

		espera = True
		while espera:
			for ev in pygame.event.get():
				if ev.type == pygame.QUIT:
					running = False
					espera = False
				elif ev.type == pygame.MOUSEBUTTONDOWN:
					mostrar_historico = False
					espera = False
		continue


	win.fill(CORPO)
	pygame.draw.rect(win, TELA, rect, border_radius=20)

	texto_entrada = fonte_tela.render(texto_aparecer_tela, True, (0,0,0))
	texto_entrada_rect = texto_entrada.get_rect(right=rect.right - 20, centery=rect.centery)
	win.blit(texto_entrada, texto_entrada_rect)

	des_historico(BORDA//2, BORDA//2, WIDTH - BORDA, 30)
	desenhar_botoes()
	
	pygame.display.update()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.MOUSEBUTTONDOWN:
			for btn_rect, rotulo in botoes_rects:
				if btn_rect.collidepoint(event.pos):
					if rotulo == 'C':
						texto_aparecer_tela = ''
					elif rotulo == '=':
						resultado_mostrado = True
						try:
							historico.append(texto_aparecer_tela)
							texto_aparecer_tela = calcular_com_funcoes(texto_aparecer_tela)
							historico.append(texto_aparecer_tela)
							for cal in historico:
								print(cal)
						except:
							texto_aparecer_tela = "Erro"
					elif rotulo == 'DEL':
						if not resultado_mostrado:
							texto_aparecer_tela = texto_aparecer_tela[:-1]
					else:
						if resultado_mostrado:
							if rotulo in {'+', '-', '/', 'x', '^'}:
								texto_aparecer_tela += rotulo
								resultado_mostrado = False
							else:
								texto_aparecer_tela = rotulo
								resultado_mostrado = False
						else:
							texto_aparecer_tela += rotulo
			for btn_his in historico_btn:
				if btn_his.collidepoint(event.pos):
					mostrar_historico = True
pygame.quit()

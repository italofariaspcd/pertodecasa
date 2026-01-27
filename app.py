import flet as ft
import requests
import time

# URL da sua API
API_URL = "http://127.0.0.1:8000"

def main(page: ft.Page):
    # --- 1. CONFIGURAÇÃO VISUAL (A Janela abre aqui) ---
    page.title = "Perto de Casa SE"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 390
    page.window_height = 844
    page.bgcolor = "#F2F2F2"
    page.scroll = "AUTO"
    page.padding = 0

    # --- 2. COMPONENTES VISUAIS (Criados vazios primeiro) ---
    
    # Cabeçalho
    header = ft.Container(
        bgcolor="blue",
        padding=20,
        content=ft.Row([
            ft.Icon("location_on", color="white"),
            ft.Text("Perto de Casa SE", color="white", size=20, weight="bold")
        ])
    )

    # Dropdown começa com aviso de "Carregando..."
    dd_categoria = ft.Dropdown(
        label="O que você precisa?",
        hint_text="Carregando categorias...",
        options=[],
        bgcolor="white",
        border_radius=10,
        filled=True,
        disabled=True # Travado até carregar
    )

    txt_bairro = ft.TextField(
        label="Qual bairro?",
        hint_text="Ex: Atalaia",
        prefix_icon="search",
        bgcolor="white",
        border_radius=10,
        filled=True
    )

    btn_buscar = ft.ElevatedButton(
        "Encontrar Profissionais",
        bgcolor="blue",
        color="white",
        height=50,
        on_click=None # Definimos a função depois
    )

    # Onde os cards vão aparecer
    lista_resultados = ft.Column(spacing=10)

    # --- 3. MONTAGEM DA TELA (Desenha tudo AGORA) ---
    page.add(
        header,
        ft.Container(
            padding=20,
            content=ft.Column([
                dd_categoria,
                txt_bairro,
                ft.Container(btn_buscar, alignment=ft.Alignment(0, 0)),
                ft.Divider(),
                ft.Text("Resultados:", weight="bold", size=16),
                lista_resultados
            ], spacing=15)
        )
    )
    page.update() # <--- FORÇA O DESENHO NA TELA

    # --- 4. LÓGICA (Roda depois que a tela já apareceu) ---

    def criar_card(p):
        cats_texto = ", ".join(p.get('categories', []))
        return ft.Card(
            elevation=2,
            content=ft.Container(
                padding=15,
                bgcolor="white",
                border_radius=10,
                content=ft.Column([
                    ft.Row([
                        ft.Icon("account_circle", size=40, color="blue"),
                        ft.Column([
                            ft.Text(p['full_name'], weight="bold", size=16),
                            ft.Text(f"📍 {p['neighborhood']}", size=12, color="grey"),
                        ], spacing=2),
                    ]),
                    ft.Text(p['bio'], size=14, max_lines=2, overflow=ft.TextOverflow.ELLIPSIS),
                    ft.Divider(),
                    ft.Row([
                        ft.Container(
                            content=ft.Text(cats_texto, size=12, color="white"),
                            bgcolor="blue", padding=5, border_radius=5
                        ),
                        ft.ElevatedButton(
                            "WhatsApp",
                            icon="message",
                            color="white",
                            bgcolor="green",
                            url=f"https://wa.me/55{p['whatsapp']}",
                            height=30
                        )
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                ])
            )
        )

    def buscar_profissionais(e):
        if not dd_categoria.value:
            return

        btn_buscar.text = "Buscando..."
        btn_buscar.disabled = True
        lista_resultados.controls.clear()
        lista_resultados.controls.append(ft.ProgressBar(width=200, color="blue"))
        page.update()

        try:
            params = {"bairro": txt_bairro.value} if txt_bairro.value else {}
            res = requests.get(f"{API_URL}/search/{dd_categoria.value}", params=params, timeout=5)
            
            lista_resultados.controls.clear()
            
            if res.status_code == 200:
                profissionais = res.json()
                if not profissionais:
                    lista_resultados.controls.append(
                        ft.Container(
                            content=ft.Text("Ninguém encontrado 😔", color="grey"),
                            padding=20,
                            alignment=ft.Alignment(0, 0)
                        )
                    )
                else:
                    for p in profissionais:
                        lista_resultados.controls.append(criar_card(p))
            else:
                lista_resultados.controls.append(ft.Text("Erro no servidor"))
                
        except Exception:
            lista_resultados.controls.clear()
            lista_resultados.controls.append(ft.Text("Erro de conexão"))
        
        btn_buscar.text = "Encontrar Profissionais"
        btn_buscar.disabled = False
        page.update()

    # --- 5. CARREGAMENTO DE DADOS (Background) ---
    # Agora que a tela já existe, vamos buscar os dados
    try:
        print("Buscando categorias...")
        res = requests.get(f"{API_URL}/categories", timeout=3)
        if res.status_code == 200:
            dd_categoria.options = [ft.dropdown.Option(key=c['slug'], text=c['name']) for c in res.json()]
            dd_categoria.disabled = False # Destrava
            dd_categoria.hint_text = "Selecione..."
            print("Sucesso!")
        else:
            dd_categoria.hint_text = "Erro ao carregar"
    except:
        print("Erro de conexão")
        dd_categoria.hint_text = "Sem conexão"

    # Conecta a função ao botão
    btn_buscar.on_click = buscar_profissionais
    page.update() # Atualiza a tela com os dados novos

if __name__ == "__main__":
    ft.app(target=main)
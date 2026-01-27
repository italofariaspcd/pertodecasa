import flet as ft
import requests

# URL da sua API
API_URL = "http://127.0.0.1:8000"

def main(page: ft.Page):
    # --- CONFIGURAÇÃO DA TELA (Visual Mobile) ---
    page.title = "Perto de Casa SE"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 390
    page.window_height = 844
    page.bgcolor = "#F2F2F2"
    page.scroll = "AUTO" # Modo de rolagem seguro
    page.padding = 0

    # --- FUNÇÕES (Lógica) ---
    
    def buscar_categorias():
        """Tenta buscar as categorias na API. Se falhar, retorna lista vazia."""
        print("Tentando buscar categorias...") # Debug no terminal
        try:
            # O timeout evita que o app trave se a internet estiver ruim
            res = requests.get(f"{API_URL}/categories", timeout=3)
            if res.status_code == 200:
                print("Categorias carregadas!")
                return [ft.dropdown.Option(key=c['slug'], text=c['name']) for c in res.json()]
        except Exception as e:
            print(f"Erro ao buscar categorias: {e}")
        return []

    def buscar_profissionais(e):
        """Ação do botão de busca"""
        if not dd_categoria.value:
            # Aviso simples se não escolher nada
            snack = ft.SnackBar(ft.Text("Escolha uma categoria primeiro!"), bgcolor="red")
            page.overlay.append(snack)
            snack.open = True
            page.update()
            return

        # Muda o visual para "Carregando"
        btn_buscar.text = "Buscando..."
        btn_buscar.disabled = True
        lista_resultados.controls.clear()
        lista_resultados.controls.append(ft.ProgressBar(width=200, color="blue"))
        page.update()

        try:
            print(f"Buscando por: {dd_categoria.value}")
            # Prepara os filtros
            params = {"bairro": txt_bairro.value} if txt_bairro.value else {}
            
            # Chama a API com timeout de 5 segundos
            res = requests.get(f"{API_URL}/search/{dd_categoria.value}", params=params, timeout=5)
            
            # Limpa a barra de progresso
            lista_resultados.controls.clear()
            
            if res.status_code == 200:
                profissionais = res.json()
                
                if not profissionais:
                    lista_resultados.controls.append(
                        ft.Container(
                            content=ft.Text("Ninguém encontrado nessa região 😔", color="grey"),
                            padding=20,
                            alignment=ft.alignment.center
                        )
                    )
                else:
                    # Cria os cards para cada profissional encontrado
                    for p in profissionais:
                        lista_resultados.controls.append(criar_card(p))
            else:
                lista_resultados.controls.append(ft.Text(f"Erro no servidor: {res.status_code}", color="red"))
                
        except Exception as erro:
            lista_resultados.controls.clear()
            lista_resultados.controls.append(
                ft.Text(f"Não foi possível conectar ao servidor.\nVerifique se o backend está rodando.", color="red")
            )
            print(f"Erro de conexão: {erro}")
        
        # Restaura o botão
        btn_buscar.text = "Encontrar Profissionais"
        btn_buscar.disabled = False
        page.update()

    def criar_card(p):
        """Cria o visual do card do profissional (Blindado)"""
        # Monta a lista de categorias do profissional
        cats_texto = ", ".join(p.get('categories', []))
        
        return ft.Card(
            elevation=2,
            content=ft.Container(
                padding=15,
                bgcolor="white",
                border_radius=10,
                content=ft.Column([
                    ft.Row([
                        # Ícone e Nome
                        ft.Icon("account_circle", size=40, color="blue"),
                        ft.Column([
                            ft.Text(p['full_name'], weight="bold", size=16),
                            ft.Text(f"📍 {p['neighborhood']}", size=12, color="grey"),
                        ], spacing=2),
                    ]),
                    # Bio
                    ft.Text(p['bio'], size=14, max_lines=2, overflow=ft.TextOverflow.ELLIPSIS),
                    ft.Divider(),
                    # Rodapé do Card
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

    # --- ELEMENTOS VISUAIS (Frontend) ---
    
    # Cabeçalho Azul
    header = ft.Container(
        bgcolor="blue",
        padding=20,
        content=ft.Row([
            ft.Icon("location_on", color="white"),
            ft.Text("Perto de Casa SE", color="white", size=20, weight="bold")
        ])
    )

    # Inputs
    opcoes_categorias = buscar_categorias() # Carrega as categorias ao abrir
    
    dd_categoria = ft.Dropdown(
        label="O que você precisa?",
        hint_text="Selecione...",
        options=opcoes_categorias,
        bgcolor="white",
        border_radius=10,
        filled=True
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
        on_click=buscar_profissionais
    )

    # Área onde os resultados aparecem
    lista_resultados = ft.Column(spacing=10)

    # Montagem Final da Tela
    page.add(
        header,
        ft.Container(
            padding=20,
            content=ft.Column([
                dd_categoria,
                txt_bairro,
                ft.Container(btn_buscar, alignment=ft.alignment.center),
                ft.Divider(),
                ft.Text("Resultados:", weight="bold", size=16),
                lista_resultados
            ], spacing=15)
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
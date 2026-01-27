import flet as ft
import requests

# URL da sua API
API_URL = "http://127.0.0.1:8000"

def main(page: ft.Page):
    # --- CONFIGURAÇÃO DA TELA ---
    page.title = "Perto de Casa SE"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 390
    page.window_height = 844
    page.bgcolor = "#F2F2F2"
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 0

    # --- FUNÇÕES ---
    
    def buscar_categorias():
        """Busca categorias na API com timeout"""
        print("Tentando buscar categorias...")
        try:
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
            snack = ft.SnackBar(ft.Text("Escolha uma categoria primeiro!"), bgcolor="red")
            page.overlay.append(snack)
            snack.open = True
            page.update()
            return

        btn_buscar.text = "Buscando..."
        btn_buscar.disabled = True
        lista_resultados.controls.clear()
        # Barra de progresso enquanto carrega
        lista_resultados.controls.append(ft.ProgressBar(width=200, color="blue"))
        page.update()

        try:
            print(f"Buscando por: {dd_categoria.value}")
            params = {"bairro": txt_bairro.value} if txt_bairro.value else {}
            
            res = requests.get(f"{API_URL}/search/{dd_categoria.value}", params=params, timeout=5)
            
            lista_resultados.controls.clear()
            
            if res.status_code == 200:
                profissionais = res.json()
                
                if not profissionais:
                    lista_resultados.controls.append(
                        ft.Container(
                            content=ft.Text("Ninguém encontrado nessa região 😔", color="grey"),
                            padding=20,
                            alignment=ft.Alignment(0, 0)
                        )
                    )
                else:
                    for p in profissionais:
                        lista_resultados.controls.append(criar_card(p))
            else:
                lista_resultados.controls.append(ft.Text(f"Erro no servidor: {res.status_code}", color="red"))
                
        except Exception as erro:
            lista_resultados.controls.clear()
            lista_resultados.controls.append(
                ft.Text(f"Erro de conexão com o servidor.", color="red")
            )
            print(f"Erro: {erro}")
        
        btn_buscar.text = "Encontrar Profissionais"
        btn_buscar.disabled = False
        page.update()

    def criar_card(p):
        """Cria o visual do card"""
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
                        # ATUALIZADO: ElevatedButton -> FilledButton (Mais moderno)
                        ft.FilledButton(
                            "WhatsApp",
                            icon="message",
                            style=ft.ButtonStyle(bgcolor="green", color="white"),
                            url=f"https://wa.me/55{p['whatsapp']}",
                            height=30
                        )
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                ])
            )
        )

    # --- ELEMENTOS VISUAIS ---
    
    header = ft.Container(
        bgcolor="blue",
        padding=20,
        content=ft.Row([
            ft.Icon("location_on", color="white"),
            ft.Text("Perto de Casa SE", color="white", size=20, weight="bold")
        ])
    )

    # Carrega categorias ao iniciar
    opcoes_categorias = buscar_categorias()
    
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

    # ATUALIZADO: ElevatedButton -> FilledButton
    btn_buscar = ft.FilledButton(
        "Encontrar Profissionais",
        style=ft.ButtonStyle(bgcolor="blue", color="white"),
        height=50,
        on_click=buscar_profissionais
    )

    lista_resultados = ft.Column(spacing=10)

    # Montagem da Tela
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

# ATUALIZADO: ft.app(target=main) -> ft.app(main) (Forma mais segura nas novas versões)
if __name__ == "__main__":
    ft.app(main)
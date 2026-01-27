import flet as ft

def main(page: ft.Page):
    page.title = "Perto de Casa (Modo Teste)"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 390
    page.window_height = 844
    page.bgcolor = "#F2F2F2"
    page.scroll = "AUTO"

    # --- DADOS DE MENTIRINHA (MOCK) ---
    categorias_fake = [
        ft.dropdown.Option("eletricista", "Eletricista"),
        ft.dropdown.Option("manicure", "Manicure"),
        ft.dropdown.Option("pedreiro", "Pedreiro"),
    ]

    def buscar_fake(e):
        # Limpa e mostra um resultado falso
        lista_resultados.controls.clear()
        lista_resultados.controls.append(
            ft.Card(
                content=ft.Container(
                    padding=10,
                    content=ft.Column([
                        ft.Text("João Eletricista (Teste)", weight="bold", size=16),
                        ft.Text("📍 Augusto Franco", color="grey"),
                        ft.Text("Faço instalações e reparos.", size=14),
                        ft.ElevatedButton("WhatsApp", bgcolor="green", color="white")
                    ])
                )
            )
        )
        page.update()

    # --- TELA ---
    header = ft.Container(
        bgcolor="blue",
        padding=20,
        content=ft.Text("Perto de Casa SE", color="white", size=20, weight="bold")
    )

    dd_categoria = ft.Dropdown(
        label="Escolha uma categoria",
        options=categorias_fake,
        bgcolor="white"
    )

    btn_buscar = ft.ElevatedButton(
        "Testar Busca", # Texto direto
        bgcolor="blue",
        color="white",
        on_click=buscar_fake
    )

    lista_resultados = ft.Column()

    page.add(
        header,
        ft.Container(
            padding=20,
            content=ft.Column([
                dd_categoria,
                btn_buscar,
                ft.Divider(),
                lista_resultados
            ])
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
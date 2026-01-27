import flet as ft

def main(page: ft.Page):
    page.title = "Teste Rápido"
    page.bgcolor = "white"
    
    # Adiciona um texto simples e um botão
    page.add(
        ft.Text("Olá! Se você está lendo isso, o Flet está funcionando.", color="black", size=20),
        ft.ElevatedButton("Clique aqui", on_click=lambda e: print("Botão clicado"))
    )

ft.app(target=main)
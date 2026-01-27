import flet as ft

def main(page: ft.Page):
    page.add(ft.Text("Funcionou! O Flet está atualizado."))

ft.app(target=main)
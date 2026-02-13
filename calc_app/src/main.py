from dataclasses import field

import flet as ft


@ft.control
class CalcButton(ft.Button):
    expand: int = field(default_factory=lambda: 1)


@ft.control
class DigitButton(CalcButton):
    bgcolor: ft.Colors = ft.Colors.WHITE_24
    color: ft.Colors = ft.Colors.WHITE


@ft.control
class ActionButton(CalcButton):
    bgcolor: ft.Colors = ft.Colors.ORANGE
    color: ft.Colors = ft.Colors.WHITE


@ft.control
class ExtraActionButton(CalcButton):
    bgcolor: ft.Colors = ft.Colors.BLUE_GREY_100
    color: ft.Colors = ft.Colors.BLACK


@ft.control
class CalculatorApp(ft.Container):
    def init(self):
        self.width = 350
        self.bgcolor = ft.Colors.BLACK
        self.border_radius = ft.BorderRadius.all(20)
        self.padding = 20
        self.result = ft.Text(value="0", color=ft.Colors.WHITE, size=20)
        self.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[self.result],
                    alignment=ft.MainAxisAlignment.END,
                ),
                ft.Row(
                    controls=[
                        ExtraActionButton(content="AC", on_click=self.button_clicked),
                        ExtraActionButton(content="+/-", on_click=self.button_clicked),
                        ExtraActionButton(content="%", on_click=self.button_clicked),
                        ActionButton(content="/", on_click=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(content="7", on_click=self.button_clicked),
                        DigitButton(content="8", on_click=self.button_clicked),
                        DigitButton(content="9", on_click=self.button_clicked),
                        ActionButton(content="*", on_click=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(content="4", on_click=self.button_clicked),
                        DigitButton(content="5", on_click=self.button_clicked),
                        DigitButton(content="6", on_click=self.button_clicked),
                        ActionButton(content="-", on_click=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(content="1", on_click=self.button_clicked),
                        DigitButton(content="2", on_click=self.button_clicked),
                        DigitButton(content="3", on_click=self.button_clicked),
                        ActionButton(content="+", on_click=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(content="0", expand=2, on_click=self.button_clicked),
                        DigitButton(content=".", on_click=self.button_clicked),
                        ActionButton(content="=", on_click=self.button_clicked),
                    ]
                ),
            ]
        )

    def button_clicked(self, e):
        data = e.control.content
        print(f"Button clicked with data = {data}")
        if data == "AC":
            self.result.value = "0"
        elif data == "+/-":
            if self.result.value[0] == "-":
                self.result.value = self.result.value[1:]
            else:
                self.result.value = "-" + self.result.value
        elif data in ".-+*/%":
            if self.result.value[-1] in ".-+*/%":
                self.result.value = self.result.value[:-1] + data
            else:
                self.result.value += data
        elif data == "=":
            try:
                if not self.result.value[-1] in ".-+*/%":
                    self.result.value = str(eval(self.result.value))
            except ZeroDivisionError:
                self.result.value = "Error"
        elif data in "0123456789":
            if self.result.value == "0":
                self.result.value = data
            else:
                self.result.value += data
        
        if self.result.value[-2:] == ".0":
            self.result.value = self.result.value[:-2]
    

def main(page: ft.Page):
    page.title = "Calc App"
    # create application instance
    calc = CalculatorApp()

    # add application's root control to the page
    page.add(calc)


if __name__ == "__main__":
    ft.run(main)
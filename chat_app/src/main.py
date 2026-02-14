from dataclasses import dataclass

import flet as ft

@dataclass
class Message:
    user: str
    text: str
    message_type: str

def main(page: ft.Page):
    page.title = ft.Text('Chat App')
    chat = ft.Column()
    new_message = ft.TextField()
    user_name = ft.TextField(label="Enter your name")


    def on_message(message: Message):
        if message.message_type == "chat message":
            chat.controls.append(ft.Text(f"{message.user}: {message.text}"))
        elif message.message_type == "login message":
            chat.controls.append(
                ft.Text(message.text, italic=True, color=ft.Colors.BLACK_45, size=12)
            )
        page.update()

    page.pubsub.subscribe(on_message)

    def send_click(e):
        page.pubsub.send_all(Message(user=page.session.store.get("user_name"), text=new_message.value, message_type="chat message"))
        # chat.controls.append(ft.Text(new_message.value))
        new_message.value = ""
    
    def join_chat(e):
        if not user_name.value:
            user_name.error = "Name cannot be blank"
            user_name.update()
        else:
            page.session.store.set("user_name", user_name.value)
            page.pop_dialog()
            page.pubsub.send_all(Message(user=user_name.value, text=f"{user_name.value} has joined the chat", message_type="login message"))
        page.update()

    page.show_dialog(
        ft.AlertDialog(
            open=True,
            modal=True,
            title=ft.Text("Welcome!"),
            content=ft.Column([user_name], tight=True),
            actions=[
                ft.Button(content='Join chat', on_click=join_chat)
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
    )

    page.add(
        chat,
        ft.Row(
            controls=
            [
                new_message,
                ft.Button("Send", on_click=send_click),
            ]
        )
    )

if __name__ == '__main__':
    ft.run(main)

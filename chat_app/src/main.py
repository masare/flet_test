from dataclasses import dataclass

import flet as ft

@dataclass
class Message:
    user: str
    text: str
    message_type: str

@ft.control
class ChatMessage(ft.Row):
    def __init__(self, message: Message):
        super().__init__()
        self.message = message
        self.vertical_alignment = ft.CrossAxisAlignment.START
        self.controls = [
            ft.CircleAvatar(
                content=ft.Text(self.get_initials(self.message.user)),
                color=ft.Colors.WHITE,
                bgcolor=self.get_avatar_color(self.message.user),
            ),
            ft.Column(
                tight=True,
                spacing=5,
                controls=[
                    ft.Text(self.message.user, weight=ft.FontWeight.BOLD),
                    ft.Text(self.message.text, selectable=True),
                ]
            )
        ]
    
    def get_initials(self, user_name: str):
        if user_name:
            # return user_name[:1].capitalize()
            return ''.join(un[0] for un in user_name.split()).upper()
        else:
            return "Unknown" 
        
    def get_avatar_color(self, user_name: str):
        colors_lookup = [
            ft.Colors.AMBER,
            ft.Colors.BLUE,
            ft.Colors.BROWN,
            ft.Colors.CYAN,
            ft.Colors.GREEN,
            ft.Colors.INDIGO,
            ft.Colors.LIME,
            ft.Colors.ORANGE,
            ft.Colors.PINK,
            ft.Colors.PURPLE,
            ft.Colors.RED,
            ft.Colors.TEAL,
            ft.Colors.YELLOW,
        ]
        return colors_lookup[hash(user_name) % len(colors_lookup)]

def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    page.title = ft.Text('Chat App')


    def on_message(message: Message):
        if message.message_type == "chat_message":
            m = ChatMessage(message)
        elif message.message_type == "login_message":
            m = ft.Text(message.text, italic=True, color=ft.Colors.BLACK_45, size=12)
        chat.controls.append(m)
        page.update()

    page.pubsub.subscribe(on_message)

    async def send_click(e):
        if new_message.value != "":
            page.pubsub.send_all(
                Message(
                    user=page.session.store.get("user_name"),
                    text=new_message.value, 
                    message_type="chat_message"
                )
            )
            new_message.value = ""
            await new_message.focus()
    
    def join_chat(e):
        if not user_name.value:
            user_name.error = "Name cannot be blank"
            user_name.update()
        else:
            page.session.store.set("user_name", user_name.value)
            welcome_dlg.open = False
            new_message.prefix = ft.Text(f"{user_name.value}: ")
            page.pubsub.send_all(
                Message(
                    user=user_name.value, 
                    text=f"{user_name.value} has joined the chat", 
                    message_type="login_message")
                )
        page.update()

    # A dialog that asks for user display name
    user_name = ft.TextField( 
        label="Enter your name to join chat",
        autofocus=True,
        on_submit=join_chat
    )

    welcome_dlg = ft.AlertDialog(
            open=True,
            modal=True,
            title=ft.Text("Welcome!"),
            content=ft.Column([user_name], width=300, height=70, tight=True),
            actions=[
                ft.Button(content='Join chat', on_click=join_chat)
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
    
    page.overlay.append(welcome_dlg)

    # chat messages
    chat = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
    )

    # A new message entry form
    new_message = ft.TextField(
        hint_text="Write a message...",
        autofocus=True,
        shift_enter=True,
        min_lines=1,
        max_lines=5,
        filled=True,
        expand=True,
        on_submit=send_click
    )

    # Add everything to the page
    page.add(
        ft.Container(
            content=chat,
            border=ft.Border.all(1, ft.Colors.OUTLINE),
            border_radius=5,
            padding=10,
            expand=True,
        ),
        ft.Row(
            controls=
            [
                new_message,
                ft.IconButton(
                    icon=ft.Icons.SEND_ROUNDED,
                    tooltip="Send message", 
                    on_click=send_click
                ),
            ]
        )
    )

if __name__ == '__main__':
    ft.run(main)

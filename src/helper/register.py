Label = '''
MDLabel:
    text: "Register Form"
    halign: "center"
    font_style: "Display"
    role: "medium"
'''

Textfields = '''
<RegisterForm@MDAnchorLayout>:
    anchor_x: 'center'
    anchor_y: 'center'

    MDGridLayout:
        cols: 1
        adaptive_width: True
        adaptive_height: True
        spacing: '16dp'
        padding: '8dp'
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}

        MDTextField:
            id: username
            mode: 'filled' 
            size_hint_x: None
            width: 300

            MDTextFieldHintText:
                text: "Enter your username"

        MDTextField:
            id: email
            mode: 'filled' 
            size_hint_x: None
            width: 300

            MDTextFieldHintText:
                text: "Enter your email"

        MDTextField:
            id: password
            mode: 'filled'   
            size_hint_x: None
            width: 300

            MDTextFieldHintText:
                text: "Enter your password"
'''

Buttons = '''
MDGridLayout:
    cols: 2
    adaptive_width: True
    adaptive_height: True
    spacing: '8dp'
    padding: '8dp'

    MDButton:
        size_hint_x: None   
        width: 150
        theme_width: "Custom"

        MDButtonText:
            text: "Register"
            pos_hint: {"center_x": .5, "center_y": .5}

    MDButton:
        size_hint_x: None   
        width: 150
        theme_width: "Custom"
        
        MDButtonText:
            text: "Login"
            pos_hint: {"center_x": .5, "center_y": .5}
'''
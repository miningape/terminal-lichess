import npyscreen

class NETWORKEDFORM(npyscreen.ActionFormV2WithMenus):
  # Just here to avoid errors when creating new forms... 
  # This function should be overridden, as it exposes the lichess event stream through json
  def generalJSON(self, json):
    pass

class CustomMenu(NETWORKEDFORM):
  class Play_Bot_Button(npyscreen.wgbutton.MiniButtonPress):
    def whenPressed(self):
      return self.parent._on_play_bot()
  
  def _on_play_bot(self):
    self.editing = self.on_play_bot()

  class Menu_Button(npyscreen.wgbutton.MiniButtonPress):
    def whenPressed(self):
      return self.parent._on_menu()
  
  def _on_menu(self):
    self.editing = self.root_menu()

  class Exit_Button(npyscreen.wgbutton.MiniButtonPress):
    def whenPressed(self):
      return self.parent._on_exit()
  
  def _on_exit(self):
    self.editing = self.on_exit()
  
  BUTTONS = {
      'PLAY_BOT': {
        'NAME': 'bot_button',
        'TYPE': Play_Bot_Button,
        'OFFSET': (1, -10),
        'TEXT': 'Play Bot'
      },
      'MENU': {
        'NAME': 'menu_button',
        'TYPE': Menu_Button,
        'OFFSET': (1, 15),
        'TEXT': 'Menu'
      },
      'EXIT': {
        'NAME': 'exit_button',
        'TYPE': Exit_Button,
        'OFFSET': (1, 5),
        'TEXT': 'Exit'
      }
  }

  # Override Methods for use later
  def on_exit(self):
    pass
  
  
  def on_play_bot(self):
    pass
  
  # Override the original method for drawing to screen
  def create_control_buttons(self):
    for button in self.BUTTONS:
      self._add_button(self.__class__.BUTTONS[button]['NAME'],
                          self.__class__.BUTTONS[button]['TYPE'],
                          self.__class__.BUTTONS[button]['TEXT'],
                          0 - self.__class__.BUTTONS[button]['OFFSET'][0],
                          0 - self.__class__.BUTTONS[button]['OFFSET'][1] - len(self.__class__.BUTTONS[button]['TEXT']),
                          None
                          )


class CustomForm(NETWORKEDFORM):
    class Input_Box(npyscreen.Textfield):
        def safe_to_exit(self): 
            self.parent._added_buttons['cover'].value = self.parent._added_buttons['input_box'].value + '                  '
            return True

    class Send_Button(npyscreen.wgbutton.MiniButtonPress):
        def whenPressed(self):
            return self.parent._on_send()

    class Menu_Button(npyscreen.wgbutton.MiniButtonPress):
        def whenPressed(self):
            return self.parent._on_menu()

    SEND_BUTTON_TYPE = Send_Button
    SEND_BUTTON_OFFSET = (1, 25)
    SEND_BUTTON_TEXT = 'Send'

    MENU_BUTTON_TYPE = Menu_Button
    MENU_BUTTON_OFFSET = (1, 15)
    MENU_BUTTON_TEXT = 'Menu'

    INPUT_BOX_TYPE = Input_Box
    INPUT_BOX_OFFSET = (1, 5)
    
    OK_BUTTON_TEXT = 'Back'

    def _on_menu(self):
        self.editing = self.root_menu()

    def _on_send(self):
        self.editing = self.on_send()

    def on_send(self):
        pass


    def create_control_buttons(self):
        tmp_rely, tmp_relx = self.nextrely, self.nextrelx
        input_box = self.add_widget(
                        self.__class__.INPUT_BOX_TYPE,
                        name = 'input_box',
                        rely = 0 - self.__class__.INPUT_BOX_OFFSET[0],
                        relx = self.__class__.INPUT_BOX_OFFSET[1],
                        when_pressed_function = None,
                        use_max_space = True,
                        width = 15,
                        value = ''
                    )
        self._added_buttons['input_box'] = input_box
        self.nextrely, self.nextrelx = tmp_rely, tmp_relx

        tmp_rely, tmp_relx = self.nextrely, self.nextrelx
        cover_box = self.add_widget(
                        self.__class__.INPUT_BOX_TYPE,
                        name = 'cover',
                        rely = 0 - self.__class__.INPUT_BOX_OFFSET[0],
                        relx = self.__class__.INPUT_BOX_OFFSET[1],
                        when_pressed_function = None,
                        use_max_space = True,
                        width = 15,
                        editable=False,
                        visible = False,
                        value = '                                                     '
                    )
        self._added_buttons['cover'] = cover_box
        self.nextrely, self.nextrelx = tmp_rely, tmp_relx
        # This is from original, probably a better solutiojn but will work for now
        self._add_button('ok_button',
                        self.__class__.OKBUTTON_TYPE,
                        self.__class__.OK_BUTTON_TEXT,
                        0 - self.__class__.OK_BUTTON_BR_OFFSET[0] + 1,
                        0 - self.__class__.OK_BUTTON_BR_OFFSET[1] - len(self.__class__.OK_BUTTON_TEXT),
                        None
                        )

        self._add_button('send_button',
                        self.__class__.SEND_BUTTON_TYPE,
                        self.__class__.SEND_BUTTON_TEXT,
                        0 - self.__class__.SEND_BUTTON_OFFSET[0],
                        0 - self.__class__.SEND_BUTTON_OFFSET[1] - len(self.__class__.SEND_BUTTON_TEXT),
                        None)
        
        self._add_button('menu_button',
                        self.__class__.MENU_BUTTON_TYPE,
                        self.__class__.MENU_BUTTON_TEXT,
                        0 - self.__class__.MENU_BUTTON_OFFSET[0],
                        0 - self.__class__.MENU_BUTTON_OFFSET[1] - len(self.__class__.MENU_BUTTON_TEXT),
                        None)
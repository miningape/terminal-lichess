import npyscreen
import random
import curses

# async io testing import
#from threading import Timer

class CustomForm(npyscreen.ActionFormExpandedV2):
    class Input_Box(npyscreen.Textfield):
        def safe_to_exit(self): 
            self.parent._added_buttons['cover'].value = self.parent._added_buttons['input_box'].value + '                  '
            return True

    class Send_Button(npyscreen.wgbutton.MiniButtonPress):
        def whenPressed(self):
            return self.parent._on_send()

    SEND_BUTTON_TYPE = Send_Button
    SEND_BUTTON_OFFSET = (1, 12)
    SEND_BUTTON_TEXT = 'Send'

    INPUT_BOX_TYPE = Input_Box
    INPUT_BOX_OFFSET = (1, 3)

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
                        width = 30,
                        value = ' '
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
                        width = 30,
                        editable=False,
                        visible = False,
                        value = '                                            '
                    )
        self._added_buttons['cover'] = cover_box
        #self.nextrely, self.nextrelx = tmp_rely, tmp_relx
        # This is from original, probably a better solutiojn but will work for now
        self._add_button('ok_button',
                        self.__class__.OKBUTTON_TYPE,
                        self.__class__.OK_BUTTON_TEXT,
                        0 - self.__class__.OK_BUTTON_BR_OFFSET[0],
                        0 - self.__class__.OK_BUTTON_BR_OFFSET[1] - len(self.__class__.OK_BUTTON_TEXT),
                        None
                        )

        self._add_button('send_button',
                        self.__class__.SEND_BUTTON_TYPE,
                        self.__class__.SEND_BUTTON_TEXT,
                        0 - self.__class__.SEND_BUTTON_OFFSET[0],
                        0 - self.__class__.SEND_BUTTON_OFFSET[1] - len(self.__class__.SEND_BUTTON_TEXT),
                        None)
        
        

class ColorCodes(npyscreen.ThemeManager): 
    _colors_to_define = (('WHITE_BLACK',      curses.COLOR_WHITE,      curses.COLOR_BLACK),
                        ('BLACK_WHITE',      curses.COLOR_BLACK,      curses.COLOR_WHITE),
                        ('BLUE_BLACK',       curses.COLOR_BLUE,       curses.COLOR_BLACK),
                        ('CYAN_BLACK',       curses.COLOR_CYAN,       curses.COLOR_BLACK),
                        ('GREEN_BLACK',      curses.COLOR_GREEN,      curses.COLOR_BLACK),
                        ('MAGENTA_BLACK',    curses.COLOR_MAGENTA,    curses.COLOR_BLACK),
                        ('RED_BLACK',        curses.COLOR_RED,        curses.COLOR_BLACK),
                        ('YELLOW_BLACK',     curses.COLOR_YELLOW,     curses.COLOR_BLACK),
                        ('BLUE_GREEN',       curses.COLOR_BLUE,       curses.COLOR_GREEN),
                        ('GREEN_BLUE',       curses.COLOR_GREEN,      curses.COLOR_BLUE))

    default_colors = {
        'DEFAULT'     : 'WHITE_BLACK',
        'FORMDEFAULT' : 'WHITE_BLACK',
        'NO_EDIT'     : 'BLUE_BLACK',
        'STANDOUT'    : 'CYAN_BLACK',
        'CURSOR'      : 'WHITE_BLACK',
        'CURSOR_INVERSE': 'BLACK_WHITE',
        'LABEL'       : 'GREEN_BLACK',
        'LABELBOLD'   : 'WHITE_BLACK',
        'CONTROL'     : 'YELLOW_BLACK',
        'IMPORTANT'   : 'GREEN_BLACK',
        'SAFE'        : 'GREEN_BLACK',
        'WARNING'     : 'YELLOW_BLACK',
        'DANGER'      : 'RED_BLACK',
        'CRITICAL'    : 'BLACK_RED',
        'GOOD'        : 'GREEN_BLACK',
        'GOODHL'      : 'GREEN_BLACK',
        'VERYGOOD'    : 'BLACK_GREEN',
        'CAUTION'     : 'YELLOW_BLACK',
        'CAUTIONHL'   : 'BLACK_YELLOW',
        'BGT'         : 'BLUE_GREEN',
        'GBT'         : 'GREEN_BLUE',
    }


class Grid(npyscreen.SimpleGrid):
    _contained_widgets = npyscreen.MultiLineEdit
    default_column_number = 8
    def custom_print_cell(self, actual_cell, cell_display_value):
        if cell_display_value == '        \n  FAI  \n       ':
            actual_cell.color = 'CURSOR' 
        elif cell_display_value == '       \n  PAS  \n       ':
            actual_cell.color = 'CURSOR_INVERSE'
        else:
            actual_cell.color = 'DEFAULT'

class App(npyscreen.NPSAppManaged):
    def onStart(self):
        npyscreen.setTheme(ColorCodes)
        self.addForm('MAIN', mainForm, name="START")

class mainForm(CustomForm):
    def selected(self):
        print("oi")

    def editValue(self):
        self.myGrid.values[0][0] = "{}".format( random.randint(0,9) )
        self.display()

    def create(self):
        self.myGrid = self.add(Grid, column_width=7, row_height=3, col_margin=0, height=24, width=56, editable=False)
        #self.add(CustomMulti, value="     \n  K  \n     ")
        
        self.myGrid.values = []
        counter = 0
        for x in range(8):
            row = []
            for y in range(8):
                if bool( counter % 2 ):
                    row.append('       \n  PAS  \n       ')
                else:
                    row.append('       \n  FAI  \n       ')
                counter = counter + 1
            counter = counter - 1
            self.myGrid.values.append(row)

        #Timer(1, self.editValue).start()

    def on_send(self):
        self.parentApp.switchForm(None)

    def on_ok(self):
        self.parentApp.switchForm(None)

if __name__ == '__main__':
    app = App()
    app.run()
    
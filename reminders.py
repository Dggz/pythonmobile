from kivy.app import App
from kivy.properties import BooleanProperty
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.lang import Builder

from models import Reminder


Builder.load_string('''
<SelectableLabel>:
    # Draw a background to indicate selection
    canvas.before:
        Color:
            rgba: (.0, 0.9, .1, .3) if self.selected else (0, 0, 0, 1)
        Rectangle:
            pos: self.pos
            size: self.size
            
    text_size: self.size
    valign: 'middle'
    padding_x: 5

<ReminderList>:
    viewclass: 'SelectableLabel'
    SelectableRecycleBoxLayout:
        default_size: None, dp(56)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
        multiselect: True
        touch_multiselect: True
''')


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    '''' Adds selection and focus behaviour to the view. '''


class SelectableLabel(RecycleDataViewBehavior, Label):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            print("selection changed to {0}".format(rv.data[index]))
        else:
            print("selection removed for {0}".format(rv.data[index]))


def get_static():
    return [
        Reminder(
            'reminder {}'.format(x),
            'reminder {} text'.format(x)
        ) for x in range(1, 4)
    ]


class ReminderList(RecycleView):
    def __init__(self, **kwargs):
        super(ReminderList, self).__init__(**kwargs)
        self.data = [{'text': x.title + '\n    ' + x.text} for x in get_static()]


class RemindersPage(GridLayout):
    def __init__(self, **kwargs):
        super(RemindersPage, self).__init__(**kwargs)
        self.rows = 2
        self.add_widget(ReminderList())
        sub_layout = GridLayout()
        sub_layout.size_hint = (.1, .1)
        sub_layout.cols = 2
        sub_layout.add_widget(Button(text='Add'))
        sub_layout.add_widget(Button(text='Edit'))
        self.add_widget(sub_layout)


class ReminderApp(App):
    def build(self):
        return RemindersPage()


if __name__ == '__main__':
    ReminderApp().run()

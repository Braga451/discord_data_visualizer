import PySimpleGUI as SG
import threading
from RetriveData import RetriveData

class Interface(RetriveData):
    def __init__(self, path : str = "") -> None:
        super().__init__(path)
        
    def start(self) -> None:
        get_path_thread = threading.Thread(target = self._getPathChats, daemon = True)
        get_path_thread.start()
        self.__debuggerGetPathChatsProgressBar()
        self.__constructMainLayout()

    def __constructMainLayout(self) -> None:
        names = [x["name"] for x in self.path_chats]
        paths = [x["path"] for x in self.path_chats]
        layout = [
                [SG.Text("Search for chat")],
                [SG.Input(size=(50, 1), enable_events = True, key = "_input_")], 
                [SG.Listbox(names, size=(50, 10), enable_events = True, key = "_list_")],
                [SG.Button("Ver mensagens", key = "_button_")]
                ]        
        window = SG.Window("Chat list", layout, finalize = True, element_justification = "c")
        window["_input_"].expand(True, False)
        while True:
            event, values = window.read()
            if event in (SG.WIN_CLOSED, 'Exit'):
                break
            if event == "_input_":
                if values["_input_"] != "":
                    search_str = values["_input_"] 
                    names = [x["name"] for x in self.path_chats if search_str in x["name"]] 
                    paths = [x["path"] for x in self.path_chats if search_str in x["name"]]
                    window["_list_"].update(names)
                else:
                    names = [x["name"] for x in self.path_chats]
                    paths = [x["path"] for x in self.path_chats]
                    window["_list_"].update(names)
            if event == "_button_" and len(values["_list_"]) != 0:
                self.__constructMessagesLayout(paths[window["_list_"].get_indexes()[0]], values["_list_"])
    
    def __constructMessagesLayout(self, path : str = "", name : str = "") -> None:
        messages = self._returnMessagesByPath(path)
        data_headings = ["ID_MENSAGEM", "HORARIO", "CONTEUDO", "MIDIA"]
        layout = [
        [SG.Table(messages, key = "_table_", headings = data_headings, auto_size_columns = True, display_row_numbers = True, justification = "c", row_height = 35, enable_events = True, select_mode = SG.TABLE_SELECT_MODE_BROWSE)],
        [SG.Button("Printar linha", key = "_outputRow_")]
                ]
        window = SG.Window(f"Mensagens com {name[0]}", layout, finalize = True, element_justification = "c", modal = True, resizable = True)
        window["_table_"].expand(True, True)
        while True:
            events, value = window.read()
            if events in (SG.WIN_CLOSED, "Exit"):
                break
            if len(value["_table_"]) != "" and events != "_outputRow_":
                SG.Popup(f"Mensagem: \n{messages[value['_table_'][0]][2]}\nMedia: {messages[value['_table_'][0]][3]}")
            if events == "_outputRow_" and len(value["_table_"]) > 0:
                print(messages[value["_table_"][0]])
    def __debuggerGetPathChatsProgressBar(self) -> None:
        while(len(self.path_chats) != self.int_total_chats):
            print(f"\r[+] Progresso: {len(self.path_chats)}/{self.int_total_chats - 1}", end="")
        print("")
        return


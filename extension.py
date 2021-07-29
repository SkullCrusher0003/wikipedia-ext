from decimal import Context
import vscode, wikipedia

ext = vscode.Extension(
    "wikipedia",
    "Wikipedia 4 Visual Studio",
    "1.0.1",
    "A simple, easy-to-use extension to quickly search wikipedia.",
    icon = "logo.png"
)

@ext.event 
def on_activate():
    return f"{ext.name} is active"

@ext.command(keybind = "alt + 3")
def search_wikipedia():
    editor = vscode.window.ActiveTextEditor()
    if not editor:
        pass
    search_query = str(editor.document.get_text(editor.selection))
    print(search_query)

    if not search_query:
        search_box = vscode.ext.InputBoxOptions(
            title = "Search For Terms On Wikipedia"
        )
        search_query = vscode.window.show_input_box(search_box)

        if not search_query:
            return 
        
    search_res = wikipedia.search(
        search_query,
        results = 10
    )
    data = []
    for res in search_res:
        title = str(res)
        option = vscode.ext.QuickPickItem(
            label = title,
            detail = None,
            link = f"https://en.wikipedia.org/wiki/{title}"
        )
        data.append(option)
    if len(data) == 0:
        vscode.window.show_error_message("No Search Results Were Found... Please try again.")
    else:
        options = vscode.ext.QuickPickOptions(match_on_detail = True)
        selected = vscode.window.show_quick_pick(data, options)
        if not selected:
            return 
        
        else:
            vscode.env.open_external(selected.link)

vscode.build(ext, publish = False)
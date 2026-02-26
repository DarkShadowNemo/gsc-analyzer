from struct import unpack
from tkinter import *
import glob
from tkinter import ttk
from tkinter import filedialog

window = Tk()
window.title("GameScene Analyzer")
window.geometry("256x512")

tree = ttk.Treeview(window)
tree.pack()

def remove_item():
    selected_item = tree.selection()
    for item in selected_item:
        tree.delete(item)

def gamescene_dialog():
    try:
        global filepath
        filepath = filedialog.askopenfilename(
        title="oldttgames gsc",
        filetypes=[("gsc", "*.gsc")]
        )
        with open(filepath, "rb") as f:
            f.seek(0)
            Chunks2 = f.read()
            f.seek(0)
            while f.tell() < len(Chunks2):
                Chunk = f.read(4)
                if Chunk == b"NU20":
                    FileSize = unpack("<i", f.read(4))[0]
                    PrimType = unpack("<I", f.read(4))[0]
                    unknown = unpack("<I", f.read(4))[0]
                    nu_id = tree.insert("", 0, text=Chunk)
                    for child in tree.get_children():
                        
                        tree.insert(nu_id, 1, text="FileSize %d" % abs(FileSize))
                        tree.insert(nu_id, 2, text="PrimType %d" % PrimType)
                        tree.insert(nu_id, 3, text="Unknown1 %d" % unknown)
                elif Chunk == b"NTBL":
                    NamedFileSize = unpack("<i", f.read(4))[0]
                    Namedtablelength = unpack("<i", f.read(4))[0]
                    nu_id1 = tree.insert("", 4, text=Chunk)
                    for child in tree.get_children():
                        tree.insert(nu_id1, 5, text="NamedFileSize %d" % NamedFileSize)
                        tree.insert(nu_id1, 6, text="Namedtablelength %d" % Namedtablelength)
                        tree.insert(nu_id1, 7, text="padding01 %d" % padding01)
    except:
        OSError

Button1 = Button(window, text="open nuscene", command=gamescene_dialog)
Button1.pack()
remove_button = Button(window, text="Remove Selected", command=remove_item)
remove_button.pack(pady=10)



window.mainloop()
    
    
    

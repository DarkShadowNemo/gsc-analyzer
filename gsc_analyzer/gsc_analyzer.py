from struct import unpack
from tkinter import *
import glob
from tkinter import ttk
from tkinter import filedialog

window = Tk()
window.title("GameScene Analyzer")
window.geometry("256x256")

tree = ttk.Treeview(window)
tree.pack()

objects=[]
pads=[]
vertices=[]

def gamescene_dialog():
    global filepath
    filepath = filedialog.askopenfilename()
    with open(filepath, "rb") as f:
        while 1:
            Chunk = f.read(4)
            if Chunk == b"NU20":
                FileSize = unpack("<i", f.read(4))[0]
                PrimType = unpack("<I", f.read(4))[0]
                unknown = unpack("<I", f.read(4))[0]
                nu_id = tree.insert("", 0, text=Chunk)
                tree.insert(nu_id, 1, text="FileSize %d" % abs(FileSize))
                tree.insert(nu_id, 2, text="PrimType %d" % PrimType)
                tree.insert(nu_id, 3, text="Unknown1 %d" % unknown)
            elif Chunk == b"NTBL":
                NTBLSize1 = unpack("<I", f.read(4))[0]
                NTBLSize2 = unpack("<I", f.read(4))[0]
                nu_id1 = tree.insert("", 1, text=Chunk)
                tree.insert(nu_id1, 2, text="NamedTableSize1 %d" % NTBLSize1)
                tree.insert(nu_id1, 3, text="NamedTableSize2 %d" % NTBLSize2)
            elif Chunk == b"TST0":
                TextureSize = unpack("<I", f.read(4))[0]
                TextureCount = unpack("<I", f.read(4))[0]
                Padding = unpack("<I", f.read(4))[0]
                nu_id2 = tree.insert("", 2, text=Chunk)
                tree.insert(nu_id2, 3, text="TextureSetSize %d" % TextureSize)
                tree.insert(nu_id2, 4, text="Texture Count %d" % TextureCount)
                tree.insert(nu_id2, 5, text="padding %d" % Padding)
                texture_data_id1 = tree.insert(nu_id2, 6, text="texture data")
            elif Chunk == b"MS00":
                MaterialSize = unpack("<I", f.read(4))[0]
                MaterialCount = unpack("<I", f.read(4))[0]
                Padding = unpack("<I", f.read(4))[0]
                nu_id3 = tree.insert("", 3, text=Chunk)
                tree.insert(nu_id3, 4, text="Material Size %d" % MaterialSize)
                tree.insert(nu_id3, 5, text="Material Count %d" % MaterialCount)
                tree.insert(nu_id3, 6, text="padding %d" % Padding)
                material_data_id1 = tree.insert(nu_id3, 7, text="material data")
            elif Chunk == b"OBJ0":
                ObjectSize = unpack("<I", f.read(4))[0]
                ObjectCount = unpack("<I", f.read(4))[0]
                Padding = unpack("<I", f.read(4))[0]
                nu_id4 = tree.insert("", 4, text=Chunk)
                tree.insert(nu_id4, 5, text="Object Size %d" % ObjectSize)
                tree.insert(nu_id4, 6, text="Object Count %d" % ObjectCount)
                tree.insert(nu_id4, 7, text="padding %d" % Padding)
                offset_data = tree.insert(nu_id4, 8, text="offset data")
            elif Chunk == b"\x03\x01\x00\x01":
                f.seek(-4,1)
                Chunks = unpack("<I", f.read(4))[0]
                f.seek(2,1)
                vertexCount = unpack("B", f.read(1))[0]
                flag1 = unpack("B", f.read(1))[0]
                for i in range(vertexCount):
                    vx = unpack("<f", f.read(4))[0]
                    vy = unpack("<f", f.read(4))[0]
                    vz = unpack("<f", f.read(4))[0]
                    vw = unpack("<f", f.read(4))[0]
                    vertices.append([vx,vz,vy,1])
                datas = tree.insert(offset_data, 5, text=hex(Chunks))
                tree.insert(datas, 6, text=vertexCount)
                triangleStrips_ = tree.insert(datas, 7, text=flag1)
                for i, v in enumerate(vertices,1):
                    tree.insert(triangleStrips_, 8, text="vx %f" % v[0])
                    tree.insert(triangleStrips_, 9, text="vz %f" % v[1])
                    tree.insert(triangleStrips_, 10,text="vy %f" % v[2])
                    tree.insert(triangleStrips_, 11,text="vw %f" % 1.0)
                
                
                    
            elif Chunk == b"SST0":
                break

Button1 = Button(window, text="open nuscene", command=gamescene_dialog)
Button1.pack()



window.mainloop()
    
    
    

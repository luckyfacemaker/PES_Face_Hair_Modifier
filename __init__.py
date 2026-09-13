from . import PES_Face_Hair_Modifier as _addon
bl_info = {'name': 'PES Face/Hair Modifier', 'author': 'the4chancup - MjTs-140914, Lucky Facemaker', 'version': (1, 0, 0), 'blender': (4, 5, 0), 'location': 'View3D > Sidebar (N) > PES Tools', 'description': 'PES Face/Hair Modifier', 'warning': '', 'wiki_url': 'https://github.com/MjTs140914/PES_Face_Hair_Modifier', 'tracker_url': 'https://github.com/luckyfacemaker/PES_Face_Hair_Modifier/issues', 'category': 'System'}

def register():
    _addon.register()

def unregister():
    _addon.unregister()

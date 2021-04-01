print("\n")
print("\n")
import bpy
import math
import sys
import os
import imp
from utils import VoiceRecognition
import cv2


#print(sys.path)
#for c in sys.path:
#    print(c)
filepath = '/Documentos/Rosana/system_image_processing_stable/utils/VoiceRecognition.py'
dir = os.path.dirname(bpy.data.filepath)


#blend_dir = '/Documentos/Rosana/system_image_processing_stable/utils'
if dir not in sys.path:
   sys.path.append(dir)
   print("-> {}".format(dir))
else:
    print("diretorio já incluso")
    for c in sys.path:
        print(c)

str = "Oi. Eu sou Goku"

current_angle = 0
fno = 1

for c in list(str):
    if c == 'a':
        angle_add = 8
    if c == 'e':
        angle_add = 7
    if c == 'i':
        angle_add = 6
    if c == 'o':
        angle_add = 5
    if c == 'u':
        angle_add = 4
    if c == '.':
        angle_add = 0
    if c == ',':
        angle_add = 0
    if c == ' ':
        angle_add = 0
    else:
        angle_add = 1
        
    ob = bpy.data.objects['Armature']
    bpy.ops.object.mode_set(mode = 'POSE')
    
    pbone = ob.pose.bones["jaw"]
    
    pbone.rotation_mode = 'XYZ'
    
    axis = 'X'
    angle = angle_add - math.degrees(current_angle)
    
    pbone.rotation_euler.rotate_axis(axis, math.radians(angle))
    
    current_angle = pbone.rotation_euler.x
    
    pbone.keyframe_insert(data_path="rotation_euler", frame=fno)
    fno+=2
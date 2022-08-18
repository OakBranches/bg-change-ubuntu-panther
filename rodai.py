from shutil import ExecError
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
from math import floor
import sys
import os
from random import randrange
# 900 x 450

pwd = '/home/matheus/Área de Trabalho/git/bg/'


def screv(texto):
    img = Image.open(pwd+"raw.png")
    draw = ImageDraw.Draw(img)
    texto, tam = calcula(texto)
    font = ImageFont.truetype(pwd+"PressStart3P.ttf", tam)
    draw.text((330, 300),texto, (53,1,128),font=font)
    img.save(pwd+'new.png')

def calcula(texto):
    ntexto = texto
    tam = 100

    # verifica se a maior palavra cabe
    maior = max(list(map(len, texto.split())))
    if maior > 9:
        tam = 100/(maior/9)
        
    # verifica se a área da certo
    if len(texto) * tam > 900 * 450:
        tam = 900 * 450 / len(texto)

    # divide as linhas
    ntexto, tam, linhas = divisor(texto, tam)

    # ultimo redimensionamento
    if len(linhas)*tam > 450:
        tam = 450 / len(linhas)

    ntexto, tam, linhas = divisor(texto, tam)
    
    return ntexto.strip(), floor(tam)


def divisor(texto, tam):
    # divide as linhas
    buff = ''
    ntexto = ''
    linhas = []
    for i in texto.split():
        if len(buff)*tam + (len(i)+1)*tam <= 900:
            buff += i + ' '
        else:
            linhas.append(buff)
            ntexto += buff + '\n'
            buff = i  + ' '
    linhas.append(buff)
    ntexto += buff + '\n'
    return ntexto, tam, linhas


def generateNsetBG(texto):
    screv(texto)
    path = str(os.path.abspath(pwd+"new.png")).replace(' ', '\ ')
    os.system(f"/usr/bin/gsettings set org.gnome.desktop.background picture-uri {path}")

if __name__ == "__main__":
    texto = ''
    try:
        if len(sys.argv) > 1:
            texto = sys.argv[1]
        else:
            f = open(pwd+"frases.txt", "r")
            frases = f.read().split('\n')
            texto = frases[randrange(len(frases))]
        generateNsetBG(texto)
    except Exception as e:
        print('ops, algo deu errado\n', e)
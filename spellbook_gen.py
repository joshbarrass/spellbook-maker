#!/usr/bin/env python2

# Written in Python 2
# Requires Python Image Library (I recommend using Pillow)

# Based on https://www.reddit.com/r/proceduralgeneration/comments/8rm3sv/procedurally_generated_spellbook_spritestitles/


from PIL import Image
import random
import math
import markov

# Book templates are tuples
# index 0 = file path
# index 1 = another tuple, indicating the area where the icon is applied
#           first two are the top left corner, second two are dimensions
TEMPLATES = [("book.png",(2,1,4,6)),
             ("borderedbook.png",(2,1,4,6)),
             ]
MODIFIERS = [None,
             "bookmark.png",
             "tabs.png",
             ]

with open("martial.txt") as text:
    MARKOV = markov.MarkovChain(text.read())

class spellbook(object):
    def __init__(self,templates=TEMPLATES,modifiers=MODIFIERS,markov_chain=MARKOV):
        self.template = templates[random.randrange(len(templates))]
        self.modifier = modifiers[random.randrange(len(modifiers))]
        self.markov = markov_chain
        self.generate()
        self.generate_title()

    def show(self,*args,**kwargs):
        if kwargs.has_key("size"):
            self.size = kwargs["size"]
        else:
            dimensions = self.template[1]
            if dimensions[2] < 200 or dimensions[3] < 200:
                if dimensions[2] > dimensions[3]:
                    scale_factor = 200/dimensions[3]
                else:
                    scale_factor = 200/dimensions[2]
                size = (dimensions[2]*scale_factor,
                        dimensions[3]*scale_factor)
        self.sprite.resize(size).show()
        

    def generate(self):
        book, icon_colour = self.colourise(Image.open(self.template[0]))#
        icon_pos = self.template[1]
        icon = self.generate_icon(icon_pos,icon_colour)
        book.paste(icon,(icon_pos[0],icon_pos[1]),icon)
        if self.modifier != None:
            modifier = Image.open(self.modifier)
            book.paste(modifier,(0,0),modifier)
        self.sprite = book

    def colourise(self,template):
        template.convert("RGBA")
        colour = (random.randrange(0,256),
                  random.randrange(0,256),
                  random.randrange(0,256),) # generate a random colour
        icon_colour = (255-colour[0],
                       255-colour[1],
                       255-colour[2])
        pix = template.load()
        for y in range(template.size[1]):
            for x in range(template.size[0]):
                pixel = pix[x,y]
                if pixel[0] == pixel[1] and pixel[1] == pixel[2]:
                    brightness = pixel[0]/255.
                    pix[x,y] = (int(colour[0]*brightness),
                                int(colour[1]*brightness),
                                int(colour[2]*brightness),
                                pixel[3])
        return template, icon_colour

    def generate_icon(self,dimensions,colour):
        icon = Image.new("RGBA",(dimensions[2],dimensions[3]),(0,0,0,0))
        pix = icon.load()
        
        icon_type = random.randrange(0,3)
        if icon_type == 0: # vertically symmetrical
            height = int(math.ceil(dimensions[3]/2.))
            for p in range(0,random.randint(0,dimensions[2]*height)):
                x = random.randrange(0,dimensions[2])
                y = random.randrange(0,height)
                pix[x,y] = colour
                pix[x,dimensions[3]-y-1] = colour
        if icon_type == 1: # horizontally symmetrical
            width = int(math.ceil(dimensions[2]/2.))
            for p in range(0,random.randint(0,dimensions[3]*width)):
                x = random.randrange(0,width)
                y = random.randrange(0,dimensions[3])
                pix[x,y] = colour
                pix[dimensions[2]-x-1,y] = colour
        if icon_type == 2: # both
            height = int(math.ceil(dimensions[3]/2.))
            width = int(math.ceil(dimensions[2]/2.))
            for p in range(0,random.randint(0,width*height)):
                x = random.randrange(0,width)
                y = random.randrange(0,height)
                pix[x,y] = colour
                pix[x,dimensions[3]-y-1] = colour
                pix[dimensions[2]-x-1,y] = colour
                pix[dimensions[2]-x-1,dimensions[3]-y-1] = colour
        return icon

    def generate_title(self):
        self.title = self.markov.words[random.randrange(0,len(self.markov.words))]
        last_word = self.title
        for i in range(random.randint(2,5)):
            last_word = self.markov.suggest(last_word)
            self.title += (" "+last_word)
        
                
class spellbook_sprite(spellbook):
    def generate_title(self):
        pass
        
        

# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class ScrapyPvItem(Item):
    # Primary fields
    principal = Field()  # principal
    categoria = Field()  # categoria
    subcategoria = Field() # subcategoria
    tipo = Field() # tipo
    titulo = Field() # titulo
    brand = Field() # brand
    codigo_producto = Field() # Código de producto web.
    imagen = Field() # imagen
    estrellas = Field() # estrela)
    especificacion = Field() # especificacion
    mejor_precio = Field() # mejor precio
    precio_normal = Field() # Precio Normal
    unidad = Field()
    promocion = Field()
    # Housekeeping fields
    url = Field()
    project = Field()
    spider = Field()
    server = Field()
    date = Field()

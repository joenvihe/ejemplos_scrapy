# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class ProductosItem(Item):
    # Primary fields
    titulo = Field()  # Titulo
    product_reference = Field()  # Producto Referencia

    group = Field() # Grupo
    subgroup = Field() # Subgrupo
    organization = Field() # organización
    brand = Field() # Marca
    web_product_code = Field() # Código de producto web.
    description = Field() # Descripción
    type = Field() # Tipo (especificación)
    number_of_average_stars = Field() # Cantidad de estrellas promedio
    image_url = Field() # Imagen
    normal_price = Field() # Precio Normal
    discount = Field() # Precio con descuento
    flag_of_supply = Field() # Flag de oferta.
    approximate_amount_for_number_of_grams = Field() # Importe aproximado por una cantidad de gramos
    promotion_description = Field() # Promociones descripción
    propmotion_valid_date = Field() # Promoción fecha valida
    additional_remarks = Field() # Observaciones adicionales (precios referenciales)

    # Calculated fields
    images = Field()
    location = Field()

    # Housekeeping fields
    url = Field()
    project = Field()
    spider = Field()
    server = Field()
    date = Field()

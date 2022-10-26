#!/usr/bin/env python3

import pandas as pd

def create_excel(shopify_filename, shipit_filename):
    """ Funcion para generar un excel con la info
    de dos archivos.
    Estos archivos son enviados desde el script
    main.py de la aplicación en formato string
    la ruta para acceder a los mismos"""


    # La configuración que se presenta a continuación
    # es específica para los archivos que necesita trabajar

    # leer archivo csv que tiene un delimitador especifico
    shopify = pd.read_csv(shopify_filename, sep=";")

    # Leer excel y extraer la info de la hoja "Envíos" para ser transformada a csv
    shipit = pd.read_excel(shipit_filename, sheet_name="Envíos")

    # Covertir a csv el excel anterior
    shipit.to_csv('./shipit.csv', index = None, header=True)

    # Trabajar con csv generado anteriormente y cambiar su index
    # a la columna "ID Envío"
    shipit = pd.read_csv('shipit.csv')
    shipit = shipit.set_index("ID Envío")

    # Comenzar a poblar un nuevo DataFrame con las casillas solicitadas
    # tomando la información de los otros archivos subidos
    informe_ventas = pd.DataFrame()
    informe_ventas["Fecha"] = shopify[["Paid at"]]
    informe_ventas["ID"] = shopify[["Name"]]
    informe_ventas["Subtotal"] = shopify[["Subtotal"]]
    informe_ventas["Neto"] = shopify["Subtotal"] - shopify["Taxes"]
    informe_ventas["IVA"] = shopify[["Taxes"]]
    informe_ventas["Costo Despacho"] = ""
    informe_ventas["Cobro Despacho"] = shopify[["Shipping"]]
    informe_ventas["Total"] = shopify[["Total"]]
    informe_ventas["SKU"] = shopify[["Lineitem sku"]]
    informe_ventas["Cantidad"] = shopify[["Lineitem quantity"]]
    informe_ventas["Detalle"] = shopify[["Lineitem name"]]

    # Loop para obtener una lista sin duplicados
    # con los ID de envío
    id_list = []
    for number_id in informe_ventas["ID"]:  # Itera sobre todos los ID
        if number_id not in id_list:  # Si el id no está en la lista, lo agrega
            id_list.append(number_id)

    # Loop para obtener una lista con cada costo
    # de despacho en base al ID de Envío.
    # Además generar una lista con cada ID que
    # coincida con los costos de despacho encontrados.
    lista_costo_despacho = []
    found_ids = []
    for number_id in id_list:  # por cada ID único, revisa si lo encuentra en la base de shipit
        if number_id in shipit.index.values:  # Agrega a listas separadas cada ID y costo despacho que coincida en la base de shipit
            lista_costo_despacho.append(shipit.loc[[number_id], ["Precio de Envío"]].iloc[0]["Precio de Envío"])
            found_ids.append(number_id)

    # Con los ID de envío que se encuentran en la base de shipit identificados
    # poblar el DataFrame informe_ventas en la columna Costo Despacho
    # para cada ID que corresponda
    for n, found_id in enumerate(found_ids):
        index_id = informe_ventas.index[informe_ventas['ID'] == found_id].to_list()[0]  # Obtiene el index que corresponda al ID en DF informe_ventas
        informe_ventas.loc[index_id, ['Costo Despacho']] = [lista_costo_despacho[n]]  # Dado el index anterior, modificar valor al costo despacho correspondiente



    # Guardar DataFrame como Excel
    informe_ventas.to_excel("./informe_ventas.xlsx")

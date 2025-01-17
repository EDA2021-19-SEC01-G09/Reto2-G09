﻿"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import mergesort as ms
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos


def newCatalog():
    """
    Inicializa el catálogo de videos. Crea una lista vacia para guardar
    todos los videos, adicionalmente, crea una lista vacia para las categorías
    """
    catalog = {'videos': None,
            'categorias': None,
              'categoriasId': None,
              'paises': None}

    catalog['videos'] = lt.newList("ARRAY_LIST")
    catalog['categorias'] = lt.newList("ARRAY_LIST", cmpfunction = compararCategorias)
    catalog['categoriasId'] = mp.newMap(67, maptype = 'PROBING', loadfactor = 0.5, comparefunction = cmpCategorias)
    catalog['paises'] = mp.newMap(23, maptype = 'PROBING', loadfactor = 0.5, comparefunction = cmpPaises)
    
    return catalog


# Funciones para creacion de datos


def newCategoria(id):
    """
    Crea una nueva estructura para modelar los libros de un autor
    y su promedio de ratings. Se crea una lista para guardar los
    libros de dicho autor.
    """
    cat = {'id' : "",
              "paises" : None}
    cat['id']= id
    cat['paises'] = mp.newMap(23, maptype = 'PROBING', loadfactor = 0.5, comparefunction = cmpCategorias)
    return cat


def newPais(nombre):
    pais = {'pais' : "",
            'videos' : None}
    pais['pais'] = nombre
    pais['videos'] = lt.newList("ARRAY_LIST", cmpPaises)
    return pais


# Funciones para agregar informacion al catalogo


def addVideo(catalog, video):
    # Se adiciona el video a la lista de videos
    lt.addLast(catalog['videos'], video)
    addCategoriaId(catalog, video['category_id'], video['country'], video)
    addPais(catalog, video['country'], video)
    

def addCategoria(catalog, categoria):
    """
    Adiciona una categoría a la lista de categorías
    """
    lt.addLast(catalog['categorias'], categoria)


def addCategoriaId(catalog, idCategoria, country, video):
    categorias =  catalog['categoriasId']
    existcategoria = mp.contains(categorias, idCategoria)
    if existcategoria:
        entry = mp.get(categorias, idCategoria)
        categoria = me.getValue(entry)
    else:
        categoria = newCategoria(idCategoria)
        mp.put(categorias, idCategoria, categoria)
    paises = categoria['paises']
    existpais = mp.contains(paises, country)
    if existpais:
        entryPais = mp.get(paises, country)
        pais = me.getValue(entryPais)
    else:
        pais = newPais(country)
        mp.put(paises, country, pais)
    lt.addLast(pais['videos'], video)
    

def addPais(catalog, paisName, video):
    paises =  catalog['paises']
    existpais = mp.contains(paises, paisName)
    if existpais:
        entry = mp.get(paises, paisName)
        pais = me.getValue(entry)
    else:
        pais = newPais(paisName)
        mp.put(paises, paisName, pais)
    lt.addLast(pais['videos'], video)


# Funciones de consulta


def filtrarRequerimiento1(catalog, categoria, country):
    cat = mp.get(catalog['categoriasId'], categoria)
    if cat:
        det = me.getValue(cat)['paises']
        pais = mp.get(det, country)
        if pais:    
            return me.getValue(pais)
    return None
   

def filtrarRequerimiento2(catalog, pais):
    listaFiltrada = lt.newList('ARRAY_LIST')
    revisar = mp.newMap(2, maptype = 'PROBING', loadfactor = 0.5)
    lista = mp.get(catalog['paises'], pais)
    paisVideos = me.getValue(lista)['videos']
    for i in range(0, lt.size(paisVideos)):
        elementos = lt.getElement(paisVideos, i)
        dislikes = int(elementos['dislikes'])
        if dislikes == 0:
            dislikes = 1
        ratio = int(elementos['likes']) / dislikes
        if ratio > 10:
            elementos['ratio_likes_dislikes'] = round(ratio, 2)
            if elementos['video_id'] != '#NAME?' and not mp.contains(revisar, elementos['video_id']):
                mp.put(revisar, elementos['video_id'], 1)
                elementos['dias'] = 1
                lt.addLast(listaFiltrada, elementos)
            elif mp.contains(revisar, elementos['video_id']):
                vidRatio = mp.get(revisar, elementos['video_id'])
                prevRatio = me.getValue(vidRatio)
                mp.remove(revisar, elementos['video_id'])
                mp.put(revisar, elementos['video_id'], prevRatio + 1)
                elementos['dias'] = prevRatio + 1
                lt.addLast(listaFiltrada, elementos)

    return listaFiltrada


def filtrarRequerimiento3(catalog, categoria):
    listaFiltrada = lt.newList('ARRAY_LIST')
    revisar = mp.newMap(2, maptype='PROBING', loadfactor=0.5)
    cat = mp.get(catalog['categoriasId'], categoria)
    paises = me.getValue(cat)['paises']
    nombres = mp.keySet(paises)
    for nombre in range(1, lt.size(nombres) + 1):
        nombrePais = lt.getElement(nombres, nombre)
        pais = mp.get(paises, nombrePais)
        vids = me.getValue(pais)['videos']
        for i in range(1, lt.size(vids) + 1):
            elementos = lt.getElement(vids, i)
            dislikes = int(elementos['dislikes'])
            if dislikes == 0:
                dislikes = 1
            ratio = int(elementos['likes']) / dislikes
            if ratio > 20:
                elementos['ratio_likes_dislikes'] = round(ratio, 2)
                if elementos['video_id'] != '#NAME?' and (mp.contains(revisar, elementos['video_id']) == False):
                    mp.put(revisar, elementos['video_id'], 1)
                    elementos['dias'] = 1
                    lt.addLast(listaFiltrada, elementos)
                elif mp.contains(revisar, elementos['video_id']) == True:
                    vidRatio = mp.get(revisar, elementos['video_id'])
                    prevRatio = me.getValue(vidRatio)
                    me.setValue(vidRatio, prevRatio + 1)
                    elementos['dias'] = prevRatio + 1
                    lt.addLast(listaFiltrada, elementos)

    return listaFiltrada


def filtrarRequerimiento4(catalog, pais, tag):
    listaFiltrada = lt.newList()
    lista = mp.get(catalog['paises'], pais)
    paisVideos = me.getValue(lista)['videos']
    for i in range(0, lt.size(paisVideos)):
        listaTags = lt.newList()
        elementos = lt.getElement(paisVideos, i)
        if tag in elementos['tags'].lower():
            tagsVid = elementos['tags'].split("|")
            for j in range(0, len(tagsVid)):
                tagsVid[j] = tagsVid[j].lower().strip("\"")
                lt.addLast(listaTags, tagsVid[j])
            if lt.isPresent(listaTags, tag) != 0:
                lt.addLast(listaFiltrada, elementos)
    return listaFiltrada


def buscarCategoria(catalog, categoria):
    """
    Retorna un autor con sus libros a partir del nombre del autor
    """
    if lt.isPresent(catalog['categorias'], categoria) > 0:
        return True
    else:
        return False
     

def buscarPais(catalog, pais):
    if mp.contains(catalog, pais) == True:
        return True
    else:
        return False


def buscarTag(catalog, tag): 
    falso = False
    for i in range(0, lt.size(catalog['videos'])):
        elemento = lt.getElement(catalog['videos'],i)
        if tag.lower() in elemento['tags'].lower():
            verificar = True
            if verificar == True:
                falso = True
                break
    return falso


# Funciones utilizadas para comparar elementos


def cmpPaises(keyname, pais):
    """
    Compara dos nombres de autor. El primero es una cadena
    y el segundo un entry de un map
    """
    authentry = me.getKey(pais)
    if (keyname == authentry):
        return 0
    elif (keyname > authentry):
        return 1
    else:
        return -1

def cmpCategorias(keyname, categoria):
    """
    Compara dos nombres de autor. El primero es una cadena
    y el segundo un entry de un map
    """
    authentry = me.getKey(categoria)
    if (keyname == authentry):
        return 0
    elif (keyname > authentry):
        return 1
    else:
        return -1

def cmpVideosByLikes(video1, video2):
    """
    Devuelve verdadero (True) si los likes de video1 son menores que los del video2
    Args:
        video1: informacion del primer video que incluye su valor 'likes'
        video2: informacion del segundo video que incluye su valor 'likes'
    """
    if (int(video1['likes']) > int(video2['likes'])):
        return True

def compararCategorias(categoria1, categoria):
    if categoria1.lower() in categoria['name'].lower():
        return 0
    return -1

def cmpVideosByDias(video1, video2):
    if (int(video1['dias']) > int(video2['dias'])):
        return True

def cmpVideosByComments(video1, video2):
    """
    Devuelve verdadero (True) si los likes de video1 son menores que los del video2
    Args:
        video1: informacion del primer video que incluye su valor 'comments'
        video2: informacion del segundo video que incluye su valor 'comments'
    """
    if (int(video1['comment_count']) > int(video2['comment_count'])):
        return True

# Funciones de ordenamiento

def sortLikes(catalog, size):
    sub_list = lt.subList(catalog, 1, lt.size(catalog))
    sub_list = sub_list.copy()
    sorted_list = ms.sort(sub_list, cmpVideosByLikes)    
    sub_list2 = lt.subList(sorted_list, 1, size)
    return sub_list2

def sortDias(catalog):
    sub_list = lt.subList(catalog, 1, lt.size(catalog))
    sub_list = sub_list.copy()
    sorted_list = ms.sort(sub_list, cmpVideosByDias)    
    sub_list2 = lt.subList(sorted_list, 1, 1)
    return sub_list2

def sortComentarios(catalog, size):
    sub_list = lt.subList(catalog, 1, lt.size(catalog))
    sub_list = sub_list.copy()
    sorted_list = ms.sort(sub_list, cmpVideosByComments)    
    sub_list2 = lt.subList(sorted_list, 1, size)
    return sub_list2


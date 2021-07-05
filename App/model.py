"""
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
            'categorias': None}

    catalog['videos'] = lt.newList("ARRAY_LIST")
    catalog['cat_name_id'] = lt.newList("ARRAY_LIST", cmpfunction=compararCategorias)
    catalog['categorias'] = mp.newMap(32, maptype='CHAINING', comparefunction=cmpCategorias)
    
    return catalog

# Funciones para creacion de datos

def newCategoria(id):
    """
    Crea una nueva estructura para modelar los libros de un autor
    y su promedio de ratings. Se crea una lista para guardar los
    libros de dicho autor.
    """
    author = {'id': "",
              "videos": None}
    author['name'] = id
    author['videos'] = lt.newList('ARRAY_LIST', cmpCategorias)
    return author

# Funciones para agregar informacion al catalogo

def addVideo(catalog, video):
    # Se adiciona el video a la lista de videos
    lt.addLast(catalog['videos'], video)
    addCategoria(catalog, video['category_id'], video)

def addCategoria(catalog, idCategoria, video):
    categorias =  catalog['categorias']
    existcategoria = mp.contains(categorias, idCategoria)
    if existcategoria:
        entry = mp.get(categorias, idCategoria)
        categoria = me.getValue(entry)
    else:
        categoria = newCategoria(idCategoria)
        mp.put(categorias, idCategoria, categoria)
    lt.addLast(categoria['videos'], video)
    

# Funciones de consulta
"""
def filtrarRequerimiento1(catalog, categoria):
    if mp.contains(catalog['categorias'], categoria):
        lista = mp.get(catalog['categorias'], categoria)
        return lista
    else:
        return None
"""
def getVideosByCat(catalog, categoria):

    cat = mp.get(catalog['categorias'], categoria)
    if cat:
        return me.getValue(cat)
    return None

# Funciones utilizadas para comparar elementos

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

def cmpVideosByViews(video1, video2):
    """
    Devuelve verdadero (True) si los likes de video1 son menores que los del video2
    Args:
        video1: informacion del primer video que incluye su valor 'likes'
        video2: informacion del segundo video que incluye su valor 'likes'
    """
    if (int(video1['views']) > int(video2['views'])):
        return True

# Funciones de ordenamiento

def sortViews(catalog, size):
    sub_list = lt.subList(catalog, 1, lt.size(catalog))
    sub_list = sub_list.copy()
    sorted_list = ms.sort(sub_list, cmpVideosByViews)    
    sub_list2 = lt.subList(sorted_list, 1, size)
    return sub_list2
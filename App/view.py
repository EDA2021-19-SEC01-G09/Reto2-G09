"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Cargar videos con más views en función de la categoría")

def initCatalog():
    """
    Inicializa el catalogo de videos
    """
    return controller.initCatalog()

def loadData(catalog):
    """
    Carga los videos en la estructura de datos
    """
    controller.loadData(catalog)

def printResultsReq1(ord_videos, n_videos):
    size = lt.size(ord_videos)
    if size >= n_videos:
        print("Los ", n_videos, " videos con más likes son: ")
        i = 1
        while i <= (n_videos):
            video = lt.getElement(ord_videos, i)
            print('Trending date: ' + video['trending_date'] + ' Título: ' +
            video['title'] + ' Nombre del canal: ' + video['channel_title'] + ' Fecha publicación: ' + video['publish_time'] + ' Vistas: ' + video['views'] + ' Likes: ' + video['likes'] + ' Dislikes: ' + video['dislikes'])
            i += 1
    return ""

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        catalog = initCatalog()
        loadData(catalog)
        print('Videos cargados: ' + str(lt.size(catalog['videos'])))


    elif int(inputs[0]) == 2:
        category_name = input('Ingrese la categoría deseada: ')
        listaFiltrada = controller.filtrarRequerimiento1(catalog, category_name)['videos']
        n_videos = int(input('Ingrese el número de videos que quiere listar: '))
        if n_videos > lt.size(listaFiltrada):
            print('La sublista deseada excede el número de videos que tienen esa categoría. Por favor ingresar otro valor.')
        else:
            result = controller.sortViews(listaFiltrada, n_videos)
            print('Cargando información de videos con más likes...')
            print(printResultsReq1(result, n_videos))


    else:
        sys.exit(0)
sys.exit(0)

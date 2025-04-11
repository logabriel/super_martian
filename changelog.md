## Cambios en el archivo settings
* se agrego la tabla **SPAWN_PLAYER** que indica la posicion de aparicion del personaje de acuerdo al nivel **{nivel: (x, y)}**
* Se agrego un nuevo sonido para la victoria
* Se agrego la logica necesaria para cargar la textura de la llave y el cubo activable **(lineas 68)**

## Cambios en el modulo assets/textures
* Se agrego textura key-gold.png para el bloque y llave necesarios para cambiar de nivel

## Cambios en el modulo assets/tilemaps
* se agrego el segundo nivel **(level2.tmx)** 

## Cambios en el script definitions/tiles.py
* Se agregaron mas bloques 

## Cambios en el script definitions/items.py
* Se agregaron los items de la llave y el bloque activable **(Lineas 87 a 104)**

## Cambios en loaders/TmsxLevelLoader.py
* ahora el metodo load_items puede trabajar con mas capas de items **(lineas 61 a 88)**

## Cambios en game_states/PlayState.py
* se agrego la logica necesaria para cambiar de nivel **(Lineas 136 a 148)**
* Se agrego la logica para que cuando se inicie el nivel el cubo y la llave esten inactivos **(Lineas 77 a 85)**

## Nueva clase game_state/TransitionState.py
* Es un estado de transicion a la hora de cambiar de nivel. Tambien se encarga implementar el la tecnica del ending circle


## Descripció General

Aquest document detalla la implementació dels components principals per al projecte final de l'assignatura de Robòtica Avançada. S'han desenvolupat un sistema de manipulació robòtica i un de robòtica mòbil.

---

## Part 1: Sistema de Manipulació Robòtica

### Objectiu

Implementar un sistema de manipulació robòtica que utilitzi un robot UR3 per resoldre el problema de les N-reines. La nostra idea inicial és tenir una peça a cada casella i acabar apilant totes les peces en la posició de la reina així creant el seu tron.

Cal mencionar, que en l'execució en el robot real i en simulació hem executat un fictici 2 reines, que no té restriccions de diagonals. Aquesta simplificació del problema es deu a la dificultat d'implementar tantes passes en el robot i modelant tantes altures com caldria.

### Eines Utilitzades

- **PDDL** (Planning Domain Definition Language) per a la definició de dominis i problemes de planificació.
- **The Kautham Project** per a la configuració i simulació d'escenaris de manipulació.
- **Robot UR3** de Universal Robots per a la implementació física de la solució.

### Estructura de Directori i Fitxers

### Directori: `manipulador`

Aquest directori conté tots els fitxers relacionats amb la manipulació robòtica.

- **kautham/**: Fitxers de configuració i scripts relacionats amb l'ús de Kautham.
    - `2queens_pls_change_poses.xml`: Problem File de Kautham on hem modificat les posicions segons les que hem obtingut des del robot real, que no són exactes en simulació degut a la diferent orientació del robot.
    - `2queens_pls.xml`: Problem File de Kautham per al problema de les peces d'escacs.
    - `poses.py`: Script en Python per definir o modificar les configuracions en el context de Kautham. Converteix els angles de graus a radiants i els normalitza entre pi i -pi.
    - `tampconfig_2queens_pls.xml`: Fitxer de configuració TAMP per a la manipulació de peces en Kautham.
- **pddls/**: Fitxers relacionats amb la planificació utilitzant PDDL.
    - `chessmanipulationdomain.pddl`: Definició del domini PDDL per a la manipulació de peces d'escacs. Aquest l'hem obtingut d'un codi antic i ens serveix per a la simplificació del problema a 2 reines.
    - `domain_movement.pddl`: Domini PDDL per a la planificació de moviments modelant les altures de les piles que creem en les posicions de les reines.
    - `domain_nofluents.pddl`: Definició del domini PDDL sense fluents (el mateix que domain_movement.pddl). Aquest es va crear ja que el el planificador que utilitza el codi preestablert que teníem a la carpeta catkin_wsTAMP no acceptava fluents. Malgrat això vam acabar utilitzant una versió encara més simplificada (chessmanipulationdomain.pddl)
    - `domain_queens.pddl`: Domini PDDL específic per resoldre el problema de les N-reines.
    - `problem_movement.pddl`: Definició d'un problema específic utilitzant el domini de moviment. Aquest problema es crea a partir de create_problem.py.
    - `problem_nofluents.pddl`: Problema PDDL associat al domini sense fluents.
    - `problem_queens.pddl`: Problema PDDL per al domini de les 4-reines.
    - `manipulation_problem_2queens_pls`: Problema PDDL per a la manipulació de les nostres peces de les 2-reines.
    - `metricff.exe`: Executable per al planificador Metric-FF. `cygwin1.dll` és necessari també per poder executar.
    - `output_movement.txt`: Sortida de l'execució del planificador per al problema de moviment.
    - `output.txt`: Sortida de l'execució del problema de les 4-reines.
    - `create_problem.py`: Executa el problema de les 4-reines i agafa la solució per a construir el goal del problema de planificació de moviments, així també executant-lo i guardant els resultats a `output.txt` i `output_movement.txt` respectivament
- **UR3e/**: Scripts i configuracions específiques per al robot UR3 i UR3e.
    - `pinza10UR3.py`: Script en Python per a la configuració de la pinça en el UR3.
    - `pinza40UR3.py`: Un altre script de configuració per a la pinça en el UR3.
    - `read_xml.py`: Script per llegir i processar el fitxer taskfile i obtenir els paths per a mandar a executar la trajectòria al robot real.
    - `taskfile_tampconfig_2queens_pls.xml`: Taskifile amb les configuracions corresponents a les trajectòries obtingut a partir del `tampconfig_2queens_pls.xml`, que utilitza RRTConnect per a planificar les trajectòries.
    - `UR3_final.py`: Script principal per a l'execució final del projecte en el UR3 a partir de les trajectòries obtingudes a partir de read_xml. Es pot configurar el valor de la variable *pick_place_count*, que indica quantes seqüències pick-place ha de realitzar.

---

## Part 2: Robot Mòbil Autònom - "El Toro Robòtic"

### Objectiu

Desenvolupar un robot mòbil autònom, modelat com un toro, que pugui navegar de forma autònoma i seguir objectes de color vermell de forma quadrada o rectangular.

### Eines Utilitzades

- **ROS** (Robot Operating System) per a la integració i el control del robot.
- **Turtlebot3 Waffle** com a plataforma de maquinari.
- **Python** per a l'scripting i el control del robot.

### Fitxers

- **Versió 1**
  - `move.py`
  - `publisher.py`
  - `red_squares.py`
- **Versió 2**
  - `move_new.py`
  - `publisher_new.py`
  - `red_new.py`
  - `send_goal_client`

### Com Utilitzar

Per la primera versió:

```bash
roslaunch final red_follower.launch
```

Per la segona versió:

```bash
roslaunch final red_follower_2.launch
```

La primera versió segueix objectes vermells i la segona, a més, aproxima la posició amb trigonometria i evita els obstacles així.

### Descripció dels fitxers:

- `move.py` i `move_new.py`: Nodes que controlen el moviment del robot.
- `publisher.py` i `publisher_new.py`: Nodes que gestionen la publicació de dades necessàries per al seguiment d'objectes.
- `red_squares.py` i `red_new.py`: Funcions auxiliars per a la detecció d'objectes vermells.
- `send_goal_client`: Node que envia els objectius de posició al robot per moure's cap a la seva destinació.


## Autors

- Casanovas Cordero, Alex Miquel
- Fuster Palà, Llum
- Gálvez Serrano, Paula
- Saurina i Ricós, Joan
- Tomás Martínez, Serg
